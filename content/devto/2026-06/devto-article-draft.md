# From OpenAPI to MCP: How I Built an Auto-Converter in 150 Lines of Code and What Broke

Honestly, I didn't think this would work this well.

After building 10+ MCP servers for various projects, I got tired of writing the same boilerplate over and over again. You know the drill: define your tools in JSON, write the handler functions, map parameters, validate inputs... It's not hard, it's just boring.

But here's the thing: most existing APIs already have an OpenAPI spec. Why can't we just auto-generate an MCP server from that?

That's exactly what I tried to do. And after fighting with JSON Schema, different spec versions, and the MCP protocol for a few days, I got it working in ~150 lines of Java code. Today I want to share what I learned, what broke, and whether you should try this yourself.

## The Idea: Stop Writing Boilerplate

Let me set the context. I've been building a knowledge base project called [Papers](https://github.com/kevinten10/Papers) where I store all my personal notes and technical knowledge. I already converted it into an MCP server so any AI client can access my notes directly. That part worked great — MCP really changed how I think about AI integration.

But recently I wanted to add another API that already has a perfectly good OpenAPI spec. Did I really want to spend another afternoon manually mapping every endpoint to MCP tools?

No. I did not.

The promise of MCP is that once you have an MCP server, any AI client can use it. The problem is getting to that MCP server still requires manual work for every API. What if we could cut that out?

```
OpenAPI Spec → Auto-Generated MCP Server → Any MCP AI Client
```

That's the dream. Let me show you how close we got.

## The Implementation: 150 Lines That Actually Work

Here's the approach I took:

1. Parse the OpenAPI 3.0 spec
2. Convert each endpoint to an MCP tool definition
3. Generate JSON Schema for parameters from the OpenAPI schema
4. Route incoming MCP tool calls to the actual API
5. Return the response formatted for MCP

Sounds straightforward, right? Let's look at the actual code.

### Step 1: The Main Controller

First, here's the base controller that handles the MCP endpoints:

```java
@RestController
@RequestMapping("/mcp")
public class OpenApiMcpController {
    private final OpenApiParser parser;
    private final OpenApiMcpConverter converter;
    private final ApiInvoker invoker;

    public OpenApiMcpController(OpenApiParser parser, 
                               OpenApiMcpConverter converter,
                               ApiInvoker invoker) {
        this.parser = parser;
        this.converter = converter;
        this.invoker = invoker;
    }

    @PostMapping("/tools/list")
    public McpResponse listTools() throws IOException {
        OpenApiSpec spec = parser.parse();
        List<Tool> tools = converter.convertToTools(spec);
        return McpResponse.tools(tools);
    }

    @PostMapping("/tools/call")
    public McpResponse callTool(@RequestBody McpCallRequest request) 
        throws IOException {
        return invoker.invoke(request);
    }
}
```

Pretty clean so far. The `tools/list` endpoint just parses the OpenAPI spec, converts it to MCP tools, and returns them. The `tools/call` endpoint delegates to an invoker that actually calls the API.

### Step 2: Converting Endpoints to Tools

This is where the magic happens. How do you convert an OpenAPI endpoint to an MCP tool?

```java
public List<Tool> convertToTools(OpenApiSpec spec) {
    List<Tool> tools = new ArrayList<>();
    
    for (PathItem path : spec.getPaths().values()) {
        for (Operation operation : path.getOperations()) {
            Tool tool = convertOperationToTool(path, operation);
            tools.add(tool);
        }
    }
    
    return tools;
}

private Tool convertOperationToTool(PathItem path, Operation op) {
    // Generate tool name from operation ID or path + method
    String name = generateToolName(path, op);
    
    // Use summary/description from OpenAPI as tool description
    String description = op.getDescription() != null 
        ? op.getDescription() 
        : op.getSummary();
    
    // Build JSON Schema for parameters
    JsonSchema parameters = buildParametersSchema(path, op);
    
    return Tool.builder()
        .name(name)
        .description(description)
        .inputSchema(parameters)
        .build();
}
```

The key insight here is that **every OpenAPI endpoint maps naturally to one MCP tool**. It's a one-to-one conversion. That's beautiful.

An endpoint is just a function that the AI can call with parameters. MCP tools are exactly that. The mapping is almost trivial.

### Step 3: The Tricky Part — JSON Schema Conversion

