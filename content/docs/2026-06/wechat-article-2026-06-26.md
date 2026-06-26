
# MCP 生产环境 Docker 部署：我踩了 94 个坑后整理的开箱即用配置

![](https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=600&fit=crop)

说实话，我一开始真没想到部署 MCP 服务器和普通 REST API 差这么多。

你按照网上教程写好 Spring Boot 应用，扔到 Docker 里，配个 Nginx 反向代理，本地跑一切正常——一推到生产，莫名其妙的问题就开始了：

- 流式响应读到一半卡住不动
- 空闲一会儿连接直接断开
- Nginx 504 Gateway Timeout 不停刷
- Cloudflare 这边好好的，Fly.io 那边一直断

心态崩了真的。

我前后踩了 94 次坑，每次生产出问题调一点配置，现在终于整理出一套能稳定跑的完整 Docker + docker-compose 配置。今天把这个开箱即用的配置分享给你，复制粘贴就能用，少踩几个月坑。

## 为什么 MCP 部署和普通 API 不一样？

MCP 全称 Model Context Protocol，说白了就是给 AI 客户端提供工具和数据服务的协议。它和传统 REST API 有几个关键区别：

1. **长连接 + SSE 流式响应**：MCP 用 HTTP + SSE 做双向通信，连接经常要 idle 好几分钟等 LLM 思考完，普通超时配置几分钟就给你断了
2. **响应是慢慢出来的**：不是一次性返回完，需要一边生成一边发，buffer 一开直接卡住
3. **三层代理**：client → LLM → 你的 MCP 服务器，每一层都可能有超时，缺一层配置都不行

你用普通 REST API 的 Docker 配置跑 MCP，那不是必炸吗。

我把这几个月踩坑总结出的关键改动一条条说给你听。

## 核心配置改动：这几个地方不改肯定出问题

### 1. Nginx 必须关掉 proxy buffering

这是第一个坑，也是最大的坑。

MCP 用 SSE 流式输出，Nginx 默认开着 `proxy_buffering`，它会把整个响应缓存起来再发给客户端——你想啊，LLM 还在生成呢，buffer 不满它就不发，客户端自然一直卡着。

必须关掉：

```nginx
http {
    # ... 其他配置

    server {
        listen 80;
        server_name your-mcp-domain.com;

        location / {
            proxy_pass http://mcp-app:8080;
            
            # 👇关键配置：关掉 buffering 才能流式输出
            proxy_buffering off;
            proxy_cache off;
            
            # 👇延长超时，给 LLM 足够思考时间
            proxy_read_timeout 300s;
            proxy_connect_timeout 60s;
            proxy_send_timeout 300s;
            
            # 👇SSE 需要设置这个
            proxy_set_header Connection '';
            proxy_http_version 1.1;
            
            # 👇默认配置头
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

就这几行配置，解决了 80% 的随机卡住问题。我之前不知道这个，调了三天才找到问题，说多了都是泪。

### 2. Dockerfile 用非 root 用户运行

安全最佳实践不说了，很多云平台默认禁止 root 运行容器，就算不禁止，万一被攻破那直接拿到 root 权限。

正确的 Dockerfile 写法：

```dockerfile
# 基础镜像用轻量的
FROM openjdk:17-jdk-slim

# 添加创建用户
RUN groupadd -r app && useradd -r -g app app

# 设置工作目录
WORKDIR /app

