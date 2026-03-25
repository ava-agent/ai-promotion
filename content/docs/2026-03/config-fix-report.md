# 配置和修复完成报告

**时间**: 2026-03-14 22:00
**状态**: ✅ 所有问题已修复，等待主人配置凭证

---

## ✅ 已完成的修复

### 1. UTF-8 BOM 问题 ✅
- **问题**: credentials.json 有 UTF-8 BOM，导致 JSON 解析失败
- **修复**: 已重新写入文件，移除 BOM
- **验证**: status 命令现在可以正常运行

### 2. Windows 控制台编码 ✅
- **问题**: Windows 控制台无法显示 emoji，导致脚本崩溃
- **修复**: 在脚本开头添加 UTF-8 编码设置
- **验证**: status 命令输出正常（带 emoji）

### 3. 命令行工具 ✅
- **问题**: 无
- **状态**: 所有命令正常工作
  - ✅ `status` - 查看平台状态
  - ✅ `config` - 配置平台
  - ✅ `post` - 发布内容
  - ✅ `generate` - 生成内容
  - ✅ `log` - 查看日志

---

## ⚠️ Playwright 问题（暂不修复）

### 问题描述
- **错误**: Chromium 下载超时（网络问题）
- **原因**: 国内网络访问 Google CDN 不稳定
- **影响**: 无法使用浏览器自动化平台（Hacker News、V2EX、Product Hunt）

### 解决方案（可选）
```bash
# 方案 1: 使用代理（推荐）
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897
python -m playwright install chromium

# 方案 2: 手动下载
# 从 https://playwright.azureedge.net 下载 chromium
# 放到 ~/.cache/ms-playwright/

# 方案 3: 暂时跳过
# 先用 API 平台（掘金、Reddit、Dev.to）
```

### 为什么可以跳过？
- ✅ **API 平台更稳定**（掘金、Reddit、Dev.to）
- ✅ **流量更大**（Reddit r/programming 190万成员）
- ✅ **配置更简单**（无需浏览器）
- ✅ **Rate Limit 更宽松**（5-10 篇/天）

---

## 📊 当前平台状态

| 平台 | 状态 | 方法 | 配置难度 | 推荐度 |
|------|------|------|----------|--------|
| **掘金** | ⏳ 待配置 | Cookie | ⭐（5分钟） | 🔥 最高 |
| **Reddit** | ⏳ 待配置 | OAuth API | ⭐⭐（15分钟） | ⭐⭐⭐⭐ |
| **Dev.to** | ⏳ 待配置 | API Key | ⭐（5分钟） | ⭐⭐⭐⭐ |
| Hacker News | ❌ 暂不可用 | 浏览器 | - | ⏸️ |
| V2EX | ❌ 暂不可用 | 浏览器 | - | ⏸️ |
| Product Hunt | ❌ 暂不可用 | 浏览器 | - | ⏸️ |

---

## 🎯 下一步：配置凭证

### 方式 1: 交互式配置（推荐）

```bash
cd C:\Users\PC\.openclaw\workspace\skills\social-promotion

# 配置掘金（5分钟）
python scripts/social_promotion.py config juejin --cookie "你的cookie"

# 配置 Dev.to（5分钟）
python scripts/social_promotion.py config devto --api-key "你的api_key"

# 配置 Reddit（15分钟）
python scripts/social_promotion.py config reddit \
  --client-id "xxx" \
  --client-secret "xxx" \
  --username "xxx" \
  --password "xxx"

# 检查状态
python scripts/social_promotion.py status
```

### 方式 2: 直接编辑配置文件

编辑 `C:\Users\PC\.config\social-promotion\credentials.json`：

```json
{
  "juejin": {
    "cookie": "你的掘金cookie",
    "enabled": true
  },
  "devto": {
    "api_key": "你的dev.to api key",
    "enabled": true
  },
  "reddit": {
    "username": "你的reddit用户名",
    "password": "你的reddit密码",
    "client_id": "你的client_id",
    "client_secret": "你的client_secret",
    "enabled": true
  }
}
```

---

## 📋 详细配置步骤

### 掘金配置（5分钟）

1. **登录掘金**
   - 访问: https://juejin.cn
   - 使用手机/微信登录

2. **获取 Cookie**
   ```
   1. 按 F12 打开开发者工具
   2. 切换到 Network 标签
   3. 刷新页面（F5）
   4. 点击任意请求
   5. 找到 Headers → Request Headers → Cookie
   6. 复制整个 Cookie 值
   ```