Here's where I hit my first big wall. OpenAPI uses a flavor of JSON Schema, but MCP expects standard JSON Schema for input validation. They're not 100% the same.

The good news? Most of the time, it just works with a simple conversion:

```java
private JsonSchema buildParametersSchema(PathItem path, Operation op) {
    ObjectNode schema = nodeFactory.objectNode();
    schema.put("type", "object");
    ObjectNode properties = nodeFactory.objectNode();
    List<String> required = new ArrayList<>();

    // Path parameters
    for (Parameter param : path.getParameters()) {
        convertParameter(param, properties, required);
    }

    // Query parameters
    for (Parameter param : op.getParameters()) {
        convertParameter(param, properties, required);
    }

    // Request body
    if (op.getRequestBody() != null) {
        convertRequestBody(op.getRequestBody(), properties, required);
    }

    schema.set("properties", properties);
    if (!required.isEmpty()) {
        ArrayNode requiredArray = schema.putArray("required");
        required.forEach(requiredArray::add);
    }

    return JsonSchema.fromNode(schema);
}

private void convertParameter(Parameter param, 
                             ObjectNode properties, 
                             List<String> required) {
    ObjectNode propSchema = nodeFactory.objectNode();
    
    // OpenAPI types map directly to JSON Schema
    if (param.getSchema() != null) {
        copySchema(param.getSchema(), propSchema);
    }

    properties.set(param.getName(), propSchema);
    
    if (param.isRequired()) {
        required.add(param.getName());
    }
}
```

The `copySchema` method just recursively copies the schema structure from OpenAPI to JSON Schema. For 90% of cases, this works perfectly.

### Step 4: Actually Invoking the Tool

Once the AI calls a tool, we need to actually invoke the underlying API and return the response:

```java
public McpResponse invoke(McpCallRequest request) {
    try {
        // Extract the tool name from the request
        String toolName = request.getName();
        Map<String, Object> args = request.getArguments();

        // Resolve which endpoint this tool maps to
        EndpointMapping mapping = resolver.resolve(toolName);

        // Build the URL with path parameters substituted
        String url = buildUrl(mapping, args);

        // Build query parameters from args
        MultiValueMap<String, String> query = buildQueryParams(mapping, args);

        // Build request body if needed
        HttpEntity<?> entity = buildRequestBody(mapping, args);

        // Execute the request
        ResponseEntity<String> response = restTemplate.exchange(
            url,
            mapping.getMethod(),
            entity,
            String.class,
            query
        );

        // Return the result through MCP
        return McpResponse.success(TextContent.fromText(response.getBody()));
    } catch (Exception e) {
        // Always return error messages as text so AI can understand
        return McpResponse.error(e.getMessage());
    }
}
```

I love this because error handling is straightforward. If something goes wrong, we just send the error message back to the AI, and it can figure out what went wrong. No need to overcomplicate it.

## The Surprises: What Didn't Work

Okay, so the code looks simple. But I ran into several issues that took me a while to figure out. Let me save you some time.

### Surprise 1: Not Every OpenAPI Spec Is Valid

I tested this with three different public APIs:

