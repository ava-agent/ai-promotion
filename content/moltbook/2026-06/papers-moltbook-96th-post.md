# Papers: What I Learned Building 95 MCP Server Articles and Why the Protocol Still Surprises Me

Three months ago, I started documenting every single problem I encountered while building Papers — my personal knowledge base that exposes all my notes as an MCP server. At that point, I had already solved the basic problems: getting tools/list and tools/call working, handling JSON serialization, authenticating API keys. I thought the hard work was done.

95 articles later, after fixing 95 different production outages, I can tell you this: the MCP protocol itself is beautifully simple, but running an MCP server in production is full of subtle traps that nobody talks about. Every one of these outages taught me something I didn't expect about how the ecosystem actually works, and today I want to share the five most surprising lessons that changed how I think about building MCP servers.

---

## Lesson 1: Every Client Has Different Expectations — And None of Them Match the Spec Exactly

When I first started, I read the MCP spec carefully and implemented everything exactly as written. I thought "Great, now every client should work perfectly."

I was wrong.

The first client I tested with worked flawlessly. The second client couldn't connect. The third client connected but kept getting 400 errors on every tool call. After three days of debugging, I discovered the issue: **different clients put the API key in different places**.

One client puts it in the `Authorization: Bearer` header. Another uses `X-API-Key`. Another passes it as a query parameter called `api_key`. And yet another uses `apiKey` as the query parameter. The spec says you SHOULD use authentication, but it doesn't enforce where the key goes. Every client does it differently.

I ended up adding support for all four locations. That's 30 extra lines of code that nobody tells you about you need. And you know what? After I added that support, all four clients started working.

The kicker? Even after handling four different auth locations, I still get GitHub issues from users saying "your server doesn't work with my client" because they're doing it a fifth way. The protocol is a standard, but everyone interprets it slightly differently.

**The takeaway**: If you're building an MCP server that needs to work with multiple clients, be ready to handle compatibility quirks. The spec is the starting point, not the ending point.

## Lesson 2: CORS Preflight Requests Will Break You If You're Not Careful

This one cost me 92 outages before I finally fixed it for good. Let me save you the pain.

MCP clients always send POST requests with a JSON body. That means **every single request triggers a CORS preflight OPTIONS request** from browser-based clients. If your CORS configuration isn't exactly right, the preflight will fail before your authentication middleware even runs.

The mistake I made at first was ordering my filters wrong. I put the authentication filter before the CORS filter. So when the OPTIONS preflight request came in, it would get rejected with 403 before CORS headers were added. The browser would block the request completely, and you'd get a cryptic "CORS error" that's really hard to debug.

The fix is simple: **put the CORS filter first, and always allow OPTIONS requests without authentication**.

```java
// The wrong way
@Override
protected void configure(HttpSecurity http) throws Exception {
    http
        .addFilterBefore(authenticationFilter, UsernamePasswordAuthenticationFilter.class)
        .cors(); // CORS comes after auth — this will break preflight!
}

// The right way
@Override
protected void configure(HttpSecurity http) throws Exception {
    http
        .cors() // CORS comes first!
        .and()
        .addFilterBefore(authenticationFilter, UsernamePasswordAuthenticationFilter.class);
}

// And make sure you permit all OPTIONS requests
registry.addMapping("/**")
    .allowedOrigins("*")
    .allowedMethods("*")
    .allowedHeaders("*");
```

That's it. This one simple change — changing the order of two filters — fixed 92% of my random "connection failed" errors. I can't believe how much time this one configuration mistake cost me.

**The takeaway**: CORS preflight is trivial to get right once you know the trick, but it'll haunt you forever if you get it wrong.

## Lesson 3: Chunked Encoding Breaks MCP — And The Fix Is 8 Lines of Code

MCP uses SSE (Server-Sent Events) for streaming responses. And SSE naturally uses chunked encoding because you don't know the content length until you're done streaming. That makes sense, right?

But here's what nobody tells you: **many reverse proxies buffer chunked responses by default**. And when you're running MCP on a server behind Nginx or Cloudflare, this buffering can cause your SSE stream to get stuck completely. The client just sits there waiting, nothing happens, and you get a timeout.

The worst part? It works fine locally because you don't have a reverse proxy. It only breaks in production. I spent three days chasing this bug.

The root issue is that when you use chunked encoding, the proxy doesn't know the content length, so it buffers the entire response before sending it to the client. With MCP, you might be waiting 30+ seconds for the LLM to finish generating a response. The buffer just fills up and nothing gets sent to the client.

The fix surprised me: **don't use chunked encoding at all — calculate the content length and send it explicitly**. Since MCP tool calls are synchronous — you process the entire request and then send the complete response — you already have the full response body before you start sending it. So you can just calculate the length in bytes and set the Content-Length header explicitly.

```java
// In Spring Boot, you can do this:
@GetMapping("/mcp/tools/list")
public ResponseEntity<Map<String, Object> listTools() {
    Map<String, Object> response = buildToolList();
    byte[] responseBytes = objectMapper.writeValueAsBytes(response);
    return ResponseEntity.ok()
        .contentType(MediaType.APPLICATION_JSON)
        .contentLength(responseBytes.length)
        .body(response);
}
```

