# CSDN 文章：说实话，养猫三年踩的坑，最后搞了个 AI 来帮忙

> 文章类型：项目推广类
> 目标项目：Dog Agent（宠物管理 AI Agent）
> 字数要求：1500-2500字
> 风格：人类化写作（反 AI 检测）

---

## 项目介绍

Dog Agent —— 一个专门帮你管理宠物健康、饮食和日常事项的 AI 助手。

GitHub: https://github.com/kevinten-ai/dog-agent
网站: https://pet.rxcloud.group

老实说，这个项目一开始就是 selfish 的——纯粹是因为我养猫三年，踩了太多坑，受不了了才做的。

---

## 背景：养猫人的痛

说实话，养猫之前我以为就是喂喂食、铲铲屎，挺简单的。然后呢，真正养了才发现，事情比想象的复杂得多。

**第一个坑：疫苗和驱虫时间完全记不住**

我家主子第一年该打什么疫苗、什么时候驱虫，我记了三个 APP，最后还是错过了狂犬疫苗的加强针。当时真的有点崩溃，宠物医院打电话来说"您的猫该打疫苗了"，我还反问"不是刚打过吗"，结果人家一查记录，已经过了三个月了。挺尴尬的是吧。

**第二个坑：饮食管理一团糟**

猫粮、罐头、零食、化毛膏... 每种东西多久喂一次、每次喂多少，我一开始就是随缘。结果呢，猫胖了，兽医说"这猫得减肥"。我当时就懵了，心想我明明没喂多少啊。后来仔细一算，各种零食加起来，热量早超了。是的我知道，挺蠢的是吧。

**第三个坑：异常症状不会判断**

猫呕吐了，是毛球还是生病？精神不好，是困了还是不舒服？我每次都是先 Google 一番，然后越看越慌，最后跑医院，医生说"没事，正常的"。反正就这样折腾了好几次。

**最后一个坑：多猫家庭的混乱**

后来我又养了一只，事情复杂度直接翻倍。两只猫的疫苗时间不一样、饮食需求不一样，经常搞混。给谁喂了驱虫药、谁还没喂，完全记不住。

我当时就想，要是有个东西能帮我记住这些事，提醒我什么时候该干嘛，顺便还能告诉我某些症状严不严重，那该多好。

然后就动手做了 Dog Agent。

---

## 技术架构

### 核心模块

```python
# 宠物档案管理
class PetProfile:
    """每只宠物一个档案，记录基本信息、健康史、饮食偏好"""
    def __init__(self, name, species, birth_date):
        self.name = name
        self.species = species  # cat, dog, etc.
        self.birth_date = birth_date
        self.health_records = []
        self.vaccine_schedule = []
        self.diet_plan = None

# 智能提醒系统
class ReminderEngine:
    """基于时间、宠物年龄、季节等因素生成提醒"""
    def get_upcoming_tasks(self, pet_id):
        # 疫苗、驱虫、体检等
        # 会考虑宠物年龄调整频率
        # 比如幼猫和老猫的驱虫频率不同
        pass

# 症状分析器
class SymptomAnalyzer:
    """分析宠物症状，给出建议"""
    def analyze(self, symptoms, pet_profile):
        # 基于症状库和宠物信息给出建议
        # 严重级别：观察、尽快就医、立即就医
        pass
```

### 技术栈

- **后端**: Python + FastAPI
- **数据库**: PostgreSQL + Redis（缓存）
- **AI 模型**: Claude API（症状分析和建议生成）
- **任务调度**: APScheduler（定时提醒）
- **前端**: 还没做，目前主要是 API 和 Telegram Bot

### 数据流

```
用户输入（新宠物/事件/症状）
    ↓
PetProfile 更新 / HealthRecord 记录
    ↓
ReminderEngine 重新计算提醒时间
    ↓
APScheduler 调度任务
    ↓
到时间发送提醒（Telegram/Email）
```

---

## 踩坑经历

做这个项目的过程中，也踩了不少坑。

**坑1：疫苗时间表太复杂**

不同疫苗的接种时间、间隔、加强针规则都不一样。更麻烦的是，不同地区的推荐方案还不一样。我一开始想自己整理一套"标准方案"，结果发现根本不存在标准方案。

