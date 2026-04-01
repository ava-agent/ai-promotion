# 小红书封面图提示词库

**创建日期**: 2026-03-26  
**更新日期**: 2026-03-26  
**版本**: v1.0 - 真实截图优先

---

## 🎯 核心原则

**优先使用真实截图**，而非 AI 生成图

小红书技术区的用户更信任：
- ✅ 真实的代码截图
- ✅ 开发环境随手拍
- ✅ GitHub 仓库截图
- ✅ 真实的报错界面
- ✅ 项目运行效果录屏

**AI 生成图仅用于**：
- 无法截图的概念图
- 需要视觉吸引力的首图
- 补充说明的配图

---

## 📸 真实截图指南

### 推荐截图类型

#### 1. 代码截图 ⭐⭐⭐⭐⭐
**适用场景**: 技术分享、踩坑实录

**截图技巧**:
- 使用 VS Code / Cursor 等现代编辑器
- 开启行号显示
- 突出关键代码（高亮或标记）
- 3:4 竖屏比例最佳
- 字体大小适中（能看清但不占满屏幕）

**构图建议**:
```
┌─────────────────┐
│   [代码区域]     │
│   高亮关键行     │
│                 │
│   [终端/输出]    │
└─────────────────┘
```

#### 2. 项目界面截图 ⭐⭐⭐⭐⭐
**适用场景**: 工具推荐、项目展示

**截图技巧**:
- 展示核心功能界面
- 使用真实数据（非测试数据）
- 保持界面整洁（关闭无关标签页）
- 3:4 比例，突出主要功能区域

#### 3. 报错截图 ⭐⭐⭐⭐
**适用场景**: 踩坑实录

**截图技巧**:
- 截全错误信息
- 保留上下文（什么操作导致的）
- 可以标注重点错误行
- 真实报错比完美的界面更有说服力

#### 4. GitHub 截图 ⭐⭐⭐⭐
**适用场景**: 开源项目、项目介绍

**截图内容**:
- README 页面
- Star/Fork 数据
- Issue/PR 列表
- 代码结构

#### 5. 开发环境随手拍 ⭐⭐⭐⭐
**适用场景**: 程序员日常、开发故事

**拍摄内容**:
- 多显示器工作环境
- 代码 + 咖啡 ☕
- 笔记本 + 手绘草图
- 深夜加班场景

---

## 🎨 AI 生成图提示词（备用）

当真实截图无法满足需求时，使用以下提示词生成封面图。

### 风格 1：扁平插画风

#### 技术/编程主题
```
Flat design illustration, programming concept, 
code editor interface with colorful syntax highlighting, 
clean minimal background in soft blue gradient, 
simple geometric shapes, modern tech aesthetic, 
3:4 aspect ratio, no text, professional and friendly vibe
```

#### AI/工具主题
```
Flat design illustration, AI assistant concept, 
robot or abstract AI figure interacting with human, 
clean minimal background in purple gradient, 
simple geometric elements, modern tech aesthetic, 
3:4 aspect ratio, no text, futuristic but approachable
```

#### 旅行/地图主题（Trip Agent）
```
Flat design illustration, travel planning concept, 
map with route markers, location pins, 
clean minimal background in teal gradient, 
simple geometric shapes, modern tech aesthetic, 
3:4 aspect ratio, no text, adventurous but organized vibe
```

---

### 风格 2：手账风

#### 开发日记主题
```
Digital journal style, handwritten notes aesthetic, 
code snippets mixed with hand-drawn doodles, 
washi tape elements, sticky notes, 
soft pastel colors, paper texture background, 
3:4 aspect ratio, cozy programmer lifestyle vibe
```

#### 项目记录主题
```
Bullet journal style, project planning layout, 
checklists, progress bars, hand-drawn icons, 
grid paper background, muted colors with accent highlights, 
3:4 aspect ratio, organized and creative vibe
```

---

### 风格 3：科技风

#### 深色模式主题
```
Dark mode tech aesthetic, neon accents in cyan or purple, 
terminal window, code visualization, 
dark background #0d1117, glowing elements, 
modern developer vibe, 3:4 aspect ratio, sleek and professional
```

#### 数据可视化主题
```
Tech visualization, data flow diagram, 
abstract network connections, node graphs, 
dark blue background with bright accent lines, 
minimal text elements, futuristic tech aesthetic, 
3:4 aspect ratio, complex but organized
```

---

### 风格 4：极简主义

#### 纯色背景 + 图标
```
Minimalist design, single large icon in center, 
solid color background (soft gradient), 
clean lines, generous whitespace, 
no text, modern and elegant, 
3:4 aspect ratio, iconic and memorable
```

#### 单色系主题
```
Monochromatic design, varying shades of single color, 
abstract geometric shapes, layered composition, 
minimalist aesthetic, no text, 
3:4 aspect ratio, sophisticated and clean
```

---

## 🖼️ 封面图尺寸规范

