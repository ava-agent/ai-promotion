# CSDN 发布日志

记录所有 CSDN 发布的内容、类型和时间。

## 发布统计

- 总发布数：3
- 已发布：3
- 最后更新：2026-03-29 23:12

## 发布记录

| 日期 | 类型 | 标题 | 项目 | 状态 | 链接 |
|------|------|------|------|------|------|
| 2026-03-29 23:10 | 项目推广 | 折腾多运行时架构半年，说说 Capa-Java 踩过的那些坑 | Capa-Java | ✅ 已发布 | [查看](https://blog.csdn.net/wsh596823919/article/details/159618979) |
| 2026-03-27 13:52 | 测试 | 修复测试 - CSDN自动发布功能验证 | Fix Test | ✅ 已发布 | [查看](https://blog.csdn.net/wsh596823919/article/details/159544480) |
| 2026-03-25 12:45 | 项目推广 | 用AI规划旅行，我翻车了好几次才搞明白这些坑 | Trip Agent | ✅ 已发布 | [查看](https://blog.csdn.net/wsh596823919/article/details/159465504) |

## 发布方式说明

### ⚠️ 重要：CSDN 只能在 main session 中通过 browser 工具发布
- **原因**: CSDN 没有公开 API，需要 browser 自动化操作编辑器
- **限制**: cron isolated session 没有 browser 工具，无法直接发布
- **方案**: cron 负责生成内容 → 保存到 `csdn_drafts/pending/` → heartbeat/main session 用 browser 发布

### 发布流程
1. browser navigate → `https://editor.csdn.net/md`
2. browser evaluate → 填写标题（nativeInputValueSetter）
3. browser evaluate → base64 解码 + textContent 注入 Markdown
4. browser click → "发布文章"按钮
5. browser evaluate → 选择"原创"
6. browser click → 弹窗中的"发布文章"确认按钮

## 轮换计划

当前轮换位置：**Capa-Java 已完成，下一个: ClawX**

- Day 1: 项目推广 + 技术分享(架构)
- Day 2: 项目推广 + 踩坑实录
- Day 3: 技术分享(源码) + 项目推广
- Day 4: 项目推广 + 工具推荐
- Day 5: 经验总结 + 项目推广
