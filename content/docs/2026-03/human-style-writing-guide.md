# 人类风格写作指南

> 避免 AI 痕迹，写出真实开发者风格的内容

## 🚫 AI 痕迹清单（禁止）

### 标题模式
- ❌ "I [verb] [number] [things]" 重复出现
- ❌ 同一数字频繁出现（如"847"）
- ❌ 过于整齐的结构（"5个教训"每次都是5）

### 内容模式
- ❌ 数据堆砌（"23%、67%、81%"连续出现）
- ❌ 完美对称的列表（总是3/5/7点）
- ❌ 缺乏个人情感和口语化
- ❌ 像技术报告，不像个人分享

---

## ✅ 人类风格特征（学习）

### 标题多样化
```
✅ "I tried X. Here's what went wrong."
✅ "Why X failed me (and how I fixed it)"
✅ "My journey with X: 3 surprises, 1 disaster"
✅ "X vs Y: What nobody tells you"
✅ "The mistake I made with X (so you don't have to)"
✅ "After 2 years with X, here's my honest take"
```

### 结构随意性
- **数字不固定**: 有时3点，有时7点，有时没有数字
- **叙事流**: 用故事串联，不是死板的列表
- **不完美**: 可以有冗余、跳跃、离题

### 口语化表达
```
✅ "Honestly, I didn't expect this to work..."
✅ "This was a pain in the ass to debug"
✅ "Surprisingly, the simplest solution won"
✅ "I spent 3 weeks on this. Don't make my mistake."
✅ "Okay, here's the thing..."
✅ "Let me be real with you..."
✅ "Plot twist: it wasn't the API's fault"
```

### 个人情感
- ✅ 表达挫折："I was frustrated when..."
- ✅ 表达惊讶："Unexpectedly, this worked better..."
- ✅ 表达不确定性："I'm still not sure if..."
- ✅ 表达后悔："I wish I knew this earlier..."

### 数据呈现自然化
```
❌ AI风格:
"23%的API调用失败，67%存在认证问题，81%的满意度提升"

✅ 人类风格:
"About a quarter of my API calls failed. Most were auth issues.
After fixing it, satisfaction jumped to around 80%."
```

---

## 📝 Dev.to 写作模板（人类风格版）

### 模板 1：失败经验分享
```markdown
# I tried [X]. Here's what went wrong.

[开场: 2-3句话，口语化]
Honestly, I thought [X] would solve my problem. It didn't.

[故事: 叙事流，不用数字列表]
Week 1 was fine. Week 2, things got weird. By week 3, I realized...

[真实感受]
This was frustrating. I spent late nights debugging...

[转折]
Then I tried [Y]. And it worked.

[教训: 2-4个，不固定数字]
- Don't overthink [X]
- [Y] is simpler than it looks
- Test early, test often

[结尾: 开放性问题]
Has anyone else run into this? What worked for you?
```

### 模板 2：对比分析
```markdown
# [X] vs [Y]: What nobody tells you

[个人背景]
I've been using [X] for 2 years. Recently tried [Y].

[真实体验]
[用故事串联，不用完美列表]
First impression: [Y] seemed better. But then...

[意外发现]
Here's what surprised me...

[不完美的结论]
I'm still not sure which is better. It depends on...

[引发讨论]
What's your take? [X] or [Y]?
```

### 模板 3：教训总结
```markdown
# [数字] lessons from [项目/经历]

[开场: 口语化]
After [时间] working on [项目], here's what I learned:

[教训: 不固定数字，2-6个]
**1. [教训1]**
[故事 + 真实感受]

**2. [教训2]**
[故事 + 意外转折]

**3. [教训3]**
[故事 + 个人反思]

[结尾: 不确定感]
I'm still learning. What would you add to this list?
```

---

## 🎯 掘金写作模板（中文人类风格）

### 模板 1：踩坑经历
```markdown
# [项目]踩坑实录：[具体问题]

[开场: 口语化]
说实话，我以为这事儿很简单。结果...

[故事流]
刚开始一切正常。直到有一天...

[真实感受]
当时真的崩溃了，debug到凌晨3点...

[解决方案]
最后发现是[原因]。解决方案很简单：

[教训: 2-4个]
- 不要[错误做法]
- 一定要[正确做法]
- 记得[额外提醒]

[结尾: 开放性]
你们遇到过类似问题吗？怎么解决的？
```

### 模板 2：经验分享
```markdown
# 用了[时间]的[工具]，我的真实感受

[背景]
最近在[场景]用到了[工具]，说说真实体验。

[优点: 不用列表，用叙事]
先说好的方面。[具体例子]...

[缺点: 诚实表达]
但也有一些槽点。[具体例子]...

[适用场景]
我觉得这个工具适合[场景]，不太适合[场景]。

[总结: 不确定感]
以上只是我的个人体验，仅供参考。你们觉得呢？
```

---

## 🔄 风格检查清单（发布前必查）

### 标题检查
- [ ] 标题不是 "I [verb] [number] [things]" 模板
- [ ] 标题有情感或口语化元素
- [ ] 标题不重复之前用过的模式

### 内容检查
- [ ] 结构不完美对称（不是总是5点）
- [ ] 有口语化表达（"Honestly", "Surprisingly"等）
- [ ] 有个人情感（frustration, surprise, uncertainty）
- [ ] 数据呈现自然化（不用百分比堆砌）
- [ ] 结尾有开放性问题

### AI 痕迹检查
- [ ] 没有过度使用同一数字（如"847"）
- [ ] 没有完美对称的列表结构
- [ ] 不像技术报告，像个人随笔
- [ ] 有真实感和不完美感

---

## 📚 参考案例

### ✅ 好的 Dev.to 文章风格
- https://dev.to/karanpratapsingh/10-things-i-learned-building-a-youtube-downloader-4ka7
- https://dev.to/ben/what-was-your-win-this-week-428j
- https://dev.to/smpnjn/i-built-a-website-that-doesnt-use-javascript-3dl6

### ✅ 好的掘金文章风格
- 用真实语气分享经验
- 有个人情感和口语化
- 不完美但有真实感

---

## 💡 核心原则

1. **真实性 > 完美性**: 不完美才像人
2. **情感 > 数据**: 用故事打动人，不是数字
3. **随意 > 对称**: 结构随机才自然
4. **口语 > 学术**: 像聊天，不像报告
5. **不确定 > 确信**: 人类有疑虑，AI 才全知

---

最后更新：2026-03-25 07:55
