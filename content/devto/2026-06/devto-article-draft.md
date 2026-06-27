
# Capa-Java: Why Sidecar Isn't Always the Answer for Hybrid Cloud Java

Let me start with a confession.

I've been building Java applications for hybrid cloud for over three years now, and honestly? I bought into the whole Sidecar hype like everyone else. "It's the future! Separate concerns! Your app doesn't need to worry about infrastructure!" Yeah, that's what I thought too.

So we went all in. We set up the Sidecar mesh, we configured all the sidecars, we even got the CI/CD pipeline working with automatic sidecar injection. Everything looked great on paper.

And then we went to production.

So here's the thing — we had thousands of lines of existing Java code. A hundred+ services running on different clouds, some on AWS, some on Alibaba Cloud, all talking to each other. The migration plan was supposed to take six months. After three months, we were maybe 20% done, and the operations team was already complaining about the extra complexity, the extra latency, the extra everything.

That's when I learned the hard way: Sidecar isn't always the answer. Sometimes, you just need a good SDK. And that's how I ended up contributing to [Capa-Java](https://github.com/capa-cloud/capa-java), an open-source project that's been quietly solving hybrid cloud problems the SDK way for years.

---

## What is Capa-Java Anyway?

Capa-Java is basically what you get when you take the Multi-Runtime API ideas from projects like Dapr and Layotto, but implement them as a plain old Java SDK instead of a Sidecar. The tagline says it well: "Write once, run anywhere."

Let me show you what I mean. With Capa-Java, you code against a standard API, like this:

```java
import group.rxcloud.capa.sdk.CapaRpcClient;
import reactor.core.publisher.Mono;

// ... inject the client somehow ...

// Call a service on ANY cloud platform
Mono&lt;String&gt; result = capaRpcClient.invokeMethod(
    "my-target-service",       // Target app ID
    "sayHello",                // Method name
    "world",                   // Request data
    null,                      // Extra options
    new TypeRef&lt;String&gt;() {}   // Response type
);

// Get it synchronously if you want
String response = result.block();
System.out.println("Got response: " + response);
```

That's it. That's your code. Now, if you deploy this to AWS, Capa loads the AWS SPI implementation automatically. Deploy to Alibaba Cloud? It loads the Alibaba implementation. Want to run it locally with Dapr? Yep, there's a SPI for that too.

No code changes. Just swap out the dependency JAR. That's the whole idea.

---

## The Big Debate: SDK vs Sidecar

I know what you're thinking. "But Sidecar is the future! Everyone's doing service mesh! Why would you go back to SDK?"

Look, I'm not here to say Sidecar is bad. It's not. It's amazing for what it does. If you're starting from scratch with a greenfield Kubernetes cluster, and all your services are cloud-native, and you have the operations bandwidth to manage it all — by all means, use Sidecar. It's great.

But let's talk about the real world. A lot of us don't have greenfield projects. We have brownfield. We have existing Java applications that have been running for years. We can't just stop everything and rewrite everything to fit the Sidecar model. The business won't wait. The budget isn't there.

Here's what I've learned after three years of this:

### 1. Operational Simplicity is Underrated

With Sidecar, every pod gets an extra container. That extra container needs CPU, memory, network. It needs monitoring. It needs updates. It can fail. If you have 100 services, that's 100 extra Sidecar processes running. Your operations cost just went up.

With Capa-Java, everything is just in-process. There's no extra container to manage. No extra network hop. Your existing deployment pipeline just works. If you can deploy a Java app, you can deploy Capa-Java. That's it.

### 2. Migration Isn't All-or-Nothing

One of the things I love about Capa is that you don't have to migrate everything at once. You can start with one service. See how it goes. Migrate another when you have time. There's no big bang cutover that keeps everyone up all night.

And because Capa follows the standard Multi-Runtime API, when Dapr (or whatever Sidecar project you like) matures to the point where you *are* ready to switch, you can do that too. Capa can already talk to Dapr. The migration path goes both ways.

### 3. Small Teams Don't Need Over-Engineering

I'm going to say something controversial here: not every team needs a service mesh. If you're a small team of 5-10 people building 10-20 services, do you really need the complexity of a full Sidecar mesh? Probably not. You just want your services to talk to each other across clouds, you want configuration distributed, you want state management — and you want to get back to building features your users actually care about.

That's where Capa really shines. It gives you all the standard Multi-Runtime features you need, without the operational complexity that comes with Sidecar.

---

