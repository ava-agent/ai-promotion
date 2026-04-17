# GitHub Trending 监控计划任务设置
Write-Host "设置GitHub Trending监控计划任务..."

# 设置任务计划
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\Users\PC\.openclaw\workspace\scripts\github-trending-monitor.py"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Days 365)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# 创建任务
$taskName = "GitHubTrendingMonitor"
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest

Write-Host "✅ GitHub Trending监控计划任务已设置"
Write-Host "🔄 运行间隔: 每30分钟"
Write-Host "📁 脚本位置: C:\Users\PC\.openclaw\workspace\scripts\github-trending-monitor.py"
Write-Host "📊 数据位置: C:\Users\PC\.openclaw\workspace\memory/"