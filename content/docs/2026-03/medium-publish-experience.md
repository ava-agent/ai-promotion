# Medium 发布经验总结

> 2026-03-29 排障修复记录，供后续参考

## 问题时间线

| 时间 | 事件 |
|------|------|
| 3/25 | 创建 Medium poster skill（Playwright + Cookie 方案） |
| 3/25 | 提取 Cookie 保存到 medium_cookies.json |
| 3/26 | 周六 cron 任务首次运行，agent 只说"让我开始"就结束（38秒），未执行脚本 |
| 3/26-3/29 | Medium 零发帖，cron 任务每次都"假成功" |
| 3/29 22:37 | 主人发现问题 |
| 3/29 22:42 | 诊断：Cookie 失效 + Cloudflare 拦截 + 选择器过时 + 登录检测 bug |
| 3/29 22:57 | 主人在 Chrome 登录 Medium |
| 3/29 23:00 | 诊断编辑器 DOM 结构成功 |
| 3/29 23:02 | Dry run 测试通过 |
| 3/29 23:04 | 正式发布成功（English Agent） |
| 3/29 23:05 | 更新 cron 任务（周三 + 周六） |
| 3/29 23:11 | 验证文章在线（2篇） |

## 根因分析

### 为什么 Cookie 方案行不通

```
独立 Playwright 浏览器
  → 无 Cloudflare 挑战记录
  → 被 CF 拦截，URL 变为 ?__cf_chl_rt_tk=xxx
  → Cookie 虽然加载了但 CF 不认
  → 访问 /new-story 跳转到 /m/signin
  → 在登录页上操作编辑器选择器全部超时
  → 备用方法（JS evaluate）在登录页上无效果
  → 脚本返回 URL = /new-story 误判为成功
```

### 为什么 is_logged_in() 误判

旧代码逻辑：
1. 访问 medium.com → CF 挑战页面（没有 sign in 按钮也没有 user menu）
2. 所有检测都跳过
3. 访问 /me/stories → 被重定向但 URL 暂时包含 stories
4. 返回 True

**正确做法**：检测 URL 是否包含 `/signin` 更可靠。

### 为什么 cron agent 没执行脚本

旧 cron prompt 让 agent：
1. 先调 mcporter 获取 content-styles 模板
2. 再调 GitHub CLI 获取项目信息
3. 再生成文章
4. 再执行 publish_task.py

Agent 在步骤 1 就耗光了 budget/timeout，根本走不到步骤 4。

**正确做法**：cron prompt 直接执行 `python publish_cdp.py`，内容生成逻辑在脚本内部完成。

## CDP 方案为什么可靠

| 对比项 | Cookie 方案 | CDP 方案 |
|--------|------------|---------|
| Cloudflare | ❌ 被拦截 | ✅ 共享浏览器 CF 状态 |
| 登录态 | ❌ 容易过期 | ✅ 跟用户共享 |
| 编辑器操作 | ❌ headless 不稳定 | ✅ 真实浏览器环境 |
| 维护成本 | 高（Cookie 定期更新） | 低（只需保持登录） |

## 编辑器关键选择器（2026-03-29）

```
标题: h3[data-testid="editorTitleParagraph"]
正文: p[data-testid="editorParagraphText"]  
发布: button:has-text("Publish")
确认: button:has-text("Publish now") 或 button:has-text("Publish"):not([disabled]).last
添加媒体: button[data-testid="editorAddButton"]
```

## 发布流程关键点

1. `page.goto("https://medium.com/new-story")` 后等 6-8 秒让编辑器完全加载
2. 标题用 `keyboard.type()` 逐字输入，不要用 `fill()`（contenteditable 不支持 fill）
3. 标题输完后按 `Enter` 切换到正文区域
4. 正文逐行输入，不要一次性注入 innerHTML
5. 点 Publish 后等 3 秒，会弹出标签/设置面板
6. 标签输入框选择器: `input[placeholder*="tag"]`
7. 最终确认按钮用 `.last`（避免点到第一个已禁用的 Publish 按钮）
8. 发布后 URL 会变为 `medium.com/p/{id}/submission?...postPublishedType=initial`

## 后续维护清单

- [ ] Medium 编辑器 UI 变更时：运行 `diagnose_cdp.py` 更新选择器
- [ ] Chrome 登录过期时：在 CDP Chrome 手动登录
- [ ] 内容质量优化：在 `publish_cdp.py` 的 `generate_content()` 里改模板
- [ ] 增加新项目：在 `publish_cdp.py` 的 `PROJECTS` 列表里添加
