# Facebook / Instagram / Threads 自动发帖调研

**创建时间**: 2026-04-13 09:06
**最后更新**: 2026-04-13 09:18
**状态**: 🔄 调研进行中，定时任务已创建

---

## 📊 调研总览

三个平台均属于 Meta 生态，共享底层认证体系。**最佳方案是 Upload-Post API**（一次配置，三个平台通用）。

---

## 方案一: Upload-Post API（⭐ 推荐）

### 概述
- **官网**: https://upload-post.com
- **API**: https://api.upload-post.com/api
- **价格**: Free 10次/月，Basic $19/月
- **支持平台**: Facebook ✅ Instagram ✅ Threads ✅（以及 TikTok、YouTube、X、LinkedIn 等 10+）

### 各平台支持情况

| 平台 | 视频 | 图片 | 纯文本 | 定时发布 | 特殊要求 |
|------|------|------|--------|---------|---------|
| **Facebook** | ✅ | ✅ | ✅ | ✅ | 需 Page ID（不支持个人主页） |
| **Instagram** | ✅ | ✅ | ❌ | ✅ | 需 Business/Creator 账号 |
| **Threads** | ✅ | ✅ | ✅ | ✅ | 需关联 Instagram 账号 |

### Facebook 特有参数
- `facebook_page_id`: Facebook Page ID（必须）
- `facebook_description`: 视频描述
- `facebook_media_type`: STORIES / REELS / regular
- `facebook_first_comment`: 自动首条评论
- `video_state`: DRAFT / PUBLISHED

### Instagram 特有参数
- `media_type`: REELS / IGTV / regular
- `share_mode`: 可选
- `collaborators`: 合作者用户名
- `instagram_first_comment`: 自动首条评论
- `cover_url`: 自定义视频封面

### Threads 特有参数
- `threads_title`: Threads 专属标题
- `threads_first_comment`: 自动首条评论
- `threads_topic_tag`: 话题标签（1-50字符）
- 支持 Carousel（与 Instagram 共享混合轮播）

### 关键端点
```bash
# 视频
POST /api/upload_videos
# 图片（支持 carousel）
POST /api/upload_photos
# 纯文本（Facebook, Threads 支持）
POST /api/upload_text

# 查询 Facebook Pages
GET /api/uploadposts/facebook/pages

# 查看历史
GET /api/uploadposts/history

# 定时发布
# 在请求中加 scheduled_date 参数
```

---

## 方案二: Meta Graph API（直接调用）

### Facebook
- 需要: Facebook App + Page Access Token
- 限制: **不支持个人主页**，只能发到 Facebook Page
- 端点: `POST /{page-id}/feed` (文本) / `POST /{page-id}/videos` (视频)
- 免费但有速率限制

### Instagram
- 需要: Instagram Business/Creator 账号 + Facebook Page + Content Publishing API
- 端点: `POST /{ig-user-id}/media` → `POST /{ig-user-id}/media_publish`
- 限制: 不支持个人账号发帖

### Threads
- 需要: Instagram 账号关联
- 端点: `POST /{threads-user-id}/threads`
- 2024年6月开放 API

---

## 🔒 需要主人介入的卡点

### 卡点 1: Upload-Post 注册和 API Key（⭐ 最优先）
- [ ] 访问 https://upload-post.com 注册账号
- [ ] 连接 Facebook / Instagram / Threads 账号
- [ ] 创建 Profile（如 "kevin"）
- [ ] 生成 API Key
- [ ] 把 API Key 和 Profile 名告诉我

### 卡点 2: Facebook Page 创建（如果还没有）
- [ ] 创建 Facebook Page（个人主页无法通过 API 发帖）
- [ ] 获取 Page ID

### 卡点 3: Instagram 账号升级
- [ ] 确认 Instagram 是 Business 或 Creator 账号
- [ ] 关联到 Facebook Page

### 卡点 4: Threads 账号确认
- [ ] 确认 Threads 已关联 Instagram

---

## 🕐 定时任务

已创建以下 cron 任务持续调研和推进：

| 任务名 | 说明 | 频率 |
|--------|------|------|
| `fb-ig-threads-research` | 持续调研自动发帖方案，尝试突破卡点 | 每4小时 |

---

## 风险和注意事项

1. **Facebook 个人主页无法 API 发帖** - 必须使用 Page
2. **Instagram 需要专业账号** - 普通个人账号无法使用 API
3. **Meta 文档在国内被墙** - 需要代理访问 developers.facebook.com
4. **Upload-Post 是第三方服务** - 账号安全取决于其安全性
5. **自动化发帖频率** - 不建议太高，可能被平台标记为 spam

---

## 下一步行动

1. **等待主人**: 完成 Upload-Post 注册 + API Key
2. **自动推进**: cron 任务会持续调研，如有新发现会通知
3. **注册完成后**: 我可以立即编写发帖脚本和定时发布流程

---

## 📋 调研日志

### 2026-04-13 13:21 (CST)