### 小红书推荐尺寸
- **比例**: 3:4（竖图）
- **推荐尺寸**: 1242×1660 px
- **最小尺寸**: 600×800 px
- **文件格式**: JPG 或 PNG
- **文件大小**: 建议 < 5MB

### 安全区域
重要内容放在中间区域，避免被 UI 遮挡：
```
┌─────────────────┐
│    [安全边距]    │
│   ┌─────────┐   │
│   │ 主要内容 │   │
│   │  放这里  │   │
│   └─────────┘   │
│    [安全边距]    │
└─────────────────┘
```

---

## 🎭 项目专属封面建议

### Trip Agent（旅行规划）
**推荐截图**:
- 路线规划界面
- 地图 + 路线可视化
- 多 Agent 协作流程图

**推荐 AI 提示词**:
```
Flat design, travel route planning concept, 
map with connected waypoints, minimalist style, 
soft teal and orange color scheme, 
clean background, 3:4 aspect ratio
```

### Capa-Java（开源中间件）
**推荐截图**:
- GitHub 仓库首页
- 架构图
- 代码结构截图

**推荐 AI 提示词**:
```
Tech illustration, middleware architecture concept, 
interconnected system modules, flow diagram style, 
blue and white color scheme, professional and technical, 
3:4 aspect ratio, clean and organized
```

### MCP 项目
**推荐截图**:
- MCP 协议文档截图
- 服务器代码架构
- 工具调用流程图

**推荐 AI 提示词**:
```
Abstract tech illustration, protocol communication concept, 
data flow between client and server, geometric shapes, 
purple and cyan gradient accents, modern tech aesthetic, 
3:4 aspect ratio, futuristic and structured
```

### OpenOctopus（AI Agent）
**推荐截图**:
- Agent 协作流程图
- 多 Agent 对话界面
- 系统架构图

**推荐 AI 提示词**:
```
Futuristic illustration, multi-agent system concept, 
interconnected AI nodes, neural network visualization, 
dark background with glowing connections, 
complex but organized, 3:4 aspect ratio
```

---

## 🧪 A/B测试建议

### 测试变量 1：真实截图 vs AI 生成图
- **A 组**: 真实项目截图
- **B 组**: AI 生成概念图
- **目标**: 点击率

### 测试变量 2：不同截图类型
- **A 组**: 代码截图
- **B 组**: 项目界面截图
- **C 组**: 报错截图
- **目标**: 点击率

### 测试变量 3：封面风格
- **A 组**: 扁平插画
- **B 组**: 手账风
- **C 组**: 科技风
- **目标**: 点击率

---

## 📋 封面图检查清单

发布前检查：
- [ ] 3:4 竖图比例
- [ ] 内容清晰可见
- [ ] 与标题内容相关
- [ ] 真实截图优先
- [ ] 无版权问题（截图用自己项目）
- [ ] 文件大小 < 5MB
- [ ] 重要内容在安全区域内

---

## 🎯 本周推荐封面策略

### 主推策略：真实截图
对于技术区内容，真实截图比精美 AI 图更有说服力：

1. **踩坑实录** → 报错截图 + 代码截图
2. **项目介绍** → 项目界面截图 + GitHub 截图
3. **技术分享** → 代码截图 + 架构图

### 配图策略
- **封面图**: 最能代表内容的真实截图
- **配图 2-3 张**: 补充说明的过程截图
- **最后一张**: 项目链接或总结图

---

## 📈 2026-04-02 更新记录

### ✅ 主要更新
1. **新增双版本封面策略** - 同一项目制作两种风格封面
2. **项目优先级重新评估** - Capa-BFF和Capa-Java成为重点
3. **MCP项目封面建议** - 新兴技术特殊策略
4. **双版本A/B测试规划** - 点击率对比测试方案

### 🎯 双版本封面策略 🆕

**适用项目**: 推广期、重要项目、高潜力内容
**执行方式**: 早8点发布双版本，不同风格对比
**预期效果**: 触达更广的用户群体

#### 双版本示例

**项目**: Capa-BFF
- **版本A**（技术专业）: 代码截图 + 架构图
- **版本B**（功能展示）: 项目界面截图 + 效果对比图

**项目**: MCP Video Gen  
- **版本A**（技术导向）: 服务器代码截图
- **版本B**（用户导向）: 生成效果展示图

**项目**: Dog Agent
- **版本A**（产品截图）: 宠物社交界面
- **版本B**（技术截图）: 后台管理系统

### 📊 本周封面策略规划

#### 4月2日 - Capa-Java（技术分享）
**主推截图**:
- 代码截图：多运行时架构设计
- 辅助截图：GitHub仓库首页
- **双版本准备**:
  - 版本A：核心代码截图（技术导向）
  - 版本B：项目功能演示（用户导向）

#### 4月3日 - ccuse + English Agent（双版本策略）
**主推截图**:
- ccuse：Claude Code切换界面
- English Agent：学习效果展示
- **双版本执行**:
  - 版本A：功能截图（实用性导向）
  - 版本B：技术截图（深度用户导向）

