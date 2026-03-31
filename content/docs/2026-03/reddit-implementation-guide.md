# Reddit 平台实施步骤指南

## 🎯 目标
使用 PRAW 库在 Reddit 发布第一条测试帖子

---

## 📋 实施步骤

### Step 1: 安装 PRAW 库 (1分钟)

```bash
pip install praw
```

验证安装:
```bash
python -c "import praw; print(praw.__version__)"
```

---

### Step 2: 创建 Reddit App (5分钟)

1. **访问应用管理页面**
   - 打开: https://www.reddit.com/prefs/apps
   - 使用 Reddit 账号登录（kevinten10）

2. **创建新应用**
   - 点击 "create another app..."（或 "create an app"）
   - 填写信息:
     - **name**: OpenClawAutoPost
     - **App type**: 选择 "script"
     - **description**: Auto-posting tool for open-source projects
     - **about url**: https://github.com/kevinten10
     - **redirect uri**: http://localhost:8080
   - 点击 "create app"

3. **获取凭证**
   - **Client ID**: 在应用名称下方（一串字符，如：abc123xyz）
   - **Client Secret**: 标记为 "secret"（更长的一串字符）
   - ⚠️ **重要**: 立即保存，只显示一次！

---

### Step 3: 配置环境变量 (2分钟)

**方法 A: 系统环境变量（推荐）**

```powershell
# Windows PowerShell
$env:REDDIT_CLIENT_ID="your_client_id_here"
$env:REDDIT_CLIENT_SECRET="your_client_secret_here"
$env:REDDIT_USERNAME="kevinten10"
$env:REDDIT_PASSWORD="your_password_here"

# 或永久设置
[Environment]::SetEnvironmentVariable("REDDIT_CLIENT_ID", "your_client_id", "User")
[Environment]::SetEnvironmentVariable("REDDIT_CLIENT_SECRET", "your_client_secret", "User")
[Environment]::SetEnvironmentVariable("REDDIT_USERNAME", "kevinten10", "User")
[Environment]::SetEnvironmentVariable("REDDIT_PASSWORD", "your_password", "User")
```

**方法 B: .env 文件**

创建 `~/.openclaw/workspace/skills/reddit-poster/.env`:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=kevinten10
REDDIT_PASSWORD=your_password_here
```

---

### Step 4: 测试 API 连接 (1分钟)

```bash
python ~/.openclaw/workspace/skills/reddit-poster/test_reddit_api.py
```

**期望输出**:
```
============================================================
🐕 Reddit API 测试脚本
============================================================
时间: 2026-03-25 13:30:00

[1/4] 检查环境变量...
  ✅ REDDIT_CLIENT_ID: abc123xy...
  ✅ REDDIT_CLIENT_SECRET: xyz789ab...
  ✅ REDDIT_USERNAME: kevinten10
  ✅ REDDIT_PASSWORD: ***

[2/4] 测试 PRAW 库...
  ✅ PRAW 版本: 7.7.1

[3/4] 测试 Reddit 认证...
  ✅ 认证成功
  用户名: kevinten10
  Karma: 123 link, 456 comment

[4/4] 测试读取功能...
  ✅ 获取到 3 条最近的帖子
  ✅ r/opensource 信息:
    订阅者: 500,000
    在线: 1,234

============================================================
✅ 测试通过！Reddit API 连接正常
============================================================
```

---

### Step 5: 生成并发布第一条帖子 (2分钟)

```bash
python ~/.openclaw/workspace/skills/reddit-poster/reddit_poster.py
```

**交互流程**:
```
============================================================
🐕 Reddit 自动发帖工具
============================================================
时间: 2026-03-25 13:35:00

✅ Reddit authenticated as: kevinten10

📊 获取最近的帖子...
  最近 3 条帖子:
    - r/opensource: Just shipped...

📝 生成测试内容...

生成内容预览:
  标题: Just shipped OpenOctopus - Realm-native life agent system
  长度: 542 字符

  正文预览:
