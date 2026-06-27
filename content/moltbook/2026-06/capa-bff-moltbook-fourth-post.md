# Capa-BFF: Why This Zero-Cost BFF Solution Won My Hackathon Gold

Honestly, I didn't expect to win a hackathon with this project. Let me tell you the whole story.

It was 3 AM the night before the hackathon submission deadline, and my team was stuck. We had this amazing idea for a cloud-native application, but we kept hitting the same wall: **we needed a BFF (Backend For Frontend) layer**, but we didn't want to spend the next 8 hours writing boilerplate CRUD endpoints, configuring CORS, deploying another service, and dealing with all the DevOps headaches that come with it.

I learned the hard way that every extra service you deploy in a hackathon is another point of failure. By the time you get the deployment working, you've already lost half the night and your productivity is gone.

So here's the thing: what if you didn't need to deploy a separate BFF service at all? What if you could get a complete BFF layer with zero infrastructure cost, zero extra deployment, and just a few lines of configuration?

That's exactly what **Capa-BFF** does. And today I want to share why I built it, how it works, and whether it's right for your next project.

## What is Capa-BFF Anyway?

Capa-BFF is a zero-cost BFF solution that runs entirely as a sidecar next to your existing backend. It gives you:

- Dynamic API aggregation from multiple backend services
- Built-in CORS handling (no more fighting with that)
- Request/response transformation with JSON DSL
- Automatic caching
- Literally zero extra infrastructure cost
- Deploy it anywhere your existing app runs

The core idea is pretty simple: instead of deploying a separate BFF service that talks to your backends, Capa-BFF runs alongside your existing backend service. It intercepts BFF requests, does the aggregation/transformation, and returns the combined response to your frontend.

No extra VMs, no extra containers, no extra bills. Just add the dependency to your existing app and you're done.

## How Does It Actually Work?

Let me show you a real example. Suppose you're building a social media app and your frontend needs:
1. User information from the user service
2. Recent posts from the post service  
3. Unread notification count from the notification service

Without BFF, your frontend has to make three separate requests. That's slow, chatty, and annoying. With Capa-BFF, you define one aggregation endpoint in a simple JSON config:

```json
{
  "name": "userDashboard",
  "aggregations": [
    {
      "name": "user",
      "source": "userService",
      "path": "/users/{userId}",
      "method": "GET",
      "placeholders": {
        "userId": "${request.query.userId}"
      }
    },
    {
      "name": "recentPosts",
      "source": "postService",
      "path": "/posts?authorId={authorId}&limit=10",
      "method": "GET",
      "placeholders": {
        "authorId": "${output.user.id}"
      }
    },
    {
      "name": "unreadNotifications",
      "source": "notificationService",
      "path": "/notifications/unread-count",
      "method": "GET",
      "placeholders": {
        "userId": "${output.user.id}"
      }
    }
  ],
  "cache": {
    "ttlSeconds": 60
  }
}
```

That's it. You save this file to your config directory, drop the Capa-BFF dependency into your Spring Boot app (it currently supports Java/Spring Boot, with more frameworks coming), and boom:

