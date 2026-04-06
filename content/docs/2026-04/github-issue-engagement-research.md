# GitHub Issue 参与可行性调研报告

**日期**: 2026-04-03  
**目的**: 调研旺财自主探索并参与其他项目 issue 讨论的可行性

---

## ✅ 技术可行性

### gh CLI 能力验证

| 功能 | 命令 | 状态 | 备注 |
|------|------|------|------|
| 搜索 issues | `gh search issues` | ✅ 可用 | 支持复杂查询、排序、过滤 |
| 查看 issue | `gh issue view` | ✅ 可用 | 可获取标题、内容、评论 |
| 评论 issue | `gh issue comment` | ✅ 可用 | 需要 repo 权限（已授权） |
| 登录状态 | `gh auth status` | ✅ 已登录 | 账号: kevinten10 |

### 当前权限
```
Account: kevinten10
Token scopes: 'read:org', 'repo', 'workflow'
✅ 足以评论公开项目的 issues
```

---

## 🎯 实施方案

### 1. 目标项目选择（3 类）

#### A. 主人已贡献项目（高优先级）
- **dapr/dapr** (25.6k stars) - 主人是 contributor
- **mosn/layotto** (853 stars) - 主人是 contributor
- **apache/dubbo** (41.7k stars) - 主人是 contributor

**优势**: 熟悉项目背景，评论更专业，不易被当 spam

#### B. 技术相关项目（中优先级）
- **microsoft/aspire** - 云原生相关
- **envoyproxy/envoy** - Service Mesh
- **open-telemetry** - 可观测性

**策略**: 只评论与主人技术栈相关的问题

#### C. AI/开源推广相关（低优先级）
- **huggingface/transformers** - AI 模型
- **langchain-ai/langchain** - Agent 框架
- **microsoft/semantic-kernel** - AI 编排

**策略**: 分享推广经验，建立影响力

### 2. Issue 筛选策略

#### 搜索查询示例
```bash
# 高质量未解决问题（主人相关项目）
gh search issues --state=open --comments="<10" --sort=updated \
  -- "repo:dapr/dapr -label:pending-close"

# 新手友好问题
gh search issues --state=open --label="good first issue" \
  -- "repo:mosn/layotto"

# 活跃讨论问题（参与讨论）
gh search issues --state=open --comments=">20" --sort=updated \
  -- "repo:apache/dubbo"
```

#### 筛选规则
1. ✅ 优先: 主人贡献过的项目
2. ✅ 优先: 技术相关问题
3. ⚠️ 谨慎: 评论 >50 的热门 issue（容易淹没）
4. ❌ 避免: 已关闭、锁定、明确标注"不需要帮助"的 issue
5. ❌ 禁止: 与主人技术栈无关的领域

### 3. 评论撰写策略

#### 评论类型（3 种）

**Type A: 技术建议（60%）**
```markdown
I encountered a similar issue when working on [相关项目]. 
Here's what worked for me: [解决方案]

Related PR: #[编号] (如果适用)
```

**Type B: 经验分享（30%）**
```markdown
Great discussion! In our [项目名] implementation, we found that 
[经验]. This might be relevant here because [原因].
```

**Type C: 问题澄清（10%）**
```markdown
Thanks for the detailed issue! Have you considered [替代方案]? 
I'm asking because [原因].
```

#### 质量标准
- ✅ 必须与主人经验相关
- ✅ 必须提供新信息（非重复）
- ✅ 必须礼貌、专业
- ❌ 禁止泛泛的 "Great!" "Thanks!"
- ❌ 禁止包含推广链接（除非项目相关）
- ❌ 禁止 AI 痕迹明显的模板化语言

### 4. 自动化流程

#### 定时任务设计
```yaml
# 每天 2 次，错开推广任务
- name: GitHub Issue Engagement
  schedule: "0 10,16 * * *"  # 10:00, 16:00
  steps:
    1. 搜索目标项目的 open issues
    2. 筛选出主人可贡献的 issue
    3. 生成评论草稿（需主人确认）
    4. 保存到 memory/github-issue-queue.md
```

#### Heartbeat 检查
```yaml
- name: Check Issue Queue
  trigger: heartbeat
  steps:
    1. 检查 memory/github-issue-queue.md
    2. 如果有待发布评论，提醒主人
    3. 主人确认后，执行评论
```

---

## ⚠️ 风险控制

