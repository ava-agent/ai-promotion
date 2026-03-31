const https = require('https');
const fs = require('fs');

// Read the article content
const bodyMarkdown = fs.readFileSync(process.argv[2], 'utf8');

const apiKey = process.argv[3];

const payload = JSON.stringify({
  article: {
    title: "I Tried to Build a Decentralized AI Agent Marketplace. Here's What Broke (and What Worked)",
    body_markdown: bodyMarkdown,
    published: true,
    tags: ["ai", "agents", "blockchain", "typescript", "opensource"]
  }
});

const options = {
  hostname: 'dev.to',
  path: '/api/articles',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'api-key': apiKey,
    'Content-Length': Buffer.byteLength(payload)
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    console.log('Status:', res.statusCode);
    console.log('Response:', data);
    try {
      const json = JSON.parse(data);
      if (json.url) {
        console.log('\nArticle URL:', json.url);
      }
    } catch (e) {}
  });
});

req.on('error', (e) => console.error('Error:', e.message));
req.write(payload);
req.end();
