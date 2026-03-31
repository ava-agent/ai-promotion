# 掘金完全自动化运营方案

**目标**: 实现每日自动发布3篇文章，无需人工介入

---

## 🎯 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    掘金自动化运营系统                          │
├─────────────────────────────────────────────────────────────┤
│  定时任务层  │  每天 12:00, 16:00, 20:00 自动触发             │
├──────────────┼──────────────────────────────────────────────┤
│  Cookie管理层 │  自动检查 → 过期预警 → 自动刷新                │
├──────────────┼──────────────────────────────────────────────┤
│  内容生成层  │  项目选择 → AI生成 → 人类化风格                │
├──────────────┼──────────────────────────────────────────────┤
│  发布执行层  │  API调用 → 发布文章 → 记录日志                │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 📦 核心组件

### 1. Cookie 自动管理 (cookie_manager.py)

**功能**:
- ✅ Cookie 有效性检查
- ✅ Cookie 自动刷新
- ✅ Cookie 状态监控
- ✅ 过期预警通知

**使用**:
```bash
# 检查 Cookie 状态
python cookie_manager.py check

# 尝试自动刷新
python cookie_manager.py refresh

# 手动保存新 Cookie
python cookie_manager.py save <sessionid> <sessionid_sig>
```

---

### 2. 浏览器自动获取 (cookie_browser.py)

**功能**:
- ✅ 通过 CDP 获取浏览器 Cookie
- ✅ 自动登录流程
- ✅ Cookie 自动保存

**使用**:
```bash
# 自动刷新（优先使用 CDP）
python cookie_browser.py refresh

# 通过 CDP 获取
python cookie_browser.py cdp

# 手动获取（打开浏览器窗口）
python cookie_browser.py manual
```

---

### 3. 自动发布器 (auto_publisher.py)

**功能**:
- ✅ 定时检查发布时间
- ✅ 自动选择推广项目
- ✅ 自动生成文章内容
- ✅ 自动发布并记录

**使用**:
```bash
# 查看状态
python auto_publisher.py status

# 立即发布一篇
python auto_publisher.py publish

# 默认运行（检查是否到发布时间）
python auto_publisher.py
```

---

## ⚙️ 自动化配置

### 方案 A: 定时任务自动发布（推荐）

修改现有的定时任务，添加 Cookie 检查和自动刷新：

```json
{
  "name": "Juejin Auto Publisher - 12:00",
  "schedule": "0 12 * * *",
  "command": "cd ~/.openclaw/workspace/skills/juejin-publisher && python auto_publish_full.py"
}
```

**auto_publish_full.py** 执行流程：
```python
1. 检查 Cookie 是否有效
2. 如果无效，尝试通过浏览器获取新 Cookie
3. 如果获取成功，保存并继续
4. 如果获取失败，发送通知给用户
5. 选择推广项目
6. 生成文章内容
7. 发布到掘金
8. 记录日志
```

---

### 方案 B: Cookie 预刷新机制

在每天首次发布前，先刷新 Cookie：

```json
{
  "name": "Juejin Cookie Refresh",
  "schedule": "30 11 * * *",
  "command": "cd ~/.openclaw/workspace/skills/juejin-publisher && python cookie_browser.py refresh"
}
```

---

### 方案 C: 失败自动重试

发布失败时自动尝试刷新 Cookie 并重试：

```python
# 伪代码
for attempt in range(3):
    success = publish_article()
    if success:
        break
    else:
        # 尝试刷新 Cookie
        refresh_cookie()
```

---

## 🔧 实施步骤

### 步骤 1: 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 步骤 2: 配置 Chrome 远程调试

创建 Chrome 快捷方式，添加参数：
```
--remote-debugging-port=18800
--user-data-dir=C:\ChromeDebug
```

### 步骤 3: 首次手动获取 Cookie

```bash
python cookie_browser.py manual
```

### 步骤 4: 测试自动发布

```bash
python auto_publisher.py publish
```

### 步骤 5: 配置定时任务

添加以下定时任务：

| 时间 | 任务 | 说明 |
|------|------|------|
| 11:30 | Cookie 预刷新 | 确保发布前 Cookie 有效 |
| 12:00 | 发布第1篇 | 自动发布 |
| 16:00 | 发布第2篇 | 自动发布 |
| 20:00 | 发布第3篇 | 自动发布 |
| 22:00 | 内容优化分析 | 更新策略 |

---

## 🛡️ 可靠性保障

### 1. 多重检查机制

- **Cookie 检查**: 每次发布前验证
- **内容质量检查**: AI 生成后人工风格审核
- **发布结果检查**: 确认文章ID和URL

### 2. 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| Cookie 过期 | 自动尝试刷新，失败则通知 |
| API 限流 | 指数退避重试 |
| 内容生成失败 | 使用备用模板 |
| 发布失败 | 记录日志，跳过本次 |

### 3. 监控告警

```python
# 关键指标监控
- Cookie 有效期监控
- 发布成功率监控
- 文章互动数据监控

# 告警触发
- Cookie 即将过期（提前12小时）
- 连续发布失败（3次）
- 日发布量不足（<3篇）
```

---

## 🚀 当前状态与下一步

### 已完成 ✅

- [x] Cookie 管理器 (cookie_manager.py)
- [x] 浏览器自动获取 (cookie_browser.py)
- [x] 自动发布器框架 (auto_publisher.py)

### 待完成 ⏳

- [ ] 完善内容生成AI调用
- [ ] 集成到定时任务系统
- [ ] 添加监控告警功能
- [ ] 测试完整流程

### 需要主人决策

1. **是否允许自动获取浏览器 Cookie？**
   - 需要 Chrome 开启远程调试
   - 需要信任自动化脚本

2. **是否存储掘金账号密码？**（不推荐）
   - 可以自动登录
   - 有安全风险

3. **失败时的通知方式？**
   - Telegram 通知
   - 邮件通知
   - 仅在日志中记录

---

## 💡 推荐方案

**混合方案**（平衡自动化和安全性）：

```
1. Chrome 保持登录状态（远程调试端口开启）
2. 每天发布前自动从浏览器获取最新 Cookie
3. 如果获取失败，发送 Telegram 通知
4. 主人手动修复后，系统自动继续
```

**优点**:
- ✅ 无需存储账号密码
- ✅ Cookie 自动刷新
- ✅ 人工兜底保障

---

## 📞 使用说明

### 立即测试

```bash
# 1. 检查当前状态
python auto_publisher.py status

# 2. 测试 Cookie 自动获取
python cookie_browser.py refresh

# 3. 手动发布一篇测试
python auto_publisher.py publish
```

### 日常维护

```bash
# 检查 Cookie 有效期
python cookie_manager.py check

# 手动刷新 Cookie
python cookie_browser.py cdp
```

---

**下一步**: 请主人确认方案，我将完成最后的集成和测试！🐕
