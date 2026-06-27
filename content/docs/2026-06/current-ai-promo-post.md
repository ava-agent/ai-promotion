# Papers: What I Learned Building 95 MCP Server Articles - The Complete Checklist I Wish I Had When I Started

Let me tell you a secret: after building 95 production MCP servers, I've learned more about what can go wrong than what can go right. And honestly? That's where the real value is. When I started building Papers - my personal knowledge base MCP server - I had no idea I'd end up writing 95 separate articles about every production issue I fixed along the way. But here we are, and today I want to share the complete checklist I wish someone had given me when I started.

If you're building an MCP server right now, bookmark this. I promise you'll thank me later.

## The Big Picture: What Nobody Tells You About Building MCP Servers

When the Model Context Protocol was announced, everyone got excited about "give your AI agent access to tools!" And that's great. But what nobody talked about is that building a production-ready MCP server is just like building any other production API - you have to handle all the boring edge cases that nobody talks about in the announcement blog post.

I've spent the past six months fighting every possible bug in my MCP server. CORS preflight breaking 92 times, connection dropping because of idle timeouts, chunked encoding breaking SSE, rate limiting, authentication, logging, monitoring, caching, timeouts, validation, Docker-compose configuration - you name it, I've fixed it.

Each of these issues took me hours to debug because there wasn't a single place that collected all the gotchas. So let's fix that. Here's everything I wish I knew before I started.

## 1. CORS Preflight is Non-Negotiable - Get it Right Early

Let me start with the issue that broke my server 92 times: CORS preflight. If you're running your MCP server behind any proxy - and you almost certainly are - you *will* get bitten by CORS.

Here's what happens: MCP clients send preflight OPTIONS requests before they send the actual POST request. If your server doesn't handle OPTIONS correctly, your MCP server will get blocked before it even starts responding.

The gotcha? Most frameworks handle CORS automatically, but when you're running behind Nginx or Cloudflare, things get messy. I spent three days debugging why my MCP server was getting 403 errors on preflight - turns out I had forgotten to whitelist the headers that MCP clients send.

