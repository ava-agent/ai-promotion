# V2EX 自动发帖调研报告

> 调研时间：2026-04-17 01:47 | 更新：2026-04-17 12:00 (Asia/Shanghai)
> 状态：⚠️ 官方 API 仅支持读取，发帖需浏览器自动化

---

## 1. 平台概况

- **网址**: https://www.v2ex.com
- **性质**: 创意工作者社区，技术向讨论为主
- **创始人**: @Livid (Babel Engine)
- **活跃度**: 日活较高，中文技术圈核心社区之一
- **注册**: **邀请码制度** — 新用户注册需邀请码（或通过 GitHub/Google OAuth 后可能需要绑定邀请码）

## 2. 官方 API 调研

### 2.1 V2EX 非官方 API（只读，djyde/V2EX-API ⭐375）

V2EX 提供的 API 全部为 **只读接口**，无写入（发帖/回帖）API。

| Endpoint | 说明 |
|----------|------|
| `/api/site/info.json` | 站点信息 |
| `/api/site/stats.json` | 站点统计 |
| `/api/nodes/all.json` | 所有节点列表 |
| `/api/nodes/show.json?id=<id>` | 单个节点信息 |
| `/api/topics/latest.json` | 最新主题 |
| `/api/topics/hot.json` | 热门主题 |
| `/api/topics/show.json?id=<id>` | 单个主题详情 |
| `/api/members/show.json?id=<id>` | 用户信息 |

### 2.2 V2EX 官方 API v2

V2EX 曾公布过 v2 API（`/api/v2/*`），支持 OAuth 2.0 认证，文档在 `https://www.v2ex.com/p/7v9KEP19`。

**已知 v2 API endpoints**:
- `GET /api/v2/topics/:topic_id` — 获取主题
- `GET /api/v2/topics/hot` — 热门主题
- `GET /api/v2/nodes/:node_name` — 节点信息
- `GET /api/v2/member` — 当前用户信息

**Token 获取**: OAuth 2.0 流程，需在 V2EX 设置中创建应用获取 Client ID/Secret。

**⚠️ 关键问题**: v2 API 同样**仅支持读取**，**没有发帖（POST topic）接口**。V2EX 从未开放写入 API。

## 3. 发帖方案评估

### 方案 A：浏览器自动化（✅ 可行，推荐）

**工具**: Playwright / Puppeteer / Selenium

**流程**:
1. 登录 v2ex.com（使用已有账号 cookie 或模拟登录）
2. 导航到目标节点，如 `https://www.v2ex.com/go/create`
3. 填写标题和内容
4. 提交表单

**Python 示例代码（Playwright）**:

```python
from playwright.sync_api import sync_playwright
import time

def post_to_v2ex(title: str, content: str, node: str = "create"):
    """通过浏览器自动化在 V2EX 发帖
    
    Args:
        title: 帖子标题
        content: 帖子内容（支持部分 Markdown）
        node: 节点名称，如 create, python, share 等
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # 方式1: 使用已有 cookie 登录
        # context.add_cookies([
        #     {"name": "A2", "value": "你的cookie值", "domain": ".v2ex.com", "path": "/"}
        # ])
        
        page = context.new_page()
        
        # 方式2: 先手动登录（首次运行）
        page.goto("https://www.v2ex.com/signin")
        print("请在浏览器中手动登录，登录完成后按回车继续...")
        input()
        
        # 导航到发帖页面
        page.goto(f"https://www.v2ex.com/go/{node}")
        page.click("text=发新主题")
        
        # 填写表单
        page.fill('input[name="title"]', title)
        page.fill('textarea[name="content"]', content)
        
        # 选择节点（如果需要更改）
        # page.select_option('select[name="node_name"]', node)
        
        # 提交
        page.click('button[type="submit"]')
        
        # 等待发布完成
        page.wait_for_url("**/t/*")
        print(f"发帖成功！URL: {page.url}")
        
        # 保存储状态用于下次
        context.storage_state(path="v2ex-auth.json")
        
        browser.close()

# 使用示例
post_to_v2ex(
    title="分享一个开源项目",
    content="项目介绍...\n\nGitHub: https://github.com/...",
    node="share"
)
```

**注意事项**:
- V2EX 有 Cloudflare 防护，headless 模式可能被拦截，建议 `headless=False`
- 首次需手动登录保存 cookie，后续可复用
- Cookie 有效期较长（数月），但需定期检查

### 方案 B：直接 HTTP POST（❌ 不推荐）

V2EX 发帖表单提交到 `https://www.v2ex.com/go/{node}` 的 POST 端点。

**理论上的 curl 示例**（需要有效 cookie 和 once token）:

```bash
# 1. 获取 once token（CSRF）
curl -s -b "A2=你的cookie" \
  "https://www.v2ex.com/go/create" | \
  grep -oP 'once="[^"]*' | head -1

# 2. 提交发帖（once 值从页面获取）
curl -X POST "https://www.v2ex.com/go/create" \
  -b "A2=你的cookie" \
  -d "title=测试标题&content=测试内容&once=从页面获取的值" \
  -H "Referer: https://www.v2ex.com/go/create"
```

**问题**:
- 需要获取 CSRF `once` token
- Cloudflare 会拦截纯 HTTP 请求（需要 cf_clearance cookie）
- 稳定性差，容易被封

### 方案 C：第三方 API 代理（❓ 待验证）

部分第三方项目试图封装 V2EX 的 Web 操作为 API，但大多已过时或不可用。

## 4. 账号与限制