最后改成可配置的，用户可以自己设置或者选择所在地区的推荐方案。

**坑2：症状分析很容易越界**

一开始我想让 AI 直接给出"这是什么病"的诊断，但很快意识到这是个严重问题——我不是兽医，AI 也不是，给出诊断是违法的，而且可能误导用户。

后来改成"风险评级 + 建议就医级别"的模式，并且明确说明"仅供参考，不能替代兽医诊断"。

**坑3：多宠物关联的逻辑比想象复杂**

比如两只猫，一只是另一只的"哥哥"，它们可能有相同的遗传病风险，但疫苗时间又不一样。这些关系建模起来还挺费劲的。

---

## 优缺点分析（实事求是）

### 优点

1. **确实解决了我自己的问题**
   
   用了三个月，没再错过疫苗时间，体重也控制住了。对我个人来说，这个项目是成功的。

2. **提醒逻辑还算智能**
   
   会根据宠物年龄调整，比如幼猫驱虫频率高，老年猫体检频率高。不是简单的定时提醒。

3. **症状分析虽然有限，但有点用**
   
   至少能告诉我"这种情况可以先观察"还是"最好明天去看医生"，减少了一些不必要的焦虑。

### 缺点

1. **数据依赖手动输入**
   
   所有的疫苗记录、体重记录都需要手动输入。如果能对接宠物医院的系统就好了，但目前做不到。

2. **症状分析的准确率有限**
   
   毕竟基于文本描述，很多症状需要实际检查才能确定。有时候 AI 给出的建议和实际情况有偏差。

3. **前端还没做**
   
   目前主要是 API 和 Telegram Bot，对普通用户不够友好。想做 Web 界面但还没时间。

4. **只支持猫狗**
   
   其他宠物（兔子、仓鼠、鸟类）的支持还没做，因为我不养这些，不了解需求。

---

## 适用场景

### 适合：

- **多宠物家庭**：记性不好，需要系统帮忙管理
- **新手养宠**：不知道疫苗、驱虫的时间节点
- **容易焦虑的主人**：有个症状想先大概了解一下严重程度

### 不适合：

- **已经有完善管理习惯的人**：如果你已经用 Excel 或者其他工具管理得很好，没必要换
- **追求医疗级诊断的人**：这只是辅助工具，不能替代兽医
- **养异宠的人**：目前只支持猫狗

---

## 代码示例

### 添加宠物档案

```python
from dog_agent import PetProfile, ReminderEngine

# 创建宠物档案
mimi = PetProfile(
    name="咪咪",
    species="cat",
    birth_date="2022-03-15"
)

# 设置疫苗计划（使用默认猫疫苗方案）
mimi.set_vaccine_schedule("cat_standard_cn")

# 查看 upcoming 任务
engine = ReminderEngine()
tasks = engine.get_upcoming_tasks(mimi.id)
for task in tasks:
    print(f"{task.date}: {task.description}")
```

### 记录症状并获取建议

```python
from dog_agent import SymptomAnalyzer

analyzer = SymptomAnalyzer()

# 记录症状
symptoms = ["呕吐", "精神状态正常", "食欲正常"]
result = analyzer.analyze(symptoms, mimi)

print(f"风险等级: {result.risk_level}")  # low/medium/high
print(f"建议: {result.recommendation}")
print(f"是否需要就医: {result.vet_needed}")
```

### 自定义提醒

```python
# 添加自定义提醒
mimi.add_custom_reminder(
    description="换猫砂",
    frequency="weekly",
    next_due="2026-03-30"
)
```

---

## 写在最后

说实话，Dog Agent 不是什么改变世界的项目，它就是解决了我自己的一个痛点。如果你也有类似的困扰，可以试试看。

如果你养宠物，肯定也有类似的崩溃时刻吧？比如忘记驱虫、搞混疫苗时间、或者半夜猫吐了不知道要不要去医院？

欢迎在评论区聊聊你的养宠踩坑经历！

---

**GitHub**: https://github.com/kevinten-ai/dog-agent
**在线体验**: https://pet.rxcloud.group