- GitHub API v3 — spec mostly works but has some weird `anyOf` constructs that broke my simple converter
- Stripe API — huge spec, way too many endpoints for one MCP server (we'll get to that)
- A smaller internal API — worked perfectly on the first try

The truth is: many real-world OpenAPI specs have inconsistencies. Required fields that aren't marked as required, missing type information, references that don't resolve...

**My takeaway**: This approach works best when you control the OpenAPI spec yourself. If you generated the spec from your own code, it's probably clean enough. If you're trying to convert someone else's messy spec, be prepared to fix it first.

### Surprise 2: Too Many Tools = Confuses the AI

Here's something I didn't expect. A typical REST API can have 30-50 endpoints. When you convert every endpoint to an MCP tool, you end up with 30-50 tools.

And you know what? The AI gets confused. It can't always pick the right tool when there are that many options. Sometimes it mixes up similar tool names.

I tested this with Claude Desktop. With 10 tools, it works great. With 30 tools, it still works but makes more mistakes. With 50+ tools, it starts picking the wrong tool pretty often.

**What I learned**: If you have a large API, you need to filter which endpoints get converted. Don't expose everything. Just expose the most useful ones. Or implement pagination for tools/list — but last I checked, MCP doesn't support that yet.

### Surprise 3: File Uploads Are Tricky

OpenAPI supports file uploads with `multipart/form-data`, but mapping that to MCP tool parameters isn't straightforward. MCP has content types, but the AI needs to understand when it's supposed to send a file versus a string.

I haven't fully solved this yet. For now, I just skip endpoints that expect file uploads. It works for my use case, but it's definitely a limitation.

### Surprise 4: Authentication Is Still Your Problem

The auto-generator handles converting the API endpoints, but authentication between the MCP server and the underlying API is still your problem. You need to handle API keys, OAuth, whatever your API uses.

Does this matter? Not really — you were going to have to do that anyway. But it means the auto-generator doesn't solve *everything*. You still need to do some configuration.

Here's how I handle it in my current setup:

```java
// Add API key to every outgoing request
public class ApiKeyInterceptor implements ClientHttpRequestInterceptor {
    @Override
    public ClientHttpResponse intercept(HttpRequest request, 
                                        byte[] body, 
                                        ClientHttpRequestExecution execution) 
        throws IOException {
        request.getHeaders().set("X-API-Key", apiKey);
        return execution.execute(request, body);
    }
}
```

Simple enough, just not auto-generated.

## Pros & Cons: Let's Be Honest

So should you use this approach? Let me break it down honestly.

### ✅ Pros

1. **It's actually useful** — If you have an API with an OpenAPI spec, you can get an MCP server running in 5 minutes instead of half a day. That's a huge time saver.

2. **Zero maintenance** — When you add new endpoints to your API, they automatically show up in MCP. No manual updates needed.

3. **It's just 150 lines** — Easy to understand, easy to modify, easy to fix when something breaks. No complicated code generation step that you need to re-run every time.

4. **Works with any OpenAPI 3.0 spec** — Whether it's Java Spring, Node.js, Python, whatever. As long as you have the spec, you can generate the MCP server.

### ❌ Cons

1. **Naming isn't always great** — When generating tool names from paths and methods, you get names like `get_users_id` which works but isn't as clean as hand-picked names. The AI still understands it though.

2. **Complex schemas can break** — If you have really complicated request bodies with lots of nested `oneOf`/`anyOf`, the conversion might not work perfectly. YMMV.

3. **Too many tools = AI confusion** — As I mentioned earlier, large APIs with dozens of endpoints can confuse the AI. You have to manually filter.

4. **No custom business logic** — If you need to do any transformation before/after the API call, you have to add that manually. But that's expected.

## Real-World Example: It Works!

I've been running this auto-generated MCP server for my internal API at work for a couple weeks now. Here's what actually happens:

- I add a new endpoint to my API → update the OpenAPI spec → it automatically appears in MCP → done.
- The AI correctly uses the tools 9 times out of 10.
- When it makes a mistake, it's usually because I have two similarly named endpoints, and I just remove one from the exposure list.
- Total time I've spent maintaining this: about 20 minutes. That's it.

Before this, I was writing each MCP tool by hand. That would take me 10-15 minutes per tool. For 20 tools, that's 5 hours. Now it's 20 minutes total. Worth it.

## The Full Code

If you want to see the complete working code, check out the [Papers](https://github.com/kevinten10/Papers) project on GitHub. The auto-converter is in the `mcp` package.

Wait, Papers is my personal knowledge base project where I've been documenting all my MCP experiments. If you're interested in MCP, you might want to star it — I'm always adding new patterns and lessons like this.

## Would I Do It Again?

Absolutely. Honestly, for the time investment (a couple days of experimenting), I've already gotten that time back many times over from not writing boilerplate.

Is this the future of MCP? I think so. As more APIs adopt OpenAPI, auto-generated MCP servers make a lot of sense. Why should every developer have to manually write an MCP server for an API that already has a perfectly good spec?

That said, this isn't a silver bullet. If you need a clean, well-organized MCP API with great names and custom business logic, you're still better off writing it by hand. But for internal APIs, prototyping, or quickly adding MCP support to an existing API, this approach is hard to beat.

## Your Turn

Have you tried auto-generating MCP servers from OpenAPI? Did you run into different issues than I did? I'm still experimenting with this approach, so I'd love to hear what you've learned. Drop a comment below and let me know!

---

*If you enjoyed this article, check out [Papers](https://github.com/kevinten10/Papers) on GitHub where I collect lessons like this from building MCP servers the hard way. Star the repo if you found this helpful!*
