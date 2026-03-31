# CSDN 发布经验记录

> 记录 CSDN 自动化发布的成功经验、踩坑记录和最佳实践
> 最后更新: 2026-03-29 23:30

## ✅ 成功的发布记录

| 日期 | 标题 | 项目 | 状态 | 链接 |
|------|------|------|------|------|
| 2026-03-29 23:10 | 折腾多运行时架构半年，说说 Capa-Java 踩过的那些坑 | Capa-Java | ✅ 已发布 | [159618979](https://blog.csdn.net/wsh596823919/article/details/159618979) |
| 2026-03-31 03:51 | 用AI帮老婆做备孕体检攻略，我差点被医生吐槽死 | Health Agent | ✅ 已发布 | [159662987](https://blog.csdn.net/wsh596823919/article/details/159662987) |
| 2026-03-27 13:52 | 修复测试 - CSDN自动发布功能验证 | Fix Test | ✅ 已发布 | [159544480](https://blog.csdn.net/wsh596823919/article/details/159544480) |
| 2026-03-25 12:45 | 用AI规划旅行，我翻车了好几次才搞明白这些坑 | Trip Agent | ✅ 已发布 | [159465504](https://blog.csdn.net/wsh596823919/article/details/159465504) |

## 🎯 核心结论

**CSDN 只能在 main session 中通过 browser 工具发布**

这是经过大量尝试后得出的唯一可行方案。

## 🔬 失败方案记录（吸取教训）

### 方案1: CDP WebSocket 连接（失败）
```python
# 尝试: 用 CDP /json/new 创建新 tab
requests.put('http://localhost:9222/json/new?about:blank')
# 结果: 新 tab 没有 CSDN 登录态，被重定向到登录页
```
**失败原因**: CSDN 依赖 sessionStorage 维持登录态，新 tab 不继承

### 方案2: Playwright + CDP（失败）
```python
browser = p.chromium.connect_over_cdp("http://localhost:9222")
context = browser.contexts[0]  # 空列表！
```
**失败原因**: Playwright 连接 CDP 后看不到已有 tab

### 方案3: websocket-client 连接 CDP（失败）
```python
ws = websocket.create_connection(ws_url)
# 结果: Handshake status 403 Forbidden
```
**失败原因**: Chrome 需要 `--remote-allow-origins` 参数，且新 tab 仍丢登录态

### 方案4: cron isolated session（失败）
```python
# cron isolated session 中尝试使用 browser 工具
browser.navigate(...)
# 结果: 工具不可用
```
**失败原因**: isolated session 没有 browser 工具

## ✅ 成功方案: Browser 工具（main session）

### 完整流程

```python
# Step 1: 导航到编辑器（使用已有登录态的 Chrome）
browser.navigate("https://editor.csdn.net/md")

# Step 2: 填写标题（关键：用 nativeInputValueSetter）
browser.evaluate(fn="""
    const title = "文章标题";
    const input = document.querySelector('input[placeholder*="标题"]');
    const setter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;
    setter.call(input, title);
    input.dispatchEvent(new Event('input', { bubbles: true }));
""")

# Step 3: 注入内容（base64 解码）
content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
browser.evaluate(fn=f"""
    const b64 = '{content_b64}';
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const content = new TextDecoder('utf-8').decode(bytes);
    
    const editor = document.querySelector('.editor__inner.markdown-highlighting');
    editor.focus();
    editor.textContent = content;
    editor.dispatchEvent(new Event('input', { bubbles: true }));
""")

# Step 4: 点击发布
browser.evaluate(fn="""
    for (const btn of document.querySelectorAll('button')) {
        if (btn.textContent.trim() === '发布文章' && btn.offsetParent !== null) {
            btn.click();
        }
    }
""")

# Step 5: 选择原创
browser.evaluate(fn="""
    for (const l of document.querySelectorAll('label')) {
        if (l.textContent.includes('原创')) { l.click(); }
    }
""")

# Step 6: 确认发布（用 browser snapshot 找到 ref 后点击）
browser.click(ref='e66')  # 弹窗中的发布按钮
```

## 🐛 踩坑详解

### 坑1: 标题设置不生效
**症状**: 设置了标题但编辑器显示空白或旧标题
**原因**: 直接 `input.value = title` 不会触发 React 的 onChange
**解决**: 使用 `nativeInputValueSetter` + `dispatchEvent`

### 坑2: 内容注入后格式丢失
**症状**: Markdown 格式没解析，显示为纯文本
**原因**: 用了 `innerHTML` 或没触发 input 事件
**解决**: 用 `textContent` + `dispatchEvent(new Event('input'))`

### 坑3: 中文乱码
**症状**: 内容中的中文显示为乱码
**原因**: base64 解码后没有正确转回 UTF-8
**解决**: `new TextDecoder('utf-8').decode(bytes)`

### 坑4: 内容太长 evaluate 失败
**症状**: 内容超过一定长度后 evaluate 报错
**解决**: 内容分块注入，或确保 base64 编码正确

### 坑5: 发布按钮点击无效
**症状**: 点击发布按钮但弹窗没出现
**原因**: 选到了隐藏的按钮或错误的按钮
**解决**: 检查 `btn.offsetParent !== null` 确保按钮可见

## 🏗️ 架构设计

### 推荐架构
```
cron (isolated session)
  ↓ 生成内容
  ↓ 保存到 csdn_drafts/pending/
  
heartbeat / main session
  ↓ 检查 pending/ 目录
  ↓ 用 browser 工具发布
  ↓ 移动文件到 published/
```

### 为什么这样设计？
1. **cron 生成内容**: isolated session 可以安全地生成内容，不依赖 browser
2. **main session 发布**: 只有 main session 有 browser 工具
3. **解耦**: 内容生成和发布分离，更可靠

## 📁 文件格式

### 草稿文件格式
`csdn_drafts/pending/2026-03-29_20-Capa-Java.md`:

```markdown
---
title: 折腾多运行时架构半年，说说 Capa-Java 踩过的那些坑
tags: Java,分布式,架构设计,Dapr,云原生
project: Capa-Java
date: 2026-03-29
---

## 先说背景

我在做分布式系统的时候...
```

### 目录结构
```
csdn_drafts/
├── pending/        # 待发布草稿
├── published/      # 已发布文章备份
└── archive/        # 历史草稿
```

## 📝 内容策略

### 高流量内容类型（已验证）
1. **踩坑实录** - 真实踩坑经历 + 解决方案
2. **架构分享** - 技术选型思考 + 架构图
3. **工具实测** - 实际使用感受 + 优缺点

### 标题模板（效果好）
- "折腾 XX 半年，说说 XX 踩过的那些坑"
- "用了 XX 三个月，我的真实感受"
- "踩了个大坑：XX"

### 反 AI 检测（必须）
- ✅ 口语化表达 ≥ 5 处
- ✅ 个人经历
- ✅ 情感表达
- ✅ 不完美结构
- ❌ 避免精确数字（"847天"）
- ❌ 避免对称结构（"5个教训"）

## ⚙️ 技术细节

### 编辑器 DOM
```html
<!-- 标题 -->
<input placeholder="请输入文章标题（5~100个字）" ... />

<!-- 编辑器 -->
<pre class="editor__inner markdown-highlighting" contenteditable="true">
</pre>
```

**关键**: 编辑器是 `contenteditable PRE`，不是 CodeMirror！

### Base64 编码/解码
```python
# Python 编码
content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')

# JavaScript 解码
const binary = atob(b64);
const bytes = new Uint8Array(binary.length);
for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
const content = new TextDecoder('utf-8').decode(bytes);
```

## 🚀 快速参考

### 发布一篇文章（手动）
```python
# 在 main session 中执行
import subprocess
result = subprocess.run([
    'python', 'csdn_publish_from_file.py',
    '--file', 'csdn_drafts/pending/2026-03-29_20-Capa-Java.md'
], capture_output=True, text=True)
print(result.stdout)
```

### Heartbeat 检查代码
```python
from pathlib import Path

pending_dir = Path('csdn_drafts/pending')
files = list(pending_dir.glob('*.md'))

if files:
    # 取最早的一个
    file = min(files, key=lambda f: f.stat().st_mtime)
    # 读取 front matter
    content = file.read_text(encoding='utf-8')
    # 用 browser 工具发布
    # ...
    # 移动到 published/
    file.rename(f'csdn_drafts/published/{file.name}')
```

## 📚 相关文件

| 文件 | 用途 |
|------|------|
| `skills/csdn-publisher/SKILL.md` | 完整技能文档 |
| `memory/csdn-publish-log.md` | 发布记录 |
| `memory/HEARTBEAT.md` | 检查项 |
| `csdn_drafts/pending/` | 待发布草稿 |
| `csdn_auto_publisher.py` | 旧版脚本（已弃用） |
| `csdn_cdp_publish.py` | CDP 脚本（已弃用） |
| `csdn_quick_publish.py` | 快速测试脚本 |

## 💡 经验总结

### 什么有效
1. ✅ browser navigate 到已有登录态页面
2. ✅ nativeInputValueSetter 设置标题
3. ✅ base64 + TextDecoder 处理中文内容
4. ✅ textContent + dispatchEvent 注入编辑器
5. ✅ evaluate + click 组合操作

### 什么无效
1. ❌ CDP 新建 tab（丢登录态）
2. ❌ Playwright 连接 CDP（看不到已有 tab）
3. ❌ websocket-client 绕过（复杂且丢登录态）
4. ❌ cron isolated session（无 browser 工具）
5. ❌ 直接 .value = 赋值（不触发 React 更新）

### 关键洞察
- **CSDN 编辑器**: 基于 contenteditable 的 Markdown 编辑器，不是 CodeMirror
- **登录态**: 依赖 sessionStorage，新 tab 不继承
- **React 表单**: 需要 native setter + dispatchEvent 才能正确更新
- **中文**: 必须用 TextDecoder UTF-8 解码 base64

## 🔮 未来优化

- [ ] 自动标签选择
- [ ] 封面图片上传
- [ ] 分类专栏自动选择
- [ ] 批量发布支持
- [ ] 发布失败重试机制

---

*记录者: 旺财 🐕*
*记录时间: 2026-03-29 23:30*
