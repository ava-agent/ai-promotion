# 微信公众号 MCP (wenyan-mcp) 使用指南

## 安装状态

✅ **已安装并配置成功**

### 配置信息
- **MCP 名称**: wenyan-mcp
- **命令**: wenyan-mcp
- **App ID**: wxc12ac29e7508ce1f
- **App Secret**: 已配置
- **状态**: ✅ 运行中 (2 tools available)

---

## 可用工具

### 1. list_themes - 列出可用主题

**功能**: 查看所有可用的文章主题样式

**使用方式**:
```bash
mcporter call wenyan-mcp.list_themes
```

**当前可用主题**:
- `default` - Default (A clean, classic layout ideal for long-form reading.)
- 更多主题: orangeheart, rainbow, lapis, pie, maize, purple, phycat

---

### 2. publish_article - 发布文章到微信公众号

**功能**: 格式化 Markdown 文章并使用指定主题发布到微信公众号

**参数**:
- `content` (required): Markdown 格式的文章内容
- `theme_id` (optional): 主题ID (默认: default)
  - 可选值: default, orangeheart, rainbow, lapis, pie, maize, purple, phycat

**使用方式**:

```bash
# 使用默认主题发布
mcporter call wenyan-mcp.publish_article content="# 文章标题\n\n文章内容..."

# 使用指定主题发布
mcporter call wenyan-mcp.publish_article content="# 文章标题\n\n文章内容..." theme_id="orangeheart"

# 从文件读取内容发布
mcporter call wenyan-mcp.publish_article content:"/path/to/article.md"
```

---

## 使用示例

### 示例 1: 简单发布
```bash
npx mcporter call wenyan-mcp.publish_article content="# 你好世界\n\n这是我的第一篇公众号文章！"
```

### 示例 2: 使用特定主题
```bash
npx mcporter call wenyan-mcp.publish_article \
  content="# 技术分享\n\n今天来聊聊..." \
  theme_id="rainbow"
```

### 示例 3: 发布文件内容
```bash
npx mcporter call wenyan-mcp.publish_article \
  content:"C:/Users/PC/Documents/article.md" \
  theme_id="lapis"
```

---

## 主题说明

| 主题ID | 名称 | 描述 |
|--------|------|------|
| default | Default | 简洁经典，适合长文阅读 |
| orangeheart | Orange Heart | 橙心主题 |
| rainbow | Rainbow | 彩虹主题 |
| lapis | Lapis | 青金石主题 |
| pie | Pie | 派主题 |
| maize | Maize | 玉米主题 |
| purple | Purple | 紫色主题 |
| phycat | Phycat | _phy主题 |

---

## Markdown 支持

wenyan-mcp 支持标准 Markdown 语法：

- 标题 (H1-H6)
- 段落和换行
- 粗体、斜体、删除线
- 列表（有序/无序）
- 链接和图片
- 代码块（支持语法高亮）
- 引用块
- 表格
- 数学公式 (MathJax)

---

## ⚠️ 重要：IP 白名单配置

**首次使用需要配置！**

错误信息示例：
```
错误码：40164
错误信息：invalid ip 180.158.134.79, not in whitelist
```

### 解决步骤

1. **登录微信公众平台**
   - 访问 https://mp.weixin.qq.com
   - 使用公众号管理员账号登录

2. **进入开发配置**
   - 左侧菜单：开发 → 基本配置
   - 找到 "IP白名单" 配置项

3. **添加 IP 地址**
   - 添加当前服务器 IP: `180.158.134.79`
   - 点击保存

4. **验证配置**
   ```bash
   npx mcporter call wenyan-mcp.list_themes
   ```

### 获取当前 IP
如果不确定当前 IP，可以访问：
- https://ip.sb
- https://ipinfo.io

---

## 故障排除

### 1. MCP 服务器离线
```bash
# 检查状态
npx mcporter list

# 如果离线，尝试重启
npx mcporter daemon restart
```

### 2. App ID/Secret 错误
如果提示认证失败，请检查：
- App ID 是否正确: `wxc12ac29e7508ce1f`
- App Secret 是否有效

### 3. IP 白名单错误 (40164)
参见上方的 "IP 白名单配置" 章节

### 4. 更新 MCP 配置
```bash
# 删除现有配置
npx mcporter config remove wenyan-mcp

# 重新添加
npx mcporter config add wenyan-mcp \
  --command "wenyan-mcp" \
  --env WECHAT_APP_ID="wxc12ac29e7508ce1f" \
  --env WECHAT_APP_SECRET="bb213f9ecbb948fbb2a12ebc902e4db6"
```

---

## 自动化发布脚本

可以创建自动化脚本定时发布文章：

```bash
#!/bin/bash
# wechat-publish.sh

ARTICLE_FILE="$1"
THEME="${2:-default}"

if [ -z "$ARTICLE_FILE" ]; then
  echo "Usage: $0 <article.md> [theme_id]"
  exit 1
fi

npx mcporter call wenyan-mcp.publish_article \
  content:"$ARTICLE_FILE" \
  theme_id:"$THEME"
```

使用:
```bash
./wechat-publish.sh article.md orangeheart
```

---

## 参考链接

- **Wenyan 官网**: https://wenyan.world
- **GitHub**: https://github.com/caol64/wenyan-mcp
- **MCP SDK**: https://github.com/modelcontextprotocol

---

**最后更新**: 2026-03-25
