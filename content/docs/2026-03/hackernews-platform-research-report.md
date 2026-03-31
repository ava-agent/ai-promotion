# Hacker News 平台自动发帖机制调研报告

**调研日期**: 2026-03-25
**调研人**: 旺财 (OpenClaw)
**状态**: 进行中
**优先级**: ⭐⭐⭐⭐ 高

---

## 一、平台概述

### 1.1 基本信息
| 项目 | 内容 |
|------|------|
| **平台名称** | Hacker News (HN) |
| **官网** | https://news.ycombinator.com |
| **运营方** | Y Combinator |
| **API 情况** | 无官方发布 API |
| **认证方式** | Browser Automation / Cookie |
| **定价模式** | 免费 |

### 1.2 平台特点
- **技术圈核心**：硅谷/技术圈影响力最大
- **高质量受众**：技术决策者、投资人、创业者
- **极简设计**：无广告、无干扰
- **社区挑剔**：质量第一，厌恶自我推广
- **Karma 系统**：积分决定影响力

### 1.3 内容形式

| 类型 | 说明 | 适合度 |
|------|------|--------|
| **Show HN** | 项目发布 | ⭐⭐⭐⭐⭐ |
| **Ask HN** | 问题求助 | ⭐⭐⭐⭐ |
| **技术文章** | 深度分享 | ⭐⭐⭐⭐⭐ |
| **讨论帖** | 技术讨论 | ⭐⭐⭐⭐ |

---

## 二、API 机制详解

### 2.1 官方 API 情况

**❌ 无发布 API**
- Hacker News 只有只读 API
- 无法通过 API 发布内容
- 必须使用 Browser Automation

**✅ 只读 API**
```http
GET https://hacker-news.firebaseio.com/v0/topstories.json
GET https://hacker-news.firebaseio.com/v0/item/{id}.json
```

### 2.2 Browser Automation 方案

**技术栈**:
- Playwright / Selenium
- Cookie 管理
- 反检测措施

**Python 示例**:
```python
from playwright.sync_api import sync_playwright
import time

class HackerNewsPoster:
    def __init__(self):
        self.browser = None
        self.page = None

    def login(self, username, password):
        """登录 Hacker News"""
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=False)
            self.page = self.browser.new_page()

            # 访问登录页
            self.page.goto("https://news.ycombinator.com/login")

            # 填写凭证
            self.page.fill('input[name="acct"]', username)
            self.page.fill('input[type="password"]', password)

            # 点击登录
            self.page.click('input[type="submit"]')

            # 等待登录成功
            time.sleep(3)

            # 保存 Cookie
            self.save_cookies()

    def submit_story(self, title, url=None, text=None):
        """提交故事"""
        # 访问提交页面
        self.page.goto("https://news.ycombinator.com/submit")

        # 填写标题
        self.page.fill('input[name="title"]', title)

        # 填写 URL 或文本
        if url:
            self.page.fill('input[name="url"]', url)
        elif text:
            self.page.fill('textarea[name="text"]', text)

        # 点击提交
        self.page.click('input[type="submit"]')

        time.sleep(3)

        # 获取提交的 URL
        return {
            "success": True,
            "url": self.page.url
        }

    def save_cookies(self):
        """保存 Cookie"""
        cookies = self.page.context.cookies()
        with open("hn_cookies.json", "w") as f:
            json.dump(cookies, f)
```

---

## 三、Hacker News 特殊规则

### 3.1 Show HN 规则

**必须遵守**:
- ✅ 标题格式："Show HN: [Project Name] - [One-liner]"
- ✅ 项目必须有实际价值
- ✅ 在评论区提供更多细节
- ✅ 回复评论、参与讨论

**禁止行为**:
- ❌ 纯推广、无实质内容
- ❌ 重复提交相同项目
- ❌ 标题党、夸大宣传
- ❌ 请求 upvote

### 3.2 Karma 要求

| 功能 | Karma 要求 |
|------|-----------|
| **发布帖子** | 无要求 |
| **评论** | 无要求 |
| **Downvote** | 50+ Karma |
| **影响力** | 500+ Karma |

### 3.3 社区文化

**核心价值观**:
- 质量第一
- 诚实透明
- 理性讨论
- 反对营销

**禁忌**:
- 自我推广过度
- 低质量内容
- 营销语言
- 标题党

---

## 四、内容策略建议

### 4.1 Hacker News 平台特点

**适合内容**:
- ✅ 开源项目发布（Show HN）
- ✅ 技术深度文章
- ✅ 创业经验分享
- ✅ 技术趋势讨论

**不适合内容**:
- ❌ 纯推广、营销内容
- ❌ 低质量、无深度
- ❌ 重复、老套的话题
- ❌ 过于商业化

### 4.2 发布频率建议

