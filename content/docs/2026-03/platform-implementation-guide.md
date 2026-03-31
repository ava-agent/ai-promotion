# Medium 和 Hacker News 平台实施步骤指南

## 🎯 目标
使用 Browser Automation (Playwright) 在 Medium 和 Hacker News 发布内容

---

## 📋 前置准备

### 安装 Playwright（2分钟）

```bash
# 安装 Playwright
pip install playwright

# 安装 Chromium 浏览器
python -m playwright install chromium
```

验证安装:
```bash
python -c "from playwright.sync_api import sync_playwright; print('✅ Playwright 已安装')"
```

---

## 平台 1: Hacker News

### Step 1: 准备账号信息（1分钟）

确认你有 Hacker News 账号：
- 用户名: kevinten10
- 密码: [你的密码]

如果没有账号，访问 https://news.ycombinator.com/login 创建。

### Step 2: 设置环境变量（1分钟）

**方法 A: 临时设置（推荐首次测试）**

```powershell
# Windows PowerShell
$env:HN_USERNAME="kevinten10"
$env:HN_PASSWORD="your_password_here"
```

**方法 B: 永久设置**

```powershell
# 添加到系统环境变量
[Environment]::SetEnvironmentVariable("HN_USERNAME", "kevinten10", "User")
[Environment]::SetEnvironmentVariable("HN_PASSWORD", "your_password_here", "User")
```

### Step 3: 测试工具（1分钟）

```bash
python ~/.openclaw/workspace/skills/hn-poster/hn_poster.py
```

**期望流程**:
```
============================================================
🐕 Hacker News 自动发帖工具
============================================================
时间: 2026-03-25 13:50:00

✅ 浏览器启动成功
🔐 登录 Hacker News...
✅ 登录成功: kevinten10
✅ Cookie 已保存

📊 获取 kevinten10 的帖子...
✅ 找到 0 条帖子

📝 生成测试内容...

生成内容预览:
  标题: Show HN: OpenOctopus - Realm-native life agent system
  长度: 542 字符

  正文预览:
Hello HN! 👋
...

确认发布? (yes/no): yes

🚀 发布中...
✅ 提交成功
  链接: https://news.ycombinator.com/item?id=12345678

✅ 发布成功!
  链接: https://news.ycombinator.com/item?id=12345678
```

### Step 4: 验证结果

1. **打开帖子链接**
   - 访问发布的链接
   - 确认帖子显示正常

2. **检查时间线**
   - 访问: https://news.ycombinator.com/submitted?id=kevinten10
   - 确认帖子出现在提交列表

3. **观察互动**
   - 检查 upvote/downvote
   - 回复评论（如有）

---

## 平台 2: Medium

### Step 1: 准备账号信息（1分钟）

确认你有 Medium 账号：
- 邮箱: [你的邮箱]
- 密码: [你的密码]

如果没有账号，访问 https://medium.com 创建。

### Step 2: 设置环境变量（1分钟）

**方法 A: 临时设置（推荐首次测试）**

```powershell
# Windows PowerShell
$env:MEDIUM_EMAIL="your@email.com"
$env:MEDIUM_PASSWORD="your_password_here"
```

**方法 B: 永久设置**

```powershell
# 添加到系统环境变量
[Environment]::SetEnvironmentVariable("MEDIUM_EMAIL", "your@email.com", "User")
[Environment]::SetEnvironmentVariable("MEDIUM_PASSWORD", "your_password_here", "User")
```

### Step 3: 测试工具（1分钟）

```bash
python ~/.openclaw/workspace/skills/medium-poster/medium_poster.py
```

**期望流程**:
```
============================================================
🐕 Medium 自动发帖工具
============================================================
时间: 2026-03-25 13:55:00

✅ 浏览器启动成功
🔐 登录 Medium...
✅ 登录成功: your@email.com
✅ Cookie 已保存

📊 获取用户文章...
✅ 找到 0 篇文章

📝 生成测试内容...

生成内容预览:
  标题: I Built OpenOctopus and Here's What I Learned
  标签: Technology, Programming, Open Source
  长度: 642 字符

  正文预览:
# I Built OpenOctopus and Here's What I Learned
...

确认发布? (yes/no/draft): draft

📝 保存草稿...
✅ 草稿已保存
  链接: https://medium.com/p/abc123

✅ 草稿已保存!
  链接: https://medium.com/p/abc123
```

**建议**: 首次使用选择 "draft" 保存草稿，人工审核后再发布。

### Step 4: 验证结果

1. **打开草稿链接**
   - 访问保存的草稿
   - 确认格式和内容正确