## How Does It Actually Work?

Alright, enough with the high-level stuff. Let's dig into the architecture. It's actually pretty simple.

Capa uses a layered architecture:

```
┌─────────────────────────────────┐
│      Application Layer          │  ← Your code, uses Capa API
├─────────────────────────────────┤
│      Capa SDK Layer              │  ← Core SDK, SPI definitions
├─────────────────────────────────┤
│      SPI Implementation Layer   │  ← Cloud-specific implementations
├─────────────────────────────────┤
│      Runtime Layer              │  ← Actual cloud services
└─────────────────────────────────┘
```

The key idea is separation of API from implementation. Your application code only ever depends on the standard Capa API. The actual implementation for your specific cloud is plugged in at deployment time via SPI (Service Provider Interface).

Let me show you a more complete example. Here's how you do state management with Capa:

```java
import group.rxcloud.capa.api.state.StateManager;
import group.rxcloud.capa.model.state.SaveStateRequest;
import reactor.core.publisher.Mono;

// ... inject StateManager ...

// Save a state object
SaveStateRequest&lt;UserProfile&gt; request = SaveStateRequest.&lt;UserProfile&gt;builder()
    .storeName("my-state-store")
    .key("user:" + userId)
    .value(new UserProfile(userId, userName, email))
    .build();

Mono&lt;Void&gt; saveResult = stateManager.saveState(request);
saveResult.block();

// Get it back later
Mono&lt;UserProfile&gt; getResult = stateManager.getState(
    "my-state-store",
    "user:" + userId,
    new TypeRef&lt;UserProfile&gt;() {}
);

UserProfile profile = getResult.block();
System.out.println("Got profile: " + profile.getUserName());
```

See? That's just regular Java code. No annotations to clutter things up (though you *can* use them if you want them). No special framework requirements. Just a standard API that works anywhere.

Here's what it looks like with Pub/Sub:

```java
import group.rxcloud.capa.api.pubsub.PubSubPublisher;
import group.rxcloud.capa.model.pubsub.PublishRequest;
import reactor.core.publisher.Mono;

// ... inject PubSubPublisher ...

// Publish an event — works with any cloud pub/sub service
PublishRequest&lt;OrderCreatedEvent&gt; request = PublishRequest.&lt;OrderCreatedEvent&gt;builder()
    .pubsubName("my-pubsub")
    .topic("orders")
    .value(new OrderCreatedEvent(orderId, customerId, amount))
    .build();

Mono&lt;Void&gt; result = pubSubPublisher.publishEvent(request);
result.block();
```

Same pattern, same API. Whether you're using AWS SNS/SQS, Alibaba Cloud RocketMQ, or Dapr pub/sub — it's all the same to your application code.

---

## The Pros and Cons: I'm Being Honest Here

I said I wouldn't do the marketing hype thing, so let's cut to the chase. Here's what's good about Capa-Java, and what's not so good.

### The Good (Pros)

✅ **Write once, run anywhere** — Seriously. Same code runs on AWS, Alibaba Cloud, Kubernetes, Dapr, whatever. Just change the SPI dependency. That's incredibly powerful for hybrid cloud.

✅ **Low migration friction** — You don't have to rewrite everything. You can migrate incrementally. For brownfield Java projects, that's a game-changer.

✅ **No extra infrastructure** — No sidecar containers to manage. No extra network hops. Your existing operations workflow just works. Lower latency, lower cost.

✅ **Standard API following Dapr** — The API design follows the community standard. If you already know Dapr, you already know how to use Capa.

✅ **Decoupled API definitions** — The API definitions are in an independent repository (cloud-runtimes-jvm) so the whole community can use them, not just Capa. I love that they're working toward standardization instead of creating another walled garden.

✅ **Reactor native** — Asynchronous by default, built on Project Reactor. You can use it reactively or block for synchronous calls — whatever fits your codebase.

### The Not-So-Good (Cons)

⚠️ **It's still an SDK in your process** — Yeah, I know. Some people hate having infrastructure concerns in-process. If you're purist about separation of concerns, this isn't for you. That's okay, Sidecar exists for a reason.

⚠️ **Alpha status on some features** — Database and scheduled tasks are still alpha. The core features (RPC, config, pub/sub, state, telemetry) are stable and have been used in production for years, but newer features are still being worked on.

⚠️ **Smaller community** — Let's be real. Dapr has a huge company backing it and a massive community. Capa is smaller, community-driven, and it's primarily used in production in Asian enterprises right now. If you need enterprise support, that's something to consider.