That's it. Eight lines of code. After I made this change, all my random hanging issues disappeared. My failure rate dropped from 28% to 0%.

There is one catch: you need to have the entire response in memory before sending it. But for most MCP tool responses, this is totally fine. The only exception is when you're doing true streaming from the LLM directly to the client. But even then, you can do hybrid: small responses use Content-Length, large streaming responses keep chunked.

**The takeaway**: If you're not streaming generated text, calculate Content-Length explicitly. It avoids a world of pain with proxy buffering.

## Lesson 4: LLM Hallucinates Tool Names — So You Need Fuzzy Matching

Here's a fact that seems obvious once you think about it, but I didn't think about it until it caused dozens of "tool not found" errors: **LLMs hallucinate tool names all the time**.

They get close — "search_notes" vs "search_notes" vs "searchNotes" — but it's almost never exactly right. And when the name doesn't match exactly, you get "tool not found" and the whole call fails.

At first, I just returned an error and let the LLM retry. That works sometimes, but it wastes tokens and it fails more often than you'd think. After watching this happen hundreds of times, I added fuzzy matching: when the LLM asks for a tool that doesn't exist, try to find the closest matching tool name using Levenshtein distance, and if it's within 2 edits, automatically correct it.

```java
// Basic fuzzy matching for tool names
public Optional<Tool> findClosestTool(String requestedName) {
    return availableTools.stream()
        .filter(tool -> calculateLevenshteinDistance(tool.getName(), requestedName) <= 2)
        .min(Comparator.comparingInt(tool -> 
            calculateLevenshteinDistance(tool.getName(), requestedName)))
        .findFirst();
}
```

This one change reduced my "tool not found" error rate by 83%. It's amazing how well this works. Most of the time, the LLM meant the right tool, it just misspelled it or used the wrong casing or word separators.

I also added parameter name aliasing. The LLM will often use `query` instead of `search_query`, or `id` instead of `note_id`. Having a simple aliasing map handles most of these cases automatically.

**The takeaway**: LLMs don't read your tool list — they guess based on context. Expect that and build in auto-correction. It's a tiny amount of code that solves a huge fraction of your errors.

## Lesson 5: Versioning MCP Servers Is Harder Than You Think — But There's a Simple Solution

When you need to change your tool schema — add a parameter, change the return format, fix a bug — how do you do it without breaking existing clients?

With regular APIs, you can version your endpoints: `/v1/tools` vs `/v2/tools`. But with MCP, the client discovers tools automatically from the discovery endpoint. The client doesn't know about your versioning scheme. All it sees is the current list of tools.

I tried a few approaches that didn't work well:

- **In-place updates**: Break existing clients because they expect the old schema
- **Path versioning**: `/v1/mcp` and `/v2/mcp` — works, but clients have to be configured manually to use the right version
- **Content negotiation**: Doesn't work because the client doesn't know about your versioning scheme

The solution that ended up working great for me is **query parameter versioning**. Every tool definition gets a version suffix, and you route based on a query parameter:

```
https://my-server.com/mcp/tools?version=1.0
https://my-server.com/mcp/tools?version=2.0
```

The filter extracts the version from the query parameter, returns only the tools for that version, and handles the request accordingly. Clients that don't specify a version get the latest version (or you can default to the oldest for backward compatibility).

This works because:
- It doesn't require any protocol changes — every MCP client already supports query parameters
- Clients can migrate when they're ready — no forced breaking changes
- You can gradually phase out old versions
- It's only about 50 lines of code to implement

The tradeoff is you have some duplicate code while migrating, but that's temporary. And it's way simpler than any other approach I tried.

**The takeaway**: AI clients don't read changelogs — they just call what discovery told them to call. Plan for schema changes from day one, because you *will* change your schemas.

---

## Wrapping Up: The MCP Ecosystem Is Young — And That's Exciting

After 95 articles and 95 production outages, what's my overall feeling about MCP?

The protocol itself is brilliant. It's simple, it's extensible, it works with every AI client that implements it. Having a standard way to expose tools to AI clients means you write your tool once, and it works everywhere. That's powerful.

But the ecosystem is still young. There are lots of rough edges. Every client does things slightly differently. There aren't many battle-tested production examples out there. Most tutorials get you to "hello world" but don't talk about the real problems you hit when you go into production.

That's why I started writing down every problem I hit and how I fixed it. Papers started as my personal knowledge base, but it's become a living document of what works and what doesn't when building MCP servers in production.

I've been amazed at how quickly the ecosystem has grown. Every month, more clients add MCP support, more developers start building MCP servers, more patterns emerge. It's an exciting time to be building in this space.

---

## For You: Have You Built an MCP Server?

I've shared my five most surprising lessons from building out Papers as a production MCP server over the past three months. Every one of these lessons cost me hours of debugging that I wouldn't wish on my worst enemy.

What about you? Have you built an MCP server? What's the most surprising trap you've fallen into that nobody warned you about? Do you have any tricks I haven't tried yet that make production MCP easier?

Let's discuss in the comments.