2. **检查草稿列表**
   - 访问: https://medium.com/me/stories
   - 确认草稿出现在列表

3. **人工审核后发布**
   - 检查内容质量
   - 调整格式和标签
   - 点击 "Publish" 正式发布

---

## 🎉 完成！下一步

### 立即可以做

**Hacker News**:
- [ ] 观察首次 Show HN 效果
- [ ] 回复评论，建立社区信任
- [ ] 准备下一个项目发布

**Medium**:
- [ ] 审核草稿内容和格式
- [ ] 发布第一篇文章
- [ ] 观察阅读量和互动

### 本周计划

**Hacker News**:
- [ ] 发布 1-2 个项目（Show HN）
- [ ] 参与 Ask HN 讨论
- [ ] 积累 Karma

**Medium**:
- [ ] 发布 1-2 篇技术文章
- [ ] 建立发布节奏（1-2 篇/周）
- [ ] 研究 SEO 优化

### 本月目标

**Hacker News**:
- [ ] 3-5 个项目 Show HN
- [ ] 建立社区声誉
- [ ] 获得首页推荐

**Medium**:
- [ ] 4-8 篇高质量文章
- [ ] 积累 100+ followers
- [ ] 申请 Medium Partner Program

---

## ⚠️ 注意事项

### 通用注意事项
1. **质量第一**: 宁可少发，也要高质量
2. **人工审核**: 建议首次使用时人工确认
3. **Cookie 管理**: Cookie 会过期，需定期重新登录
4. **反检测**: 模拟真实用户，随机延迟

### Hacker News 特殊注意
1. **社区挑剔**: 质量差的内容会被 downvote
2. **避免营销**: 拒绝营销话术
3. **积极参与**: 发布后要回复评论
4. **Show HN 最佳时间**: 工作日 9-11 AM EST

### Medium 特殊注意
1. **内容长度**: 2000-5000 字最佳
2. **标题优化**: 吸引眼球但真实
3. **标签策略**: 选择 3-5 个相关标签
4. **SEO 友好**: 使用清晰的标题结构（H1, H2, H3）

---

## 🆘 常见问题

### Q: Playwright 安装失败？
**A**: 尝试以下方法:
```bash
# 方法 1: 使用国内镜像
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方法 2: 手动下载浏览器
python -m playwright install --help
```

### Q: 登录失败？
**A**: 检查:
- 用户名/邮箱和密码是否正确
- 账号是否已验证
- 网络连接是否正常
- 是否有验证码（需要人工处理）

### Q: Cookie 什么时候过期？
**A**: 
- Hacker News: 通常 30 天
- Medium: 通常 30 天
- 建议每月重新登录一次

### Q: 发布失败？
**A**: 可能原因:
- 登录状态过期 → 重新登录
- 网络问题 → 检查网络
- 页面变化 → 更新脚本

### Q: 内容格式错乱？
**A**: 
- 检查 Markdown 格式
- 避免特殊字符
- 使用标准段落结构

---

## 📞 需要帮助？

- **Playwright 文档**: https://playwright.dev/python
- **Hacker News Guidelines**: https://news.ycombinator.com/newsguidelines.html
- **Medium Help**: https://help.medium.com

---

## 🚀 进阶使用

### 批量发布（不推荐）

```python
# 示例：批量发布（谨慎使用）
from hn_poster import HackerNewsPoster

poster = HackerNewsPoster()
poster.start()

if poster.login("kevinten10", "password"):
    projects = [
        {"name": "Project1", "url": "..."},
        {"name": "Project2", "url": "..."}
    ]
    
    for project in projects:
        result = poster.submit_story(
            title=f"Show HN: {project['name']}",
            url=project['url']
        )
        time.sleep(3600)  # 间隔 1 小时

poster.close()
```

### 定时任务（推荐）

```python
# 添加到 OpenClaw Cron（人工触发）
# 不建议完全自动化，应该人工审核后发布

# 可以设置监控任务
from openclaw import cron

cron.add(
    name="HN Comment Monitor",
    schedule="0 */2 * * *",  # 每 2 小时
    command="python ~/.openclaw/workspace/skills/hn-poster/monitor_comments.py"
)

cron.add(
    name="Medium Weekly Reminder",
    schedule="0 10 * * 1",  # 每周一 10:00
    command="python ~/.openclaw/workspace/skills/medium-poster/reminder.py"
)
```

---

**预计总时间**: 15-20 分钟（两个平台）
**难度**: ⭐⭐ (简单)
**成功率**: 90%+

开始实施吧！🐕🚀
