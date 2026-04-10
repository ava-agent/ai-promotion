# 写了个"乞丐版"Dapr，三年后发现有些场景还真够用

> 先声明一下，这篇不是来碰瓷 Dapr 的。Dapr 很厉害，25k+ star，社区活跃，我这小项目真没法比。但有时候吧，资源有限、历史包袱重的情况下，一个"精简版"的方案反而更顺手。这篇文章就是想说说我这三年维护 Capa-Java 的一些真实感受。

## 先说说背景，为啥不直接用 Dapr

2021 年我在携程中间件团队，公司业务要出海，核心系统得部署到 AWS。

问题是我们内部的中间件生态全是在私有云上建的：RocketMQ、Nacos、自研日志系统……一股脑儿换到 AWS 的理论上可行，但成本太高了。😅

当时 Dapr 刚出来不久，Multi-Runtime 的概念确实让我眼前一亮。但我们评估了一下，直接上 Dapr 有几个现实问题：

1. **太重了**： sidecar 模式对资源消耗不小，而且我们有些老系统对延迟很敏感
2. **学习成本高**：业务团队那么多人，全员学习 Dapr 的 API 和概念，培训成本吓人
3. **存量代码迁移难**：成千上万的接口如果都要改，这活儿三年内干不完
4. **内部已有沉淀**：公司其实已经有了一套比较成熟的中间件封装，推倒重来有点浪费

所以我们就想，能不能搞一个**更轻量的方案**——不用 sidecar，直接通过 SDK 抽象，让业务代码写一次，换环境的时候只改配置就行。

这就是 Capa-Java 的由来，GitHub 地址：https://github.com/capa-cloud/capa-java

说实话，开始做的时候心里也没底。毕竟"重复造轮子"这个帽子谁都不想戴。但后来发现，有些轮子你不自己造，还真不好上车。😂

## Capa-Java 定位：不是替代 Dapr，是另一种解法

如果你把 Dapr 比作一辆功能齐全的 SUV，Capa-Java 更像是一辆改装过的皮卡——没那么多花里胡哨的功能，但拉货搬家特别顺手。

我们的核心目标是：**Write once, run anywhere**。但这个"anywhere"不是指操作系统，而是指**云环境**——私有云、AWS、阿里云，业务代码不用动。

架构上非常简单，就三层：

```java
// 1. 业务层：完全无感知
@Service
public class OrderService {
    @Autowired
    private CapaMessageClient messageClient;
    
    public void createOrder(Order order) {
        messageClient.publish("order-created", order);
    }
}
```

```java
// 2. Capa 抽象层：统一 API
public interface CapaMessageClient {
    void publish(String topic, Object payload);
    void subscribe(String topic, MessageListener<?> listener);
}
```

```java
// 3. 实现层：根据环境自动加载不同实现
@Component
@ConditionalOnProperty(name = "capa.message.provider", havingValue = "rocketmq")
public class RocketMQCapaMessageClient implements CapaMessageClient {
    // RocketMQ 的具体实现……
}
```

通过 Spring 的 `@ConditionalOnProperty` 和 SPI 机制，启动时会根据配置文件自动注入对应的实现类。

配置文件示例：

```yaml
capa:
  environment: aws
  message:
    provider: sqs
  config:
    provider: appconfig
  lock:
    provider: dynamodb
```

改成 `environment: private-cloud`，provider 全换成内部中间件，代码一行不改。

哈哈，听着是不是很理想化？但说实话，前两年我们就靠这个思路，把一个核心交易系统从私有云迁到了 AWS，业务代码几乎零改动。😎

## 贴一段真实的迁移前后对比

先看一下没用 Capa 之前，一个通知服务的代码长啥样：

```java
// 私有云版本
@Service
public class NotificationService {
    @Autowired
    private RocketMQTemplate rocketMQTemplate;
    
    @Autowired
    private NacosConfigService nacosConfig;
    
    public void sendNotification(String userId, String content) {
        String topic = nacosConfig.getConfig("notification.topic");
        rocketMQTemplate.asyncSend(topic, content, new SendCallback() {
            @Override
            public void onSuccess(SendResult result) {
                log.info("发送成功: {}", result.getMsgId());
            }
            @Override
            public void onException(Throwable e) {
                log.error("发送失败", e);
            }
        });
    }
}
```

到了 AWS 环境，这条代码基本得重写，换成 SQS 的 API：

```java
// AWS 版本（痛苦的重复劳动）
@Service
public class NotificationServiceAWS {
    @Autowired
    private AmazonSQS sqsClient;
    
    @Autowired
    private AWSSimpleSystemsManager ssmClient;
    
    public void sendNotification(String userId, String content) {
        String queueUrl = ssmClient.getParameter(
            new GetParameterRequest().withName("/prod/notification-queue")
        ).getParameter().getValue();
        
        sqsClient.sendMessage(new SendMessageRequest()
            .withQueueUrl(queueUrl)
            .withMessageBody(content));
    }
}
```

两个版本除了底层实现不同，业务逻辑一模一样。😓 一旦业务逻辑要改，两边都得改，迟早会出不一致的 bug。

用了 Capa 之后，代码变成了这样：

```java
@Service
public class NotificationService {
    @Autowired
    private CapaMessageClient messageClient;
    
    @CapaConfig(key = "notification.topic", defaultValue = "default-notify")
    private String topic;
    
    public void sendNotification(String userId, String content) {
        messageClient.publish(topic, new NotificationEvent(userId, content));
    }
}
```