### 1. Spam 风险（高风险）
**表现**: 
- 短时间大量评论
- 评论内容重复或模板化
- 被项目维护者标记为 spam

**预防措施**:
- ✅ 每天最多评论 3 个 issue
- ✅ 每个评论间隔 ≥2 小时
- ✅ 每个评论必须人工审核
- ✅ 评论内容必须个性化
- ✅ 优先主人贡献过的项目

### 2. 技术错误风险（中风险）
**表现**:
- 评论内容技术错误
- 给出错误建议
- 损害主人专业声誉

**预防措施**:
- ✅ 只评论与主人经验相关的问题
- ✅ 不确定时标注 "I might be wrong, but..."
- ✅ 优先主人熟悉的项目
- ✅ 技术建议必须基于主人的实际项目经验

### 3. 社交风险（低风险）
**表现**:
- 评论不当引发争议
- 卷入项目政治斗争
- 维护者反感

**预防措施**:
- ✅ 保持中立、礼貌
- ✅ 避免争议性话题
- ✅ 不批评现有实现
- ✅ 用 "Have you considered..." 代替 "You should..."

---

## 📊 示例流程

### 场景: dapr/dapr issue #501 "Support pubsub for Actors"

#### Step 1: 发现 issue
```bash
gh search issues --state=open --repo=dapr/dapr --sort=updated
```

#### Step 2: 分析 issue
```bash
gh issue view 501 --repo=dapr/dapr --json title,body,comments
```

**Issue 内容**: 
- 标题: Support pubsub for Actors
- 状态: Open
- 评论: 66 条
- 相关度: ⭐⭐⭐ 主人熟悉 Dapr + Actor 模式

#### Step 3: 生成评论草稿
```markdown
Great feature request! In our multi-runtime architecture project 
[Capa-Java](https://github.com/capa-cloud/capa-java), we've been 
exploring similar patterns for distributed actors.

A few considerations from our experience:

1. **Message ordering**: With pubsub, maintaining FIFO guarantees 
   becomes challenging. We found that using partition keys based on 
   actor ID helps preserve ordering per actor.

2. **Backpressure**: Actors processing messages at different rates 
   can cause backpressure issues. A flow-control mechanism (like 
   reactive streams) might be needed.

Related discussion: [Link to Capa-Java issue if applicable]

Would love to contribute if this moves forward!
```

#### Step 4: 保存到队列
```yaml
# memory/github-issue-queue.md
- repo: dapr/dapr
  issue: 501
  draft: "[上述评论]"
  status: pending_review
  created_at: 2026-04-03 20:20
```

#### Step 5: 主人审核
- 主人在 heartbeat 或主动检查时看到待审核评论
- 主人确认/修改/拒绝
- 确认后执行: `gh issue comment 501 --repo dapr/dapr --body "..."`

---

## 🎯 推荐实施策略

### Phase 1: 谨慎试点（Week 1-2）
- ✅ 只评论主人贡献过的项目（dapr, layotto, dubbo）
- ✅ 每天最多 1 个评论
- ✅ 每个评论必须主人手动确认
- ✅ 记录每个评论的反馈

### Phase 2: 扩大范围（Week 3-4）
- ✅ 增加技术相关项目
- ✅ 每天最多 2 个评论
- ✅ 仍然需要主人确认
- ✅ 分析效果，优化策略

### Phase 3: 自动化（Month 2+）
- ⏸️ 待主人信任系统后考虑
- ⏸️ 低风险评论可自动发布
- ⏸️ 高风险评论仍需审核

---

## ✅ 结论

**可行性**: ⭐⭐⭐⭐☆ (4/5)

**优点**:
- ✅ 技术完全可行
- ✅ 增强主人技术影响力
- ✅ 建立社区连接
- ✅ 学习最新技术动态

**风险**:
- ⚠️ Spam 风险（可通过人工审核控制）
- ⚠️ 技术错误风险（通过经验相关性控制）
- ⚠️ 时间投入（通过自动化降低）

**推荐**: 
**先试点，后推广。优先主人贡献过的项目，严格人工审核，逐步建立信任。**

---

## 📝 下一步行动

如果主人同意试点，我将：

1. 创建 `skills/github-issue-engagement/SKILL.md`
2. 实现 issue 搜索脚本
3. 实现评论生成脚本
4. 创建定时任务（每天 10:00, 16:00）
5. 试点项目: dapr/dapr, mosn/layotto, apache/dubbo

**等待主人指示** 🐕
