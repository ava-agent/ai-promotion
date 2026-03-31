# Hacker News 任务体系设计

**设计日期**: 2026-03-25
**平台**: Hacker News
**账号**: kevinten10
**状态**: 已接入，Ask HN 可用，Show HN 待解锁

---

## 🎯 任务体系概览

```
┌─────────────────────────────────────────────────────────────┐
│                    Hacker News 任务体系                       │
├─────────────────────────────────────────────────────────────┤
│  Level 1: 基础互动 (Karma 积累期)                              │
│    ├── Ask HN 发帖 (每周 2-3 次)                              │
│    ├── 评论互动 (每天 3-5 条)                                 │
│    └── 链接分享 (有价值的技术文章)                             │
├─────────────────────────────────────────────────────────────┤
│  Level 2: 项目展示 (Karma 解锁后)                              │
│    ├── Show HN 项目发布 (每月 1-2 次)                         │
│    ├── 项目更新分享 (重大功能)                                │
│    └── 技术深度讨论 (Launch 后跟进)                           │
├─────────────────────────────────────────────────────────────┤
│  Level 3: 社区影响 (长期建设)                                  │
│    ├── 成为领域专家 (持续高质量贡献)                          │
│    ├── 引导技术讨论 (话题发起者)                              │
│    └── 社区声誉建设 (被认可的声音)                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 任务分类详解

### 1. Ask HN 任务体系

**目的**: 建立社区声誉、积累 Karma、了解社区需求

#### 1.1 技术问题类 (40%)

**频率**: 每周 1-2 次
**最佳时间**: 工作日 9-11 AM EST

**内容方向**:
- 架构设计问题
- 技术选型困惑
- 性能优化挑战
- 工程实践疑问

**模板示例**:
```
标题: Ask HN: How do you handle {technical_challenge} in {context}?

正文:
I'm working on {project_description}, and we're facing a challenge with {specific_problem}.

