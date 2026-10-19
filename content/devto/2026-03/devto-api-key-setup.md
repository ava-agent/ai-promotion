# Dev.to 凭据配置与泄露处置

发布脚本仅从 `DEVTO_API_KEY` 环境变量读取凭据。不接受命令行 key，
不读取仓库内的 key 文本文件，不打印认证异常详情或完整 API 响应。

## 已公开凭据的处置

删除源码不等于撤销凭据，也不会删除 Git 历史。账号持有人应在
[Dev.to 扩展设置](https://dev.to/settings/extensions) 确认旧 key 已撤销；
需要继续发布时再生成新 key，并通过私有凭据管理器注入环境变量。
不要用旧 key 发请求验证其是否有效，不要把新 key 写进仓库、命令参数或 shell 历史。

## 运行

先通过私有运行环境注入 `DEVTO_API_KEY`，再运行以下任一命令：

```bash
python devto_publish.py article.md
node devto-publish.js article.md
```

这两个命令会实际发布文章，不是 dry-run；Python 版本需要 `requests`。
未提供凭据时会在发送请求前退出。只输出 HTTP 状态，不输出完整响应。

离线验证（只用合成值和模拟网络）：

```bash
python -m unittest discover -s tests -p 'test_devto_publish.py'
node --test tests/devto-publish.test.cjs
```