**发现**: Upload-Post API 新增 **AutoDM Monitors** 功能（Instagram 自动私信）

- 功能：设置持久监控器，自动给在 Instagram 帖子下评论的用户发送私信（DM）
- 限制：
  - 仅支持 Instagram
  - 每个账号每天最多创建 2 个监控器
  - 监控器 15 天后自动过期
  - Free 计划 10 DM/天，Paid 计划 500 DM/天
  - Meta 限制每小时 200 DM
  - 只能回复 7 天内的评论
- API 端点：`POST /api/autodms/start`（创建监控）、`GET /api/autodms/status`（查状态）等
- 支持 `trigger_keywords` 过滤评论关键词（支持重音/大小写不敏感匹配）

**其他方案调研**:
- Buffer API：仍可用（`api.bufferapp.com/1/`），60 请求/分钟限速，支持 Facebook/Instagram/Twitter 发帖，但功能较基础，不如 Upload-Post 全面
- n8n 集成：有 Facebook Graph API 节点，但本质还是封装 Meta API，同样需要 Page + Business 账号
- Meta 开发者文档（developers.facebook.com）无法直接抓取（网络限制），未发现 API 政策变化

**结论**: Upload-Post 仍是最佳方案，且在持续增加新功能。无新的替代方案。卡点不变，仍需主人介入注册 Upload-Post 并连接社交账号。

### 2026-04-13 21:26 (CST)

**发现**: Upload-Post API 新增功能：

1. **FFmpeg Editor API** (`POST /api/ffmpeg-editor`)
   - 在服务端安全执行 FFmpeg 命令处理媒体
   - 支持视频转码、提取音频、多视频拼接等
   - 支持 multi-input（`{input0}`, `{input1}`...），可做 concat
   - 配额按媒体时长（分钟/月）：Free 30min, Basic 300min, Pro 1000min, Business 10000min
   - 异步模式：提交后轮询 job status

2. **Analytics API** (`GET /api/analytics/profile_username`)
   - 跨平台分析数据获取
   - 可查询多个社交平台的分析指标

3. **Current User API** (`GET /api/current-user`)
   - 验证 API Key 有效性
   - 返回关联邮箱和订阅计划信息

**Meta 开发者文档**: developers.facebook.com 仍无法直接抓取（网络限制），无法确认 Meta API 最新变化。

**结论**: Upload-Post 持续在扩展功能（视频编辑、数据分析），API 能力越来越完整。无新的替代方案出现。卡点不变 — 仍需主人介入注册。

### 2026-04-14 13:31 (CST)

**发现**: Upload-Post API 新增多项重要功能，API 文档大幅扩展：

1. **Instagram Comments API** (`GET /api/uploadposts/comments`)
   - 获取帖子评论列表（支持 post_id 或 post_url）
   - 发送私信回复评论（Private Reply）：`POST /api/uploadposts/comments/reply`
   - 速率限制：每帖 10 分钟内只能查询一次

2. **Instagram DMs API**（直接消息）
   - 发送 DM：`POST /api/dms/send`（需 recipient_id）
   - 获取对话列表：`GET /api/dms/conversations`
   - Instagram 要求接收者先发过消息（24h 窗口）

3. **跨平台 Media List API** (`GET /api/uploadposts/media`)
   - 支持 Instagram、TikTok、YouTube、LinkedIn、Facebook、X、Threads、Pinterest、Bluesky、Reddit
   - 统一返回结构（id、caption、media_type、media_url、permalink、timestamp）
   - 可用于获取帖子 ID 和 URL 以配合 AutoDM

4. **Reddit 详细帖子 API** (`GET /api/uploadposts/reddit/detailed-posts/`)
   - 含完整媒体信息（图片、画廊、视频）
   - 自动分页，最多 2000 条

5. **新增平台支持**
   - **Google Business Profile**：`GET /api/uploadposts/google-business/locations` 查询位置，支持发帖
   - **Bluesky**：Analytics 和 Media List 已支持

6. **新增资源查询端点**
   - LinkedIn Pages：`GET /api/uploadposts/linkedin/pages`
   - Pinterest Boards：`GET /api/uploadposts/pinterest/boards`

7. **FFmpeg 新增 Advanced 计划**：3000 分钟/月（位于 Professional 1000min 和 Business 10000min 之间）

**Meta 开发者文档**: developers.facebook.com 仍无法直接抓取（网络限制）。

**其他方案**:
- 搜索了 Buffer、n8n 等替代方案，无实质变化
- Buffer 仍为基础发帖功能，不如 Upload-Post 全面
- n8n 本质是封装 Meta Graph API，同样需要 Page + Business 账号

**结论**: Upload-Post 持续快速迭代，已从单纯的发帖 API 扩展为完整社交媒体管理平台（发帖 + 评论管理 + DM + 数据分析 + 媒体处理）。对于我们的用例，Instagram 评论管理和 DM 自动化是很有价值的附加功能。**卡点不变 — 仍需主人介入注册 Upload-Post 并连接社交账号。**
