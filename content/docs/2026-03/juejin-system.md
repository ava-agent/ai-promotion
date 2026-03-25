# 掘金自动发布系统 ✨

## 系统概述（2026-03-24 新增）

### 功能特性
- ✅ Markdown 文章自动发布
- ✅ 标题、标签、分类设置
- ✅ GitHub 链接支持
- ⏳ 本地图片上传（待实现）
- ⏳ 批量发布（待实现）

### 技术实现
```
juejin-publisher/
├── SKILL.md              # 使用说明
├── config.yaml           # 配置文件
├── .env                  # Cookie 存储
├── juejin_client.py      # API 客户端
├── test_api.py           # API 测试
├── publish_test.py       # 发布测试
└── test_article.md       # 测试文章
```

### API 端点
- 创建草稿: `POST /content_api/v1/article_draft/create`
- 发布文章: `POST /content_api/v1/article/publish`
- 获取分类: `POST /tag_api/v1/query_category_list`
- 获取标签: `POST /tag_api/v1/query_tag_list`

### Cookie 管理
- **有效期**: ~30 天
- **存储**: `.env` 文件
- **过期提醒**: 待实现
- **自动刷新**: 待实现（Browser 兜底）

### 发布流程
```
1. 读取 Markdown 文件
2. 解析元数据（标题、标签、分类）
3. 上传本地图片（如有）
4. 创建草稿 → API 调用
5. 发布文章 → API 调用
6. 记录到 juejin-promo-log.md
```

### 定时任务
- **推广频率**: 每天 3 次（12:00, 16:00, 20:00）
- **与知乎、Dev.to 共用**: github-projects-rotation.md 项目列表
- **格式**: Markdown
- **允许链接**: ✅ 可以包含 GitHub 链接

### 平台特性
- **内容格式**: Markdown（比知乎的 HTML 更方便）
- **标签限制**: 最多 5 个标签
- **分类**: 后端、前端、AI、Android、iOS 等 8 个
- **发布频率**: 建议单日 ≤10 篇，单小时 ≤3 篇

### 推广日志
- **日志文件**: `memory/juejin-promo-log.md`
- **记录内容**: 发布时间、标题、URL、效果数据

---

## 跨平台推广矩阵 ✨

### 平台对比

| 特性 | 知乎 | Dev.to | 掘金 |
|------|------|--------|------|
| **格式** | HTML | Markdown | Markdown |
| **允许链接** | ✅ | ✅ | ✅ |
| **标签限制** | 5 个 | 5 个 | 5 个 |
| **发布频率** | 3 次/天 | 3 次/天 | 3 次/天 |
| **受众** | 中文技术 | 国际开发者 | 中文开发者 |
| **Cookie 有效期** | 1-3 月 | API Key | ~30 天 |

### 时间错开策略

```
10:00 - 知乎推广
11:00 - Dev.to 推广
12:00 - 掘金推广 ✨
14:00 - 知乎推广
15:00 - Dev.to 推广
16:00 - 掘金推广 ✨
18:00 - 知乎推广
19:00 - Dev.to 推广
20:00 - 掘金推广 ✨
```

### 内容复用策略

- **知乎（HTML）** ← 转换 ← **Markdown 原稿**
- **Dev.to（Markdown）** ← 直接使用 ← **Markdown 原稿**
- **掘金（Markdown）** ← 直接使用 ← **Markdown 原稿**

### 推广效果预期

| 平台 | 阅读量/篇 | 点赞/篇 | 评论/篇 |
|------|----------|---------|---------|
| 知乎 | 50-200 | 5-15 | 2-5 |
| Dev.to | 100-500 | 10-30 | 5-10 |
| 掘金 | 100-500 | 5-20 | 2-5 |

---

## 更新日志

### 2026-03-24
- ✅ 创建 `juejin-publisher` Skill
- ✅ 实现掘金 API 客户端
- ✅ 测试文章成功发布（文章 ID: 7620769530676707368）
- ✅ 创建定时任务（每天 3 次）
- ✅ 更新 MEMORY.md
- ✅ 创建推广日志文件
