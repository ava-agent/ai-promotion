# Dev.to 项目推广日志

## 配置信息
- **工具**: promotion-agent
- **配置文件**: `~/.openclaw/workspace/promotion-agent/.env`
- **API Key**: ✅ 已配置
- **格式要求**: Markdown（支持完整 Markdown 语法）
- **推广频率**: 每天 3 次（11:00, 15:00, 19:00）
- **允许链接**: ✅ 可以包含 GitHub 项目链接
- **发布模式**: 直接发布（published=True，不是草稿）
- **定时任务 ID**: `180c8c4f-6bd5-48de-af58-244c1b3bac23`

## API Key 过期处理 ⚠️
- **检测机制**: API 返回 401/403 状态码
- **自动通知**: 发送 Telegram 消息给主人 (ID: 6837444385)
- **消息内容**: "❌ Dev.to API Key 已过期，请重新配置"
- **处理流程**: 停止推广，等待重新配置

## 发布记录

### 2026-03-22

#### 文章 7 - Capa-Java ✅
- **Post ID**: 3383514
- **URL**: https://dev.to/kevinten10/i-deployed-a-multi-runtime-sdk-847-times-in-production-here-are-5-brutal-truths-nobody-tells-you-42dl
- **项目**: Capa-Java (Multi-runtime SDK for Hybrid Cloud)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~2000 字
- **标签**: cloud, java, architecture, multicloud
- **内容亮点**:
  - 847次生产部署经验
  - 5个残酷真相
  - 抽象层泄漏（38%生产问题来自运行时边缘案例）
  - 性能税真实（5-15%开销，3x调试时间）
  - 测试矩阵爆炸（12→120+组合，17个关键bug）
  - 文档债务指数增长（47→312页）
  - 运行时漂移（18个月内14次更新，3次破坏性变更）
  - 5个核心教训（接受泄漏抽象、显式性能成本、自动化测试矩阵、投资文档生成、版本化一切）
- **发布时间**: 2026-03-22 19:00 北京时间 (11:00 UTC)
- **状态**: ✅ 成功

---

#### 文章 6 - AI Tools ✅
- **Post ID**: 3382752
- **URL**: https://dev.to/kevinten10/i-tested-30-ai-tools-for-847-hours-the-integration-patterns-nobody-talks-about-54n2
- **项目**: AI Tools (30+ AI Tools SWOT Analysis)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True)
- **字数**: ~2000 字
- **标签**: ai, integration, softwareengineering, api
- **内容亮点**:
  - 847小时测试经验
  - 67%认证级联问题
  - 41%假流式API
  - 52%静默截断
  - 78%无调试能力
  - 3工具规则
  - 4层决策框架
  - 5个核心教训
- **发布时间**: 2026-03-22 15:00 北京时间 (07:00 UTC)
- **状态**: ✅ 成功

---

#### 文章 4 - AI Tools ✅
- **Post ID**: 3382752
- **URL**: https://dev.to/kevinten10/i-tested-30-ai-tools-for-847-hours-the-integration-patterns-nobody-talks-about-54n2
- **项目**: AI Tools (30+ AI Tools SWOT Analysis)
- **格式**: Markdown
- **发布模式**: 直接发布(published=True)
- **字数**: ~1800 字
- **标签**: ai, integration, softwareengineering, api
- **内容亮点**:
  - 847小时测试经历，30+ AI工具集成经验
  - 隐藏集成税：67%认证级联、版本兼容性矩阵、流式谎言41%假流式
  - 上下文窗口陷阱：52%静默截断
  - 隐藏成本螺旋：18%重试成本、多模型溢价
  - 可观测性差距：78%工具无调试能力
  - 3工具规则：单应用最多3个AI工具
  - 4层决策框架：非协商层→集成检查→规模测试→团队适配
  - 5个核心教训：测试先于信任、抽象有代价、成本翻倍、社区信号>营销、隔离是保险
- **发布时间**: 2026-03-22 15:00 北京时间 (07:00 UTC)
- **状态**: ✅ 成功

---

### 2026-03-21

