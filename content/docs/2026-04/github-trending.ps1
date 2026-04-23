# 获取过去1小时内创建的热门项目
$oneHourAgo = Get-Date (Get-Date).AddHours(-1) -Format 'yyyy-MM-ddTHH:mm:ssZ'
$url = "https://api.github.com/search/repositories?q=created:$oneHourAgo&sort=stars&order=desc&per_page=10"

try {
    $response = Invoke-RestMethod -Uri $url -Method GET
    $response.items | ForEach-Object {
        Write-Output "$($_.full_name) - $($_.description) - ⭐ $($_.stargazers_count)"
    }
} catch {
    Write-Output "GitHub API请求失败: $_"
}