#### 4月4日 - Trip Agent + Capa-BFF（重点推广）
**主推截图**:
- Trip Agent：路线规划界面截图
- Capa-BFF：BFF框架架构截图
- **双版本执行**:
  - 版本A：代码截图（技术专业）
  - 版本B：界面截图（功能展示）

#### 4月5日 - MCP Video Gen + ccuse
**主推截图**:
- MCP Video Gen：生成流程截图
- ccuse：使用流程截图
- **封面策略**:
  - 重点展示工具的实际使用效果

#### 4月6日 - Dog Agent + MCP Video Gen
**主推截图**:
- Dog Agent：宠物社交界面截图
- MCP Video Gen：视频生成效果对比
- **封面策略**:
  - 真实使用场景展示

#### 4月7日 - OpenOctopus + OpenOctopus（双版本策略）
**主推截图**:
- OpenOctopus：Agent协作流程截图
- **双版本执行**:
  - 版本A：技术架构图（开发者导向）
  - 版本B：使用效果展示（用户导向）

### 🧪 新增A/B测试计划

#### Test-002：封面风格对比（规划中）
- **项目**: Capa-BFF
- **变量A**: 代码截图（技术专业）
- **变量B**: 界面截图（功能展示）
- **目标**: 点击率对比
- **执行时间**: 4月4日或后续

#### Test-007：封面类型对比（新增）
- **项目**: MCP Video Gen
- **变量A**: 真实截图（代码+效果）
- **变量B**: AI生成图（扁平插画风）
- **目标**: 点击率对比
- **执行时间**: 4月5日准备

### 🎨 项目专属封面建议（更新版）

#### Capa-BFF（零成本BFF - 36 stars ⭐）
**优先级**: 最高推广项目
**推荐截图**:
- GitHub仓库首页（36 stars突出显示）
- 代码核心截图（零成本架构）
- 性能对比图表
- **双版本策略**:
  - 版本A：代码架构图（技术专业）
  - 版本B：性能提升对比图（用户价值）

#### Capa-Java（混合云SDK - 14 stars ⭐）
**优先级**: 高推广项目
**推荐截图**:
- 混合云架构设计图
- 多运行时适配代码
- GitHub仓库首页
- **双版本策略**:
  - 版本A：技术架构图（开发者）
  - 版本B：使用场景图（运维人员）

#### MCP Video Gen（新兴热点）
**优先级**: 新技术机会
**推荐截图**:
- 多视频生成引擎截图
- 生成的视频效果对比
- MCP服务器代码
- **封面策略**:
  - 重点展示多引擎支持的独特性

#### Trip Agent（核心应用）
**推荐截图**:
- 路线规划界面
- 多Agent协作流程
- 用户交互界面
- **双版本策略**:
  - 版本A：技术实现图
  - 版本B：用户体验图

### 📋 每日封面检查清单（更新版）

发布前检查：
- [ ] 3:4 竖图比例
- [ ] 内容清晰可见
- [ ] 与标题内容相关
- [ ] 真实截图优先（除非特殊需求）
- [ ] 无版权问题
- [ ] 文件大小 < 5MB
- [🔄] 双版本项目需准备两种风格截图
- [🔄] 重点推广项目需制作双版本封面

---

### 🎯 本周封面策略重点

#### 高优先级项目（双版本策略）
1. **Capa-BFF** - 零成本BFF，Hackathon金奖
2. **Capa-Java** - 混合云SDK，技术价值高  
3. **Trip Agent** - 核心应用，用户价值高

#### 中优先级项目
1. **MCP Video Gen** - 新兴热点，技术区稀缺
2. **Dog Agent** - 产品截图有吸引力
3. **OpenOctopus** - 架构独特性展示

#### 低优先级项目
1. **ccuse** - CLI工具截图相对简单
2. **English Agent** - 效果展示为主

### 📊 封面效果追踪表

| 日期 | 项目 | 封面类型 | 版本 | 期望效果 | 实际效果 | 数据 |
|------|------|----------|------|----------|----------|------|
| 04-01 | Trip Agent | 真实截图 | Test-001 | 高点击率 | 待记录 | 需查看后台 |
| 04-02 | Capa-Java | 代码截图 | 单版本 | 技术专业性 | 待执行 | 预期良好 |
| 04-03 | ccuse/English | 双版本 | 双版本 | 覆盖双用户群 | 待执行 | 预期优秀 |
| 04-04 | Capa-BFF | 双版本 | 双版本 | 高推广效果 | 待执行 | 重点目标 |

---

*下次更新*: 根据双版本封面效果数据更新策略
**特别注意**: 
1. 推广重点项目采用双版本封面策略
2. 真实截图始终是技术区首选
3. 建立封面效果数据追踪机制
4. 浏览小红书竞品封面样式（今日重点任务）
