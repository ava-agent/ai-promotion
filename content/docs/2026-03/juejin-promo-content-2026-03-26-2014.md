# 用 MCP 协议封装 AI 视频生成，我踩了这些坑

说实话，一开始我觉得这事儿挺简单的。不就是封装个 API 吗？结果真搞起来才发现，MCP 协议虽然设计得挺优雅，但魔鬼藏在细节里。

## 先说说背景

最近做了个 AI 视频生成的小工具 [mcp-video-gen](https://github.com/kevinten-ai/mcp-video-gen)。初衷很简单：让 Claude 这样的 AI 助手能直接调用视频生成功能，不用手动复制粘贴 prompt 到各个平台。

GitHub 地址：https://github.com/kevinten-ai/mcp-video-gen

用了 MCP（Model Context Protocol）协议来做这件事。如果你还没听说过 MCP，简单说它就是 AI 和外部工具之间的"通用语言"，类似于 USB 接口之于电脑外设。

## 架构设计

整个系统分成三层：

**MCP 协议层**：处理请求解析、参数校验、响应封装
**服务编排层**：根据模型选择调用不同的视频生成服务
**外部 API 层**：实际对接各个视频生成平台的接口

```python
# 核心架构示意
class VideoGenServer:
    def __init__(self):
        self.providers = {
            "luma": LumaProvider(),
            "runway": RunwayProvider(),
            "pika": PikaProvider()
        }
    
    async def generate(self, prompt: str, provider: str, **kwargs):
        # 参数校验
        validated = self.validate_params(prompt, kwargs)
        
        # 调用对应 provider
        result = await self.providers[provider].generate(
            prompt, **validated
        )
        
        # 统一响应格式
        return self.format_response(result)
```

看起来挺清晰对吧？但实现起来有不少坑。

## 踩坑实录

### 坑 1：MCP 的"优雅"协议格式

MCP 协议要求请求和响应都遵循特定的 JSON-RPC 格式。刚开始我以为就是普通的 REST API，结果发现根本不是一回事。

```json
// 我以为的请求格式
{
  "prompt": "一只猫在跳舞",
  "model": "luma"
}

// 实际的 MCP 请求格式
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "generate_video",
    "arguments": {
      "prompt": "一只猫在跳舞",
      "provider": "luma"
    }
  },
  "id": 1
}
```

这个多层嵌套的结构让我一开始调试的时候头疼了好几天。特别是 `tools/call` 这个 method 名，文档里写得不太明显，害我翻了好几遍源码才搞明白。

### 坑 2：异步等待的坑

视频生成是个耗时操作，短则几十秒，长则几分钟。MCP 协议本身不支持长轮询，所以我得设计一个"提交任务 → 轮询状态 → 返回结果"的流程。

```python
async def generate_video(self, prompt: str, provider: str):
    # 提交任务
    task_id = await self.submit_task(prompt, provider)
    
    # 轮询等待
    max_wait = 300  # 最多等5分钟
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        status = await self.check_status(task_id)
        if status == "completed":
            return await self.get_result(task_id)
        elif status == "failed":
            raise GenerationError("生成失败")
        
        await asyncio.sleep(5)  # 每5秒检查一次
    
    raise TimeoutError("生成超时")
```

问题出在哪呢？不同 provider 的状态机不一样。有的用 `pending/processing/completed`，有的用 `queued/running/success`。我得为每个 provider 写适配器来统一状态。

### 坑 3：错误处理的复杂性

视频生成失败的原因五花八门：

- prompt 违反内容政策
- 账户余额不足
- 服务器繁忙
- 网络超时
- 视频格式不支持

一开始我只做了简单的 try-except，结果用户看到的错误信息云山雾罩的。后来改成了分级错误处理：

```python
try:
    result = await provider.generate(prompt)
except ContentPolicyError as e:
    # 明确的政策违规提示
    return {"error": f"Prompt违反内容政策: {e.message}"}
except InsufficientBalanceError:
    # 余额不足
    return {"error": "账户余额不足，请充值"}
except ProviderError as e:
    # 提供商内部错误
    return {"error": f"{provider.name}服务暂时不可用，请稍后重试"}
except Exception as e:
    # 兜底
    logger.error(f"未知错误: {e}")
    return {"error": "生成失败，请稍后重试"}
```

这样用户至少能知道是哪里出了问题，而不是一脸懵。

### 坑 4：资源清理

视频生成会产生临时文件。一开始我没注意清理，跑了几天服务器磁盘就满了。后来加了自动清理机制：

```python
async def cleanup_temp_files(self, max_age_hours=24):
    """清理超过24小时的临时文件"""
    temp_dir = Path("./temp")
    cutoff = time.time() - (max_age_hours * 3600)
    
    for file in temp_dir.glob("*"):
        if file.stat().st_mtime < cutoff:
            file.unlink()
            logger.info(f"清理过期文件: {file}")
```

这个在 MCP 协议文档里当然没提，但生产环境必须得做。

## 实现难点

### 1. 多 Provider 的统一抽象

每个视频生成平台的 API 设计都不一样：

| 平台 | 认证方式 | 异步模式 | 返回格式 |
|------|----------|----------|----------|
| Luma | API Key | Webhook | JSON |
| Runway | OAuth | 轮询 | JSON |
| Pika | API Key | 轮询 | JSON |

为了让上层调用者不用关心这些差异，我设计了一个统一的 Provider 接口：

```python
from abc import ABC, abstractmethod

class VideoProvider(ABC):
    @abstractmethod
    async def authenticate(self) -> str:
        """返回认证令牌"""
        pass
    
    @abstractmethod
    async def generate(self, prompt: str, **options) -> str:
        """返回任务ID"""
        pass
    
    @abstractmethod
    async def check_status(self, task_id: str) -> str:
        """返回状态: pending/processing/completed/failed"""
        pass
    
    @abstractmethod
    async def get_result(self, task_id: str) -> dict:
        """返回视频URL和元数据"""
        pass
```

每个具体 provider 实现这个接口，上层代码就可以无感知切换了。

### 2. 流式状态反馈

用户肯定不想干等着。我加了一个 SSE（Server-Sent Events）端点，让前端能实时看到生成进度：

```python
async def status_stream(task_id: str):
    while True:
        status = await check_status(task_id)
        yield f"data: {json.dumps({'status': status})}\n\n"
        
        if status in ["completed", "failed"]:
            break
        
        await asyncio.sleep(2)
```

这个虽然不是 MCP 协议的一部分，但对用户体验提升很大。

### 3. Prompt 优化

不同平台对 prompt 的解析逻辑不同。同样的描述在 Luma 上效果可能很好，在 Runway 上就一般。我加了一个简单的 prompt 优化器：

```python
def optimize_prompt(prompt: str, provider: str) -> str:
    """针对不同平台优化 prompt"""
    optimizations = {
        "luma": lambda p: f"Cinematic shot. {p}. High quality, 4K.",
        "runway": lambda p: p,  # Runway 对原生 prompt 支持更好
        "pika": lambda p: f"{p}. Professional video, smooth motion."
    }
    
    return optimizations.get(provider, lambda p: p)(prompt)
```

简单但有效。

## 优缺点分析

**优点**：

- 统一接口确实方便，Claude 调用起来很顺畅
- MCP 协议的生态正在壮大，未来兼容性好
- 架构灵活，加新 provider 比较容易

**缺点**：

- MCP 协议还在演进，文档不够完善
- 调试起来比较麻烦，错误信息有时候很晦涩
- 异步状态管理比想象中复杂
- 视频生成成本不低，需要自己控制调用频率

**适合场景**：

- 需要集成多个 AI 视频生成平台
- 已经有基于 MCP 的 AI 助手架构
- 愿意花时间调试协议细节

**不适合场景**：

- 只想快速生成几个视频（直接用平台更简单）
- 对稳定性要求极高的生产环境
- 没有技术能力处理协议细节

## 代码示例

最简单的使用方式：

```python
from mcp_video_gen import VideoGenClient

client = VideoGenClient(provider="luma")

# 生成视频
result = await client.generate(
    prompt="一只柴犬在海边奔跑",
    duration=5,  # 秒
    resolution="720p"
)

print(f"视频地址: {result['video_url']}")
```

配合 Claude 使用：

```
用户：帮我生成一个猫咪跳舞的视频

Claude：我来帮你生成这个视频。
[调用 mcp-video-gen.generate_video]

生成完成！视频地址：https://...
```

## 总结

说实话，这个项目比我预期的复杂。MCP 协议的设计理念很好，但实际落地时还是有不少坑要踩。不过一旦跑通了，扩展性确实不错。

如果你也在做类似的 MCP 封装，我的建议是：

1. 先仔细阅读官方示例代码，光看文档容易漏细节
2. 错误处理一定要做充分，视频生成的不确定性很高
3. 异步状态机设计要仔细，不同 provider 差异很大
4. 记得做资源清理，临时文件会累积得很快

有同样在研究 MCP 协议的朋友吗？欢迎交流经验，特别是那些文档里没写的坑 😂
