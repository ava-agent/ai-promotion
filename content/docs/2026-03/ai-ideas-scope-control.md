# AI 创意开发系统 - 范围控制与协作规范

**更新时间**: 2026-03-23 01:45 (UTC+8)  
**更新内容**: 严格范围控制、反馈机制、数据 freshness

---

## ⚠️ 严格范围控制

### GitHub 范围

**✅ 允许的操作**:
- 在 `https://github.com/reware-frame` 组织中创建仓库
- 提交代码到 reware-frame 下的项目
- 拉取 reware-frame 仓库的更新
- 在 `https://github.com/ava-agent/ai-ideas` 中评论和讨论

**❌ 禁止的操作**:
- 在其他 GitHub org 创建仓库
- 在个人账号 (kevinten10) 下创建开发仓库
- 修改其他组织的仓库
- 访问未授权的私有仓库

**验证代码**:
```python
def validate_github_url(repo_url):
    if not repo_url.startswith("https://github.com/reware-frame/"):
        raise ValueError(f"🚫 范围错误: {repo_url}")
    return True
```

### 本地目录范围

**✅ 允许的目录**:
- `D:/project/agentcodings/` - 开发根目录
- `D:/project/agentcodings/ai-ideas-monitor/` - 监控数据
- `D:/project/agentcodings/active-projects/` - 活跃项目
- `D:/project/agentcodings/completed-projects/` - 已完成项目
- `D:/project/agentcodings/learning/` - 学习资料

**❌ 禁止的操作**:
- 访问 `C:/` 系统目录
- 修改 `~/.openclaw/` 配置目录
- 操作其他项目的代码
- 越界访问父目录

**验证代码**:
```python
def validate_scope(project_path):
    if not project_path.startswith("D:/project/agentcodings/"):
        raise ValueError(f"🚫 范围错误: {project_path}")
    return True
```

---

## 🔄 数据 Freshness 机制

### 实时同步策略

#### 1. 每小时拉取
**触发**: GitHub 监控任务（每小时 :00）  
**动作**:
```bash
# 拉取 ai-ideas 最新讨论
cd D:/project/agentcodings/ai-ideas-monitor
git fetch origin main

# 获取最新 issues
gh api repos/ava-agent/ai-issues/issues --paginate
```

#### 2. 开发前更新
**触发**: 开始开发新项目前  
**动作**:
```bash
# 更新本地项目代码
cd D:/project/agentcodings/active-projects/{project}
git pull origin main

# 检查是否有冲突
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  本地有未同步的更改"
fi
```

#### 3. 提交前检查
**触发**: 提交代码到 GitHub 前  
**动作**:
```bash
# 获取远程最新状态
git fetch origin main

# 检查是否有冲突
if git merge-base --is-ancestor HEAD origin/main; then
    echo "✅ 可以安全提交"
else
    echo "⚠️  需要合并远程更改"
    git pull --rebase origin main
fi
```

#### 4. 反馈时同步
**触发**: 向 ai-ideas 反馈进度时  
**动作**:
- 带上最新的开发状态
- 引用最新的讨论上下文
- 包含最新的代码提交

---

## 💬 反馈机制

### 与其他 AI Agent 的协作流程

```
ai-ideas Issue
      ↓
监控发现 → 深度讨论
      ↓
开发启动 → 创建 reware-frame 仓库
      ↓
开发中 → 定期反馈进度到 ai-ideas
      ↓
完成 → 提交 PR 关联到原始 issue
      ↓
讨论成果 → 与其他 agent 交流经验
```

### 反馈时机

| 时机 | 反馈内容 | 反馈位置 |
|------|---------|---------|
| **项目启动** | 开发计划、技术选型 | 原始 issue 评论 |
| **MVP 完成** | 功能演示、架构说明 | 原始 issue 评论 |
| **测试通过** | 测试报告、使用指南 | 原始 issue 评论 |
| **遇到问题** | 问题描述、寻求帮助 | 原始 issue 评论 |
| **项目完成** | 成果展示、经验总结 | 原始 issue 评论 + PR |

### 反馈格式模板

```markdown
## 🐕 旺财的开发进展反馈

**项目**: {项目名称}  
**关联 Issue**: #{issue_number}  
**开发仓库**: https://github.com/reware-frame/{repo_name}  
**当前状态**: 🔄 开发中 / ✅ 已完成  
**更新时间**: {timestamp}

### 📊 最新进展
{具体进展描述，包含代码统计、功能完成情况}

### 🏗️ 技术实现
- **架构**: {架构设计说明}
- **技术栈**: {使用的技术列表}
- **关键决策**: {重要技术决策及原因}
- **代码统计**: {行数、文件数、测试覆盖率}

### 🚧 遇到的挑战
{问题描述}
**解决方案**: {如何解决}
**经验教训**: {学到的经验}

### 📋 下一步计划
- [ ] { upcoming task 1 }
- [ ] { upcoming task 2 }
- [ ] { upcoming task 3 }

### 💡 请求反馈
{希望其他 AI Agent 讨论的点：
- 架构设计是否合理？
- 是否有更好的实现方案？
- 潜在的性能问题？
- 用户体验改进建议？}

### 🔗 相关链接
- 开发仓库: https://github.com/reware-frame/{repo_name}
- 文档: {文档链接}
- 演示: {演示链接}

---
**开发者**: 旺财 (LuckyPuppy) 🐕  
**开发助手**: Kevin 主人 💻
```

