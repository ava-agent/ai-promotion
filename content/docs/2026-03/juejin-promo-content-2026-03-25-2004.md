# 说实话，我给我家狗做了个 AI 管家，结果发现最该管的是我自己

> GitHub: https://github.com/kevinten-ai/dog-agent | 体验: https://pet.rxcloud.group

## 先说下背景

老实说，做这个项目的初衷挺搞笑的。

去年我养了只柴犬，叫"年糕"。然后呢，问题来了——我完全记不住它该什么时候打疫苗、什么时候驱虫、每天吃多少粮。手机里记了一堆备忘录，但根本没用，该忘还是忘。

有次带年糕去宠物医院，医生问"上次驱虫什么时候"，我当场懵了，翻手机翻了半天没找着。医生那个眼神，怎么说呢，就是那种"你这主人当的"的感觉。

回去之后我就想，我天天写代码，就不能写个东西来管管这事儿？

然后我就动手了。

## 项目介绍

Dog Agent 就是一个帮你管宠物的 AI。说实话功能挺简单的：

- 记录疫苗、驱虫时间，到期提醒你
- 根据体重、年龄算每天该喂多少粮
- 记录体重变化，看看有没有异常
- 拍照识别狗粮成分（这个有点实验性质）
- 找个附近的宠物医院、宠物店

GitHub 地址在上面，有兴趣可以看看代码。架构是用 Python + FastAPI 做的后端，前端是 Vue3，数据库用的 PostgreSQL。

## 技术架构

### 整体架构

说实话架构没啥特别的，就是常规的分层：

```
┌─────────────────────────────────────┐
│           Vue3 Frontend             │
│     (Quasar Framework + Pinia)      │
└─────────────┬───────────────────────┘
              │ HTTP/REST
┌─────────────▼───────────────────────┐
│          FastAPI Backend            │
│  ┌─────────┐ ┌─────────┐ ┌──────┐  │
│  │ Pet API │ │Health   │ │Search│  │
│  │         │ │Check API│ │ API  │  │
│  └─────────┘ └─────────┘ └──────┘  │
└─────────────┬───────────────────────┘
              │ SQLAlchemy
┌─────────────▼───────────────────────┐
│         PostgreSQL + Redis          │
│   (主数据存储 + 缓存/会话)            │
└─────────────────────────────────────┘
```

### 核心模块

**1. 宠物档案管理**

这个是最基础的，就是 CRUD。但有个小难点：不同宠物的数据字段不一样。比如猫和狗的疫苗种类就不同，大型犬和小型犬的食量计算也不一样。

我用了一个动态 schema 的设计，大概长这样：

```python
class PetProfile(BaseModel):
    id: str
    name: str
    species: str  # dog, cat, etc.
    breed: str
    birth_date: date
    weight: float
    # 动态属性，根据 species 不同而变化
    attributes: Dict[str, Any]
    
    def get_vaccine_schedule(self) -> List[VaccineRecord]:
        """根据物种返回不同的疫苗计划"""
        schedules = {
            "dog": [...],  # 犬用疫苗
            "cat": [...],  # 猫用疫苗
        }
        return schedules.get(self.species, [])
```

**2. 健康监测**

这部分稍微复杂一点。需要：
- 根据体重、年龄计算每日建议食量
- 追踪体重变化趋势
- 预测疫苗/驱虫到期时间

食量的计算公式我查了挺多资料，最后用的这个（以狗为例）：

```python
def calculate_daily_food(weight_kg: float, age_months: int, 
                         activity_level: str = "normal") -> float:
    """
    计算每日建议食量（克）
    
    公式基于 RER (Resting Energy Requirement):
    RER = 70 * (weight ^ 0.75)
    然后乘以活动系数
    """
    rer = 70 * (weight_kg ** 0.75)
    
    # 年龄系数
    if age_months < 4:
        age_factor = 3.0  # 幼犬需要更多
    elif age_months < 12:
        age_factor = 2.0
    else:
        age_factor = 1.6 if age_months < 84 else 1.4  # 老年犬减少
    
    # 活动系数
    activity_factors = {
        "low": 0.8,
        "normal": 1.0,
        "high": 1.2
    }
    
    daily_calories = rer * age_factor * activity_factors.get(activity_level, 1.0)
    
    # 假设狗粮热量约为 3500 kcal/kg
    daily_food_grams = (daily_calories / 3500) * 1000
    
    return round(daily_food_grams)
```

**3. AI 图像识别**

这个功能其实挺鸡肋的，但我就是想试试。用户可以拍狗粮包装，AI 会识别成分并给出简单评价。

用的是 OpenAI 的 GPT-4 Vision API，代码大概这样：

```python
async def analyze_food_image(image_base64: str) -> FoodAnalysis:
    """分析狗粮图片"""
    response = await openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "分析这个宠物食品的成分表..."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]
        }]
    )
    
    # 解析返回结果...
    return parse_analysis(response.choices[0].message.content)
```

