# 开发宠物AI助手时，我被这些坑整崩溃了

说实话，做 Dog Agent 这个项目之前，我以为就是个简单的提醒工具。结果呢？踩的坑比我养猫三年踩的还多。今天不说虚的，就聊聊那些让我半夜睡不着觉的技术难题。

---

## 先说背景

GitHub 地址先放这儿，有兴趣的可以去看看代码：
**https://github.com/kevinten-ai/dog-agent**

网站也部署了：https://pet.rxcloud.group

做这个项目的初衷挺简单的——我自己养猫，总是记不住疫苗时间，猫咪有点异常也分不清是小事还是大事。当时我就想，能不能搞个AI来帮忙管理这些？

听起来不难对吧？**然后我就掉坑里了。**

---

## 坑1：疫苗时间表，比我想象的复杂100倍

最开始我想，疫苗不就是固定的几针吗？第一次打完，第二次间隔几周，打完就行了。

**太天真了。**

实际情况是啥呢？

- 不同的疫苗，间隔时间不一样
- 有些疫苗需要加强针，有些不需要
- 幼猫和成年猫的接种方案完全不同
- 不同品牌的疫苗，建议间隔还有差异
- 如果中间漏了一针，是补打还是重新来？

我当时就懵了。这哪是简单的提醒功能，这是个**规则引擎**啊！

### 我的解决方案

后来我想明白了，不能把疫苗时间表写死在代码里。得做成可配置的：

```python
class VaccineSchedule:
    """疫苗时间表引擎"""
    
    def __init__(self):
        # 不同疫苗类型的基础规则
        self.vaccine_rules = {
            'core_cat': {  # 猫核心疫苗
                'initial_doses': 3,
                'interval_weeks': [0, 4, 4],  # 第一针后4周第二针，再4周三针
                'booster_months': 12,  # 一年后加强
            },
            'rabies': {  # 狂犬疫苗
                'initial_doses': 1,
                'booster_months': 12,
            }
        }
    
    def calculate_schedule(self, vaccine_type, pet_age_months, last_dose_date=None):
        """
        根据宠物年龄和疫苗历史，计算接种计划
        返回: [(疫苗名称, 建议日期, 说明), ...]
        """
        rule = self.vaccine_rules.get(vaccine_type)
        if not rule:
            return []
        
        schedule = []
        
        # 幼猫需要完整的初始接种
        if pet_age_months < 16 and not last_dose_date:
            base_date = datetime.now()
            for i, weeks in enumerate(rule['interval_weeks']):
                dose_date = base_date + timedelta(weeks=sum(rule['interval_weeks'][:i+1]))
                schedule.append({
                    'dose_number': i + 1,
                    'date': dose_date,
                    'note': f'第{i+1}针，{rule["interval_weeks"][i]}周后'
                })
        
        # 成年猫或已完成初始接种的，计算加强针
        elif last_dose_date:
            booster_date = last_dose_date + timedelta(days=rule['booster_months'] * 30)
            schedule.append({
                'dose_number': '加强针',
                'date': booster_date,
                'note': f'距离上次接种{rule["booster_months"]}个月'
            })
        
        return schedule
```

这个方案的好处是，规则可以灵活调整。不同地区、不同医院的建议可能不一样，用户可以自己配置。

**但是**，这又带来了新问题：用户怎么知道该用什么规则？所以我后来又加了默认配置和建议系统。

---

## 坑2：症状分析，AI的判断边界在哪里？

这是让我最头疼的一个功能。

用户输入"我的猫吐了"，AI该怎么回应？

- 如果只是一次性呕吐，可能没事
- 但如果伴随其他症状，可能是重病
- 有些情况需要立刻去医院，有些可以观察

**最麻烦的是，我不能替代兽医。**

如果说得太轻描淡写，宠物出事了怎么办？如果说得太严重，用户会不会过度焦虑？

### 我的解决方案

我设计了一个**三级响应系统**：

```python
class SymptomAnalyzer:
    """症状分析器"""
    
    SEVERITY_LEVELS = {
        'critical': {  # 紧急情况
            'keywords': ['呼吸困难', '昏迷', '抽搐', '大量出血'],
            'response': '请立即联系附近的宠物医院！',
            'action_required': True,
        },
        'warning': {  # 需要注意
            'keywords': ['连续呕吐', '食欲不振', '精神萎靡'],
            'response': '建议尽快就医检查',
            'action_required': True,
        },
        'info': {  # 一般情况
            'keywords': ['偶尔', '一次', '轻微'],
            'response': '可以观察一下，如有变化再联系兽医',
            'action_required': False,
        }
    }
    
    def analyze(self, symptom_description):
        """
        分析症状，返回严重程度和建议
        """
        # 使用关键词匹配 + 语义分析
        severity = self._classify_severity(symptom_description)
        
        response = {
            'severity': severity,
            'message': self.SEVERITY_LEVELS[severity]['response'],
            'disclaimer': '注意：这只是初步判断，不能替代专业兽医诊断',
            'suggested_actions': self._get_actions(symptom_description, severity)
        }
        
        return response
    
    def _classify_severity(self, text):
        # 简化的分类逻辑
        text_lower = text.lower()
        
        for level, config in self.SEVERITY_LEVELS.items():
            for keyword in config['keywords']:
                if keyword in text_lower:
                    return level
        
        return 'info'  # 默认一般情况
```

