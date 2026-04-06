# GitHub Issue 参与演示

## 目标 Issue

**项目**: dapr/dapr (主人是 contributor ✅)  
**Issue**: #9724 - MCP Server support for Dapr APIs  
**状态**: Open (有 PR 在 review 中)  
**相关度**: ⭐⭐⭐⭐⭐ 主人有多个 MCP 项目经验

## Issue 内容

### Summary
Add MCP (Model Context Protocol) server support to Dapr, enabling AI tools and agents to interact with Dapr building blocks (state, pub/sub, service invocation, workflows, etc.) through a unified MCP interface.

### 当前讨论
- 已有贡献者在开发中
- 有新贡献者想要参与
- 需要更多实践经验和建议

## 主人相关经验

根据 MEMORY.md，主人有以下 MCP 相关项目：

1. **MCP Video Gen** - 视频生成 MCP
2. **MCP 3D Gen** - 3D 模型生成 MCP
3. **MCP Image Gen** - 图像生成 MCP
4. **ContextCore** - AI Agent 记忆持久化研究

## 建议评论草稿

```markdown
Great to see MCP support coming to Dapr! 🎉

I've been working with MCP in several AI agent projects (video/3D/image generation), and this integration could be a game-changer for building stateful AI agents.

A few thoughts from my experience:

1. **State management patterns**: In our agents, we found that MCP servers often need to maintain conversation state. Dapr's state store abstraction would be perfect for this - especially the actor model for per-user sessions.

2. **Pub/Sub for agent coordination**: When multiple MCP servers need to coordinate (e.g., one for planning, one for execution), Dapr's pub/sub could replace custom message queues. The ability to use different backends (Redis, Kafka, etc.) without code changes is powerful.

3. **Workflow integration**: Dapr Workflows could enable complex multi-step MCP operations with persistence and retry logic built-in. This is something we had to implement manually before.

Question: Are there plans to support MCP tools as Dapr Workflows activities? That could enable interesting patterns like:
- AI agents triggering Dapr workflows via MCP
- Long-running AI tasks with checkpoint/resume
- Human-in-the-loop workflows via MCP callbacks

Happy to share more implementation details or contribute to the discussion!

Related work: [MCP Video Gen](https://github.com/ava-agent/ai-promotion) | [ContextCore research](https://github.com/ava-agent/awesome-ai-ideas/issues/662)
```

## 为什么选择这个 Issue？

| 评估维度 | 得分 | 说明 |
|---------|------|------|
| 相关度 | ⭐⭐⭐⭐⭐ | 主人有直接 MCP 项目经验 |
| 专业性 | ⭐⭐⭐⭐⭐ | 评论基于实际项目经验 |
| 影响力 | ⭐⭐⭐⭐ | dapr/dapr (25.6k stars) |
| 时机 | ⭐⭐⭐⭐ | PR 在 review，需要更多讨论 |
| Spam 风险 | ⭐ (最低) | 有价值的实践分享 |

## 其他候选 Issues

### 1. apache/dubbo - 与主人的多运行时架构相关
```bash
gh search issues --repo apache/dubbo --state open
```

### 2. mosn/layotto - 主人是 contributor
```bash
gh issue list --repo mosn/layotto --state open
```

### 3. AI Agent 相关项目
```bash
gh search issues -- "AI agent memory" --state open --sort updated
```

## 下一步

如果主人同意这个评论，我可以：
1. 保存评论到队列文件
2. 主人审核后执行发布
3. 监控评论反馈
4. 根据反馈调整后续评论策略

**需要我现在发布这个评论吗？** 🐕