| 项目 | 详情 |
|------|------|
| **注册方式** | 邀请码制度，需老用户邀请；或通过 GitHub/Google OAuth |
| **邀请码** | 老用户可通过每日签到获得邀请码名额 |
| **新号限制** | 新注册账号无法立即发帖，需一定的活跃度/等级 |
| **发帖频率** | 同一节点发帖间隔约 10 分钟以上；每日总量无硬限制但不建议过多 |
| **内容审核** | 社区自治，违规会被管理员降权/封号 |
| **Markdown** | 支持 **有限的 Markdown**：粗体、斜体、链接、代码块、图片；**不支持**表格、脚注等高级语法 |
| **封号风险** | ⚠️ **高风险** — V2EX 对机器人发帖容忍度极低，被发现会立即封号。建议：模拟人类行为、间隔随机、内容有价值 |

## 5. GitHub 相关项目

### API 封装（读取为主）

| 项目 | Stars | 说明 |
|------|-------|------|
| [djyde/V2EX-API](https://github.com/djyde/V2EX-API) | ⭐375 | 非官方 API 文档，只读 |
| [funnyzak/react-native-v2ex](https://github.com/funnyzak/react-native-v2ex) | ⭐292 | RN 客户端，含 API 调用示例 |
| [isaced/V2exAPI](https://github.com/isaced/V2exAPI) | — | Swift 封装 |

### Bot 类项目

| 项目 | Stars | 说明 |
|------|-------|------|
| [im3x/GeekBot](https://github.com/im3x/GeekBot) | ⭐81 | 企业微信推送 V2EX 热帖（只读抓取） |
| [yanglbme/v2ex-action](https://github.com/yanglbme/v2ex-action) | — | GitHub Action 推送 V2EX 热帖 |

### 2026-04-17 更新搜索结果

**API 类项目**（均为只读封装）:
- Vue 全家桶二次开发 V2EX 社区（支持 CORS）
- V2ex API Swift 封装（iOS/macOS）
- v2ex 接口 NestJS 版本

**Bot 类项目**（均为签到/读取/推送）:
- V2EX GitHub Action — 自动发送热门内容到企业微信/钉钉
- 企业微信机器人推送（天气、V2EX 帖子等）
- V2EX 签到 + Telegram 推送（Python3）
- 文章爬取 Bot（V2EX 等平台转 Markdown）
- V2EX 交易区监控机器人
- GLaDOS + V2EX 自动签到工具（支持 Bark/Telegram 通知）

**结论**: GitHub 上**没有找到**可靠的 V2EX 自动发帖项目，仅有读取/签到/推送类工具。与上次调研一致。

## 6. 推荐实施方案

### 最终推荐：Playwright 浏览器自动化

```
1. 人工登录 V2EX → 保存 cookie/storage state
2. Playwright 加载 storage state → 自动化发帖
3. 随机间隔（10-30 分钟）
4. 内容必须有价值，避免灌水
5. 定期检查 cookie 有效性
```

**集成到 OpenClaw 的方式**:
- 使用 `browser` 工具直接操作
- 或调用 Playwright Python 脚本
- Cookie/状态文件保存在 `memory/v2ex-auth.json`

## 7. 风险评估

| 风险 | 级别 | 缓解措施 |
|------|------|---------|
| 封号 | 🔴 高 | 控制频率、内容质量优先、模拟人类行为 |
| Cloudflare 拦截 | 🟡 中 | 使用有头浏览器、保存 cookie |
| Cookie 过期 | 🟢 低 | 定期检查、设置提醒重新登录 |
| 内容审核 | 🟡 中 | 避免广告、水帖，发布有价值内容 |

---

## ⚠️ 需要用户介入的卡点

### 卡点 1：🔑 V2EX 账号（阻塞）

- **问题**: 需要一个有效的 V2EX 账号
- **用户需做**: 
  - 确认是否已有 V2EX 账号
  - 如无账号，需要邀请码注册（Kevin 主人是否已有邀请码？）
- **状态**: ❓ 待确认

### 卡点 2：🍪 Cookie/登录态（阻塞）

- **问题**: 浏览器自动化需要有效的登录 cookie
- **用户需做**: 
  - 在浏览器中手动登录 V2EX
  - 导出 A2 cookie 或配合手动登录流程
- **状态**: ❓ 待确认

### 卡点 3：📍 发帖节点选择

- **问题**: V2EX 按节点（Node）组织内容，需选择合适的节点
- **常见节点**: `share`（分享）、`create`（创意）、`python`、`programmer`、`opensource`
- **用户需做**: 确认常发帖的节点
- **状态**: ❓ 待确认

### 卡点 4：📝 内容策略

- **问题**: V2EX 社区对内容质量要求较高，纯推广帖会被踩/封
- **建议**: 
  - 技术分享型内容（开源项目介绍、技术教程）
  - 先参与社区讨论建立信誉，再发推广
- **用户需做**: 确认内容方向
- **状态**: ❓ 待确认

### 卡点 5：⚖️ 封号风险评估

- **问题**: V2EX 对机器人行为零容忍
- **用户需做**: 确认是否接受账号风险（建议用小号）
- **状态**: ❓ 待确认

---

## 结论

**V2EX 没有官方写入 API，自动发帖只能通过浏览器自动化实现。** 技术上可行但风险较高，建议：
1. 使用 Playwright 浏览器自动化方案
2. 控制发帖频率（每天 ≤ 3 帖）
3. 内容质量为王，避免纯推广
4. 优先选择 `share`、`create` 等适合分享的节点
5. 考虑使用小号而非主力账号