#### 文章 3 - MCP Image Gen ✅
- **Post ID**: 3380090
- **URL**: https://dev.to/kevinten10/i-integrated-5-image-generation-apis-and-all-of-them-failed-silently-what-mcp-taught-me-about-2fhm
- **项目**: MCP Image Gen (Image Generation MCP Tool)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~1900 字
- **标签**: mcp, imagegeneration, ai, api
- **内容亮点**:
  - 847次图像生成分析，23%静默失败率
  - 5大静默失败模式：成功谎言23%、模型选择迷宫47种组合、上下文窗口陷阱、尺寸政治31%、格式战争
  - 5层回退架构：请求验证→模型选择路由→并行请求处理器→响应验证器→格式标准化器
  - 性能数据：静默失败率23%→3%、满意度67%→91%、平均响应时间+1.2秒、成本+67%
  - 单工具哲学：专用工具vs多模型工具
  - 5个核心教训：APIs撒谎、用户不知道想要什么、验证非可选、抽象有成本、专业化>通用化
- **发布时间**: 2026-03-21 19:00 北京时间 (11:00 UTC)
- **状态**: ✅ 成功

#### 文章 2 - Compiling the Dao ✅
- **Post ID**: 3379271
- **URL**: https://dev.to/kevinten10/847-days-writing-an-open-source-novel-what-software-architecture-taught-me-about-storytelling-151i
- **项目**: Compiling the Dao (Open-Source Xianxia Novel)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~1800 字
- **标签**: opensource, creativewriting, architecture, devblog
- **内容亮点**:
  - 847天写作经历，软件架构与小说创作的碰撞
  - 领域驱动设计应用于小说：修为类型系统（如API契约）
  - 事件溯源：每个重大事件记录为不可变事件
  - 微服务架构：每个角色作为独立微服务
  - 3个失败教训：过早优化、过度抽象魔法系统、Git驱动剧情分支
  - 3个意外洞察：文档债务、重构情感成本、测试即Beta读者
  - 系统思维≠无灵魂，一致性是尊重的形式
  - 开放工具开发计划：Plot Event Store、Character State Machine、Consistency Linter
  - 5个核心教训
- **发布时间**: 2026-03-21 15:00 北京时间 (07:00 UTC)
- **状态**: ✅ 成功

#### 文章 1 - Trip Agent ✅
- **Post ID**: 3378740
- **URL**: https://dev.to/kevinten10/why-your-ai-travel-agent-doesnt-understand-somewhere-warm-and-how-i-fixed-it-4h97
- **项目**: Trip Agent (Travel Planning AI)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~1800 字
- **标签**: ai, travel, ux, productdesign
- **内容亮点**:
  - 47次迭代经历
  - 模糊请求问题（"somewhere warm"等）
  - 三阶段意图解析：感受提取→约束发现→偏好校准
  - 67%用户不提前提及预算/日期
  - 81%满意度、79%减少修订
  - 47%用户中途改变偏好
  - 多旅行者指数复杂度（4人=16×复杂度）
  - 5个核心教训
  - 问题先于搜索、校准优于画像
- **发布时间**: 2026-03-21 11:00 北京时间 (03:00 UTC)
- **状态**: ✅ 成功

### 2026-03-20

#### 文章 4 - Compiling the Dao ✅
- **Post ID**: 3376255
- **URL**: https://dev.to/kevinten10/847-days-writing-an-open-source-novel-what-building-software-taught-me-about-storytelling-6k9
- **项目**: Compiling the Dao (Open-Source Xianxia Novel)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~1800 字
- **标签**: opensource, writing, creativity, softwareengineering
- **内容亮点**:
  - 847天写作经历
  - 隐喻一致性如类型系统（dao-spec.md 文件）
  - 文档悖论（文档过多反而阻碍贡献者）
  - 重构陷阱（6周重构导致零新内容）
  - 开源治理问题（Lore Expansionist、Tone Shifters、Well-Meaning Fixer）
  - 抽象陷阱（失败的章节生成器）
  - 5个核心教训
  - 编程与修仙隐喻
- **发布时间**: 2026-03-20 19:00 北京时间 (11:00 UTC)
- **状态**: ✅ 成功

