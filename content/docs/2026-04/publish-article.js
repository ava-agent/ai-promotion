const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

// 设置工作目录
process.chdir('C:/Users/PC/.openclaw/workspace');

// 读取文章内容
const content = fs.readFileSync('memory/wechat-article-openoctopus.md', 'utf8');

// 转义JSON字符串中的特殊字符
const escapedContent = content.replace(/"/g, '\\"').replace(/\n/g, '\\n');

// 创建JSON参数
const jsonArgs = {
  content: content,
  theme_id: 'default'
};

console.log('准备发布参数:', JSON.stringify(jsonArgs, null, 2));

// 尝试发布
try {
  const command = `mcporter call wenyan-mcp.publish_article --args '${JSON.stringify(jsonArgs)}'`;
  console.log('执行命令:', command);
  
  const result = execSync(command, { encoding: 'utf8', stdio: 'pipe' });
  console.log('发布成功:', result);
  
  // 保存结果
  fs.writeFileSync('memory/publish-result.json', JSON.stringify({
    success: true,
    result: result,
    timestamp: new Date().toISOString()
  }, null, 2));
  
} catch (error) {
  console.error('发布失败:', error.message);
  
  // 保存错误
  fs.writeFileSync('memory/publish-result.json', JSON.stringify({
    success: false,
    error: error.message,
    timestamp: new Date().toISOString()
  }, null, 2));
}