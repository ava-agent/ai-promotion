# X 平台实施步骤指南

## 🎯 目标
使用 Free API 级别在 X 平台发布第一条测试推文

---

## 📋 实施步骤

### Step 1: 申请 X Developer 账号 (5分钟)

1. **访问开发者门户**
   - 打开: https://developer.x.com
   - 点击 "Sign up" 或 "Login"

2. **登录 X 账号**
   - 使用现有 X 账号: @kevinten1024
   - 输入密码登录

3. **申请开发者权限**
   - 填写申请表格:
     - **Use case**: "I want to share my open-source projects and technical insights automatically"
     - **Description**: "I'm a software architect building AI tools and cloud-native projects. I want to share updates about my work on GitHub."
     - **Country**: China
     - **Developer category**: Hobbyist/Personal

4. **等待审核**
   - 通常即时批准（Free 级别）
   - 或几分钟到几小时

---

### Step 2: 创建 App 获取 API Keys (5分钟)

1. **进入 Developer Portal**
   - 登录后访问: https://developer.x.com/en/portal/dashboard

2. **创建新 App**
   - 点击 "Create App"
   - **App name**: "OpenClawAutoPost"
   - **Description**: "Auto-posting tool for my open-source projects"

3. **获取 Keys**
   - 在 App 设置页面找到 "Keys and Tokens"
   - 复制 **Bearer Token**
   - ⚠️ **重要**: 立即保存，只显示一次！

4. **设置权限**
   - 确保有 "Read and Write" 权限
   - Free 级别自动有发帖权限

---

### Step 3: 配置本地环境 (2分钟)

**方法 A: 环境变量（推荐）**

```bash
# Windows PowerShell
$env:X_BEARER_TOKEN="your_bearer_token_here"

# 或添加到系统环境变量
[Environment]::SetEnvironmentVariable("X_BEARER_TOKEN", "your_token", "User")
```

**方法 B: .env 文件**

创建 `~/.openclaw/workspace/skills/x-poster/.env`:
```
X_BEARER_TOKEN=your_bearer_token_here
```

---

### Step 4: 测试 API 连接 (1分钟)

```bash
# 运行测试脚本
python ~/.openclaw/workspace/test_x_api.py
```

**期望输出**:
```
============================================================
🐕 X API 测试脚本
============================================================
时间: 2026-03-25 12:20:00

[1/3] 测试 API 连接...
  状态: success
  消息: API connection successful
  用户名: kevinten1024

[2/3] 获取 API 限额...
  状态: success
  限额: 100
  剩余: 100

[3/3] 测试发布推文...
  ⚠️  此测试会实际发布推文
  是否继续? (yes/no):
```

---

### Step 5: 生成并发布第一条推文 (2分钟)

```bash
# 运行发帖脚本
python ~/.openclaw/workspace/skills/x-poster/x_poster.py
```

**交互流程**:
```
============================================================
🐕 X 平台自动发帖
============================================================

📊 API 限额:
  发帖: 0/100 (剩余 100)
  读取: 0/500 (剩余 500)

📝 生成推文内容...

生成内容:
Just shipped realm-native context handling in OpenOctopus! 🚀

It's not about the tech, it's about the problem you're solving

github.com/open-octopus/openoctopus

长度: 142 字符

确认发布? (yes/no): yes

✅ 发布成功!
  推文ID: 1234567890
  链接: https://x.com/kevinten1024/status/1234567890
```

---

### Step 6: 验证结果

1. **打开推文链接**
   - 在浏览器中访问发布的链接
   - 确认推文显示正常

2. **检查时间线**
   - 访问: https://x.com/kevinten1024
   - 确认推文出现在时间线上

3. **截图保存**
   - 保存首次发帖成功的截图
   - 记录推文 ID

---

## 🎉 完成！下一步

### 立即可以做
- [ ] 观察首次发帖效果（互动、浏览）
- [ ] 调整内容风格
- [ ] 设置定时任务（如需）

### 本周计划
- [ ] 发布 5-10 条测试推文
- [ ] 找到最佳发布时间
- [ ] 确定受欢迎的内容类型

### 本月目标
- [ ] 用完 Free 级别 100 条限额
- [ ] 评估效果决定是否升级 Basic

---

## ⚠️ 注意事项

### Free 级别限制
- **100 posts/月** ≈ 3 条/天
- **500 reads/月** ≈ 16 次/天
- 超出后需等待下月或升级

### 内容质量
- 宁可少发，也要高质量
- 每次发帖都要有价值
- 避免刷屏

### 安全
- 不要分享 Bearer Token
- 不要在代码中硬编码 Token
- 定期检查 Token 是否泄露

---

## 🆘 常见问题

### Q: Developer 申请被拒绝？
**A**: 重新申请，描述更详细：
- 具体项目名称
- GitHub 链接
- 使用场景说明

### Q: 无法获取 Write 权限？
**A**: Free 级别默认有写权限，检查：
- App 设置中的权限
- 是否完成手机号验证

### Q: API 返回 401？
**A**: Token 无效，检查：
- Token 是否复制完整
- 是否有多余空格
- 是否已过期（重新生成）

### Q: 发布失败 403？
**A**: 权限不足，检查：
- App 是否有 Read+Write 权限
- 账号是否被限制

---

## 📞 需要帮助？

- **X Developer 文档**: https://developer.x.com/en/docs/x-api
- **开发者论坛**: https://devcommunity.x.com
- **GitHub 示例**: https://github.com/xdevplatform

---

**预计总时间**: 15-20 分钟
**难度**: ⭐⭐ (简单)
**成功率**: 95%+

开始实施吧！🐕🚀
