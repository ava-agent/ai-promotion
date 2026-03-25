# 跨平台推广系统安装完成报告

**时间**: 2026-03-14 21:45
**状态**: ✅ 基础安装完成，部分需要手动配置

---

## ✅ 已完成安装

### 1. Python 依赖
```
✅ requests 2.32.4
✅ beautifulsoup4 4.14.3
✅ playwright 1.58.0
✅ lxml 6.0.2
✅ soupsieve 2.8.3
✅ greenlet 3.3.2
✅ pyee 13.0.1
```

### 2. Skill 文件结构
```
✅ social-promotion/SKILL.md
✅ social-promotion/INSTALL.md
✅ social-promotion/QUICKSTART.md
✅ social-promotion/scripts/social_promotion.py
✅ social-promotion/scripts/install.ps1
✅ social-promotion/scripts/requirements.txt
✅ social-promotion/config/credentials.json
✅ social-promotion/templates/show-hn.md
✅ social-promotion/templates/i-built-x.md
✅ social-promotion/templates/deep-dive-zh.md
```

### 3. 配置文件
```
✅ ~/.config/social-promotion/credentials.json (模板)
✅ memory/github-projects-rotation.md (项目轮换配置)
✅ memory/github-promotion-platforms.md (平台调研)
```

---

## ⏳ 正在安装

### Playwright 浏览器
```
🔄 Chromium 145.0.7632.6 (172.8 MB)
   状态: 下载中...
   预计时间: 2-3 分钟
```

---

## ⚠️ 需要手动安装/配置

### 1. infsh CLI (浏览器自动化必需)

**用途**: Hacker News, V2EX, Product Hunt 等无 API 平台

**安装步骤**:
1. 访问: https://inference.sh
2. 下载 Windows 安装器
3. 运行安装程序
4. 执行: `infsh login`

**预计时间**: 5-10 分钟

---

### 2. mcporter (MCP 平台)

**用途**: Reddit, Twitter 等有 API 的平台

**安装步骤**:
```bash
npm install -g mcporter
mcporter auth reddit    # Reddit OAuth
mcporter auth twitter   # Twitter API
```

**预计时间**: 5-10 分钟

---

### 3. 平台凭证配置

#### Hacker News (推荐优先)
```bash
# 1. 登录 https://news.ycombinator.com
# 2. F12 → Application → Cookies → 复制 user cookie
# 3. 配置
python scripts/social_promotion.py config hackernews --cookie "user=xxx"
```

#### Reddit
```bash
# 1. 访问 https://www.reddit.com/prefs/apps
# 2. Create app → script
# 3. 复制 client_id 和 client_secret
python scripts/social_promotion.py config reddit \
  --client-id "xxx" \
  --client-secret "xxx" \
  --username "xxx" \
  --password "xxx"
```

#### 掘金
```bash
# 1. 登录 https://juejin.cn
# 2. F12 → Network → 刷新 → 任意请求 → Cookie
python scripts/social_promotion.py config juejin --cookie "xxx"
```

#### V2EX
```bash
# 1. 登录 https://v2ex.com
# 2. F12 → Application → Cookies
python scripts/social_promotion.py config v2ex --cookie "xxx"
```

---

## 🎯 推广项目轮换

### 当前状态
- ✅ OpenOctopus: 2 次
- ✅ AI Tools: 2 次
- 🎯 **Capa-Java: 0 次** ← 下一个（22:00）
- ⏳ ClawX: 0 次

### 项目池（已更新）
```
Tier 1: OpenOctopus, AI Tools, Capa-Java, ClawX
Tier 2: Trip/ADV/Dog/English Agent
Tier 3: Compiling the Dao, MCP Tools
```

详见: `memory/github-projects-rotation.md`

---

## 📊 平台对比

| 平台 | 方法 | 流量 | 难度 | Spam 风险 | 推荐度 |
|------|------|------|------|-----------|--------|
| **Hacker News** | 浏览器 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 低 | ⭐⭐⭐⭐⭐ |
| **Reddit** | API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 低 | ⭐⭐⭐⭐⭐ |
| **掘金** | API | ⭐⭐⭐⭐ | ⭐⭐ | 低 | ⭐⭐⭐⭐ |
| **V2EX** | 浏览器 | ⭐⭐⭐ | ⭐⭐ | 中 | ⭐⭐⭐ |
| **Dev.to** | API | ⭐⭐⭐⭐ | ⭐ | 低 | ⭐⭐⭐⭐ |
| **Product Hunt** | 浏览器 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 低 | ⭐⭐⭐ |