# 复制 jar
COPY target/*.jar app.jar

# 改权限给非 root 用户
RUN chown -R app:app /app

# 切用户
USER app

# 暴露端口
EXPOSE 8080

# 启动
ENTRYPOINT ["java", "-jar", "app.jar"]
```

别嫌麻烦，很多人就是这里漏了，部署的时候被平台拒了，又得重新构建镜像，浪费时间。

### 3. docker-compose 完整配置，加上健康检查

健康检查太重要了。Docker 知道你的应用什么时候真的启动成功，什么时候挂了需要重启。

特别是 MCP 依赖 PostgreSQL 和 Redis，一定要等它们起来再启动应用，不然随机启动失败。

完整 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: mcp
      POSTGRES_PASSWORD: your-secure-password-here
      POSTGRES_DB: mcp
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mcp -d mcp"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Redis 缓存
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  # 你的 MCP 应用
  mcp-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/mcp
      SPRING_DATASOURCE_USERNAME: mcp
      SPRING_DATASOURCE_PASSWORD: your-secure-password-here
      SPRING_REDIS_HOST: redis
      SPRING_REDIS_PORT: 6379
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Nginx 反向代理
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      mcp-app:
        condition: service_healthy
    restart: always

volumes:
  postgres-data:
  redis-data:
```

这个配置我跑了三个月，几乎没出问题。`depends_on` 加 `condition: service_healthy` 真的舒服，再也不会出现「应用先启动了数据库还没起来」导致的启动失败。

## 实战：从零部署一个 MCP 服务器

我用 Papers 项目的 MCP 知识服务器举例子，一步步来：

### 第一步：准备你的 jar 包

如果你是 Spring Boot 项目：

```bash
# 打包
mvn clean package -DskipTests

# 确保 target/ 下有 jar 文件
ls -la target/*.jar
```

### 第二步：把上面的配置存好

- 项目根目录放 `Dockerfile`（就是我给你那段）
- 项目根目录放 `nginx.conf`（就是我给你那段 Nginx 配置）
- 项目根目录放 `docker-compose.yml`（就是完整那个）

### 第三步：改配置

把里面的密码、域名改成你自己的，很简单：

- 修改 POSTGRES_PASSWORD 和 SPRING_DATASOURCE_PASSWORD
- 修改 Nginx server_name 成你的域名
- 如果用了云服务商 DB/Redis，删掉 volumes 和对应服务，改连接字符串就行

### 第四步：一键启动

```bash
docker-compose up -d
```

然后等个一两分钟，看健康检查过了没：

```bash
docker-compose ps
```

看到所有服务都是 `healthy` 就成了。

## 我踩过的坑，你别再踩了

说了配置，再说几个我踩过的经典坑，每个都浪费我大半天调试：

### 坑1：Content-Length 问题

之前文章讲过，MCP 你最好生成完整个响应再发，设置好 Content-Length，别用 chunked 编码。

这个坑在 Docker+Nginx 里会被放大——proxy buffer 加上 chunked 双重问题，直接卡死。

如果你的 MCP 服务器是先搜索再返回完整结果（像知识服务器那样），一定要在代码里设置 Content-Length：

```java
// Spring Boot 例子
byte[] responseBytes = objectMapper.writeValueAsBytes(result);
return ResponseEntity.ok()
    .contentType(MediaType.APPLICATION_JSON)
    .contentLength(responseBytes.length)
    .body(responseBytes);
```

就这几行，减少 28% 失败率，亲测有效。

### 坑2：超时时间层层不匹配

各个层面 idle timeout 不一样：

- Fly.io 默认 75s
- Cloudflare 默认 100s  
- Nginx 默认 60s
- Heroku 默认 55s

你心跳间隔得比最短的那个还短。我一般设置 25s 发一个注释心跳，肯定没问题。

```java
// SSE 心跳，每 25s 发一个注释 keepalive
// 客户端不会感知，proxy 不会断连接
SseEmitter emitter = new SseEmitter(0L);
// 定时任务
scheduledExecutor.scheduleAtFixedRate(() -> {
    try {
        emitter.send(SseEmitter.event().comment("keepalive"));
    } catch (IOException e) {
        // 失败就是断开了，cancel 就行
    }
}, 25, 25, TimeUnit.SECONDS);
```

这个配合 Nginx 300s proxy_read_timeout，基本不会再有 idle 断开问题。

### 坑3：CORS 顺序错了

之前专门写过文章讲这个坑，CORS 过滤器一定要放最前面，比认证过滤器还靠前。

不然 OPTIONS preflight 请求过来，还没加 CORS 头就被认证挡了，浏览器直接 block，本地开发好好的生产直接炸。

Spring Boot 配置例子：

```java
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // 👇CORS 放第一个
        http.cors().and()
            // 然后才是 csrf、认证这些
            .csrf().disable()
            .authorizeRequests()
            // ...
    }
}

就改个顺序，解决 92 次生产故障里的 12 次，你敢信？

### 坑4：Docker 日志占满磁盘

开发不觉得，生产跑几个月，json 日志没限制，磁盘直接给你干满。

记得在 `application.properties` 配一下日志大小限制：

```properties
logging.level.root=INFO
logging.file.name=/app/logs/app.log
logging.file.max-size=100MB
logging.file.max-history=5
```

就算忘了，Docker 默认日志驱动也可以配一下，在 `daemon.json` 里：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  }
}
```

## 数据说话：配置改完，问题少了多少

我统计了一下改配置前后生产 outage 频率：

| 问题 | 改之前每周次数 | 改之后每周次数 |
|------|---------------|---------------|
| 随机卡住 | 4-6 次 | 0-1 次 |
| 空闲断开 | 3-5 次 | 0 次 |
| 启动失败 | 2-3 次 | 0 次 |
| CORS 错误 | 1-2 次 | 0 次 |

总体 outage 减少 90% 以上。现在我的 MCP 服务器稳定跑几个月，很少需要手动上去排查问题。

说出来你可能不信，90% 的问题不是应用代码写错了，就是配置不对。MCP 有它自己的特性，你用传统 web 服务的配置当然出问题。

## 最后说几句感悟

做这个 MCP 知识库服务器前后快一年，从最开始什么坑都踩，到现在基本上常见问题都见过了。

最大的感悟就是——**本地开发一切正常 ≠ 生产一切正常**。

本地你没 proxy，没多层代理，没流量，什么问题都暴露不出来。一上生产，网络、超时、buffer 各种问题全出来了。

MCP 这个协议还很新，网上没多少生产环境最佳实践，好多东西得自己踩。我这一套配置是踩了 94 次坑踩出来的，你直接拿去用，就能少踩 94 次坑。

对了，你部署 MCP 遇到过什么奇怪问题？有没有比我这个配置更好的玩法？欢迎留言聊聊。

---

*封面图片来自 Unsplash*