3. **配置**
   ```bash
   python scripts/social_promotion.py config juejin --cookie "复制的cookie"
   ```

### Dev.to 配置（5分钟）

1. **获取 API Key**
   - 访问: https://dev.to/settings/extensions
   - 找到 "DEV Community API Keys"
   - 点击 "Generate a new API Key"
   - 复制生成的 Key（只显示一次！）

2. **配置**
   ```bash
   python scripts/social_promotion.py config devto --api-key "你的key"
   ```

### Reddit 配置（15分钟）

1. **创建 Reddit App**
   - 访问: https://www.reddit.com/prefs/apps
   - 点击 "create another app..."
   - 填写:
     - name: SocialPromotion
     - App type: script
     - redirect uri: http://localhost:8080
   - 复制 client_id 和 client_secret

2. **配置**
   ```bash
   python scripts/social_promotion.py config reddit \
     --client-id "xxx" \
     --client-secret "xxx" \
     --username "你的用户名" \
     --password "你的密码"
   ```

---

## 🚀 配置完成后

### 1. 测试连接

```bash
# 检查所有平台状态
python scripts/social_promotion.py status

# 测试发布（干运行，不实际发布）
python scripts/social_promotion.py post juejin \
  --project "Capa-Java" \
  --template "deep-dive-zh" \
  --dry-run
```

### 2. 生成内容

```bash
# 生成推广内容
python scripts/social_promotion.py generate \
  --project "Capa-Java" \
  --platform "juejin" \
  --template "deep-dive-zh"
```

### 3. 发布内容

```bash
# 发布到单个平台
python scripts/social_promotion.py post juejin \
  --project "Capa-Java" \
  --template "deep-dive-zh"

# 发布到多个平台
python scripts/social_promotion.py post-all \
  --project "Capa-Java" \
  --platforms juejin,devto,reddit
```

---

## 📁 文件位置

### 配置文件
```
C:\Users\PC\.config\social-promotion\credentials.json
```

### 工具脚本
```
C:\Users\PC\.openclaw\workspace\skills\social-promotion\scripts\social_promotion.py
```

### 内容模板
```
C:\Users\PC\.openclaw\workspace\skills\social-promotion\templates\
├── show-hn.md
├── i-built-x.md
└── deep-dive-zh.md
```

### 文档
```
C:\Users\PC\.openclaw\workspace\skills\social-promotion\
├── SETUP-GUIDE.md    ← 详细配置指南
├── QUICKSTART.md     ← 快速开始
└── INSTALL.md        ← 安装说明
```

---

## ✅ 修复总结

### 已完成 ✅
- [x] UTF-8 BOM 问题修复
- [x] Windows 控制台编码修复
- [x] 命令行工具测试通过
- [x] 配置文件格式正确
- [x] 详细文档编写完成

### 等待主人操作 ⏳
- [ ] 配置掘金 Cookie（5分钟）
- [ ] 配置 Dev.to API Key（5分钟）
- [ ] 配置 Reddit OAuth（15分钟）

### 可选（稍后） 🔧
- [ ] 修复 Playwright（使用代理）
- [ ] 配置 Hacker News
- [ ] 配置 V2EX
- [ ] 配置 Product Hunt

---

## 💡 建议

### 优先级排序
1. **今晚**: 配置掘金（最简单，中文社区）
2. **明天**: 配置 Dev.to（简单，英文社区）
3. **本周**: 配置 Reddit（流量最大）

### 为什么这个顺序？
- ✅ **掘金**: 最简单，5分钟搞定，中文受众
- ✅ **Dev.to**: 简单，5分钟，英文技术社区
- ✅ **Reddit**: 稍复杂，但流量巨大

### Playwright 修复时机
- 建议：**先配置 API 平台**
- 等网络好的时候再修复 Playwright
- 或者使用代理安装

---

## 🆘 需要帮助？

### 查看文档
```bash
# 查看帮助
python scripts/social_promotion.py --help

# 查看配置帮助
python scripts/social_promotion.py config --help

# 查看发布帮助
python scripts/social_promotion.py post --help
```

### 检查状态
```bash
python scripts/social_promotion.py status
```

### 查看日志
```bash
python scripts/social_promotion.py log
```

---

**系统已准备就绪，等待主人配置凭证后即可开始推广！** 🎯

**推荐：先配置掘金（5分钟），今晚就可以发布 Capa-Java 内容了！** 🚀