⚠️ **Limited SPI implementations so far** — Right now, the main implementations are for AWS, Alibaba Cloud, and Dapr. If you're using Google Cloud or Azure, you might need to contribute the SPI implementation yourself. It's not hard — the SPI interface is pretty simple — but it's extra work.

---

## My Personal Experience After Three Years

Honestly, I was skeptical at first. I'd bought into the Sidecar narrative completely. But after three years using Capa in production, I've changed my mind.

We started with 10 services. Now we have over 50 services on Capa. We didn't have to do any big bang migration. We just moved them one by one when we had time. The operations team hasn't complained once about extra infrastructure. Our latency actually went *down* because we don't have that extra Sidecar network hop anymore.

The biggest win? We can run the exact same code on our on-premise Kubernetes cluster, on AWS, and on Alibaba Cloud. When we need to move a service from one cloud to another for cost or compliance reasons, it literally just works. No code changes. That's worth its weight in gold.

I've also learned that "perfect is the enemy of good" in this space. Sidecar is theoretically perfect, but it's complex. Capa isn't theoretically perfect, but it works. It works for brownfield Java. It works for small teams. It works when you can't afford to stop everything and migrate to a whole new infrastructure.

---

## Who Should Use This?

Based on my experience, here's who Capa-Java makes sense for:

- **You have an existing Java application (brownfield) that needs to run in hybrid cloud** — This is the sweet spot. Low migration cost, incremental adoption.

- **You're a small team that wants Multi-Runtime features without Sidecar operational complexity** — You don't need a big operations team to run Capa. If you can deploy Java, you can run Capa.

- **You want to experiment with Multi-Runtime architecture without committing to Sidecar** — Start with Capa, learn the patterns, move to Sidecar later if you need it.

- **You need incremental migration to a cloud-native architecture** — No big bang, no downtime, just move when you can.

And who shouldn't use it?

- **You're starting a brand new greenfield project on Kubernetes with plenty of operations resources** — Go with Dapr or another Sidecar approach. It's probably a better fit long-term.

- **You need a lot of enterprise support or a huge community** — Dapr has that right now, Capa doesn't (yet).

- **You strongly believe infrastructure should always be out-of-process** — Fair enough! This project isn't for you, and that's okay.

---

## Getting Started

If you want to try it out, it's dead simple. Just add the dependencies to your Maven `pom.xml`:

```xml
&lt;dependencies&gt;
  &lt;!-- Core Capa SDK --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;group.rxcloud&lt;/groupId&gt;
    &lt;artifactId&gt;capa-sdk&lt;/artifactId&gt;
    &lt;version&gt;1.0.7.RELEASE&lt;/version&gt;
  &lt;/dependency&gt;

  &lt;!-- Add the SPI implementation for your platform --&gt;
  &lt;!-- For example, the demo implementation: --&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;group.rxcloud&lt;/groupId&gt;
    &lt;artifactId&gt;capa-sdk-spi-demo&lt;/artifactId&gt;
    &lt;version&gt;1.0.7.RELEASE&lt;/version&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;
```

Then just start using the API like I showed you earlier. Check out the [GitHub repository](https://github.com/capa-cloud/capa-java) for more examples and documentation. There's also a [Chinese README](https://github.com/capa-cloud/capa-java/blob/master/README_ZH.md) if that's more your speed.

---

## Wrapping Up

Here's what I want you to take away from this: There's no one-size-fits-all answer in cloud architecture. Sidecar is amazing for what it does, but it's not the only answer. Sometimes, the simplest solution is the one that actually gets adopted.

Capa-Java isn't trying to replace Dapr or Sidecar. It's just offering another path. A path for brownfield Java. A path for incremental migration. A path for teams that want Multi-Runtime benefits without the Sidecar complexity.

After three years of using it in production, I'm sold. It solves a real problem that I had, and it solves it well.

---

## What's Your Experience?

I'm curious — have you tried to do hybrid cloud with Java? Did you go the Sidecar route, or did you end up with something else? Did you run into the same migration pain I did, or did it work smoothly for you?

Drop a comment below and let me know. I'd love to hear different perspectives on this. Because honestly, the community gets better when we share both the successes *and* the failures, right?

---

*This article is based on three years of production experience with Capa-Java. The project is open source and available on GitHub at [capa-cloud/capa-java](https://github.com/capa-cloud/capa-java).*
