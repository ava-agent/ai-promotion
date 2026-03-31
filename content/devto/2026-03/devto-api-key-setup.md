# Dev.to API Key 配置说明

## 当前状态
❌ API Key 未配置

## 如何获取 API Key

1. 访问: https://dev.to/settings/extensions
2. 登录 Dev.to 账号 (kevinten10)
3. 点击 "Generate API Key"
4. 复制生成的 Key

## 配置方法

### 方法1: 直接创建文件
```bash
echo "your-api-key-here" > ~/.openclaw/workspace/memory/devto-api-key.txt
```

### 方法2: 手动创建
在 `C:\Users\PC\.openclaw\workspace\memory\` 目录下创建 `devto-api-key.txt` 文件，内容为 API Key。

## 验证配置
```bash
cd ~/.openclaw/workspace
python scripts/devto-publish.py memory/devto-promo-content-2026-03-25-1100.md --dry-run
```

## 待发布文章
- **文件**: `memory/devto-promo-content-2026-03-25-1100.md`
- **标题**: Honestly, I wasted 2 years chasing AI side hustles. Here's what finally worked.
- **项目**: ClawX
- **生成时间**: 2026-03-25 11:00
- **状态**: 等待 API Key 配置后发布
