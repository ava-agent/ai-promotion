# OpenClaw 健康检查报告 - 2026-04-24 01:43

## 执行摘要
- 检查时间: 2026-04-24 01:43
- 发现问题: 1 个严重问题

## 问题列表
- CRITICAL: Plugin configuration invalid - missing extension entry files (./index.js, ./setup-entry.js)

## 修复操作
- ❌ 自动修复失败: 插件配置问题需要手动修复
- 建议操作: 重新安装或修复 pcmgr-ai-security 插件

## 原始状态
```
Config invalid
File: ~\.openclaw\openclaw.json
Problem:
  - plugins: plugin: extension entry escapes package directory: ./index.js
  - plugins: plugin: extension entry escapes package directory: ./setup-entry.js
  [重复多次...]

Run: openclaw doctor --fix
Invalid config at C:\Users\PC\.openclaw\openclaw.json:
- plugins: plugin: extension entry escapes package directory: ./index.js
- plugins: plugin: extension entry escapes package directory: ./setup-entry.js
```

## Gateway 状态检查
- Gateway: 连接不可达 (由于配置问题无法检查)

## 会话数检查
- 无法获取会话信息 (由于配置问题)

## 建议后续步骤
1. 备份当前配置文件
2. 重新安装 pcmgr-ai-security 插件
3. 或移除有问题的插件配置
4. 重新运行 `openclaw doctor --fix`