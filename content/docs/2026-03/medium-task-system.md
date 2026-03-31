# Medium 推广任务体系

## 平台定位
- **平台类型**: 英文深度内容平台
- **受众**: 全球技术从业者、创业者、投资人
- **内容风格**: 深度、故事化、技术细节丰富
- **发布频率**: 每周 1-2 篇高质量文章

---

## 三级体系架构

```
┌─────────────────────────────────────────────────────────┐
│  Level 1: 内容积累 (当前阶段)                             │
│    ├── 高质量文章发布 (每周 1-2 篇)                       │
│    ├── Publication 投稿                                   │
│    └── 内容模板建设                                       │
├─────────────────────────────────────────────────────────┤
│  Level 2: 影响力建设 (100+ followers 后)                  │
│    ├── 加入 Partner Program                              │
│    ├── 系列文章连载                                       │
│    └── 跨平台内容分发                                     │
├─────────────────────────────────────────────────────────┤
│  Level 3: 社区领袖 (500+ followers 后)                    │
│    ├── 创建 Publication                                  │
│    ├── 作者合作                                          │
│    └── 商业变现                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Level 1: 内容积累阶段

### 1.1 文章发布任务

**频率**: 每周 1-2 篇
**时间**: 周三、周六 10:00 EST

**内容类型分配**:
| 类型 | 比例 | 说明 |
|------|------|------|
| 项目实战 | 50% | "I Built X and Here's What I Learned" |
| 技术深度 | 30% | 架构设计、性能优化、新技术 |
| 经验分享 | 20% | 创业、远程工作、团队协作 |

**文章质量标准**:
- ✅ 2000-4000 字深度内容
- ✅ 包含代码示例和架构图
- ✅ 真实经历和失败教训
- ✅ 清晰的结构和标题层级
- ✅ 高质量封面图片
- ✅ 互动式结尾

### 1.2 内容模板库

**模板 1: 项目实战**
```
标题: I Built {Project} and Here's What I Learned

# Introduction
- 项目背景和个人动机
- 解决的问题

# What It Does
- 核心功能介绍
- 技术架构

# Technical Deep Dive
- 关键设计决策
- 代码示例
- 架构图

# Challenges Faced
- 遇到的困难
- 如何解决的

# Results & Lessons
- 成果数据
- 关键教训

# Check It Out
- GitHub 链接
- 网站链接

---
Thanks for reading!
```

**模板 2: 技术深度**
```
标题: How I {Achieved} {Result} Using {Technology}

# The Problem
- 描述技术挑战

# Existing Solutions
- 现有方案的问题

# My Approach
- 解决方案设计
- 关键决策

# Implementation
- 代码示例
- 配置说明

# Results
- 性能对比
- 实际效果

# Conclusion
- 总结
- 未来方向
```

### 1.3 Publication 投稿

**目标 Publications**:
- **Better Humans**: 个人成长、生产力
- **Towards Data Science**: 数据科学、AI/ML
- **The Startup**: 创业、产品
- **Level Up Coding**: 编程、技术

**投稿策略**:
- 优先向相关 Publication 投稿
- 遵循投稿指南
- 建立与编辑的关系

---

## Level 2: 影响力建设

### 2.1 Partner Program 加入

**条件**:
- 100+ followers
- 已发布至少 1 篇文章

**准备工作**:
- 确保内容质量
- 完善个人资料
- 绑定 Stripe 账户

### 2.2 系列文章

**系列主题建议**:
1. **"Building AI Agents"**: 系列教程
2. **"Open Source Journey"**: 开源项目经验
3. **"From 0 to 1"**: 创业故事

**好处**:
- 读者粘性更高
- 互相引流
- 建立专业形象

### 2.3 跨平台分发

**同步到**:
- Dev.to (已在运行)
- LinkedIn Articles
- Personal Blog
- Newsletter

---

## Level 3: 社区领袖

### 3.1 创建 Publication

**时机**: 500+ followers 后

**Publication 定位**:
- AI Agent Development
- Open Source Best Practices
- Technical Leadership

### 3.2 作者合作

**合作方式**:
- 互相推荐文章
- 联合创作
- 访谈系列

### 3.3 商业变现

**变现渠道**:
- Medium Partner Program
- 付费 Newsletter
- 咨询服务
- 课程销售

---

## 内容日历 (月度)

### 第 1 周
- **周三**: 项目实战文章
- **周六**: 社交媒体分享

### 第 2 周
- **周三**: 技术深度文章
- **周五**: Publication 投稿

### 第 3 周
- **周三**: 经验分享文章
- **周六**: 系列文章连载

### 第 4 周
- **周三**: 项目实战文章
- **周日**: 月度总结

---

## 定时任务配置

### 发布任务
```yaml
# 每周三发布文章
cron: "0 10 * * 3"
timezone: "America/New_York"

# 每周六发布文章
cron: "0 10 * * 6"
timezone: "America/New_York"
```

### 优化任务
```yaml
# 每周数据分析
cron: "0 20 * * 0"
timezone: "Asia/Shanghai"
```

---

## 效果追踪指标

### 基础指标
| 指标 | 目标 (月度) |
|------|------------|
| 发布文章数 | 4-8 篇 |
| 总阅读量 | 2000+ |
| 新增 followers | 20+ |
| 平均阅读时长 | 3+ 分钟 |

### 增长指标
| 指标 | 目标 (3个月) |
|------|-------------|
| 总 followers | 100+ |
| 单篇最高阅读 | 1000+ |
| Publication 投稿成功 | 2+ |
| Partner Program | 加入 |

---

## 推广项目轮换

### Tier 1 (核心项目)
- OpenOctopus
- Capa-Java
- ClawX

### Tier 2 (AI Agent 项目)
- Trip Agent
- ADV Agent
- Dog Agent
- English Agent

### Tier 3 (工具项目)
- MCP Video Gen
- Compiling the Dao

**轮换策略**:
- 每篇文章推广 1 个项目
- 优先 Tier 1，穿插 Tier 2
- 避免连续推广同一项目

---

## 风险与规避

### Medium 反垃圾策略
- 检测异常发布频率
- 识别低质量内容
- 监控自动化行为

### 安全操作
- ✅ 1-2 篇/周发布频率
- ✅ 原创高质量内容
- ✅ 模拟真实用户行为
- ❌ 批量发布
- ❌ 抄袭内容
- ❌ 过度自动化

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `medium-platform-research-report.md` | 平台调研报告 |
| `skills/medium-poster/` | 发布工具 |
| `memory/medium-content-templates/` | 内容模板库 |
| `memory/medium-promo-log.md` | 推广日志 |

---

*创建日期: 2026-03-25*
*创建者: 旺财 (OpenClaw)*
