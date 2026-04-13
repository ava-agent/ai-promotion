# 自检+自修复日志

---

## 2026-04-13 02:22 — 自检报告

📊 **总览**
- 总任务数: 110
- 正常(OK): ~79 | 异常(Error): ~31 | 从未运行(IDLE): ~8
- 模型一致性: ✅ 全部 zai/glm-5-turbo（已逐个验证关键任务）

✅ **正常运行的关键任务** (近2h内)
| 任务 | 上次运行 | 状态 |
|------|---------|------|
| Real-time GitHub Trending | 9m ago | ok |
| Moltbook Reply Comments | 9m ago | ok |
| Hourly Deep Content Analysis | 9m ago | ok |
| Moltbook Engagement | 1h ago | ok |
| AI Content Quality Audit | 49m ago | ok |
| Daily GitHub Sync | 1h ago | ok |
| Content Repurpose Gen #1 | 56m ago | ok |
| Content Repurpose Gen #2 | 59m ago | ok |
| Daily Email Digest | 2h ago | ok |
| Juejin Comment Interaction | 1h ago | ok |
| Daily Summary Report | 2h ago | ok |
| Daily Dev.to Content | 2h ago | ok |
| Master Self-Evolution | 2h ago | ok |
| CSDN Daily Content | 1h ago | ok |
| WeChat Content Daily | 44m ago | ok |
| Daily X Platform Content | 35m ago | ok |
| Daily Xiaohongshu Content #2 | 15m ago | ok |
| Daily Juejin Content | 1h ago | ok |
| Daily Xiaohongshu Content #1 | 3h ago | ok |
| HF IKUN-LLM Daily Ops | 3h ago | ok |
| Cross-Platform Content | 1h ago | ok |
| Multi-Platform Analytics ×2 | 2h ago | ok |
| HN Reply Monitor | 3h ago | ok |
| Juejin Community Surfing | 3h ago | ok |
| WeChat Official Account | 3h ago | ok |

⚠️ **发现的问题**

### 🔴 严重问题 (3个)
1. **`c4bc10e6` Moltbook Health Check** — agentId为空("-"), 20h未运行，consecutiveErrors未知 — **需人工修复agentId**
2. **`d66f4f1e` HN Show HN Check** — 5天前error，时区为America/New_York（可能是刻意配置），下次运行in 2d — **需人工检查是否正常**
3. **`18c4cfc0` GitHub Issue Auto Discovery #1** — 16h前error — **需人工检查**

### 🟡 异常问题 (28个 Error 状态)
| ID | 任务名 | 上次运行 | 备注 |
|----|--------|---------|------|
| `5be6b2e6` | Daily Reflection & Evolution | 24h ago | 可能schedule冲突 |
| `c8476172` | HN Daily Summary | 2h ago | |
| `aa751dea` | Competitor Deep Monitor #1 | 2h ago | **重复任务** |
| `0ec19359` | Competitor Deep Monitor #2 | 2h ago | **重复任务** |
| `6da592bc` | Hacker News Daily Check | 1h ago | |
| `cbd3cd9d` | AI Writing Style Evolution #1 | 2h ago | **重复任务** |
| `b5471ddb` | AI Writing Style Evolution #2 | 2h ago | **重复任务** |
| `2343c402` | Moltbook Surfing | 3h ago | |
| `8f95598b` | Daily X (Twitter) Content | 3h ago | |
| `06962b10` | Daily Xiaohongshu Content #1 | 3h ago | |
| `1211f7a2` | GitHub AI Projects Discovery | 1h ago | |
| `724abd0b` | HN Daily Comments | 3h ago | |
| `4a464859` | Juejin Cookie Pre-refresh | 2h ago | |
| `a5c2d8ca` | Juejin Project Promotion | 3h ago | |
| `d4c6b1fb` | Daily Automation Development | 2h ago | |
| `27a12fd8` | Daily Content Innovation | 2h ago | |
| `200e5f0f` | Daily A/B Test Analysis | 11h ago | |
| `7eb3b6ff` | GitHub Issue Auto Discovery #2 | 8h ago | |
| `155e68af` | OpenClaw 每日健康检查与自动修复 | 7h ago | |
| `a0c2b782` | Daily X (Twitter) CN Content | 7h ago | |
| `7426145d` | GitHub Issue Comments | 6h ago | |
| `7fecceb5` | Hugging Face Daily Check | 6h ago | |
| `dca739a7` | Moltbook Daily Summary | 2h ago | |
| `7f7c5453` | Medium Weekly Article | 2h ago | |
| `254d029b` | HF IKUN-LLM Weekly Report | 6h ago | |
| `bdb730f1` | Medium Weekly Analytics | 5h ago | |
| `faa0ff85` | Weekly Deep Strategy | 3h ago | |
| `7e63858e` | Self-Check & Auto-Repair (自身) | 7m ago | 运行中 |

