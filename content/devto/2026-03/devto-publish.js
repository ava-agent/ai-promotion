const https = require('https');
const fs = require('fs');

function main(args = process.argv.slice(2)) {
  if (args.length > 1) {
    console.error('Usage: node devto-publish.js [article.md]; supply DEVTO_API_KEY privately.');
    process.exitCode = 1;
    return;
  }
  const apiKey = (process.env.DEVTO_API_KEY || '').trim();
  if (!apiKey) {
    console.error('Missing DEVTO_API_KEY; no request was sent.');
    process.exitCode = 1;
    return;
  }
  let bodyMarkdown;
  try {
    bodyMarkdown = fs.readFileSync(args[0] || 'article.md', 'utf8');
  } catch {
    console.error('Cannot read the article; no request was sent.');
    process.exitCode = 1;
    return;
  }
  const payload = JSON.stringify({
    article: {
      title: "I Tried to Build a Decentralized AI Agent Marketplace. Here's What Broke (and What Worked)",
      body_markdown: bodyMarkdown,
      published: true,
      tags: ['ai', 'agents', 'blockchain', 'typescript', 'opensource']
    }
  });
  const req = https.request({
    hostname: 'dev.to', path: '/api/articles', method: 'POST',
    headers: {
      'Content-Type': 'application/json', 'api-key': apiKey,
      'Content-Length': Buffer.byteLength(payload)
    }
  }, (res) => {
    // Discard bodies: they may contain credentials or private article content.
    res.resume();
    res.on('end', () => {
      console.log('Status:', res.statusCode);
      if (!(res.statusCode >= 200 && res.statusCode < 300)) process.exitCode = 1;
    });
    res.on('error', () => {
      console.error('Dev.to response failed; details withheld.');
      process.exitCode = 1;
    });
  });
  req.setTimeout(30000, () => req.destroy(new Error('Request timed out')));
  req.on('error', () => {
    console.error('Dev.to request failed; details withheld.');
    process.exitCode = 1;
  });
  req.end(payload);
}

module.exports = { main };
if (require.main === module) main();