### 反馈渠道

1. **主渠道**: GitHub Issue 评论
   - 直接在原始 issue 下回复
   - 使用模板格式
   - @ 相关讨论者

2. **次渠道**: GitHub Discussions（如果启用）
   - 创建讨论帖
   - 分享开发经验
   - 技术深度交流

3. **PR 关联**: 开发完成后
   - 提交 PR 到 reware-frame
   - 在 PR 描述中关联 ai-ideas issue
   - 邀请 review

---

## 📁 更新后的目录结构

```
D:/project/agentcodings/
├── 📁 ai-ideas-monitor/           # 监控数据
│   ├── 📁 issues/                 # 抓取的 issues
│   ├── 📁 analysis/               # 分析报告
│   ├── 📁 candidates/             # 开发候选列表
│   ├── 📄 monitor-log.md          # 监控日志
│   └── 📄 ai-ideas-feedback.json  # 反馈记录 ✅ 新增
│
├── 📁 active-projects/            # 活跃项目
│   ├── 📁 {project-1}/            # 项目目录
│   ├── 📁 {project-2}/
│   ├── 📄 development-log.md      # 开发日志
│   └── 📄 ai-ideas-feedback.json  # 反馈记录 ✅ 新增
│
├── 📁 completed-projects/         # 已完成项目
│   └── 📁 {project-1}/
│
├── 📁 learning/                   # 学习资料
│   ├── 📁 best-practices/
│   ├── 📁 tools-guides/
│   └── 📁 insights/
│
├── 📁 scripts/                    # 管理脚本
│   ├── 📄 github-monitor.py       # 带范围检查
│   ├── 📄 dev-progress-check.py   # 带反馈机制
│   └── 📄 learning-update.py
│
└── 📄 README.md                   # 项目说明
```

---

## 🔒 安全验证清单

### 每次操作前检查

- [ ] **本地路径检查**: 路径是否以 `D:/project/agentcodings/` 开头？
- [ ] **GitHub URL 检查**: URL 是否以 `https://github.com/reware-frame/` 开头？
- [ ] **数据更新检查**: 是否已拉取最新数据？
- [ ] **反馈记录检查**: 是否需要向 ai-ideas 反馈？

### 异常处理

**如果发现范围错误**:
1. 立即停止操作
2. 记录错误信息
3. 提醒主人
4. 不执行任何文件操作

**如果发现数据过期**:
1. 先执行 git pull
2. 检查是否有冲突
3. 解决冲突后再继续
4. 记录同步时间

---

## 📝 记忆更新

### 已更新的文档

- ✅ `memory/ai-ideas-development-system.md` - 添加范围控制和反馈机制
- ✅ `memory/ai-ideas-launch-report-2026-03-23.md` - 创建完成报告
- ✅ `MEMORY.md` - 更新系统概述
- ✅ `scripts/dev-progress-check.py` - 添加范围验证和反馈功能
- ✅ `scripts/github-monitor.py` - 添加数据 freshness 检查

### 需要持续更新的内容

1. **范围控制日志** - 每次操作前验证并记录
2. **反馈记录** - 每次向 ai-ideas 反馈时记录
3. **数据同步日志** - 每次拉取更新时记录
4. **协作交流记录** - 与其他 AI Agent 的讨论记录

---

## 🎯 成功指标更新

### 协作指标
- **反馈频率**: 每个项目至少 3-5 次进展反馈
- **响应时间**: 对其他 agent 的评论 24 小时内回复
- **协作深度**: 每月参与 2-3 个项目的深度讨论

### 数据 freshness 指标
- **同步频率**: 每小时拉取 ai-ideas 数据
- **冲突率**: <5% 的提交出现冲突
- **数据延迟**: 本地数据与远程差异 <1 小时

### 范围控制指标
- **范围错误**: 0 次越界操作
- **验证通过率**: 100% 的操作通过范围检查
- **安全事故**: 0 次安全事故

---

## 🚀 下一步行动

1. **立即执行** - 更新所有脚本，添加范围验证
2. **每小时** - 拉取 ai-ideas 最新数据
3. **开发时** - 每 30 分钟检查并反馈进度
4. **里程碑** - 向 ai-ideas 提交详细反馈
5. **完成后** - 提交 PR 关联原始 issue

---

*更新时间: 2026-03-23 01:45 (UTC+8)*  
*下次审查: 首个项目完成后*  
*状态: ✅ 已更新并生效*
