# Capa-Java: The Service Discovery Lie We Tell Ourselves in Multi-Cloud

When I started building Capa-Java, I thought service discovery was solved. DNS round-robin, health checks, maybe some Consul or Eureka if you're fancy. How hard could it be?

Eighteen months later, I've realized that service discovery in multi-cloud environments is one of those problems that looks simple until you actually try to solve it. And the "solutions" we've convinced ourselves work? They're mostly polite fiction.

Let me share what I learned from watching service discovery fail in production across 7 different cloud providers.

---

## The DNS Illusion

Everyone starts with DNS. It's simple, it's universal, it's been around forever. Want load balancing? Just add multiple A records. Want failover? Set low TTL and update when things break.

Here's what actually happens in multi-cloud:

**Scenario**: You have a service running on AWS, Azure, and GCP. Each cloud has its own DNS-based load balancer. You configure your application to use the service endpoint.

**The Problem**:
- AWS Route53 returns endpoints weighted by your configuration
- Azure Traffic Manager returns endpoints based on geographic proximity
- GCP Cloud DNS returns endpoints in the order you defined

When a client makes a request, which endpoint do they get? The answer depends on:
- Which DNS resolver they're using
- Which cloud provider's DNS that resolver prefers
- The phase of the moon (okay, not really, but it feels like it)

**What I learned**: DNS is not service discovery. DNS is "here's a list of IPs in some order, good luck." Real service discovery needs to understand:
- Which instances are actually healthy (not just "responding to ping")
- Which instances have capacity
- Which instances are in the same failure domain as the caller
- Which instances have the features the caller needs

DNS answers none of these. It just gives you addresses.

---

## The Health Check Theater

Okay, so DNS isn't enough. Let's add health checks. A simple `/health` endpoint that returns 200 if the service is working, right?

Here's a real production incident from our testing:

A service in Azure was returning 200 on its health endpoint but failing 40% of actual requests. The health check said "I'm alive" but didn't verify "I can actually do my job."

**What was happening**:
- The application was running
- The HTTP server was accepting connections
- The database connection pool was exhausted
- Every real request was timing out

The health check passed because it didn't try to use the database.

**The deeper problem**: Health checks check if a process is running. They don't check if a service is *functional*.

We had to build what we call "semantic health checks" - health endpoints that actually exercise the critical paths:
- For a database service: run a simple query
- For a cache service: set and get a value
- For an API service: make a real downstream call

But this creates a new problem: semantic health checks are expensive. They consume resources, they add latency, they can even cause cascading failures if you're not careful.

**What I learned**: A health check that doesn't test functionality is theater. A health check that does test functionality is a potential liability. The balance is the hardest part.

---

## The Cross-Cloud Latency Trap

Here's something that caught us completely off guard:

We had a service deployed across AWS and Azure. Same instance types, same configuration, same code. Response times should be similar, right?

AWS to AWS: 12ms average
Azure to Azure: 15ms average
AWS to Azure: 180ms average

Wait, what?

The cross-cloud latency wasn't just higher - it was *15x higher*. And it wasn't consistent. Sometimes it was 50ms, sometimes it was 400ms.

**The root causes**:
- Egress costs mean traffic routes through the cheapest path, not the fastest
- Different clouds have different peering arrangements
- Cross-cloud traffic often goes through public internet exchanges
- Encryption/decryption overhead at cloud boundaries

**What this means for service discovery**:

If your service discovery returns endpoints across clouds without considering latency, you're going to have a bad time. A "healthy" endpoint that's 400ms away might be worse than a "degraded" endpoint that's 10ms away.

We had to build latency-aware discovery that:
- Tracks real latency to each endpoint
- Prefers endpoints with acceptable latency
- Falls back to cross-cloud only when necessary
- Has different latency budgets for different operations

**What I learned**: In multi-cloud, "healthy" isn't binary. A healthy but distant endpoint might be worse than a degraded but nearby one.

---

## The Metadata Complexity Spiral

Service discovery is supposed to tell you where services are. But in production, you need to know much more:

- Is this instance in the canary deployment or stable?
- What version is it running?
- Does it support the new API?
- Is it in the same region as the caller?
- What tenant does it belong to?

We started with simple key-value metadata. Then we needed:
- Hierarchical metadata (region > zone > cluster)
- Computed metadata (derived from other metadata)
- Dynamic metadata (changes based on runtime state)
- Scoped metadata (visible only to certain callers)

Before long, our "simple" service discovery had a metadata system more complex than most databases.

**The trap**: You think you're just tracking endpoints. You're actually building a distributed configuration system with consistency requirements, access control, and query semantics.

**What I learned**: Metadata isn't optional. Every service discovery system eventually becomes a metadata system. Plan for it from the start.

---

## The CAP Theorem Punches You in the Face

You know CAP theorem. Consistency, Availability, Partition tolerance - pick two.

In multi-cloud service discovery, you don't get to pick. Network partitions between clouds are a fact of life. You *will* have partitions. The question is: what breaks when they happen?

**Scenario**: A partition isolates AWS from Azure.

If you choose consistency:
- Service discovery becomes unavailable during the partition
- Services can't find each other even within the same cloud
- Everything breaks

If you choose availability:
- AWS services see one view of the world
- Azure services see a different view
- When the partition heals, you have to reconcile conflicts

**What we actually did**:

We went with eventual consistency, but with a twist:
- Each cloud has its own discovery domain
- Cross-cloud discovery is a separate, slower path
- Services prefer same-cloud endpoints
- Cross-cloud is opt-in for specific use cases

This means we accept that during a partition, services can't discover cross-cloud endpoints. But same-cloud discovery keeps working.

**What I learned**: In multi-cloud, you're not choosing between C and A. You're choosing what *fails gracefully* during a partition.

---

## The Costs Nobody Talks About

Service discovery isn't free. In multi-cloud, it's surprisingly expensive.

**Direct costs**:
- DNS queries (Route53 charges $0.40 per million queries)
- Health check probes (across 1000 instances, every 10 seconds = 8.6M checks/day)
- Cross-cloud traffic (health check traffic alone can be significant)
- Control plane resources (storing and replicating state)

**Hidden costs**:
- Every microsecond of discovery latency adds to request latency
- Failed discovery attempts waste caller resources
- Stale data causes requests to fail
- Debugging discovery issues takes enormous engineering time

We discovered that our "lightweight" discovery system was costing more in operational overhead than some of our actual services.

**What I learned**: Service discovery is infrastructure. It needs the same rigor as databases, message queues, and load balancers. Treat it accordingly.

---

## What Actually Works

After all these lessons, here's what our service discovery looks like now:

1. **Layered Discovery**: DNS for bootstrapping, dedicated discovery for runtime
2. **Semantic Health Checks**: Expensive but necessary for catching silent failures
3. **Latency-Aware Routing**: Track real latency, not theoretical topology
4. **Metadata-First Design**: Everything is metadata, even "simple" endpoints
5. **Eventual Consistency with Bounded Staleness**: Accept delays, but not forever
6. **Isolation by Default**: Each cloud is its own domain, cross-cloud is explicit

Is it perfect? No. Do we still have incidents? Yes. But at least now they're the kind we can understand and fix.

---

## The Question

If you've built multi-cloud systems: what's the one thing about service discovery that surprised you most? The thing you wish someone had told you before you started?

I'm genuinely curious, because I'm still not sure we've found all the edge cases.