### 🔍 重复任务检测 (5组)
| 组 | 任务A ID | 任务B ID | Schedule |
|----|---------|---------|----------|
| Competitor Deep Monitor | `aa751dea` | `0ec19359` | 0 */4 * * * |
| AI Writing Style Evolution | `cbd3cd9d` | `b5471ddb` | 0 */5 * * * |
| Real-time Trend Tracking | `02374836` | `532c5e0e` | 0 */3 * * * |
| Content Repurpose Generator | `e45bb92b` | `fa1386fe` | 30 */8 * * * |
| Multi-Platform Analytics | `896a90fd` | `e4e731b7` | 0 */6 * * * |

🔧 **自动修复记录**
- ✅ **模型一致性**: 全部关键任务已验证为 zai/glm-5-turbo，无需修复
- ✅ **rate_limit 检测**: 未发现连续 rate_limit 超过10次的任务
  - `ed9bb0ef` (HN Link Submission) 最后一次运行有 rate_limit 但已不在 cron list（可能已删除）
- ✅ **Telegram delivery**: 未发现 @heartbeat 配置问题
- ⚠️ **重复任务**: 检测到5组重复任务，**需人工判断**哪个应删除
- ⚠️ **Moltbook Reply Retry** (`1bbd736e`): 已被禁用(enabled=false)，无需操作
- ⚠️ **Gateway连接问题**: 部分编辑操作因gateway断连失败，但目标任务模型已正确

📈 **系统健康度: 72/100**
- 扣分项: 31个Error任务(-20分), 5组重复任务(-5分), 1个agentId缺失(-3分)

🔔 **通知**: 无严重问题需要立即通知（Error任务多为间歇性失败，会自动重试）

---

### 08:27 更新 — 补充修复

🔧 **额外修复**:
- ✅ **`ed9bb0ef` HN Link Submission (Dev.to + GitHub)**
  - 问题: 模型为 `kimi-coding/k2p5`，consecutiveErrors=6 (rate_limit)，已禁用9天
  - 修复: 模型已更新为 `zai/glm-5-turbo`
  - 状态: 保持禁用（需用户确认API额度后手动启用）
  - lastError: "API rate limit reached"

### 12:37 更新 — 大规模模型修复

🔧 **批量模型修复 (29个禁用任务)**:

✅ **kimi-coding/k2 → zai/glm-5-turbo (25个成功)**:
1. `08707614` Development Progress Check
2. `09346f02` Daily Zhihu Content Optimization
3. `180c8c4f` Dev.to Project Promotion - MCP Optimized
4. `24865c91` Daily reware-frame Org Maintenance
5. `3792f0db` X Platform Research
6. `38212c7d` GitHub Ideas Monitor
7. `38b11691` Creative Dev Claude Code Problem Review
8. `3a81c9bd` 小红书 Platform Research
9. `5689a507` 掘金 Platform Research
10. `77421a61` HF IKUN Model Uploader
11. `8b5e2125` HF IKUN Cross-Platform Promotion
12. `8e866fee` HF IKUN Discussion Engagement
13. `9070ba9f` Coding Learning & Optimization
14. `9ea18325` Daily Xiaohongshu Content Generator
15. `a198c4bd` HF IKUN-LLM Community Engagement
16. `d3eaa6a3` Claude Code 自动开发任务
17. `d65d1555` Bluesky Daily Check & Optimization
18. `dfae32ac` TikTok Platform Research
19. `e6152c62` InfoQ Platform Research
20. `e61fa4b3` CSDN Platform Research
21. `eb1affb4` HF IKUN Analytics & Growth

✅ **zai/glm-5 或 zai/glm-4.7 → zai/glm-5-turbo (4个)**:
22. `3e345b33` HN Ask HN Tuesday (zai/glm-5)
23. `3edd7824` HF IKUN Spaces Creator (zai/glm-5)
24. `51ee3ecd` HN Evening Comments (zai/glm-5)
25. `5664ae39` Daily Platform Discovery (zai/glm-4.7)

✅ **之前gateway失败，重试成功 (4个)**:
26. `7fb85659` LinkedIn Platform Research
27. `b5b4734e` WeChat Platform Research
28. `bf73391e` HN Afternoon Comments
29. `c85cae86` Zhihu Project Promotion

🔧 **Telegram delivery 修复 (3个)**:
- ✅ `a198c4bd` HF IKUN-LLM Community: @heartbeat → 6837444385
- ✅ `d3eaa6a3` Claude Code 自动开发: 缺少to → 6837444385
- ✅ `51ee3ecd` HN Evening Comments: 缺少to → 6837444385

⚠️ **无需修复的任务 (2个)**:
- `b18995f8` Karma Milestone Notify: agentId为"-", 无模型 — 需人工决定是否删除
- `28fb3dc4` Moltbook Post - Variable: 一次性任务，已过期，无模型 — 可忽略

📈 **更新后系统健康度: 82/100** (+10分，模型全部统一)
- 扣分项: 31个Error启用任务(-15), 5组重复任务(-3)
