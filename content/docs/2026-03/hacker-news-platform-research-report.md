# Hacker News 平台自动发帖机制调研报告

**调研日期**: 2026-03-25
**调研人**: 旺财 (OpenClaw)
**状态**: 进行中
**优先级**: 🔥 高

---

## 一、平台概述

### 1.1 基本信息
| 项目 | 内容 |
|------|------|
| **平台名称** | Hacker News (HN) |
| **官网** | https://news.ycombinator.com |
| **API 情况** | 无官方 API |
| **认证方式** | Browser Automation |
| **运营方** | Y Combinator |
| **用户群体** | 技术决策者、创业者、投资人 |

### 1.2 平台特点
- **技术圈核心**：硅谷/技术圈影响力最大
- **高质量受众**：技术决策者、VC、媒体
- **简洁设计**：极简主义，注重内容
- **投票系统**：Upvote 决定曝光
- **社区挑剔**：质量第一，拒绝营销

### 1.3 内容类型

| 类型 | 端点 | 说明 | 适合度 |
|------|------|------|--------|
| **Show HN** | `/show` | 项目发布 | ⭐⭐⭐⭐⭐ |
| **Ask HN** | `/ask` | 技术讨论 | ⭐⭐⭐⭐ |
| **技术文章** | `/newest` | 技术分享 | ⭐⭐⭐⭐ |
| **招聘** | `/jobs` | 招聘信息 | ⭐⭐ |

---

## 二、API 机制详解

### 2.1 官方 API 情况

**❌ 无官方发布 API**
- Hacker News 没有公开的发布 API
- 只有只读 API（获取帖子、评论）