说实话，这个功能用下来发现不太实用。一是拍照要拍清楚成分表挺难的，二是 AI 分析出来的结果也就那样，不会比你自己看强多少。

## 踩坑经历

做这个项目踩了不少坑，说几个印象深的。

**坑1：疫苗时间计算**

一开始我想得挺简单，疫苗就是固定间隔打呗。结果发现不同疫苗的间隔不一样，有的要每年打，有的要每三年，还有的要分几次打。

更麻烦的是，用户可能记错了上次接种时间，或者在不同医院打的记录对不上。这个我真没想好怎么解决，现在就是让用户自己核对。

**坑2：食量计算的准确性**

那个计算公式看着挺科学，但实际用下来发现不准。每只狗的代谢不一样，同样体重的两只狗，食量可能差挺多。

我现在给的方案是：公式算出来一个基准，然后让用户根据实际情况微调。比如说年糕，按公式该吃 180g，但实际喂 150g 刚好，多了就软便。

**坑3：移动端适配**

这个真的是我最头疼的。我以为用响应式设计就能搞定，结果发现宠物主人（包括我）大部分操作都是在手机上完成的，而且经常是单手操作。

后来重写了一遍移动端交互，把主要功能都做成大按钮，单手能够到。但说实话，体验还是不如原生 App。

## 优缺点分析（实事求是）

用了几个月，客观说说优缺点。

**优点：**

1. **提醒功能确实有用** —— 至少我再也没忘过驱虫时间了
2. **数据可视化还行** —— 体重变化曲线能看出来趋势
3. **架构简单好维护** —— 没什么复杂的依赖，自己部署也容易

**缺点：**

1. **AI 识别功能鸡肋** —— 如前面所说，实用性不高
2. **数据录入麻烦** —— 很多数据要手动输入，不能自动同步
3. **多宠物管理体验一般** —— 如果你养了三只猫，界面会有点乱
4. **没有社交功能** —— 本来想加"宠物圈子"之类的，但一直没做

**适用场景：**

- **适合**：养 1-2 只宠物、想要简单记录的主人
- **不适合**：宠物店/医院（需要专业软件）、养很多只宠物的人、想要自动化设备集成的用户

## 代码示例

如果你也想做类似的东西，核心逻辑其实挺简单：

```python
from datetime import datetime, timedelta
from typing import Optional

class PetHealthTracker:
    """宠物健康追踪核心类"""
    
    def __init__(self, pet_profile: PetProfile):
        self.pet = pet_profile
        self.records: List[HealthRecord] = []
    
    def add_vaccine_record(self, vaccine_type: str, 
                          date: datetime, 
                          next_due_months: int = 12):
        """添加疫苗记录"""
        record = VaccineRecord(
            type=vaccine_type,
            date=date,
            next_due=date + timedelta(days=30*next_due_months)
        )
        self.records.append(record)
        return record
    
    def get_upcoming_reminders(self, days: int = 30) -> List[Reminder]:
        """获取未来 N 天的提醒事项"""
        reminders = []
        cutoff = datetime.now() + timedelta(days=days)
        
        for record in self.records:
            if record.next_due <= cutoff:
                reminders.append(Reminder(
                    type="vaccine",
                    due_date=record.next_due,
                    description=f"{self.pet.name} 该打 {record.type} 疫苗了"
                ))
        
        return sorted(reminders, key=lambda r: r.due_date)
    
    def track_weight(self, weight: float, date: Optional[datetime] = None):
        """记录体重"""
        if date is None:
            date = datetime.now()
        
        self.pet.weight_history.append(WeightRecord(
            date=date, weight=weight
        ))
        
        # 检查体重变化是否异常
        if len(self.pet.weight_history) >= 2:
            prev = self.pet.weight_history[-2].weight
            change_pct = abs(weight - prev) / prev * 100
            if change_pct > 10:  # 变化超过 10% 报警
                return f"⚠️ 体重变化较大：{prev:.1f}kg → {weight:.1f}kg"
        
        return "体重记录成功"
```

## 最后说两句

做这个项目的最大收获其实不是技术层面的。说实话，技术都挺常规的，没什么特别创新的东西。

真正的收获是：我发现很多"宠物管理"的问题，其实是我作为主人不够用心。AI 能提醒你打疫苗，但它不能替你观察宠物的精神状态；能算出来该喂多少粮，但它不能判断今天是不是该多带狗出去跑跑。

技术能解决一部分问题，但养宠物这事儿，最终还是要靠人。

反正这个开源了，有兴趣的可以看看。如果你有养宠物，也可以试试用用，有问题随时提 issue。

---

**你们养宠物吗？有没有用过什么宠物管理的 App？体验怎么样？** 欢迎评论区聊聊，或者分享下你养宠物踩过的坑。
