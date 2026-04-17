# OpenClaw 健康检查报告 - 2026-04-14 19:06

## 执行摘要
- 检查时间: 04/14/2026 19:06:32
- 发现问题: 2 个
- 系统状态: ⚠️  需要关注

## 问题列表
- ⚠️  Port 18789 已被占用 (Gateway 正在运行)
- ⚠️  会话数过多: 406 个
- ℹ️  信息: Tailscale 已关闭

## 修复操作
- ✅ Gateway 连接正常，无需修复
- ⚠️  会话数过多，建议定期清理
- ℹ️  插件配置正常

## 系统详细信息
**版本**: 2026.4.11  
**操作系统**: Windows 10.0.26200 (x64)
**Node 版本**: 22.17.0
**Gateway**: ws://127.0.0.1:18789 (可达，延迟 32ms)
**Telegram**: 已配置，状态 OK
**活动会话**: 406 个 (1 个活跃)
**端口占用**: PID 21820 正在使用 18789

## 建议
1. 定期清理超过 30 天的会话文件
2. 考虑启用 Tailscale 以支持远程连接
3. 监控会话数量增长趋势

## 原始状态
<details>
<summary>点击查看完整状态信息</summary>

`
[plugins] [pcmgr-ai-security 1.0.2] Plugin initialized (promptSecurity:true, promptAudit:true, skillAudit:true, scriptAudit:true).
OpenClaw status --all

Overview
+-----------------+----------------------------------------------------------------------------------------------------+
| Item            | Value                                                                                              |
+-----------------+----------------------------------------------------------------------------------------------------+
| Version         | 2026.4.11                                                                                          |
| OS              | windows 10.0.26200 (x64)                                                                           |
| Node            | 22.17.0                                                                                            |
| Config          | ~\.openclaw\openclaw.json                                                                          |
| Dashboard       | http://127.0.0.1:18789/                                                                            |
| Tailscale       | off                                                                                                |
| Channel         | stable (default)                                                                                   |
| Update          | pnpm 路 npm update 2026.4.12                                                                        |
| Gateway         | local 路 ws://127.0.0.1:18789 (local loopback) 路 reachable 37ms 路 auth token 路 KevinPC (172.25.32.  |
|                 | 1) app 2026.4.11 windows 10.0.26200                                                                |
| Security        | Run: openclaw security audit --deep                                                                |
| Gateway self    | unknown                                                                                            |
| Gateway service | Scheduled Task installed 路 registered 路 unknown                                                    |
| Node service    | Scheduled Task not installed                                                                       |
| Agents          | 1 total 路 0 bootstrapping 路 1 active 路 406 sessions                                                |
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
| main       | ABSENT         |      406 | 1m ago   | ~\.openclaw\agents\main\sessions\sessions.json                   |
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


`
</details>