不管是在私有云还是 AWS，这段代码都不变。配置文件决定底层走哪个实现。

说实话，这个改动省下来的维护成本，远比那点抽象开销值钱。

## 几个真实踩过的坑

### 坑 1：SPI 扫描把启动时间拖惨了

最早我们用的 Java 原生 SPI（`ServiceLoader`），启动时要扫描整个 classpath。😰 一个中等规模的应用启动时间从 12 秒变成了 40 秒。

业务团队开始疯狂吐槽。后来我们改成了 Spring 的 `SpringFactoriesLoader`，并且让各个实现模块在编译期生成索引文件。启动时间降到了 8 秒左右，才算是 acceptable。

```java
// 优化后的 SPI 加载方式
public class CapaSPI {
    public static <T> T load(Class<T> clazz, String provider) {
        List<T> factories = SpringFactoriesLoader.loadFactories(clazz, null);
        return factories.stream()
            .filter(f -> f.getClass().getSimpleName().toLowerCase().contains(provider))
            .findFirst()
            .orElseThrow(() -> new CapaException("找不到 provider: " + provider));
    }
}
```

### 坑 2：不同消息队列的语义差异，真不是换个 API 那么简单

RocketMQ 和 AWS SQS 看着都是消息队列，但细节差异能把人搞疯：

- RocketMQ 支持**顺序消息**，SQS 默认 FIFO 队列才能保证顺序，标准队列不保证
- RocketMQ 延时消息精确到秒级，SQS 只有固定的 15 个延时等级（最长 15 分钟）
- 消息属性大小限制：RocketMQ 单个属性最多 16KB，SQS 全部属性加起来最多 256KB
- 消费确认机制也不同：RocketMQ 是 offset 提交，SQS 是显式删除消息

我们最后的解法挺无奈的——搞了一套"最小公约数"抽象。😅 只支持两边都能实现的能力，比如普通消息、延迟消息（取 SQS 的最大值限制）、广播/集群消费模式等。一些高级特性比如事务消息，在跨云场景下干脆不支持。

这个决策当时有争议，有人说"功能阉割太厉害了"。但从实际落地来看，绝大多数业务场景根本用不到那些高级特性。反而是"能跑通、不出错"比什么都重要。

### 坑 3：本地开发和 CI 测试的折磨

业务同学最大的抱怨不是运行时的问题，而是**本地没法调试**。"我连不上 AWS 的 SQS 啊，你让我怎么跑测试？"

这确实是我们早期设计考虑不周的地方。后来我们搞了一套本地模拟器，用 Testcontainers 在本地启动 LocalStack，模拟 AWS 的服务环境。

```java
@Test
@CapaTestEnvironment(provider = "sqs")
public class NotificationServiceTest {
    @Autowired
    private CapaMessageClient messageClient;
    
    @Test
    public void testSendNotification() {
        messageClient.publish("test-topic", new NotificationEvent("user_001", "hello"));
        // 验证消息是否送达...
    }
}
```

测试启动时自动拉起 LocalStack 容器，跑完自动销毁。业务团队在本地也能完整跑 CI 了，这个改动获得了无数好评。🎉

## 这个项目的优势，我得客观说说

用了三年，Capa-Java 确实解决了我们的核心问题，但优点和缺点都挺明显的。

**优点：**

1. **足够轻量**：就是一套 Java SDK，没有 sidecar，没有额外的进程开销
2. **迁移成本低**：老系统接入基本只改配置文件，业务代码几乎不用动
3. **学习曲线平缓**：API 设计参考了 Spring 的风格，Java 开发者基本秒懂
4. **内部已验证**：在携程核心系统跑了两年多，稳定性还行

**缺点（实话实说）：**

1. **社区几乎为零**：GitHub 只有 14 个 star，主要靠公司内部几个人维护，外部贡献很少
2. **文档不全**：最佳实践、故障排查这些文档都比较欠缺
3. **语言绑定严重**：只有 Java 版本，Go/Python 版本一直没排上优先级
4. **功能深度不够**：事务消息、死信队列这些高级特性支持得比较粗糙

所以这个项目适合什么场景呢？我觉得：

- ✅ **适合**：有存量 Java 系统、需要平滑上云/混合云、有中间件团队支撑的公司
- ❌ **不适合**：从零开始的新系统（直接上 Dapr 或云原生框架更好）、对延迟极其敏感的场景、没有专职中间件团队的小团队

## 最后碎碎念几句

开源三年，这个项目从来没有"火"过。14 个 star 说实话有时候看着也挺沮丧的。😅 但我后来想明白了，**开源项目不一定要火，能解决真实问题就够了**。

我们在生产环境里用它迁移了好几个核心系统，省下了大量的人力和时间成本。对于做基础架构的人来说，这种"幕后英雄"的角色其实也挺有成就感的。

如果你也在做多运行时架构、或者正在为上云迁移头疼，欢迎来 GitHub 交流。虽然回复不一定特别及时，但都会认真看。

🔗 GitHub: https://github.com/capa-cloud/capa-java

最后想问问大家：**你们公司在做云迁移的时候，是怎么处理存量系统的中间件依赖问题的？是直接重写一遍，还是做了一层抽象？** 评论区聊聊呗，挺好奇大家都是怎么选的。🤔
