# 🚨 系统警报

**更新时间**: 2026-04-06 16:25 (Asia/Shanghai)

---

## 🔴 严重问题（需要主人处理）

### 1. Chrome CDP 无法连接
- **时间**: 2026-04-06 16:39 (更新)
- **影响平台**: CSDN、Medium
- **症状**: browser 工具无法连接到 Chrome
- **错误**: `Could not find DevToolsActivePort for chrome`
- **尝试次数**: 2 次（16:25, 16:39）
- **需要操作**: 
  1. ⚠️ **Chrome 可能未运行或 CDP 端口未开启**
  2. 用 PowerShell 命令启动 Chrome 并开启 CDP：
     ```powershell
     # 关闭所有 Chrome 进程
     taskkill /F /IM chrome.exe
     
     # 启动 Chrome 并开启 CDP（端口 9222）
     & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
     
     # 等待 Chrome 启动后，登录 CSDN 和 Medium
     ```
  3. 或者手动发布 CSDN 文章（见下方操作指引）

### 2. CSDN 待发布文章堆积
- **时间**: 2026-04-06
- **状态**: 3 篇文章待发布
- **文件列表**:
  - `csdn_drafts/pending/2026-04-03_20-00-Fish-Agent.md` ⭐ 优先发布
  - `csdn_drafts/pending/2026-04-03_12-00-Capa-BFF.md`
  - `csdn_drafts/pending/2026-04-02_20-00-Capa-Java.md`
- **阻塞原因**: Chrome CDP 无法连接

---

## 🟡 重要异常（自动修复中）

### 暂无

---

## 🟢 已解决

### 暂无

---

## 📝 待办事项

- [ ] 主人启动 Chrome 并开启 CDP（端口 9222）
- [ ] 确认 Chrome 已登录 CSDN 和 Medium
- [ ] heartbeat 检查时自动发布 CSDN 文章

---

*此文件由旺财自动维护 🐕*
