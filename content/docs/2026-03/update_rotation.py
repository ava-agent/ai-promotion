import re

with open('memory/github-projects-rotation.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 更新轮换状态
content = content.replace(
    '**当前项目**: Dog Agent（Tier 2 - 新轮6-1）📝',
    '**当前项目**: Dog Agent（Tier 2 - 新轮6）✅ 已完成'
)

# 更新推广进度
content = content.replace(
    '📝 Dog Agent 新轮6进行中（1次推广，还需1次）',
    '✅ Dog Agent 新轮6已完成（2次推广）'
)

# 添加新的发布记录
new_entry = """106. **Dog Agent** (7次/新轮6-2) - CSDN (2026-03-25 20:17)
  - 标题: 开发宠物AI助手时，我被这些坑整崩溃了
  - 内容类型: 踩坑实录/技术分享
  - 字数: ~2100字
  - GitHub: https://github.com/kevinten-ai/dog-agent

---

## 轮换历史"""

content = content.replace('## 轮换历史', new_entry)

with open('memory/github-projects-rotation.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('轮换配置已更新')
