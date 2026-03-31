# CSDN 全自动发布系统

## 系统概述

实现了从 Markdown 文件到 CSDN 的**全自动文章发布**，无需人工干预。

## 核心功能

### 1. 自动内容注入
- 通过 Playwright 控制浏览器
- 直接操作 CSDN 编辑器的 contenteditable 元素
- 自动填写标题、注入完整文章内容
- 支持 Markdown 格式保留

### 2. 定时发布
- 每天 12:00, 16:00, 20:00 自动检查
- 每次发布前截图确认
- 自动记录发布日志
- 支持发布队列管理

### 3. 内容管理
- 文章存放目录：`D:/project/ai-promotion/content/csdn/`
- 自动读取 Markdown 文件
- 自动提取标题（第一行）
- 支持批量文章队列

## 文件结构

```
workspace/
├── csdn_auto_publisher.py      # 核心发布脚本
├── csdn_publish_cron.py        # 定时任务脚本
├── memory/
│   ├── csdn-publish-log.md     # 发布日志
│   └── csdn-publish-state.json # 发布状态
└── temp_csdn_article.md        # 示例文章

D:/project/ai-promotion/content/csdn/  # 文章存放目录
```

## 使用方法

### 方式1：命令行直接发布

```bash
# 发布默认文章
python C:/Users/PC/.openclaw/workspace/csdn_auto_publisher.py

# 发布指定文章
python C:/Users/PC/.openclaw/workspace/csdn_auto_publisher.py "path/to/article.md"
```

### 方式2：定时任务自动发布

定时任务已创建：
- **Job ID**: `e55ee694-036d-4261-b03d-34020949adbe`
- **执行时间**: 每天 12:00, 16:00, 20:00
- **时区**: Asia/Shanghai

查看任务状态：
```bash
openclaw cron list
```

手动触发任务：
```bash
openclaw cron run e55ee694-036d-4261-b03d-34020949adbe
```

### 方式3：手动添加文章到队列

1. 将 Markdown 文件放入 `D:/project/ai-promotion/content/csdn/`
2. 等待定时任务执行
3. 或手动运行 `python csdn_publish_cron.py`

## 发布流程

```
1. 检查发布时间
   ↓
2. 读取待发布文章
   ↓
3. 连接浏览器 (CDP)
   ↓
4. 自动填写标题
   ↓
5. 注入文章内容
   ↓
6. 验证内容完整性
   ↓
7. 截图保存
   ↓
8. 等待人工确认（或自动发布）
   ↓
9. 记录发布日志
```

## 技术突破

### 难题解决

**问题**: CSDN 编辑器的内容注入困难
- CodeMirror 6 定制化程度高
- 普通自动化方法无法操作
- 编码问题导致内容损坏

**解决方案**:
1. 通过浏览器 DevTools 分析发现实际使用的是 `contenteditable` 编辑器
2. 使用 Playwright 的 `page.evaluate()` 直接操作 DOM
3. 逐行插入内容，保留换行符
4. 触发 input/change 事件让编辑器识别变化

### 关键技术点

```javascript
// 找到编辑器元素
const editor = document.querySelector('.editor__inner.markdown-highlighting');

// 清空并逐行插入
editor.innerHTML = '';
lines.forEach(line => {
    const div = document.createElement('div');
    div.textContent = line || ' ';
    editor.appendChild(div);
});

// 触发事件
editor.dispatchEvent(new Event('input', { bubbles: true }));
```

## 配置参数

### 发布时间表
```python
PUBLISH_SCHEDULE = ["12:00", "16:00", "20:00"]  # 每天3次
```

### 内容目录
```python
CONTENT_DIR = Path("D:/project/ai-promotion/content/csdn")
```

### 浏览器端口
```python
browser_port = 18800  # Chrome DevTools Protocol
```

## 日志查看

### 发布日志
```bash
# 查看最新发布记录
cat C:/Users/PC/.openclaw/workspace/memory/csdn-publish-log.md
```

### 发布状态
```bash
# 查看JSON状态文件
cat C:/Users/PC/.openclaw/workspace/memory/csdn-publish-state.json
```

示例状态：
```json
{
  "last_publish": "2026-03-25 12:30:00",
  "published_today": 1,
  "total_published": 10,
  "queue": []
}
```

## 注意事项

1. **浏览器必须保持运行**: CSDN 发布需要已登录的浏览器会话
2. **首次使用需登录**: 确保浏览器已登录 CSDN 账号
3. **发布前截图**: 每次发布前会截图保存，便于检查
4. **人工确认**: 默认需要人工确认后才点击发布按钮

## 故障排除

### 问题1: 无法连接到浏览器
**解决**: 确保浏览器已启动并保持运行
```bash
openclaw browser start
```

### 问题2: 内容注入失败
**解决**: 检查 CSDN 页面是否已完全加载
- 脚本会自动等待编辑器加载（10秒超时）
- 如失败会重试

### 问题3: 发布按钮点击失败
**解决**: CSDN 界面可能已更新
- 检查选择器是否正确
- 查看截图确认界面状态

## 扩展计划

- [ ] 支持自动标签选择
- [ ] 支持文章分类选择
- [ ] 支持定时预约发布
- [ ] 支持多账号切换
- [ ] 支持发布结果通知（Telegram/邮件）

## 总结

CSDN 全自动发布系统已实现：

- ✅ 全自动内容注入（无需人工复制粘贴）
- ✅ 定时任务调度（每天3次自动发布）
- ✅ 发布日志记录（Markdown格式）
- ✅ 截图验证（发布前检查）
- ✅ 队列管理（支持多篇文章）

**状态**: 系统已上线运行 🎉
