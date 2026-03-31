# 小红书每日内容自动化系统 V2.0

**创建日期**: 2026-03-26
**更新时间**: 2026-03-26 09:40
**状态**: ✅ 已上线运行

---

## 系统概述

每天自动生成**2次**小红书内容并发送到主人邮箱（596823919@qq.com）。

### 核心特点
1. **每天2次**: 早上 09:00 + 晚上 21:00
2. **配图AI提示词**: 提供 Midjourney / 即梦 / 可灵 三种格式的提示词
3. **一键复制**: 标题、正文、标签合并在一起，方便直接复制
4. **真实项目**: 只写 Kevin 的 GitHub 项目
5. **去模板化**: 禁用"姐妹们""救命""挖到宝"等套路词

---

## 定时任务

### 早上任务
- **任务ID**: `9ea18325-95b5-4a0b-bde1-078561576032`
- **时间**: 每天 09:00 (Asia/Shanghai)
- **主题**: 📕 小红书早 - YYYY-MM-DD（项目名）

### 晚上任务
- **任务ID**: `a9f2f834-3f64-4315-92f1-e336979115e6`
- **时间**: 每天 21:00 (Asia/Shanghai)
- **主题**: 📕 小红书晚 - YYYY-MM-DD（项目名）

---

## 自动化脚本

**位置**: `~/.openclaw/workspace/skills/imap-smtp-email/scripts/generate-and-send.js`

**使用方法**:
```bash
cd ~/.openclaw/workspace/skills/imap-smtp-email

# 发送早上版
node scripts/generate-and-send.js 596823919@qq.com morning

# 发送晚上版
node scripts/generate-and-send.js 596823919@qq.com evening
```

---

## 项目轮换计划

### 早上版 (09:00)
| 星期 | 项目 | 类型 | 故事主题 |
|------|------|------|----------|
| 周一 | Capa-Java | 开源中间件 | 开源社区经历 |
| 周二 | ccuse | CLI 工具 | 开发效率工具 |
| 周三 | Trip Agent | AI 旅行规划 | 地图 API 踩坑 |
| 周四 | Capa-BFF | 黑客松金奖 | 比赛经历 |
| 周五 | MCP Video Gen | MCP 服务器 | MCP 协议踩坑 |
| 周六 | Dog Agent | 宠物社交 | 产品设计 |
| 周日 | OpenOctopus | AI Agent 系统 | 架构思考 |

### 晚上版 (21:00)
| 星期 | 项目 | 类型 | 故事主题 |
|------|------|------|----------|
| 周一 | Compiling the Dao | 开源修仙小说 | AI 辅助创作 |
| 周二 | English Agent | 英语学习 | 教育产品设计 |
| 周三 | Trip Agent | AI 旅行规划 | 产品使用体验 |
| 周四 | Capa-Java | 开源中间件 | 技术架构深度 |
| 周五 | ccuse | CLI 工具 | 效率技巧 |
| 周六 | MCP Video Gen | MCP 服务器 | AI 视频生成 |
| 周日 | OpenOctopus | AI Agent 系统 | 架构思考 |

---

## 邮件内容格式

### 一键复制区
```
📝 一键复制区（标题 + 正文 + 标签）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[标题]
[正文内容]
[标签]
```

### 配图 AI 提示词
提供 **3 种格式**的提示词：

1. **Midjourney** - 适合 Discord 使用
2. **即梦** - 字节跳动的中文 AI 绘图
3. **可灵** - 快手的 AI 绘图工具

### 配图类型
- **封面图**: 程序员踩坑场景
- **配图1**: 代码截图风格
- **配图2**: 架构图/流程图
- **配图3**: 产品界面
- **配图4**: 表情包/幽默风格

---

## 配图 AI 提示词示例

### 封面图 - 程序员踩坑场景

**Midjourney**:
```
A programmer debugging code late at night, multiple monitors showing code and error messages, coffee cups scattered around, warm desk lamp lighting, cozy but chaotic workspace, flat illustration style, soft pastel colors with hints of orange and blue, 3:4 vertical aspect ratio, suitable for Xiaohongshu cover, clean and modern aesthetic --ar 3:4 --style raw
```

**即梦**:
```
扁平插画风，程序员深夜调试代码场景，多显示器显示代码和报错信息，咖啡杯散落周围，温暖的台灯照明，舒适但有点乱的桌面，柔和 pastel 配色配橙色和蓝色点缀，3:4竖图比例，适合小红书封面，干净现代美学
```

**可灵**:
```
一个程序员深夜调试代码，多显示器显示代码和错误信息，桌上散落着咖啡杯，温暖的台灯，舒适但略显凌乱的工作空间，扁平插画风格，柔和 pastel 配色带橙色和蓝色点缀，3:4竖图，适合小红书封面
```

---

## 发送记录

### 2026-03-26

**早上版 (09:00)**
- **时间**: 09:38
- **项目**: Capa-BFF
- **主题**: 📕 小红书早 - 2026-03-26（Capa-BFF）
- **状态**: ✅ 发送成功
- **内容**: 黑客松 48 小时拿金奖

**晚上版 (21:00)**
- **时间**: 09:40（测试发送）
- **项目**: Capa-Java
- **主题**: 📕 小红书晚 - 2026-03-26（Capa-Java）
- **状态**: ✅ 发送成功
- **内容**: 多云 SDK 架构设计

---

## 项目清单

### Tier 1 重点项目
1. **Trip Agent** - AI 旅行规划
2. **Capa-Java** - 开源中间件
3. **Capa-BFF** - 黑客松金奖
4. **OpenOctopus** - AI Agent 系统

### Tier 2 工具/应用
5. **ccuse** - CLI 工具
6. **MCP Video Gen** - MCP 服务器
7. **Dog Agent** - 宠物社交
8. **English Agent** - 英语学习

### 创意项目
9. **Compiling the Dao** - 开源修仙小说

---

## 使用流程

### 每天收到邮件后
1. **打开邮件** - 查看主题确认是哪个项目
2. **复制内容** - 一键复制区的标题+正文+标签
3. **生成配图** - 使用提示词在 Midjourney/即梦/可灵 生成
4. **发布到小红书** - 复制内容 + 上传图片

### 配图生成建议
- **封面图**: 必须生成，决定点击率
- **配图1-2**: 选 2 张相关风格的
- **配图3-4**: 可选，增加内容丰富度

---

## 禁用词汇清单

**绝对禁止**:
- "姐妹们！"、"救命！"、"挖到宝了！"
- "绝绝子！"、"yyds！"、"快冲！"
- "保姆级教程"、"有手就会"
- "神仙工具"、"宝藏app"、"效率翻倍"
- "不看后悔"、"太香了"

---

## 后续优化计划

- [x] 每天发送2次（早晚各一次）
- [x] 添加配图AI提示词
- [x] 标签和内容合并方便复制
- [ ] 根据效果数据优化标题
- [ ] 增加更多项目故事
- [ ] 支持手动指定项目生成内容

---

*最后更新: 2026-03-26*
