# 跨平台推广系统 - 安装状态

**时间**: 2026-03-14 21:50
**状态**: ⚠️ 部分完成

---

## ✅ 已完成

| 组件 | 状态 | 说明 |
|------|------|------|
| Python 脚本 | ✅ | `social_promotion.py` 已创建 |
| 依赖包 | ✅ | requests, beautifulsoup4, playwright |
| 配置文件 | ✅ | credentials.json 模板 |
| 内容模板 | ✅ | 3 个模板（HN/Reddit/掘金） |
| 文档 | ✅ | INSTALL.md, QUICKSTART.md |
| 项目轮换 | ✅ | github-projects-rotation.md |

---

## ⚠️ 需要手动完成

### 1. Playwright 浏览器（下载失败）

**问题**: 网络原因导致 Chromium 下载失败（172.8 MB）

**解决方案**:
```powershell
# 方案 A: 使用镜像（推荐）
$env:PLAYWRIGHT_DOWNLOAD_HOST = "https://npmmirror.com/mirrors/playwright"
python -m playwright install chromium

# 方案 B: 手动下载
# 1. 访问: https://playwright.azureedge.net/builds/chromium/
# 2. 下载对应版本
# 3. 解压到: ~/.cache/ms-playwright/

# 方案 C: 跳过（如果只用 API 平台）
# 不影响 Reddit, Dev.to, 掘金等 API 平台
```

### 2. infsh CLI（浏览器自动化）

**用途**: Hacker News, V2EX 等无 API 平台

**安装**:
1. 访问: https://inference.sh
2. 下载 Windows 安装器
3. 运行: `infsh login`

**或者**: 暂时跳过，先使用 API 平台（Reddit, 掘金, Dev.to）

### 3. mcporter（MCP 平台）

```bash
npm install -g mcporter
```

---

## 🎯 立即可用的平台（无需 Playwright）

| 平台 | 方法 | 配置时间 | 推荐度 |
|------|------|---------|--------|
| **Reddit** | API | 15 分钟 | ⭐⭐⭐⭐⭐ |
| **Dev.to** | API | 5 分钟 | ⭐⭐⭐⭐ |
| **掘金** | API (Cookie) | 5 分钟 | ⭐⭐⭐⭐ |
| **Twitter/X** | API (付费) | 20 分钟 | ⭐⭐⭐ |

**需要 Playwright 的平台**: Hacker News, V2EX, Product Hunt

---

## 📋 快速开始（无需 Playwright）

### Step 1: 配置掘金（最简单）

```bash
# 1. 登录 https://juejin.cn
# 2. F12 → Network → 刷新 → 任意请求 → Headers → Cookie
# 3. 配置
cd C:\Users\PC\.openclaw\workspace\skills\social-promotion
python scripts/social_promotion.py config juejin --cookie "your_cookie_here"

# 4. 测试
python scripts/social_promotion.py post juejin \
  --project "Capa-Java" \
  --template "deep-dive-zh"
```

### Step 2: 配置 Reddit（流量最大）

```bash
# 1. 访问 https://www.reddit.com/prefs/apps
# 2. Create app → script
# 3. 配置
python scripts/social_promotion.py config reddit \
  --client-id "xxx" \
  --client-secret "xxx" \
  --username "xxx" \
  --password "xxx"

# 4. 测试
python scripts/social_promotion.py post reddit \
  --project "OpenOctopus" \
  --subreddit programming \
  --template "i-built-x"
```

### Step 3: 配置 Dev.to（社区友好）

```bash
# 1. 访问 https://dev.to/settings/extensions
# 2. Generate API key
# 3. 配置
python scripts/social_promotion.py config devto --api-key "xxx"

# 4. 测试
python scripts/social_promotion.py post devto \
  --project "AI-Tools" \
  --template "i-built-x"
```

---

## 📊 项目轮换状态

| 项目 | Tier | Moltbook | 其他平台 | 下次推广 |
|------|------|----------|---------|---------|
| OpenOctopus | 1 | 2次 (spam) | 0 | - |
| AI Tools | 1 | 2次 (spam) | 0 | - |
| **Capa-Java** | 1 | 0 | 0 | **22:00** |
| ClawX | 1 | 0 | 0 | - |

---

## 💡 建议

### 立即可做（今晚）
1. ✅ 配置掘金（5 分钟）
2. ✅ 准备 Capa-Java 推广内容（15 分钟）
3. ✅ 22:00 在掘金发布 Capa-Java 深度文章

### 明天
1. 配置 Reddit
2. 配置 Dev.to
3. 多平台推广 Capa-Java

### 本周
1. 修复 Playwright 安装
2. 安装 infsh
3. 配置 Hacker News
4. 建立完整的多平台推广系统

---

## 📁 文件位置

```
skills/social-promotion/
├── SKILL.md              # Skill 说明
├── INSTALL.md           # 详细安装指南
├── QUICKSTART.md        # 快速开始
├── scripts/
│   └── social_promotion.py
├── config/
│   └── credentials.json
└── templates/
    ├── show-hn.md
    ├── i-built-x.md
    └── deep-dive-zh.md

memory/
├── social-promotion-setup-report.md  # 本文件
├── github-projects-rotation.md       # 项目轮换
└── github-promotion-platforms.md     # 平台调研
```

---

**准备好了吗？从掘金开始吧！** 🚀
