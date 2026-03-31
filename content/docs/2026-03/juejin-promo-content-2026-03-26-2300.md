# 老实说，我做这个语音笔记助手是因为自己记性太差了

说实话，我这人有个毛病——脑子里经常冒出各种想法，但是转眼就忘。

以前我试过用纸笔记录，结果纸找不到了。用过各种笔记App，但是打字太慢，等打开App，灵感已经飞走了。后来我想，要不做个语音笔记助手吧？说句话就能记下来，多方便啊。

然后呢，我就开始动手了。

## 这个项目是干嘛的

简单说，Voice Notes Assistant 就是一个**语音转文字的笔记工具**。但是说实话，如果只是语音转文字，那跟手机自带的备忘录有什么区别呢？

我想解决的问题有几个：

- **快速记录**：按住说话，松手就保存，不超过3秒
- **智能整理**：自动提取关键词、生成摘要
- **多设备同步**：手机录的，电脑上也能看
- **隐私优先**：数据存在本地，不上传到不明服务器

嗯，理想挺美好的，实际做起来...说实话，踩了不少坑，后面会说。

## 技术架构长啥样

整个项目的技术栈其实挺常见的，但我花了不少时间选型。

### 前端
用的是 **Next.js + TypeScript**。为什么选这个呢？老实说，我之前用 React 写过几个项目，但是每次配置路由、状态管理都挺烦的。Next.js 自带了很多东西，省了不少事。

### 语音识别
这部分是最头疼的。一开始我想直接用浏览器的 Web Speech API，免费嘛，谁不喜欢免费的？结果呢，这个API有几个问题：

-  Chrome 支持还行，Firefox 就... 不太行
-  识别准确率，怎么说呢，有点看运气
-  中文支持在某些系统上怪怪的

后来我换成了 **Whisper**，OpenAI 开源的那个。效果好多了，但是需要自己部署，服务器成本就上去了。

### 后端和存储
后端用的 **Python FastAPI**，简单直接。存储方面，我纠结过用 PostgreSQL 还是 SQLite，最后选了 SQLite + 本地文件存储。因为我想让这个工具可以**完全离线运行**，保护隐私嘛。

### 架构图

```
┌─────────────────┐
│   Web App       │  Next.js + TypeScript
│   (Next.js)     │
└────────┬────────┘
         │ WebSocket / HTTP
         ▼
┌─────────────────┐
│   API Server    │  FastAPI + Python
│   (FastAPI)     │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌──────────┐
│Whisper │  │  SQLite  │
│ Engine │  │ Database │
└────────┘  └──────────┘
```

## 核心代码长啥样

分享一下语音识别这块的核心代码吧，可能有人感兴趣：

```python
from fastapi import FastAPI, WebSocket
import whisper
import numpy as np

app = FastAPI()
model = whisper.load_model("base")

@app.websocket("/transcribe")
async def transcribe(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # 接收音频数据
            audio_data = await websocket.receive_bytes()
            
            # 转换为 numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.float32)
            
            # 语音识别
            result = model.transcribe(audio_array, language="zh")
            
            # 返回结果
            await websocket.send_json({
                "text": result["text"],
                "confidence": result.get("confidence", 0)
            })
            
    except Exception as e:
        print(f"转录出错: {e}")
        await websocket.close()
```

这段代码看着简单，但是说实话，上线之后发现了很多问题...

## 踩坑经历（血泪史）

### 坑1：音频格式兼容性

我以为 Web Audio API 录出来的音频直接扔给 Whisper 就行了，结果呢？

不同浏览器录出来的格式不一样，采样率也不一样。Chrome 是 48kHz，Safari 有时候是 44.1kHz。Whisper 要求 16kHz，所以我得自己做重采样。

当时 debug 这个搞了一晚上，人都傻了。

### 坑2：WebSocket 断连问题

因为录音是实时转文字，所以用的 WebSocket。但是移动端浏览器有个特性——**切到后台就断开连接**。

用户录着录着，去回个微信，回来发现断了。这种体验太糟糕了。

我的解决方案是：**录音完成后再发送**。虽然牺牲了一点实时性，但是稳定性好了很多。

### 坑3：Whisper 模型加载慢

Whisper 的 base 模型有几百MB，第一次加载要等好几秒。用户打开App，点录音，然后... 啥反应没有，因为模型还在加载。

我现在的做法是：App 启动时就预加载模型。虽然启动慢了一点，但是录音的时候就不会卡了。

说实话，这个权衡挺难做的。

## 优缺点分析（实事求是）

### 优点

1. **隐私保护做得好**：所有数据本地存储，不需要注册账号
2. **速度快**：本地语音识别，不需要联网等待
3. **开源免费**：代码全开源，可以自己部署

### 缺点

1. **部署门槛高**：需要自己有服务器，对普通用户不友好
2. **识别准确率一般**：Whisper base 模型在某些场景下识别错误率还挺高的
3. **功能相对简单**：没有云同步、团队协作这些高级功能

老实说，这个项目目前更适合**技术玩家**自己折腾，普通用户用起来可能还是有点麻烦。

## 未来的计划

说实话，这个项目我还会继续维护，但是优先级可能没那么高了。现在主要想改进几个地方：

- 支持更多的语音识别模型，让用户自己选
- 加个简单的导出功能（Markdown、PDF）
- 优化移动端体验

也有可能，我会把它改成纯客户端的版本，用 Electron 或者 Tauri，这样部署就简单多了。

## 最后

做这个项目的初衷，其实是为了解决自己的问题。虽然它还不完美，但是至少我现在有个工具，可以快速记录想法了。

如果你也对语音笔记感兴趣，或者想自己搭建一个类似的工具，可以看看我的代码：

👉 **GitHub**: https://github.com/reware-frame/voice-notes-assistant

欢迎提 issue、PR，或者直接找我聊聊。说实话，一个人做开源挺无聊的，有人交流一下会好很多。

---

你们平时用什么工具记录灵感？遇到过什么坑吗？在评论区聊聊呗 👇
