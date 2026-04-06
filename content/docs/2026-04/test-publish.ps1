# 读取内容
$content = Get-Content "memory/wechat-article-openoctopus.md" -Raw
$theme = "default"

# 创建JSON
$json = @{
    content = $content
    theme_id = $theme
} | ConvertTo-Json

# 保存到临时文件
$json | Set-Content "memory/temp-params.json" -Encoding UTF8

# 调用mcporter
Write-Host "JSON参数已生成，长度: $($json.Length) 字符"
Write-Host "调用mcporter发布..."

$command = "mcporter call wenyan-mcp.publish_article --args `"$(Get-Content memory/temp-params.json -Raw | ForEach-Object { [System.Text.RegularExpressions.Regex]::Escape($_) })`""
Write-Host "执行命令: $command"

Invoke-Expression $command