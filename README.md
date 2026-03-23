# AI Promotion Content Assets

## 📚 项目介绍

本项目用于保存和管理 AI 推广内容的资产，包括：
- 各平台发布的文章原文
- 内容模板和最佳实践
- 数据分析和洞察报告
- 发布历史记录

## 📁 目录结构

- `content/` - 按平台和时间组织的发布内容
- `templates/` - 内容模板（技术分享、互动讨论等）
- `archive/` - 草稿、被拒绝、spam 标记的内容
- `analytics/` - 数据分析和洞察报告
- `scripts/` - 管理脚本
- `docs/` - 文档和规范

## 🔄 自动同步

每日自动任务：
- 08:00 - 整理昨日新内容
- 20:00 - 生成当日摘要
- 22:00 - 提交到 GitHub

## 📊 内容统计

- Moltbook: 深度讨论社区
- 知乎: 中文技术社区
- Dev.to: 国际开发者社区
- ... (持续扩展中)

## 🎯 使用指南

### 查看内容
```bash
cd content/moltbook/2026-03
ls -la
```

### 提交更改
```bash
git add .
git commit -m "feat: add daily content"
git push origin main
```

## 📝 维护者

- **Owner**: Kevin (kevinten10)
- **Assistant**: 旺财 (LuckyPuppy) 🐕
- **Last Update**: 2026-03-23

---

*本项目由 AI 助手旺财自动维护*
