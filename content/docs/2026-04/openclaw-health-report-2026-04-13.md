# OpenClaw 健康检查报告 - 2026-04-13 19:04

## 执行摘要
- 检查时间: 04/13/2026 19:04:30
- 发现问题: 5 个
- 状态: 需要关注

## 问题列表
- PORT: 端口 18789 已被占用（但 Gateway 正在运行）
- TAILSCALE: Tailscale 未启用
- PLUGIN: 插件兼容性警告 (pcmgr-ai-security)
- SESSIONS: 会话数过多 (434)
- SCHEDULE: 计划任务未安装


## 修复操作
- ✅ Gateway 连接正常
- ⚠️ 会话数过多，已尝试清理旧会话
- ❌ 需要手动检查配置

## 建议后续操作
1. 检查并配置 Tailscale
2. 更新 pcmgr-ai-security 插件以支持显式能力注册
3. 考虑配置计划任务
4. 监控会话增长情况

## 原始状态
<details>
<summary>点击查看</summary>

```
| Node service    | Scheduled Task not installed                                                                       |
| Agents          | 1 total 路 0 bootstrapping 路 1 active 路 434 sessions                                                |
| Secrets         | none                                                                                               |
+-----------------+----------------------------------------------------------------------------------------------------+

Channels
+----------+---------+--------+----------------------------------------------------------------------------------------+
| Channel  | Enabled | State  | Detail                                                                                 |
+----------+---------+--------+----------------------------------------------------------------------------------------+
| Telegram | ON      | OK     | token config (sha256:baa68e23 路 len 46) 路 accounts 1/1                                 |
+----------+---------+--------+----------------------------------------------------------------------------------------+

Telegram accounts
+----------+----------+------------------------------------------------------------------------------------------------+
| Account  | Status   | Notes                                                                                          |
+----------+----------+------------------------------------------------------------------------------------------------+
| default  | OK       | token:config                                                                                   |
+----------+----------+------------------------------------------------------------------------------------------------+

Agents
+------------+----------------+----------+----------+------------------------------------------------------------------+
| Agent      | Bootstrap file | Sessions | Active   | Store                                                            |
+------------+----------------+----------+----------+------------------------------------------------------------------+
| main       | ABSENT         |      434 | 1m ago   | ~\.openclaw\agents\main\sessions\sessions.json                   |
+------------+----------------+----------+----------+------------------------------------------------------------------+

Diagnosis (read-only)

Gateway connection details:
  Gateway target: ws://127.0.0.1:18789
  Source: local loopback
  Config: C:\Users\PC\.openclaw\openclaw.json
  Bind: loopback

鉁?Config: C:\Users\PC\.openclaw\openclaw.json
鉁?Secret diagnostics (0)
鉁?Restart sentinel: none
! Port 18789
  Port 18789 is already in use.
  - pid 21820: "C:\Program Files\nodejs\node.exe" --disable-warning=ExperimentalWarning C:\Users\PC\AppData\Roaming\npm\node_modules\openclaw\dist\entry.js gateway --port 18789 (127.0.0.1:18789)
  - Gateway already running locally. Stop it (openclaw gateway stop) or use a different port.
! Tailscale: off 路 unknown
鉁?Skills: 63 eligible 路 0 missing 路 C:\Users\PC\.openclaw\workspace
! Plugin compatibility (1)
  - [info] pcmgr-ai-security is hook-only. This remains a supported compatibility path, but it has not migrated to explicit capability registration yet.
鉁?Channel issues (none)

Pasteable debug report. Auth tokens redacted.
Troubleshooting: https://docs.openclaw.ai/troubleshooting

```
</details>
