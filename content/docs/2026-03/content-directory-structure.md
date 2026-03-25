# AI Promotion Content Assets

## 📁 目录结构说明

```
D:\project\ai-promotion/
├── 📁 content/                    # 原始内容资产
│   ├── 📁 moltbook/              # Moltbook 平台内容
│   │   ├── 📁 2026-03/           # 按月组织
│   │   │   ├── 2026-03-22-capajava-context-management.md
│   │   │   ├── 2026-03-22-openoctopus-realm-architecture.md
│   │   │   └── ...
│   │   └── 📁 2026-04/
│   ├── 📁 zhihu/                 # 知乎平台内容
│   │   ├── 📁 2026-03/
│   │   └── 📁 2026-04/
│   ├── 📁 devto/                 # Dev.to 平台内容
│   │   ├── 📁 2026-03/
│   │   └── 📁 2026-04/
│   ├── 📁 infoq/                 # InfoQ 平台内容（待创建）
│   ├── 📁 juejin/                # 掘金平台内容（待创建）
│   ├── 📁 xiaohongshu/           # 小红书平台内容（待创建）
│   ├── 📁 x/                     # X/Twitter 平台内容（待创建）
│   ├── 📁 tiktok/                # TikTok 平台内容（待创建）
│   ├── 📁 linkedin/              # LinkedIn 平台内容（待创建）
│   ├── 📁 csdn/                  # CSDN 平台内容（待创建）
│   └── 📁 wechat/                # 微信服务号内容（待创建）
│
├── 📁 templates/                  # 内容模板
│   ├── 📁 moltbook/
│   │   ├── technical-share.md    # 技术分享模板
│   │   ├── interactive-discussion.md  # 互动讨论模板
│   │   ├── greeting.md           # 问候模板
│   │   └── fun-observation.md    # 趣味观察模板
│   ├── 📁 zhihu/
│   │   └── article-template.html # 知乎文章模板
│   ├── 📁 devto/
│   │   └── article-template.md   # Dev.to 文章模板
│   └── 📁 common/
│       ├── project-intro.md      # 项目介绍模板
│       └── lesson-learned.md     # 经验总结模板
│
├── 📁 archive/                    # 归档内容
│   ├── 📁 drafts/                # 草稿箱
│   ├── 📁 rejected/              # 被平台拒绝的内容
│   ├── 📁 spam/                  # 被标记为 spam 的内容（用于分析）
│   └── 📁 backup/                # 定期备份
│
├── 📁 analytics/                  # 数据分析
│   ├── 📁 performance/           # 内容表现数据
│   │   ├── 2026-03-performance.md
│   │   └── ...
│   ├── 📁 insights/              # 洞察报告
│   │   ├── best-performing-topics.md
│   │   ├── optimal-posting-times.md
│   │   └── audience-engagement-patterns.md
│   └── 📁 ab-tests/              # A/B 测试结果
│
├── 📁 scripts/                    # 管理脚本
│   ├── content-organizer.py      # 内容整理脚本
│   ├── github-sync.py            # GitHub 同步脚本
│   ├── content-optimizer.py      # 内容优化脚本
│   └── publish-checker.py        # 发布检查脚本
│
├── 📁 docs/                       # 文档
│   ├── content-strategy.md       # 内容策略文档
│   ├── platform-guidelines.md    # 各平台发布规范
│   ├── quality-standards.md      # 质量标准
│   └── workflow.md               # 工作流程
│
├── 📄 README.md                   # 项目说明
├── 📄 .gitignore                  # Git 忽略文件
└── 📄 content-index.json          # 内容索引（自动更新）
```

## 🎯 设计原则

### 1. 按平台组织
- 每个平台独立目录
- 便于平台-specific 的搜索和管理
- 支持不同平台的内容格式差异

### 2. 按时间归档
- 按月分子目录
- 便于历史查找和趋势分析
- 支持长期的内容资产积累

### 3. 状态管理
- content/: 已发布的内容
- archive/drafts/: 草稿
- archive/rejected/: 被拒绝的内容
- archive/spam/: 被标记 spam 的内容（用于学习）

### 4. 元数据记录
- 文件名包含日期和主题
- content-index.json 自动维护索引
- 支持快速检索和关联分析

## 📊 文件命名规范

```
{日期}-{项目名}-{主题关键词}.{格式}

示例：
2026-03-22-capajava-context-management.md
2026-03-22-openoctopus-realm-architecture.md
2026-03-23-clawx-money-making-insights.md
```

## 🔄 工作流程

### 内容创建流程
1. 在 temp/ 目录创建草稿
2. 完善后移动到 content/{平台}/{月份}/
3. 更新 content-index.json
4. 提交到 GitHub

### 内容优化流程
1. 从 analytics/insights/ 获取优化建议
2. 修改 content/ 中的原始文件
3. 在 archive/backup/ 保留历史版本
4. 提交到 GitHub（带优化说明）

### GitHub 同步流程
1. 每日自动整理新内容
2. 生成当日提交摘要
3. 提交到 GitHub（auto-commit）
4. 更新远程内容索引

## 📈 价值体现

- **内容复用**: 跨平台内容改编
- **趋势分析**: 长期数据积累
- **质量提升**: 基于历史数据优化
- **资产沉淀**: 打造个人内容库
- **团队协作**: Git 版本控制支持

---

*设计时间: 2026-03-23 01:34 (UTC+8)*
*版本: v1.0*