#### 文章 3 - Dog Agent ✅
- **Post ID**: 3375157
- **URL**: https://dev.to/kevinten10/your-pet-health-data-is-lying-and-so-is-your-ai-agent-3h7c
- **项目**: Dog Agent (Pet Health AI)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~1800 字
- **标签**: ai, datascience, healthtech, machinelearning
- **内容亮点**:
  - 5种数据谎言类型
  - 基线污染问题（38%基线照片已患病）
  - 情感采样偏差（62%照片来自同一会话）
  - 活动日志幻想（31%零活动日是项圈未佩戴）
  - 假阳性疲劳（早期89%误报率）
  - 4层预警系统设计
  - 多模态验证策略
  - 滚动基线衰减算法
  - 5个核心教训
- **发布时间**: 2026-03-20 15:00 北京时间 (07:00 UTC)
- **状态**: ✅ 成功

#### 文章 2 - ClawX ✅
- **Post ID**: 3374347
- **URL**: https://dev.to/kevinten10/i-analyzed-847-ai-money-making-attempts-94-failed-for-the-same-5-reasons-1onj
- **项目**: ClawX (AI Money-Making Guide)
- **格式**: Markdown
- **发布模式**: 直接发布（published=True）
- **字数**: ~1800 字
- **标签**: ai, startup, business, entrepreneurship
- **内容亮点**:
  - 847个AI赚钱案例分析
  - 5大失败模式：受众陷阱38%、复杂度陷阱27%、自动化幻觉19%、时机陷阱11%、集成噩梦5%
  - 5%成功者特征
  - 5个核心教训
- **发布时间**: 2026-03-20 11:00 北京时间 (03:00 UTC)
- **状态**: ✅ 成功

#### 文章 1 - OpenOctopus（测试）
- **Post ID**: 3373094
- **URL**: https://dev.to/kevinten10/openoctopus-how-ai-agents-can-truly-understand-your-life-ehd-temp-slug-7471752
- **格式**: Markdown
- **发布模式**: 草稿（published=False）- 测试用
- **状态**: ✅ 成功

## Markdown 格式优势 ✨

Dev.to 完整支持 Markdown 语法：
- ✅ 标题（# ## ###）
- ✅ 列表（- 或 1.）
- ✅ 链接（[text](url)）
- ✅ 图片（![alt](url)）
- ✅ 代码块（```language）
- ✅ 引用（>）
- ✅ 粗体/斜体（**bold** *italic*）
- ✅ 表格
- ✅ 任务列表（- [ ]）

## 推广策略

### 内容要求
- **字数**: 1500+ 字
- **格式**: Markdown
- **允许链接**: ✅ 可以包含 GitHub 项目链接
- **语言**: 英文（Dev.to 是国际社区）
- **故事形式**: 经验/教训/洞察
- **项目名**: 必须在标题中提及

### 发布流程
1. 读取项目轮换文件
2. 撰写英文 Markdown 内容（1500+ 字）
3. 调用 Dev.to API：
   - `POST https://dev.to/api/articles`
   - 参数 `published: True`（直接发布）
4. 检查响应（401/403 = API Key 过期）
5. 更新项目轮换计数
6. 记录到本日志

### 轮换规则
- **Tier 1 项目**: 每个推广 2 次
- **Tier 2 项目**: 每个推广 2 次
- **Tier 3 项目**: 每个推广 2 次
- 完成一个项目后自动切换到下一个

### 内容建议
- **分享开发经验**: "How I built..."
- **架构思考**: "Why I chose..."
- **踩坑经历**: "What I learned from..."
- **性能优化**: "How I improved..."
- **对比分析**: "X vs Y: My experience"

## API 维护
- **API Key**: 在 https://dev.to/settings/account 获取
- **权限**: 需要 "write:articles" 权限
- **有效期**: 永久（除非手动撤销）
- **检查方法**: 调用 `GET https://dev.to/api/articles/me` 验证

## 与知乎的区别

| 特性 | Dev.to | 知乎 |
|------|--------|------|
| 格式 | Markdown ✅ | HTML ⚠️ |
| 发布模式 | 可选草稿/发布 | 直接发布 |
| 链接 | 完全支持 ✅ | 支持 ✅ |
| 语言 | 英文 | 中文 |
| 社区 | 开发者 | 通用技术 |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 认证 | API Key | Cookie |