**但是说实话**，这个方案还是不够完美。

用户描述症状的准确度差异很大。有些人能详细描述，有些人就说"好像不太对"。我后来加了一些引导性问题，帮助用户更准确地描述症状。

---

## 坑3：多宠物管理，数据关联是个噩梦

一开始我只考虑了一只宠物的情况。后来有用户反馈说，他们家有3只猫，怎么管理？

这时候我发现，数据库设计完全没考虑多宠物场景。

### 最初的设计（有问题的）

```python
# 糟糕的设计 - 把宠物信息直接存在用户表里
class User:
    pet_name: str
    pet_birthday: datetime
    pet_type: str  # 猫/狗
```

### 重构后的设计

```python
# 用户和宠物分离
class User:
    id: int
    name: str
    pets: List[Pet]  # 一个用户可以有多个宠物

class Pet:
    id: int
    owner_id: int
    name: str
    birthday: datetime
    pet_type: str
    breed: str  # 品种
    medical_records: List[MedicalRecord]
    vaccination_history: List[VaccinationRecord]

class MedicalRecord:
    pet_id: int
    date: datetime
    symptom: str
    diagnosis: str
    treatment: str
    vet_name: str
```

看起来简单对吧？**但迁移数据的时候我真的心态崩了。**

原有的用户数据需要拆分，疫苗记录需要重新关联到具体的宠物。还好用户量不大，我手动处理了一下。如果用户量很大，这简直是个灾难。

---

## 坑4：时间提醒，考虑不周就会漏掉

提醒功能看起来简单，但细节超多：

- 提醒时间应该根据用户习惯来
- 需要考虑时区（虽然我目前只有国内用户）
- 如果用户当天没打开应用，怎么补提醒？
- 疫苗到期前多久提醒比较合适？

我一开始只做了简单的定时任务，结果发现：

- 有些用户早上看消息，有些晚上看
- 疫苗提前1天提醒和提前1周提醒，效果完全不同
- 如果连续提醒几次用户都没反应，应该停止还是继续？

### 我的方案

```python
class ReminderEngine:
    """提醒引擎"""
    
    REMINDER_RULES = {
        'vaccine': {
            'before_days': [7, 3, 1],  # 提前7天、3天、1天各提醒一次
            'time_of_day': '09:00',    # 早上9点提醒
        },
        'checkup': {
            'before_days': [14, 7],
            'time_of_day': '10:00',
        }
    }
    
    def schedule_reminders(self, event_type, event_date, user_preferences):
        """
        根据事件类型和用户偏好，安排提醒
        """
        rules = self.REMINDER_RULES.get(event_type, {})
        reminders = []
        
        for days_before in rules.get('before_days', []):
            reminder_date = event_date - timedelta(days=days_before)
            reminder_time = rules.get('time_of_day', '09:00')
            
            # 如果用户有自定义偏好，使用用户的设置
            if user_preferences.get('preferred_time'):
                reminder_time = user_preferences['preferred_time']
            
            reminders.append({
                'type': event_type,
                'scheduled_at': f"{reminder_date.date()} {reminder_time}",
                'message': f"距离{event_type}还有{days_before}天"
            })
        
        return reminders
    
    def should_send_reminder(self, reminder, user_last_active):
        """
        判断是否该发送提醒
        """
        # 如果用户很久没活跃，降低提醒频率
        if user_last_active and (datetime.now() - user_last_active).days > 30:
            return False  # 可能已经不使用了
        
        return True
```

---

## 优缺点分析（实话实说）

**优点：**
- 确实解决了我自己养猫的痛点，疫苗不会再忘了
- 症状分析功能帮我在几次紧急情况下快速判断需要去医院
- 多宠物管理对于有多个毛孩子的家庭很实用

**缺点：**
- 症状分析还不够智能，有时候判断会偏保守或激进
- 疫苗规则需要用户自己配置，对新手不够友好
- 界面还比较简陋，移动端体验一般
- 数据库设计一开始没考虑好，导致后期重构很麻烦

**适合：**
- 有宠物的新手主人，需要提醒功能
- 多宠物家庭，需要集中管理
- 愿意花时间配置疫苗规则的用户

**不适合：**
- 希望完全自动化的用户
- 需要专业医疗建议的情况（还是要看兽医）

---

## 最后想说

做这个项目的收获挺大的。一开始我以为是个小工具，结果涉及到的技术点还挺多的——规则引擎、自然语言处理、数据库设计、提醒系统。

**老实说**，现在的版本还有很多可以改进的地方。但至少解决了我自己的需求，也帮助了一些朋友。

如果你也在做类似的项目，或者养宠过程中有什么好的想法，欢迎在评论区聊聊。大家一起交流，避免踩同样的坑！

---

*项目代码开源在 GitHub：https://github.com/kevinten-ai/dog-agent*
*在线体验：https://pet.rxcloud.group*
