# 微信公众号发布经验总结

## 2026-03-25 首次发布成功

### 技术突破

#### 1. MCP 直接使用 SDK 调用
**问题**: mcporter CLI 无法正确传递文件内容和图片
**解决**: 直接使用 MCP SDK 的 Client 连接

**成功代码模式**:
```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const transport = new StdioClientTransport({
  command: 'node',
  args: ['path/to/wenyan-mcp-server/dist/index.js'],
  env: {
    WECHAT_APP_ID: 'xxx',
    WECHAT_APP_SECRET: 'xxx'
  }
});

const client = new Client({ name: 'wenyan-client', version: '1.0.0' });
await client.connect(transport);

const result = await client.callTool({
  name: 'publish_article',
  arguments: {
    content: articleContent,  // 直接传递字符串
    theme_id: 'orangeheart'
  }
});
```

**关键点**:
- 直接传递内容字符串，而不是文件路径
- 图片通过 frontmatter 和正文中的 markdown 图片语法嵌入
- 使用 node 直接运行，通过 npx mcporter 有转义问题

---

#### 2. 文章格式要求

**必须包含 Frontmatter**:
```markdown
---
title: 文章标题
cover: https://example.com/cover.jpg  # 或本地路径
---

# 文章标题
...
```

**必须包含图片**:
- 封面图（cover）
- 或正文中至少一张图片
- 支持在线图片 URL 或本地路径

---

### 内容质量经验

#### 高流量内容特征（初步观察）

**1. 标题技巧**
- 口语化："我踩了这些坑"、"说实话"
- 反直觉："AI 不是万能的"
- 个人经历："三个月才做出来"
- 避免：模板化、纯数字堆砌

**2. 内容结构**
- 开头：Hook 故事（个人真实经历）
- 中间：技术深度 + 踩坑实录
- 结尾：互动提问

**3. 技术深度**
- 架构说明
- 代码示例
- 实现难点
- 解决方案

**4. 实事求是**
- 讲优点也讲缺点
- 适用场景说明
- 不夸大宣传

---

### 发布流程优化

#### 推荐流程
```
1. 选题（项目推广/技术分享/经验总结）
2. 创作（使用高质量模板）
3. 添加封面图（Unsplash 或本地）
4. 本地预览（wenyan render）
5. MCP 发布（使用 SDK）
6. 后台检查草稿
7. 定时群发
```

#### 主题选择
- **orangeheart**: 橙心主题，温暖亲切
- **default**: 简洁经典
- **rainbow**: 彩虹主题，活泼
- 根据内容情感选择

---

### 待优化方向

1. **封面图自动化**
   - 使用 AI 生成封面图
   - 或从 Unsplash 自动匹配

2. **内容选题研究**
   - 研究高阅读量的公众号文章
   - 分析流量密码
   - 建立选题库

3. **发布时间优化**
   - 测试不同时段的阅读量
   - 找到最佳发布时间

4. **互动提升**
   - 结尾引导评论
   - 及时回复读者

---

### 与其他平台对比

| 平台 | 链接政策 | 内容风格 | 技术深度 |
|------|----------|----------|----------|
| 微信公众号 | ✅ 允许 | 深度长文 | 高 |
| CSDN | ✅ 允许 | 技术分享 | 高 |
| 掘金 | ✅ 允许 | 技术干货 | 高 |
| Dev.to | ✅ 鼓励 | 英文技术 | 高 |
| 知乎 | ⚠️ 谨慎 | 问答形式 | 中 |
| Moltbook | ❌ 禁止 | 社区分享 | 中 |

**策略**: 微信公众号适合深度长文，可以发 2000+ 字的技术文章

---

*最后更新: 2026-03-25*