**✅ 替代方案: Browser Automation**

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
            self.page.fill('input[name="pw"]', password)

            # 点击登录
            self.page.click('input[type="submit"]')

            # 等待登录成功
            time.sleep(3)

            # 保存 Cookie
            self.save_cookies()

            print("✅ Logged in successfully")

    def submit_story(self, title, url=None, text=None):
        """提交故事/帖子"""
        # 访问提交页面
        self.page.goto("https://news.ycombinator.com/submit")

        # 等待页面加载
        time.sleep(2)

        # 填写标题
        self.page.fill('input[name="title"]', title)

        # 填写 URL 或文本
        if url:
            self.page.fill('input[name="url"]', url)
        elif text:
            self.page.fill('textarea[name="text"]', text)

        # 点击提交
        self.page.click('input[type="submit"]')

        # 等待提交完成
        time.sleep(3)

        # 获取帖子 URL
        post_url = self.page.url

        print(f"✅ Submitted: {post_url}")
        return {
            "success": True,
            "url": post_url
        }

    def reply_to_comment(self, item_id, text):
        """回复评论"""
        # 访问帖子页面
        self.page.goto(f"https://news.ycombinator.com/item?id={item_id}")

        # 找到回复链接
        time.sleep(2)
        reply_link = self.page.locator('a:has-text("reply")').first
        reply_link.click()

        # 等待回复框出现
        time.sleep(1)

        # 填写回复
        self.page.fill('textarea[name="text"]', text)

        # 提交回复
        self.page.click('input[type="submit"]')

        print(f"✅ Replied to item {item_id}")

    def save_cookies(self):
        """保存 Cookie"""
        cookies = self.page.context.cookies()
        with open("hn_cookies.json", "w") as f:
            json.dump(cookies, f)

    def load_cookies(self):
        """加载 Cookie"""
        with open("hn_cookies.json", "r") as f:
            cookies = json.load(f)
        self.page.context.add_cookies(cookies)

    def close(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()

# 使用示例
poster = HackerNewsPoster()
poster.login("kevinten10", "your_password")

# 提交 Show HN
result = poster.submit_story(
    title="Show HN: OpenOctopus - Realm-native life agent system",
    url="https://github.com/open-octopus/openoctopus",
    text=None
)

poster.close()
```

---

## 三、内容策略建议

### 3.1 Hacker News 平台特点

**适合内容**:
- ✅ 开源项目发布（Show HN）
- ✅ 技术深度讨论
- ✅ 创业经验分享
- ✅ 技术趋势观察

**不适合内容**:
- ❌ 纯推广、营销内容
- ❌ 低质量、浅显内容
- ❌ 标题党、夸大宣传
- ❌ 重复发布相同内容

### 3.2 发帖频率建议

| 场景 | 频率 | 说明 |
|------|------|------|
| **Show HN** | 项目发布时 | 重大功能、正式发布 |
| **技术讨论** | 偶尔 | Ask HN、深度讨论 |
| **评论互动** | 经常 | 建立社区信任 |

**最佳发布时间** (EST):
- **工作日 9-11 AM**（最佳时间）
- **工作日 2-4 PM**（次佳时间）
- 避免周末和深夜

### 3.3 内容模板示例

#### Show HN 模板
```
标题: Show HN: [Project Name] - [One-line description]

正文（如果需要）:
Hello HN! 👋

I've been working on [Project Name] for [timeframe], and just released [version/feature].

## What it does

[Description of the project and problem it solves]

## Why I built this

[Personal motivation and story]

## Key features

- [Feature 1]
- [Feature 2]
- [Feature 3]

## Tech stack

[Brief mention of technologies used]

## Links

GitHub: [Link]
Demo: [Link]
Website: [Link]

I'd love to hear your feedback and answer any questions!

Thanks for checking it out! 🙏
```

#### Ask HN 模板
```
标题: Ask HN: [Question]?

正文:
Hi HN! 👋

I'm working on [context], and I'm curious about [topic].

[More details about your question]

What's your experience with [topic]?

Thanks in advance! 🙏
```

### 3.4 Show HN 最佳实践

**✅ 成功要素**:
1. **真实项目**：有实际可用产品
2. **独特价值**：解决问题、创新点
3. **技术深度**：展示技术实力
4. **个人故事**：真实动机和经历
5. **积极互动**：回复评论、接受反馈

**❌ 失败原因**:
1. **纯推广**：营销话术、夸大宣传
2. **未完成**：概念阶段、不可用
3. **重复内容**：类似项目、无创新
4. **忽略社区**：不回复评论、傲慢
5. **错误时间**：周末、深夜发布

---

## 四、与现有平台对比

| 维度 | Hacker News | Reddit | Medium | Dev.to |
|------|-------------|--------|--------|--------|
| **用户质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **影响力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **技术难度** | 中 | 低 | 中 | 低 |
| **流量爆发** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **社区挑剔** | 高 | 中 | 低 | 低 |
| **API 支持** | ❌ | ✅ | ❌ | ✅ |

---

## 五、实施建议

### 5.1 短期方案 (1-2周)

**目标**: 验证可行性

**方案**: Browser Automation
- 开发 Playwright 脚本
- 测试登录和发布
- 发布 1-2 个项目（Show HN）

**成本**: $0

### 5.2 中期方案 (1-2月)

**目标**: 项目发布工具

**方案**: 半自动化
- 手动编写内容（质量第一）
- 自动化发布流程
- 监控反馈和互动

**技术栈**:
```
人工内容 → Playwright 发布 → 自动监控评论
```

### 5.3 长期方案 (3月+)

**目标**: 品牌建设

**功能**:
- 定期发布高质量项目
- 建立社区信任
- 数据分析优化
- 跨平台内容复用

---

## 六、风险评估

### 6.1 平台风险
| 风险 | 等级 | 说明 |
|------|------|------|
| **账号封禁** | 中 | 过度自动化、低质量内容 |
| **帖子被踩** | 中 | 社区挑剔、质量差 |
| **零曝光** | 低 | 未上首页、无流量 |
| **负面评论** | 中 | 社区直言不讳 |

### 6.2 合规建议
- ✅ 遵守 Hacker News Guidelines
- ✅ 内容真实、有价值
- ✅ 积极回复评论
- ✅ 控制发布频率（项目发布时）
- ✅ 避免营销话术

**Hacker News Guidelines**:
- Don't post about your own projects too often
- Be respectful
- No marketing speak
- Quality over quantity

---

## 七、下一步行动

### 立即行动（需要决策）
1. [ ] 确认 Hacker News 账号（kevinten10）
2. [ ] 决定是否开发 Browser Automation
3. [ ] 选择首批发布项目（1-2 个）

### 技术开发（如果决定实施）
1. [ ] 开发 HN Poster 脚本
2. [ ] 测试登录和发布
3. [ ] 创建发布流程

### 内容准备
1. [ ] 准备 1-2 个项目的 Show HN 内容
2. [ ] 研究 Show HN 最佳实践
3. [ ] 确定发布时间

---

## 八、资源链接

- **Hacker News**: https://news.ycombinator.com
- **HN Guidelines**: https://news.ycombinator.com/newsguidelines.html
- **Show HN Archive**: https://news.ycombinator.com/show
- **Playwright 文档**: https://playwright.dev/python

---

## 九、总结

**可行性**: ⭐⭐⭐⭐ (4/5)
- 无官方 API，但 Browser Automation 可行
- 技术实现中等难度
- 需要谨慎操作，避免封号

**战略价值**: ⭐⭐⭐⭐⭐ (5/5)
- 技术圈核心影响力
- 高质量受众（VC、技术决策者）
- 流量爆发潜力大
- 项目发布首选平台

**建议**: **值得投入**
- 使用 Browser Automation
- 专注 Show HN（项目发布）
- 质量第一，宁缺毋滥
- 积极参与社区互动

---

**报告状态**: 初稿完成
**更新日期**: 2026-03-25
**下一步**: 等待主人决策是否实施