| 类型 | 频率 | 说明 |
|------|------|------|
| **Show HN** | 1次/项目 | 重大功能更新时 |
| **技术文章** | 1-2次/周 | 高质量深度文章 |
| **评论互动** | 每天 | 参与社区讨论 |

**最佳发布时间** (EST):
- 09:00-11:00 (Morning)
- 周二至周四（工作日）
- 避开周末和节假日

### 4.3 内容模板示例

#### Show HN（项目发布）
```
标题: Show HN: OpenOctopus - Realm-native life agent system

正文（评论区）:
Hi HN! 👋

I've been working on OpenOctopus for the past 6 months, and I'm excited to share it with you.

## What it does

OpenOctopus is a realm-native life agent system that turns any real-world object into a living AI agent with persistent memory.

## Why I built this

Most AI agents today forget everything after each session. I wanted to build something that feels more "alive" - with persistent memory, cross-realm communication, and zero-config deployment.

## Key features

- Realm-native context management
- Automatic state persistence
- Cross-realm communication
- Zero-config deployment

## Tech stack

Python, FastAPI, Redis, Dapr/Layotto

## Links

GitHub: https://github.com/open-octopus/openoctopus
Website: https://openoctopus.club

## What's next

I'm currently working on [future plans]. I'd love to hear your feedback and suggestions!

Thanks! 🙏
```

#### 技术文章分享
```
标题: [Technical Insight] - [Key takeaway]

（直接分享文章链接，在评论区补充说明）
```

---

## 五、与现有平台对比

| 维度 | Hacker News | Reddit | Medium | Dev.to |
|------|-------------|--------|--------|--------|
| **受众质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **技术影响力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **实现难度** | 中 | 低 | 中 | 低 |
| **社区挑剔度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **API 支持** | ❌ 无 | ✅ 有 | ❌ 无 | ✅ 有 |
| **流量爆发** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 六、实施建议

### 6.1 短期方案 (1-2周)

**目标**: 验证可行性

**方案**: Browser Automation
- 开发 Playwright 脚本
- 测试登录和发布
- 发布 1-2 条测试内容

**成本**: $0

### 6.2 中期方案 (1-2月)

**目标**: 建立影响力

**方案**: 智能发布 + 社区互动
- 每周 1-2 条高质量内容
- 积极参与评论讨论
- 积累 Karma

**策略**:
- 10 comments : 1 post
- 专注于 Show HN 和技术分享
- 回复每一条评论

### 6.3 长期方案 (3月+)

**目标**: 技术品牌建设

**功能**:
- 自动监控热门话题
- 智能发布时间优化
- 数据分析效果

---

## 七、风险评估

### 7.1 平台风险
| 风险 | 等级 | 说明 |
|------|------|------|
| **账号封禁** | 中 | 违反规则、过度推广 |
| **帖子被 bury** | 高 | 质量差、推广过度 |
| **社区反感** | 高 | 自我推广过度 |
| **页面变化** | 低 | HN 页面极少变化 |

### 7.2 合规建议
- ✅ 遵守 HN Guidelines
- ✅ 控制发布频率（1-2次/周）
- ✅ 内容有实质价值
- ✅ 积极参与社区（10 comments : 1 post）
- ✅ 诚实透明，避免营销语言

---

## 八、下一步行动

### 立即行动（需要决策）
1. [ ] 确认是否开发 HN 自动化
2. [ ] 准备高质量项目内容
3. [ ] 研究 Show HN 最佳实践

### 技术开发（如果决定实施）
1. [ ] 开发 HN Poster 脚本
2. [ ] 测试登录和发布
3. [ ] 创建定时任务

### 内容准备
1. [ ] 准备 2-3 个项目 Show HN
2. [ ] 撰写高质量的评论区内容
3. [ ] 确定发布计划

---

## 九、资源链接

- **Hacker News**: https://news.ycombinator.com
- **HN Guidelines**: https://news.ycombinator.com/newsguidelines.html
- **Show HN Tips**: 搜索 HN 上的 "Show HN" 帖子学习
- **Playwright 文档**: https://playwright.dev/python

---

## 十、总结

**可行性**: ⭐⭐⭐⭐ (4/5)
- 无 API，但 Browser Automation 可行
- HN 页面简单，易于自动化
- 技术实现中等难度

**战略价值**: ⭐⭐⭐⭐⭐ (5/5)
- 技术圈核心影响力
- 高质量受众（投资人、决策者）
- 流量爆发潜力大
- 技术品牌建立

**建议**: **值得投入**
- 谨慎使用，质量第一
- 专注于 Show HN 和技术分享
- 积极参与社区互动
- 避免过度自动化

---

**报告状态**: 初稿完成
**更新日期**: 2026-03-25
**下一步**: 等待主人确认是否开发