Hey r/opensource! 👋

I've been working on OpenOctopus for a few months, and just shipped a new version!

## What it does
...

确认发布到 r/opensource? (yes/no): yes

🚀 发布中...
✅ Posted to r/opensource: https://reddit.com/r/opensource/comments/abc123/...

✅ 发布成功!
  链接: https://reddit.com/r/opensource/comments/abc123/...
```

---

### Step 6: 验证结果

1. **打开帖子链接**
   - 在浏览器中访问发布的链接
   - 确认帖子显示正常

2. **检查时间线**
   - 访问: https://www.reddit.com/user/kevinten10/submitted
   - 确认帖子出现在提交列表中

3. **观察互动**
   - 检查 upvote/downvote
   - 回复评论（如有）

---

## 🎉 完成！下一步

### 立即可以做
- [ ] 观察首次发帖效果（upvote、评论）
- [ ] 调整内容风格
- [ ] 发布到其他子版块（r/programming, r/Python）

### 本周计划
- [ ] 发布 5-10 条测试帖子
- [ ] 找到最佳发布时间
- [ ] 确定受欢迎的内容类型
- [ ] 测试不同子版块

### 本月目标
- [ ] 建立 3-5 个主力子版块
- [ ] 每周 5-10 条高质量内容
- [ ] 积累 100+ Karma
- [ ] 创建定时任务自动化

---

## ⚠️ 注意事项

### 速率限制
- **同一子版块**: 1 post/10min
- **API 调用**: 60 requests/min（PRAW 自动处理）
- **总发帖**: 建议 <10 posts/day

### 内容质量
- 宁可少发，也要高质量
- 每次发帖都要有价值
- 避免"仅推广"账号
- 保持 10 comments : 1 post 比例

### 安全
- 不要分享 Client Secret
- 不要在代码中硬编码凭证
- 定期检查 Token 是否泄露

---

## 🆘 常见问题

### Q: 创建 App 时找不到 "script" 选项？
**A**: 确保已登录 Reddit 账号，并且账号已验证邮箱

### Q: 认证失败 "invalid_grant"？
**A**: 检查:
- 用户名和密码是否正确
- 账号是否已验证邮箱
- 是否启用了两步验证（需要应用密码）

### Q: 发帖失败 "RATELIMIT"？
**A**: 等待 10 分钟后再试，或换一个子版块

### Q: 帖子被删除？
**A**: 检查子版块规则，可能违反了版规

### Q: 如何找到子版块规则？
**A**: 访问子版块，查看右侧边栏 "Rules" 或 "Posting Guidelines"

---

## 📞 需要帮助？

- **PRAW 文档**: https://praw.readthedocs.io
- **Reddit API 文档**: https://www.reddit.com/dev/api
- **Reddit 帮助**: https://www.reddithelp.com

---

## 🚀 进阶使用

### 多子版块发布

```python
from reddit_poster import RedditPoster, RedditContentGenerator

poster = RedditPoster()

# 生成内容
content = RedditContentGenerator.generate_project_post(
    project_name="OpenOctopus",
    description="Realm-native life agent system",
    features=["Context management", "State persistence"],
    github_url="https://github.com/open-octopus/openoctopus"
)

# 发布到多个子版块
subreddits = ["opensource", "programming", "Python"]
for sub in subreddits:
    result = poster.submit_post(
        subreddit=sub,
        title=content["title"],
        text=content["text"]
    )
    if result["success"]:
        print(f"✅ Posted to r/{sub}")
```

### 定时任务

```python
# 添加到 OpenClaw Cron
from openclaw import cron

cron.add(
    name="Reddit Daily Post",
    schedule="0 14 * * *",  # 每天 14:00 UTC
    command="python ~/.openclaw/workspace/skills/reddit-poster/reddit_poster.py"
)
```

---

**预计总时间**: 10-15 分钟
**难度**: ⭐⭐ (简单)
**成功率**: 95%+

开始实施吧！🐕🚀