```java
@SpringBootApplication
@EnableCapaBFF
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

Now you have a brand new endpoint at `/bff/userDashboard` that automatically calls all three services, aggregates the results, and returns everything the frontend needs in one single request.

```json
{
  "user": {
    "id": 123,
    "name": "John Doe",
    "avatarUrl": "https://..."
  },
  "recentPosts": [
    { "id": 456, "title": "...", "createdAt": "..." },
    ...
  ],
  "unreadNotifications": 3
}
```

How cool is that? In our hackathon project, this setup took us about 15 minutes to get working instead of the 4+ hours we originally budgeted. That freed us up to work on the actual features that won us the competition.

## The Performance Numbers That Surprised Even Me

I wasn't expecting much in terms of performance when I built this. After all, it's doing extra work on your existing server. But the numbers we got during benchmarking honestly shocked me.

We ran a simple benchmark with 1000 concurrent requests aggregating three backend services:

| Configuration | Average Latency | QPS |
|---------------|-----------------|-----|
| Three separate frontend requests | ~180ms | ~660 |
| Capa-BFF aggregation | ~82ms | ~1200 |

That's **2.2x faster** and **nearly double the throughput** compared to the frontend doing three separate requests. And remember, this is all running on your existing infrastructure.

The 1200 QPS came from a single container with 0.5 vCPU and 256MB memory. We were getting **1200 QPS for 0.8ms average processing overhead** on top of the backend calls. That's nothing. Most of the time, it's just waiting for the backend services to respond in parallel anyway.

Honestly, I thought the overhead would be way higher. But after profiling it for a while, most of the time is spent in JSON parsing and network I/O, which is already optimized pretty well.

## Pros & Cons: Let's Be Real Here

I'm not here to sell you on some perfect solution that solves every problem. Capa-BFF is great for certain use cases, but it's definitely not for everyone. Let me break it down honestly:

### ✅ Pros

1. **Zero extra cost**. I mean it. You don't pay anything extra. It runs on your existing infrastructure. If you're a side project developer like me or working on a startup with limited resources, this is a game-changer.

2. **Extremely fast to get started**. 15 minutes from "What's a BFF?" to "It's working." That's the timeline. No DevOps, no deployment pipelines to update, nothing.

3. **Parallel requests out of the box**. All your aggregations run in parallel automatically. You don't have to write any extra code to make that happen. It just works.

4. **No more CORS headaches**. Capa-BFF handles CORS for you automatically. Your frontend talks to one domain, everything else is proxied through the sidecar. I can't tell you how much time this has saved me over the years fighting CORS configs in different services.

5. **Dynamic updates**. Change your aggregation config? Just update the JSON file and restart. No need to redeploy the entire backend service if you're running it separately (though in our case, it's all together anyway).

### ❌ Cons

1. **Not suitable for very high-traffic production systems**. If you're running Netflix-scale traffic, you probably still want a dedicated BFF deployment. This shares resources with your main backend, so you have to be conscious of that.

2. **Currently only supports Java/Spring Boot**. I know, I know. We're working on Go and Node.js versions, but they're not ready yet. If you're not in the Java ecosystem, you'll have to wait or contribute. (Hey, open source, right?)

3. **JSON DSL only**. Some people want code-level control over their aggregations. The JSON approach is great for most cases, but if you need really complex transformation logic, you might outgrow it. We're planning to add support for custom scripts down the line, but it's not there yet.

4. **Couples your BFF to your main deployment**. If you need to scale BFF independently from your backend, this approach isn't for you. The whole point is that they're together. If you need independent scaling, go with a dedicated BFF service.

## My Personal Journey Building This

I've been building side projects and startups for about 8 years now, and I can't tell you how many times I've run into this exact problem:

> You need a BFF, but you don't want to manage another service.

Every time, I'd end up writing the same boilerplate aggregation code, fighting CORS, setting up caching, doing the same dance over and over again. After doing this for the fifth time, I thought: "Why isn't there an off-the-shelf solution for this that just runs as a sidecar?"

I looked around. Everything I found either required a separate deployment, was too heavyweight, or cost money. I couldn't find anything that fit my use case: "I just want to drop this into my existing app and be done with it."

So I started building Capa-BFF on a train ride home from a conference. Yeah, that's how most of my side projects start – I get bored on a train and start coding. Three hours later, I had a working prototype.

The hackathon came up a month later, and we decided to use it. We won gold, and other teams kept asking us "How did you get everything done so fast?" That's when I realized this thing was actually useful to other people too. So I open-sourced it.

I'll be honest with you – I'm not a full-time maintainer. This is a side project I work on when I have time. But I do review PRs and fix bugs when they come in. It's been pretty stable so far, and we've been using it in production for some internal tools at my day job with zero issues.

## Common Use Cases Where It Shines

From what I've seen so far, Capa-BFF works really well in these scenarios:

1. **Hackathons**. Duh. We won a hackathon with it. Speed is everything, and this gives you a complete BFF in 15 minutes.

2. **Side projects**. You're not made of money. Every extra service you run is another bill. Why run another service when you don't need to?

3. **Internal tools and admin dashboards**. You don't need independent scaling here. You just need something that works with minimal effort.

4. **Early-stage startups**. You're moving fast, you're iterating, you don't want to spend time on infrastructure. Get your product out the door, then worry about splitting services when you actually need to.

5. **Applications where the BFF logic is simple**. Most BFFs are just aggregating data from a few services anyway. That's exactly what this is built for.

## What I Learned Building This

Building Capa-BFF taught me a few lessons that I think are worth sharing:

First, **simplicity beats features every time**. The whole system is about 2,000 lines of code. That's it. It doesn't do a million things. It does one thing really well: aggregates APIs with zero extra deployment. That's all it needs to do.

Second, **sidecar architecture is underrated for side projects and small teams**. Everyone talks about sidecars for service meshes in big Kubernetes clusters, but the same pattern works really well for small apps too. Why split things out before you need to?

Third, **you don't always need the "best practice" architecture**. Best practices say you should have a separate BFF service. That's great if you're a big team with resources. But if you're a solo developer or a small team, sometimes the practical approach is better than the "correct" approach. I'd rather ship something now than over-architecture it and never ship at all.

I know that goes against what all the architecture astronauts tell you, but honestly – most projects don't need Netflix-scale architecture on day one. YAGNI, people. You Ain't Gonna Need It.

## Getting Started

If you want to try Capa-BFF, it's really easy. Just add the dependency to your Spring Boot project:

```xml
<dependency>
    <groupId>cloud.capa</groupId>
    <artifactId>capa-bff-spring-boot-starter</artifactId>
    <version>1.0.0</version>
</dependency>
```

Add the `@EnableCapaBFF` annotation to your application class, create your aggregation configs in `src/main/resources/bff/`, and you're good to go.

Check out the GitHub repository for more detailed examples and documentation.

## Wrapping Up

Capa-BFF isn't going to solve all your problems. It won't replace your dedicated BFF service if you need independent scaling or high availability at massive scale. But for hackathons, side projects, early-stage startups, and internal tools? It's pretty amazing what you can get done with zero extra cost and 15 minutes of setup.

I built it because I needed it, and I open-sourced it because I figured other people probably have the same problem. Maybe you're reading this at 3 AM before your hackathon submission deadline wondering how you're going to get everything done. Give this a shot – it might just save your competition, like it saved ours.

---

## What Do You Think?

I'm curious – do you still deploy separate BFF services for every project, or have you found shortcuts that work for you? Have you tried the sidecar approach for BFF before? Did it work for you, or did you run into problems I didn't mention here?

Drop a comment below and let me know your experience. I'd love to hear how other people are solving this problem.

And if you try Capa-BFF, let me know how it goes! Star the repository if you find it useful – that helps other people find it too.