**Your action item**:
- Explicitly handle OPTIONS requests for all MCP endpoints
- Allow the headers: `Authorization`, `Content-Type`, `Accept`
- Expose the header: `Access-Control-Allow-Origin: *` (or your specific origin if you're doing it properly)
- Make sure your proxy doesn't block OPTIONS requests
- Test with curl first: `curl -X OPTIONS https://your-mcp-server.com/mcp -v`

I can't tell you how much time this saved me after I got this right. Do it first. Don't be like me.

## 2. Timeouts are Everything - Different Timeouts for Different Things

The #1 cause of outages in my MCP server wasn't CORS - it was timeouts. And not just one timeout - you need *different* timeouts for different things.

Here's the thing: when an LLM is calling your MCP server, it might take a few seconds for it to generate the response. But if your proxy has an idle timeout of 60 seconds, and your LLM takes 70 seconds to respond, your connection gets dropped halfway through.

I learned this the hard way when I was testing with a particularly complex query that took 75 seconds to complete. Everything was happening - the server was processing, the response was streaming - and *boom* - Cloudflare dropped the connection at 60 seconds. Gone. No response. Just an error.

What timeouts do you need?

- **Connect timeout**: 10 seconds - if you can't connect in 10 seconds, something's wrong
- **Idle timeout**: 300 seconds - yes, five minutes. LLMs are slow. Give them time.
- **Read timeout**: 300 seconds - same reason
- **Write timeout**: 60 seconds - most requests aren't that big, but give it room

And if you're using Cloudflare, their default idle timeout is 100 seconds. If you're on the free tier, you can't increase it. Keep that in mind when you're choosing where to host.

**Your action item**:
- Go through every component in your stack - server, proxy, CDN, cloud provider - and check all the timeout settings
- Set idle timeout to at least 300 seconds
- Document all your timeout settings somewhere - you'll forget

## 3. SSE and Chunked Encoding Breaks Everything

MCP uses Server-Sent Events for streaming responses. And most of the time, that works great. But when you start putting proxies and buffers in front of it, things get weird.

The issue I kept hitting: chunked encoding. When your proxy buffers the response content-length gets messed up, and SSE stops working. I spent a week wondering why my responses were getting cut off halfway through - turns out my proxy was buffering the response and not sending it chunked, so the content-length was wrong, and the client closed the connection early.

Another issue: `Transfer-Encoding: chunked` means you don't send a `Content-Length` header. If you send both, some clients get confused. I learned that the hard way.

The Nginx specific gotcha: `proxy_buffering off` is *required* for SSE. If you leave it on, Nginx will buffer the response and your SSE events won't get sent in real-time. Your client will wait until the whole response is done before it gets any data. That's not what you want for streaming.

**Your action item**:
- Turn off proxy buffering in Nginx for MCP endpoints: `proxy_buffering off;`
- Don't send both `Transfer-Encoding: chunked` and `Content-Length`
- Make sure your proxy doesn't buffer SSE responses
- Test with curl: `curl -N https://your-mcp-server.com/mcp` to see if streaming works

## 4. Content-Length Will Break Your Server When You Least Expect It

Speaking of content-length - here's another gotcha I stepped in: when you're doing chunked encoding, the proxy calculates the content-length incorrectly if you're not careful. And when that happens, the connection gets closed early.

I had this happen after I fixed the proxy buffering issue. Everything seemed to work - but every once in a while, a longer response would get cut off. Turns out my proxy was buffering the response to calculate the content-length, and when it didn't expect the longer response, it cut it off.

**Your action item**:
- If you're using chunked encoding, make sure your proxy passes the chunks through immediately
- Don't let your proxy rewrite the content-length header when you're using chunked encoding
- Test with different response sizes - from small (1KB) to large (100KB) to make sure they all complete

## 5. Authentication: Don't Log Full API Keys

This one's part security, part debugging. When you're adding authentication to your MCP server, you *must* not log the full API key. Log only the first 4 characters. That's enough for debugging, and it keeps your API keys safe.

I see this mistake all the time - people turn on debug logging and accidentally log the entire API key. Don't do that. It's an easy mistake to make, and it's easy to fix.

**Your action item**:
- Create a logging filter that masks API keys - log only first 4 chars
- Make sure authentication happens early in your filter chain before logging
- Don't log any headers that contain credentials

## 6. Log Everything That Matters, But Don't Log Content

MCP servers handle user requests, and those requests contain user content. You need to log metadata about every request - start time, end time, whether it succeeded, tool name, error message - but don't log the actual request/response content. That's user data, and you don't need it in your logs for debugging anyway.

But you do need to log when a request starts and when it ends. Because the #1 question you'll ask when debugging is "did the request ever reach the server?" Having start/end timestamps in your logs answers that question immediately.

I also add a unique request ID to every request, and log it with every entry. That way you can trace an end-to-end request through your entire stack.

**Your action item**:
- Log every request: start time, end time, duration, status code, request ID, tool name
- Don't log request/response content
- Mask any sensitive data like API keys
- Add a request ID to every request for tracing

## 7. Handle "Tool Not Found" Gracefully - LLMs Hallucinate Tool Names All The Time

Here's something I never expected: LLMs hallucinate tool names *all the time*. They'll see your tool list, and then they'll call a tool that sounds right, but doesn't actually exist.

If you just return "error: tool not found", the LLM will just try again and get it wrong again. But if you return a list of the closest matching tool names, the LLM can correct itself.

I added fuzzy matching to my server, and it cut down on "tool not found" errors by almost 30%. That's a huge improvement in user experience for almost no code. The entire fuzzy matcher is about 50 lines of code. Totally worth it.

**Your action item**:
- When tool not found, return the top 3 closest matching tool names
- Use Levenshtein distance for fuzzy matching
- Keep it simple - you don't need anything fancy

## 8. Caching: Cache What You Can, But Don't Cache Stale Data

Once your server is running for a while, you'll notice that some tools get called over and over with the same arguments. Caching helps a lot here. I added simple Redis caching to my server, and it cut response times from 320ms to 12ms. That's a 27x improvement.

But the gotcha? Don't cache when the data changes underneath. My knowledge base gets updated all the time, so I only cache public static content. Keep your caching strategy simple - if it doesn't change, cache it. If it changes, don't.

**Your action item**:
- Add caching for frequently-called static data
- Use Redis for simple key/value caching
- Invalidate cache when content changes
- Don't overcomplicate it - start simple

## 9. Rate Limiting: Protect Your Server, But Don't Block Local Development

If you're running a public MCP server, you need rate limiting. Even if it's just for your personal use, someone might accidentally call your endpoint in a loop and take your server down.

I use simple token bucket rate limiting in Spring Boot, and it works great. It's easy to add, and it keeps your server safe. The gotcha? Make sure you exempt localhost for development, so you don't get rate limited while testing.

**Your action item**:
- Add rate limiting per API key
- Exempt localhost/private IPs for development
- Return proper 429 status code when rate limited
- Set reasonable limits based on your hosting capacity

## 10. Docker Compose: The Production Configuration I Wish I Had When I Started

After 95 outages, I finally have a docker-compose configuration that just works. Here are the key things that I got wrong at first:

- **Non-root user by default**: Don't run your app as root inside the container. It's bad practice, and it's easy to fix. Just create a non-root user in your Dockerfile.
- **Healthchecks**: Add a healthcheck endpoint to your MCP server, and declare it in docker-compose. That way Docker can tell if your server is healthy and restart it if it's not.
- **Depends on with condition**: Make sure your app depends on redis/postgres being healthy before it starts. Don't just start it in order.
- **Environment variables for everything**: Don't hardcode configuration. Put everything in environment variables so you can change it without rebuilding the image.
- **Logging configuration**: Make sure your app logs to stdout/stderr so Docker can collect the logs. Don't write logs to a file inside the container.

**Your action item**:
- Use a non-root user in your Dockerfile
- Add a healthcheck endpoint
- Configure docker-compose with healthcheck depends on conditions
- Don't run as root

## 11. Versioning: Handle Multiple Versions Without Downtime

When you need to update your MCP server schema, how do you handle it without breaking existing clients? I tried several approaches, and the simplest thing that works is running both versions side by side while clients migrate.

The code is really simple - add a filter that handles `/v1/mcp` and `/v2/mcp`. That's it. You don't need anything fancier. When all clients have migrated, you can remove the old version.

**Your action item**:
- Version your MCP API from day one
- Keep old versions running until all clients migrate
- Don't force breaking changes on your users

## 12. Validation: Validate Every Input, Early

The LLM will send you bad data. It just happens. Validate every input *early* in your controller, before you do any processing. Return a clear error message saying what's wrong.

I use Jakarta validation with Spring Boot, and it automatically returns clear error messages when validation fails. That's saved me so much time debugging weird errors that were just bad input.

**Your action item**:
- Add input validation to every endpoint
- Return clear error messages when validation fails
- Validate early, before you do any processing

## Putting It All Together: The Checklist

Here's the complete checklist you can go through when you're building your MCP server:

- [ ] CORS preflight handled correctly
- [ ] All timeout settings configured correctly (connect, idle, read, write)
- [ ] Proxy buffering turned off for SSE
- [ ] Chunked encoding handled correctly, no conflicting Content-Length
- [ ] API keys masked in logs (only first 4 chars logged)
- [ ] Request metadata logged, content not logged
- [ ] Request ID added for tracing
- [ ] Fuzzy matching for tool not found returns closest 3 matches
- [ ] Caching implemented for static content
- [ ] Rate limiting configured with development exemptions
- [ ] Dockerfile uses non-root user
- [ ] Docker-compose configured with healthchecks
- [ ] API versioning from day one
- [ ] Input validation on all endpoints

## Final Thoughts

Building an MCP server is really fun. It's exciting to give your AI agent access to your personal data. But getting to production is all about handling the boring edge cases that nobody talks about.

I've spent six months and 95 articles figuring all this out. Use this checklist, and you'll save yourself weeks of debugging.

What's the biggest surprise I found? Most of the work isn't the MCP-specific protocol stuff - it's just standard production API best practices that you have to get right. The MCP protocol is straightforward once you get all the boring infrastructure stuff sorted out.

If you're just starting building your first MCP server, good luck. You got this. And if you found this helpful, let me know what other gotchas you've run into - I'd love to hear about them.

---

What's the most surprising MCP production gotcha you've run into that wasn't on this list?