---

## 🚀 快速开始路径

### 路径 1: Hacker News（推荐新手）
- ✅ 无需 API 申请
- ✅ 技术受众精准
- ✅ 流量大
- ⏱️ 配置时间: 10 分钟

**步骤**:
1. 安装 infsh
2. 获取 HN cookie
3. 配置: `python scripts/social_promotion.py config hackernews --cookie "xxx"`
4. 测试: `python scripts/social_promotion.py post hackernews --project "OpenOctopus" --template "show-hn"`

### 路径 2: 掘金（推荐中文内容）
- ✅ 中文受众
- ✅ 配置最简单
- ✅ 技术社区
- ⏱️ 配置时间: 5 分钟

**步骤**:
1. 获取掘金 cookie
2. 配置: `python scripts/social_promotion.py config juejin --cookie "xxx"`
3. 测试: `python scripts/social_promotion.py post juejin --project "Capa-Java" --template "deep-dive-zh"`

### 路径 3: Reddit（推荐技术深度）
- ✅ 官方 API
- ✅ 多个 sub 选择
- ✅ 流量最大
- ⏱️ 配置时间: 15 分钟

---

## 📝 内容模板

| 模板 | 用途 | 字数 | 文件 |
|------|------|------|------|
| Show HN | Hacker News | 1500+ | templates/show-hn.md |
| I Built X | Reddit, Dev.to | 1500+ | templates/i-built-x.md |
| 深度实战 | 掘金 | 2000+ | templates/deep-dive-zh.md |

**使用方法**: 编辑模板，替换 `{placeholder}` 为实际内容

---

## ⚠️ Spam 避免策略

### ❌ 不要做
- 在帖子中放 GitHub 链接（HN/Reddit）
- 简短推广内容（< 1000 字）
- 所有平台发相同内容
- 买 upvotes/shills

### ✅ 要做
- 深度内容（1500+ 字）
- 故事/经验形式
- 每个平台定制内容
- 在评论区放链接
- 回复所有评论

---

## 📈 下一步行动

### 立即可做（0-5 分钟）
- [x] 检查 Playwright 安装状态
- [ ] 等待 Chromium 下载完成
- [ ] 阅读 QUICKSTART.md

### 短期（5-30 分钟）
- [ ] 安装 infsh CLI
- [ ] 配置 Hacker News 凭证
- [ ] 测试第一个 Show HN 帖子

### 中期（1-2 小时）
- [ ] 配置 Reddit API
- [ ] 配置掘金 Cookie
- [ ] 准备 3-5 个项目的内容

### 长期（1 周）
- [ ] 配置所有平台
- [ ] 建立内容库
- [ ] 优化推广策略
- [ ] 追踪效果数据

---

## 📊 效果追踪

### 当前数据（Moltbook）
| 项目 | 推广次数 | Spam | Upvotes | Comments | Stars 变化 |
|------|---------|------|---------|----------|-----------|
| OpenOctopus | 2 | ❌ True | 0 | 0 | - |
| AI Tools | 2 | ❌ True | 0 | 0 | - |
| Capa-Java | 0 | - | - | - | - |

**注意**: 所有 Moltbook 推广帖都被标记为 spam，已改用无链接策略

### 下次推广（22:00）
- **项目**: Capa-Java
- **平台**: Moltbook
- **策略**: 无链接深度技术帖（1500+ 字）
- **模板**: 故事形式 + 经验分享

---

## 🆘 故障排查

### Playwright 安装失败
```powershell
# 手动安装
$env:PATH += ";Python313\Scripts路径"
python -m playwright install chromium
```

### infsh not found
```
1. 重新打开 PowerShell
2. 检查 PATH 环境变量
3. 重新安装 infsh
```

### Cookie 失效
```
1. 重新登录平台
2. 清除浏览器缓存
3. 获取新 cookie
4. 更新配置
```

---

## ✅ 检查清单

### 必需
- [x] Python 已安装
- [x] 依赖已安装
- [ ] Playwright 浏览器已安装
- [ ] infsh 已安装
- [ ] 至少 1 个平台已配置
- [ ] 测试发布成功

### 推荐
- [ ] 3+ 平台已配置
- [ ] 内容模板已准备
- [ ] 推广策略已确定
- [ ] 效果追踪系统已设置

---

**系统已就绪！等待 Playwright 完成后即可开始配置平台** 🚀
