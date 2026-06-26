# OpenClaw 健康检查报告 - 2026-06-25 19:03

## 执行摘要
- 检查时间: 2026年6月25日 19:03
- 发现问题: 0 个

## 问题列表
- 无问题

## 修复操作
- 无需修复

## 原始状态
<details>
<summary>点击查看</summary>

```
OpenClaw status --all

Overview
+--------------------+-------------------------------------------------------------------------------------------------+
| Item               | Value                                                                                           |
+--------------------+-------------------------------------------------------------------------------------------------+
| Version            | 2026.6.10                                                                                       |
| OS                 | windows 10.0.26200 (x64)                                                                        |
| Node               | 22.23.1                                                                                         |
| Config             | ~\.openclaw\openclaw.json                                                                       |
| Dashboard          | http://127.0.0.1:19001/                                                                         |
| Tailscale exposure | off                                                                                             |
| Channel            | stable (default)                                                                                |
| Update             | npm · up to date · npm latest 2026.6.10 · deps ok                                               |
| Gateway            | local · ws://127.0.0.1:19001 (local loopback) · reachable 246ms · auth token · KevinPC (192.    |
|                    | 168.71.22) app 2026.6.10 windows 10.0.26200                                                     |
| Security           | Run: openclaw security audit --deep                                                             |
| Gateway self       | unknown                                                                                         |
| Gateway service    | Scheduled Task installed · registered · running (pid 67356, Verified gateway listener detected  |
|                    | on port 19001 even though schtasks did not report a running task.)                              |
| Node service       | Scheduled Task not installed                                                                    |
| Agents             | 1 total · 0 bootstrapping · 1 active · 55 sessions                                              |
| Secrets            | none                                                                                            |
+--------------------+-------------------------------------------------------------------------------------------------+

Channels
+----------+---------+--------+----------------------------------------------------------------------------------------+
| Channel  | Enabled | State  | Detail                                                                                 |
+----------+---------+--------+----------------------------------------------------------------------------------------+
| Telegram | ON      | OK     | token config (sha256:baa68e23 · len 46) · accounts 1/1                                 |
+----------+---------+--------+----------------------------------------------------------------------------------------+

Telegram accounts
+----------+----------+------------------------------------------------------------------------------------------------+
| Account  | Status   | Notes                                                                                          |
+----------+----------+------------------------------------------------------------------------------------------------+
| default  | OK       | token:config · credential available in gateway runtime                                         |
+----------+----------+------------------------------------------------------------------------------------------------+

Agents
+------------+----------------+----------+----------+------------------------------------------------------------------+
| Agent      | Bootstrap file | Sessions | Active   | Store                                                            |
+------------+----------------+----------+----------+------------------------------------------------------------------+
| main       | ABSENT         |       55 | just now | ~\.openclaw\agents\main\sessions\sessions.json                   |
+------------+----------------+----------+----------+------------------------------------------------------------------+

Diagnosis (read-only)

Gateway connection details:
  Gateway target: ws://127.0.0.1:19001
  Source: local loopback
  Config: C:\Users\PC\.openclaw\openclaw.json
  Bind: loopback

✓ Config: C:\Users\PC\.openclaw\openclaw.json
✓ Secret diagnostics (0)
✓ Restart sentinel: none
✓ Port 19001
  Detected OpenClaw Gateway listener on the configured port.
! Tailscale exposure: off · daemon unknown
✓ Skills: 72 eligible · 0 missing · C:\Users\PC\.openclaw\workspace
✓ Plugin compatibility (none)
✓ Agent activity: 1 active in 30m · 55 sessions
✓ Inbound delivery telemetry: received 0 · dispatch 0/0 · turns 3 · processed 29
  latest delivery event: 1m ago

Gateway restart attempts (tail): C:\Users\PC\.openclaw\logs\gateway-restart.log
  [锟斤拷锟斤拷 2026/06/25  9:46:06.43] openclaw restart log initialized
  [锟斤拷锟斤拷 2026/06/25  9:46:06.43] openclaw restart attempt source=windows-task-handoff target="OpenClaw Gateway"
✓ Channel issues (none)

Pasteable debug report. Auth tokens redacted.
Troubleshooting: https://docs.openclaw.ai/troubleshooting
```
</details>
