# OpenClaw 健康检查报告 - 2025-04-06 19:07

## 执行摘要
- 检查时间: 2025-04-06 19:07:00
- 发现问题: 3 个
- 整体状态: ⚠️ 需关注

## 问题列表
- WARN: Port 18789 已被占用 (Gateway 正在运行)
- WARN: Tailscale 未运行 (非关键)
- INFO: 缺少 operator.read scope

## 修复操作
- 无需自动修复 - Gateway 正常运行中

## 详细分析

### ✅ 正常项目
- Config 配置正常
- Skills: 56 个可用，0 个缺失
- Agent 状态正常 (main: 140 sessions)

### ⚠️ 警告项目
1. **Port 18789 占用** - 这是预期的，Gateway 正在本地运行
2. **Tailscale 状态** - Windows 环境下未安装/运行，不影响本地使用
3. **operator.read scope** - 可选权限，不影响核心功能

### 📊 会话统计
- Main Agent: 140 个会话
- 最后活动: 2 分钟前

## 原始状态
<details>
<summary>点击查看完整状态</summary>

```
Account  | Status   | Notes
---------+----------+-----------------------------------
default  | OK       | token:config

Agents
+------------+----------------+----------+----------+------+
| Agent      | Bootstrap file | Sessions | Active   | Store |
+------------+----------------+----------+----------+------+
| main       | ABSENT         |      140 | 2m ago   | ...  |
+------------+----------------+----------+----------+------+

Diagnosis:
✓ Config: C:\Users\PC\.openclaw\openclaw.json
! Port 1879: Gateway already running locally
! Tailscale: off (Windows 环境正常)
✓ Skills: 56 eligible · 0 missing
```
</details>
