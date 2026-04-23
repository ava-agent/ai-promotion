# Dev.to 自动发帖经验总结

> 最后更新：2026-03-29 23:20

## ✅ 正确的发帖流程

### 1. 生成文章内容
- 读取 `memory/github-projects-rotation.md` 获取当前推广项目
- 用 GitHub CLI 拉取真实项目数据
- 写 1500-2500 词英文文章
- 保存到 `memory/devto-article-draft.md`

### 2. 生成 JSON Body 文件
```powershell
node -e "
const fs = require('fs'), os = require('os');
const md = fs.readFileSync(os.homedir() + '/.openclaw/workspace/memory/devto-article-draft.md', 'utf8');
const title = md.split('\n')[0].replace(/^#\s*/, '').trim();
const body = JSON.stringify({ article: { title, body_markdown: md, published: true, tags: ['ai','opensource'] } });
fs.writeFileSync(os.homedir() + '/.openclaw/workspace/scripts/devto-publish-body.json', body);
console.log('Title:', title, '| Size:', body.length);
"
```

### 3. 用 curl.exe 发布（关键！）
```powershell
$apiKey = (Get-Content ~/.openclaw/workspace/memory/devto-api-key.txt).Trim()
curl.exe -s -w "`nHTTP:%{http_code}" -X POST "https://dev.to/api/articles" `
  -H "Content-Type: application/json" `
  -H "api-key: $apiKey" `
  -H "User-Agent: OpenClaw/1.0" `
  -d "@C:\Users\PC\.openclaw\workspace\scripts\devto-publish-body.json"
```

### 4. 验证结果
- HTTP 201 = 成功，提取返回的 `url` 和 `id`
- HTTP 403 = 检查是否误用了 Node.js（见下方踩坑记录）
- HTTP 422 = JSON 格式或内容问题

## ⚠️ 踩坑记录

### 坑1: Node.js https 模块在 Windows 下调 Dev.to API 返回 403
- **现象**: 用 Node.js `https.request()` POST 到 `dev.to/api/articles` 返回 403，响应体为空
- **原因**: Windows 环境下 Node.js 的 TLS/代理处理与 curl.exe 不同
- **解决**: **必须用 curl.exe + @file 方式传 JSON body**
- **验证**: 同一个 API key，curl.exe 返回 201，Node.js 返回 403
- **时间**: 2026-03-29

### 坑2: kimi 模型在 isolated session 中只输出开场白
- **现象**: output_tokens 只有 80-243，agent 只说"主人好！旺财来帮你执行..."就结束
- **原因**: Prompt 太长太复杂，kimi 在 isolated session 中不稳定
- **解决**: Prompt 开头加 `【重要：直接执行以下步骤，不要输出开场白或寒暄。第一步就开始调用工具。】`
- **效果**: output_tokens 从 243 提升到 13,591（56倍）
- **时间**: 2026-03-29

### 坑3: kimi API "引擎过载" rate limit (429)
- **现象**: `429 {"error":{"type":"rate_limit_error","message":"The engine is currently overloaded"}}`
- **原因**: 多个 cron 任务同时向 kimi API 发请求（08:00 三个同时，09:00 四个同时，20:00 三个同时）
- **解决**:
  1. 错开任务时间，每个时间段最多 1 个任务，间隔 ≥15 分钟
  2. maxConcurrent 从 4 降到 2
- **时间**: 2026-03-29

### 坑4: OpenClaw 重试间隔太短
- **现象**: rate limit 后 OpenClaw 只等 4s/4s/6s/10s 就放弃（总共 ~25 秒）
- **kimi 过载恢复**: 通常需要 1-2 分钟
- **缓解**: 通过错开时间避免同时触发，而不是依赖重试

## 📋 Dev.to API Key 信息
- **文件位置**: `~/.openclaw/workspace/memory/devto-api-key.txt`
- **权限**: 读写都有 ✅
- **账号**: kevinten10
- **测试方法**: `curl.exe -s -H "api-key: $(Get-Content ~/.openclaw/workspace/memory/devto-api-key.txt)" "https://dev.to/api/articles/me?per_page=1"`

## 📋 Cron 任务配置 (2026-04-20更新)

### ❌ 当前手动流程 (即将弃用)
- **Job ID**: `180c8c4f-6bd5-48de-af58-244c1b3bac23`
- **名称**: Dev.to Project Promotion (手动版)
- **执行时间**: 每天 11:00, 15:00, 19:00 (Asia/Shanghai)
- **模型**: kimi-coding/k2p5
- **timeout**: 900 秒
- **问题**: 仍使用手动curl.exe流程，技能闲置

### ✅ 新自动化流程 (立即启用)
- **Job ID**: `devto-publisher-v2`
- **名称**: Dev.to Auto Publisher (技能版)
- **执行时间**: 每天 11:00, 15:00, 19:00 (Asia/Shanghai)
- **模型**: kimi-coding/k2p5
- **timeout**: 900 秒
- **技能集成**: 启用 `skills/devto-publisher/`
- **关键优势**:
  - 自动质量检测 (≥0.8分)
  - 自动发布数据追踪
  - A/B测试框架集成
  - 错误处理和重试机制
  - 数据驱动优化建议

### 🚀 立即执行计划
```markdown
1. 🚨 今天立即切换到自动化技能
2. 🚨 启用Test-D001标题风格A/B测试
3. 🚨 建立完整数据追踪体系
4. 🚨 废弃手动curl.exe流程
```

## 📋 文件路径
| 文件 | 用途 |
|------|------|
| `memory/devto-api-key.txt` | API Key |
| `memory/devto-article-draft.md` | 文章草稿（每次覆盖） |
| `scripts/devto-publish-body.json` | curl 发布用的 JSON body |
| `scripts/devto-publish-now.js` | 手动发布脚本（备用，但在 Windows 下可能 403） |
| `memory/devto-promo-log.md` | 发布日志 |
| `memory/github-projects-rotation.md` | 项目轮换记录 |