Current approach:
- {what_we_tried}
- {what_worked}
- {what_didn't_work}

Specific questions:
1. {question_1}
2. {question_2}

What's your experience with this? Any lessons learned or best practices?

Thanks!
```

**质量检查清单**:
- [ ] 问题具体、可回答
- [ ] 已尝试过解决方案
- [ ] 有明确的上下文
- [ ] 邀请经验分享

#### 1.2 经验征询类 (30%)

**频率**: 每周 1 次
**最佳时间**: 工作日 2-4 PM EST

**内容方向**:
- 技术趋势看法
- 工具使用体验
- 工作流程优化
- 职业发展建议

**模板示例**:
```
标题: Ask HN: What's your experience with {technology/topic}?

正文:
Context: {why_asking}

Specific questions:
- {question_1}
- {question_2}
- {question_3}

Looking for real-world experiences and practical advice.

Thanks!
```

#### 1.3 社区互动类 (30%)

**频率**: 每周 1 次
**最佳时间**: 周末 10 AM - 12 PM EST

**内容方向**:
- 有趣的技术发现
- 行业观察分享
- 轻松技术话题
- 社区氛围建设

---

### 2. 评论互动任务体系

**目的**: 建立社区存在感、积累 Karma、建立声誉

#### 2.1 评论策略

**频率**: 每天 3-5 条高质量评论
**分配**:
- 技术帖子: 2 条
- Show HN: 1-2 条
- Ask HN: 1-2 条

**评论类型**:

**A. 技术深度评论** (40%)
```
内容结构:
1. 肯定/认可对方的观点
2. 补充技术细节或经验
3. 提出建设性问题
4. 分享相关资源

示例:
"Great point about {topic}. We've seen similar results in our system.

One thing to watch out for: {potential_issue}.

We solved this by {solution}, which reduced latency by ~30%.

Related: {link_to_resource}"
```

**B. 经验分享评论** (30%)
```
内容结构:
1. 简短的个人经验
2. 具体的做法/工具
3. 结果/影响
4. 开放性问题

示例:
"We faced this exact issue last year. Here's what worked for us:

- {approach_1}
- {approach_2}

Result: {outcome}

Curious if others have tried {alternative_approach}?"
```

**C. 问题探讨评论** (20%)
```
内容结构:
1. 表达兴趣
2. 提出深度问题
3. 分享思考角度
4. 邀请讨论

示例:
"Interesting approach! Have you considered {alternative_perspective}?

In our experience, {related_challenge} becomes significant at scale.

Would love to hear your thoughts on how you handle {specific_aspect}."
```

**D. 资源分享评论** (10%)
```
内容结构:
1. 简短认可
2. 相关资源链接
3. 资源价值说明
4. 适用场景

示例:
"Thanks for sharing! For anyone interested in {topic}, this might be helpful:

{resource_link}

It covers {specific_aspect} which complements your approach."
```

#### 2.2 评论时机

| 时机 | 策略 | 说明 |
|------|------|------|
| **新帖发布** (0-2h) | 抢先评论 | 早期曝光高，易获 upvote |
| **热门帖** (2-6h) | 深度评论 | 流量大，建立专业形象 |
| **深夜** (EST) | 避免评论 | 流量低，效果差 |

#### 2.3 评论禁忌

❌ **避免**:
- 简短无营养回复 ("Thanks", "Great", "Agreed")
- 纯粹的表情符号
- 与主题无关的评论
- 攻击性或负面评论
- 自我推广过度

✅ **必须**:
- 每条评论至少 2-3 句话
- 提供价值或引发思考
- 保持礼貌和专业
- 与帖子主题相关

---

### 3. Show HN 任务体系

**目的**: 项目曝光、获取反馈、建立技术声誉
**状态**: 待解锁（需积累 Karma）

#### 3.1 解锁条件

**预计需要**:
- Karma: 10-50
- 评论数: 20-50 条
- 账号年龄: 1-2 周

**当前进度**:
- Karma: 0 (新账号)
- 评论数: 0
- Ask HN: 已发布 1 条

#### 3.2 Show HN 发布计划

**频率**: 每月 1-2 次（重大里程碑）
**最佳时间**: 周二/周四 9-11 AM EST

**发布时机**:
1. **项目正式发布** (v1.0)
2. **重大功能更新** (里程碑版本)
3. **开源项目开源** (首次公开)
4. **有趣的技术实验** (创新项目)

**项目优先级**:
1. OpenOctopus (Realm-native agent)
2. Trip Agent (旅行规划)
3. Capa-Java (多运行时 SDK)
4. AI Tools (工具分析)

#### 3.3 Show HN 内容模板

```
标题: Show HN: {Project Name} - {One-line description}

正文结构:

## What it does
{Clear description of the problem it solves}

## Key features
- {Feature 1 with benefit}
- {Feature 2 with benefit}
- {Feature 3 with benefit}

## Why I built this
{Personal story and motivation}

## Tech stack
{Technologies used}

## Demo/Links
- Live demo: {url}
- GitHub: {url}
- Website: {url}

## Feedback welcome!
{Specific questions for community}
```

#### 3.4 Show HN 后续跟进

**发布后 24h 内**:
- [ ] 回复所有评论（前 6 小时最关键）
- [ ] 感谢建设性反馈
- [ ] 记录有价值的建议
- [ ] 澄清误解

**发布后 1 周内**:
- [ ] 根据反馈更新项目
- [ ] 发布更新评论
- [ ] 继续参与讨论

---

### 4. 链接分享任务体系

**目的**: 分享有价值内容、建立技术品味

#### 4.1 分享策略

**频率**: 每周 1-2 次
**内容来源**:
- 自己的技术博客文章
- 发现的有价值的开源项目
- 优质技术文章/视频
- 行业趋势分析

**质量要求**:
- 必须自己阅读/使用过
- 有实质性的技术价值
- 不是纯粹的新闻
- 有明确的受众

#### 4.2 分享格式

```
标题: {Article/Project Title}

链接: {url}

一句话说明: {why_its_valuable}
```

---

## ⏰ 定时任务配置

### 每日任务

```yaml
# 评论监控任务 (每 2 小时)
- name: "HN Comment Monitor"
  schedule: "0 */2 * * *"
  action: monitor_comments
  duration: 5min

# 每日评论任务
- name: "HN Daily Comments"
  schedule: "0 10,14,18 * * *"  # EST 10AM, 2PM, 6PM
  action: post_comments
  count: 3-5
  duration: 15min
```

### 每周任务

```yaml
# Ask HN 发布
- name: "HN Ask HN Weekly"
  schedule: "0 10 * * 2,4"  # 周二/周四 10AM EST
  action: post_ask_hn
  count: 2-3/week
  duration: 10min

# Show HN 检查 (解锁后)
- name: "HN Show HN Check"
  schedule: "0 9 * * 2"  # 周二 9AM EST
  action: check_show_hn_unlock
  duration: 2min

# 数据汇总
- name: "HN Weekly Summary"
  schedule: "0 20 * * 0"  # 周日 8PM
  action: generate_summary
  duration: 10min
```

---

## 📊 数据追踪体系

### 追踪指标

| 指标 | 目标 | 追踪频率 |
|------|------|---------|
| **Karma** | 50+ | 每日 |
| **评论数** | 20+/周 | 每日 |
| **Ask HN 回复数** | 5+ per post | 每次 |
| **Show HN upvote** | 10+ (解锁后) | 每次 |
| **评论质量** | avg 2+ upvote | 每周 |

### 数据记录

```json
{
  "date": "2026-03-25",
  "karma": 0,
  "posts": {
    "ask_hn": 1,
    "show_hn": 0,
    "links": 0
  },
  "comments": {
    "total": 0,
    "avg_upvotes": 0
  },
  "engagement": {
    "replies_received": 0,
    "mentions": 0
  }
}
```

---

## 🔄 优化总结流程

### 每日优化 (自动)

**时间**: 每天 23:00
**任务**:
1. 分析今日评论效果
2. 识别高互动话题
3. 调整明日策略
4. 记录成功案例

### 每周优化 (人工审核)

**时间**: 每周日 21:00
**任务**:
1. 周数据汇总分析
2. 评论质量评估
3. 内容策略调整
4. 下周计划制定

### 每月优化 (深度复盘)

**时间**: 每月最后一周
**任务**:
1. Show HN 解锁评估
2. Karma 增长分析
3. 社区声誉评估
4. 长期策略调整

---

## 📝 内容日历模板

### 第 1 周 (Karma 积累期)

| 日期 | 任务 | 内容方向 |
|------|------|---------|
| Mon | Ask HN | 架构设计问题 |
| Tue | Comments | 技术帖子 3 条 |
| Wed | Ask HN | 工具使用体验 |
| Thu | Comments | Show HN 2 条 |
| Fri | Comments | Ask HN 2 条 |
| Sat | Ask HN | 轻松技术话题 |
| Sun | Summary | 数据分析 |

### 第 2-4 周 (持续积累)

- 保持每周 2-3 个 Ask HN
- 每天 3-5 条高质量评论
- 周末检查 Karma 进度
- 准备 Show HN 内容

### 解锁后 (Show HN + Ask HN)

| 周 | Ask HN | Show HN | Comments |
|----|--------|---------|----------|
| 5 | 2 | 0 | 25 |
| 6 | 2 | 1 | 25 |
| 7 | 1 | 0 | 20 |
| 8 | 2 | 1 | 25 |

---

## 🎯 成功标准

### 短期目标 (1-2 周)
- [ ] Karma: 10+
- [ ] 评论: 20+
- [ ] Ask HN: 3-5 条
- [ ] 建立基本存在感

### 中期目标 (1 个月)
- [ ] Karma: 50+
- [ ] 评论: 100+
- [ ] Show HN: 解锁
- [ ] 发布第一个项目

### 长期目标 (3 个月)
- [ ] Karma: 200+
- [ ] Show HN: 3-5 个项目
- [ ] 社区认可的声音
- [ ] 项目获得流量

---

## 📁 相关文件

- 主脚本: `skills/hn-poster/hn_poster_v2.py`
- Ask HN 测试: `skills/hn-poster/test_ask_hn.py`
- 任务配置: `memory/hn-task-schedule.yaml`
- 数据追踪: `memory/hn-analytics.json`
- 内容模板: `memory/hn-content-templates.md`

---

**状态**: 任务体系设计完成
**下一步**: 配置定时任务，开始执行
