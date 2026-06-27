# Building Dog Agent: Why I Built an AI-Powered Community for Dog Walking Adventures (And What Broke Along The Way)

Honestly, I never thought I'd be writing a technical article about building an app for my dog. Three months ago, if you told me I'd spend 80+ hours coding something just so my golden retriever could find new walking routes, I'd laugh at you. But here we are — and honestly, it's been one of the most surprisingly fun side projects I've built in years.

Let me back up. My dog, Max, is three years old and has the energy of a thousand puppies. Every single day we go walking, and every single day he expects a new route. If we repeat the same route too many times, he gets bored halfway through, plants his butt on the sidewalk, and refuses to move. I'm not kidding — that's actually what started this whole project.

I tried all the usual apps: AllTrails, Google Maps, even some dog-specific walking apps. But none of them really solved *my* problem. I didn't need popular hiking trails 50 miles away from the city. I needed to find interesting, new neighborhood walks within a 2-mile radius, shared by other local dog people who actually walked them. And I wanted AI to help recommend routes that matched our energy level — sometimes we want a quick 20-minute loop, sometimes we want a two-hour adventure with lots of grass and places to swim.

So I did what any engineer does when their dog is bored: I built my own app. That's how Dog Agent was born.

## What is Dog Agent?

Dog Agent is an open-source AI-powered community for dog walking adventures. It lets you:
- Share your favorite dog walking routes
- Discover new routes near you based on location and distance
- Get AI recommendations that match your energy level and dog's personality
- Save your favorite routes and keep track of where you've gone
- All photos are automatically compressed to save on storage (trust me, you need this)
- Privacy-first: all your personal data stays under your control, we don't sell anything to anyone

The tech stack looks like this:
- **Backend**: Go (because it's fast, simple, compiles to a single binary — perfect for side projects)
- **Mobile App**: React Native (so it works on both iOS and Android, I only have to write it once)
- **Database**: PostgreSQL with PostGIS extension for spatial queries (more on this magic later)
- **AI**: OpenAI text-embedding-3-small for route recommendations + cosine similarity matching
- **Storage**: Cloudflare R2 for photos (no egress fees — game-changer for side projects)

You can check out the full code here: https://github.com/kevinten10/dog-agent

Honestly, it's still in beta. Android testing is mostly done but we're ironing out a few kinks. But it already works well enough that a handful of local dog owners are using it every day. So I wanted to share what I learned building it — the good, the bad, and the "why did my bill jump $80 in one month" part.

## The Good Stuff: PostGIS Changed Everything

When I started this project, I knew I'd need to do spatial queries — like "find all routes within 2 miles of my current location". I started off thinking I'd need a separate spatial database like Elasticsearch or something fancy. But then I remembered: PostgreSQL has PostGIS, and it's actually really good at this stuff.

I learned the hard way that you don't need a fancy specialized spatial database for most side project spatial needs. PostGIS does everything I need, and it's already part of your normal PostgreSQL setup if you enable the extension.

Here's basically how I set it up:

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Create routes table with geography column for location
CREATE TABLE routes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  location GEOGRAPHY(Point, 4326) NOT NULL, -- 4326 is WGS84, standard for GPS
  distance_km DOUBLE PRECISION NOT NULL,
  estimated_minutes INTEGER NOT NULL,
  difficulty INTEGER NOT NULL, -- 1-5 scale
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_by UUID REFERENCES users(id)
);

-- Create spatial index — this makes queries fast!
CREATE INDEX idx_routes_location ON routes USING GIST (location);
```

And then querying for nearby routes is *so* simple:

```go
// Go code example: find all routes within 2km of current location
query := `
  SELECT 
    id, name, description, distance_km, estimated_minutes, difficulty,
    ST_Distance(location, ST_SetSRID(ST_MakePoint($1, $2), 4326)) AS dist
  FROM routes
  WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint($1, $2), 4326), $3 * 1000)
  ORDER BY dist
  LIMIT 20
`
rows, err := db.Query(query, lng, lat, radiusKm)
```

That's it. That's the whole spatial query. 100x simpler than I thought it would be, and it's fast. Even with a few thousand routes, queries return in 20-30ms. I was shocked.

The key lesson here: don't overcomplicate things. PostGIS does 99% of what most people need for spatial applications. You don't need a fancy specialized solution until you have *millions* of routes. For a side project like this, it's perfect.

## The AI Part: Simple is Better Than Complex

Here's the thing about AI recommendation for something like this: you don't need to train a whole model from scratch. I thought about fine-tuning a model to learn what kind of routes Max likes, but honestly... that's overkill.

What I do instead is:
1. When a user creates a route, they write a short description: "flat walking trail with lots of grass, creek access for dogs, not too crowded"
2. I generate an embedding for that description using OpenAI's text-embedding-3-small
3. When a user says "I want a flat walk with creek access", I generate an embedding for their query
4. I compute cosine similarity between the query embedding and all route embeddings
5. Sort by similarity + distance, return the top matches

That's it. That's the whole AI recommendation system. ~50 lines of code, and it works shockingly well.

Here's the embedding generation code in Go:

```go
package main

import (
	"context"
	"github.com/sashabaranov/go-openai"
)

type EmbeddingService struct {
	client *openai.Client
}

func NewEmbeddingService(apiKey string) *EmbeddingService {
	return &EmbeddingService{
		client: openai.NewClient(apiKey),
	}
}

func (e *EmbeddingService) CreateEmbedding(ctx context.Context, text string) ([]float32, error) {
	resp, err := e.client.CreateEmbeddings(ctx, openai.EmbeddingRequest{
		Input: []string{text},
		Model: openai.SmallEmbedding3,
		Dimensions: 512,
	})
	if err != nil {
		return nil, err
	}
	return resp.Data[0].Embedding, nil
}

// Cosine similarity between two embeddings
func CosineSimilarity(a, b []float32) float32 {
	var dotProduct float32
	var magA float32
	var magB float32
	for i := range a {
		dotProduct += a[i] * b[i]
		magA += a[i] * a[i]
		magB += b[i] * b[i]
	}
	if magA == 0 || magB == 0 {
		return 0
	}
	return dotProduct / (sqrt(magA) * sqrt(magB))
}
```

I use 512 dimensions instead of the full 1536 — this cuts embedding size by 2/3, and I haven't noticed any difference in recommendation quality for my use case. The cost? Insignificant. 512 dimensions is 512 floats per embedding — that's 2KB per route. Even with 10,000 routes that's 20MB. Nothing.

And the cost for the OpenAI API? $0.00002 per embedding. So even generating 1,000 embeddings costs two cents. Are you kidding me? That's nothing.

I was worried this approach would be too simple, but honestly — it works better than I expected. Users get recommendations that actually match what they're asking for, and I don't have to maintain any complex AI infrastructure.

## The Surprising Pains I Didn't Expect

Okay, let's get real. Not everything went smoothly. Here are the three biggest pains that caught me completely off guard.

### 1. Mapbox Pricing Got Me

I started off using Mapbox for maps in the React Native app. Their free tier is 50,000 monthly active users — that sounds like way more than I'd ever need for a local dog walking app, right? Wrong.

Wait, no — actually, I misread the pricing. Mapbox pricing is *per month*, and it's based on monthly active users. But the catch: if you go over the free tier, you don't just get charged for the overage — you get charged *retroactively for all your users*. So when I had 12 local dog owners start using it regularly, I got a bill for $80. For twelve users. That's more than my entire server cost.

I was shocked. I knew Mapbox wasn't cheap, but I didn't expect that pricing model. So I'm currently evaluating alternatives — Google Maps has a better pricing model for small apps, and there's also MapLibre which is open source. I haven't switched yet, but that's definitely on the roadmap.

Lesson learned: *always* read the fine print on pricing before you integrate a third-party service. Even if it says "free tier", make sure you understand what happens when you grow past it.

### 2. Image Compression is Non-Negotiable

When users upload photos of their walks and their dogs, those photos are huge — like 12MP from a modern phone, 4-5MB per photo. If you just store them as-is and serve them directly, you'll burn through storage and bandwidth super fast.

I learned this the hard way after a week: 50 photos uploaded, and we'd already used 200MB of storage. That doesn't sound like much, but it adds up quickly — especially if the app grows.

So I added automatic image compression on the client before upload. In React Native, it's pretty straightforward with the `react-native-image-compressor` package:

```javascript
import ImageCompressor from 'react-native-image-compressor';

const compressedImage = await ImageCompressor.compress(imageUri, {
  quality: 0.7,
  maxWidth: 1200,
  maxHeight: 1200,
});
```

That's it. This drops most photos from 4-5MB down to 200-300KB without any noticeable quality loss for mobile viewing. 10x smaller. Game-changer. I should have done this from day one — don't make the same mistake I did.

### 3. Privacy Matters — Even for a Dog Walking App

Because this is a community app, users share their current location and their favorite routes. I thought about making all routes public by default, but then I thought: what if someone shares their favorite secret spot that's really quiet, and then a hundred people show up the next weekend? That ruins it for everyone.

So I added privacy controls: you can choose for each route whether it's:
- Public (visible to everyone)
- Unlisted (visible only to people with the link)
- Private (only visible to you)

This way, people can keep their favorite secret spots secret if they want. I think that's really important — especially for things like hiking and dog walking where overuse can ruin a good thing.

And because all user authentication is done with good old email/password and JWT, and photos are stored in my own Cloudflare R2 bucket, I don't have to send user data to a third party for storage. That's a win for privacy, and it keeps costs predictable.

## Pros and Cons: Let's Be Honest

I think too many project READMEs just list all the good stuff and ignore the bad. So here's my honest Pros and Cons breakdown for Dog Agent, and for this approach to building an AI-powered community app:

### Pros

1. **Solves a real personal problem**: This isn't a project built for "learn AI" or "get a VC deal" — I built it because I actually needed it. That keeps you motivated when things get frustrating.

2. **Simple architecture, easy to hack**: No fancy microservices, no Kubernetes, just Go backend + React Native app + PostgreSQL. You can get the whole thing running locally in 10 minutes if you know what you're doing.

3. **Privacy by design**: Users control their own data, no selling user data, everything is open source so you can self-host if you want.

4. **Cost is almost nothing**: For 100 active users, my total monthly cost is: Server $5, Cloudflare R2 $0.10, OpenAI embeddings $0.50. That's it. Way cheaper than I expected.

5. **AI doesn't have to be complicated**: Simple embeddings + cosine similarity gets you 80% of the way for most recommendation use cases, and it's super cheap and easy to maintain.

### Cons

1. **Still beta, Android not fully tested**: I'm an iOS user, so Android testing has been slower. If you're an Android developer and want to help, PRs are welcome!

2. **Mapbox dependency still needs replacing**: As I mentioned earlier, the pricing is scary for growth. We're working on switching to MapLibre.

3. **No social features yet**: No comments, no likes, no following other dog walkers. That's on the roadmap, but it's not done yet.

4. **Requires your own OpenAI API key if you self-host**: That's not a big deal for developers, but it does mean non-technical users can't just spin it up easily.

5. **Recommendation quality depends on user descriptions**: If people write bad descriptions, recommendations are bad. That's inherent to this approach. I'm working on automatically extracting better descriptions from metadata, but it's not perfect yet.

## What I Learned Building This

Honestly, this project surprised me. I started it as a silly side project to keep my dog happy, and I ended up learning a bunch of stuff I didn't expect:

1. **The best side projects solve your own problems**: If you have a real problem you're actually annoyed by, you'll stick with it longer and build something better than if you build something you don't care about just because it's trendy.

2. **Simple almost always beats complex**: I didn't need a fancy vector database — PostgreSQL does the job just fine for this scale. I didn't need to fine-tune a large language model — simple embeddings work great. Keep it simple.

3. **Pricing surprises will get you**: Always check third-party pricing multiple times. I thought I understood Mapbox pricing, and I still got surprised.

4. **Privacy isn't just for "big apps"**: Even a small dog walking app needs to think about privacy — both for users and for the places they share. Giving users control over who can see their routes is the right thing to do.

5. **Dog owners love talking about their dogs**: Who knew? Local dog owners have been really excited about this app, and the community is growing faster than I expected. People actually want this.

## Try It Out

If you're a dog owner who gets bored walking the same route every day, or you're a developer who wants to hack on an open source AI side project, go check it out: https://github.com/kevinten10/dog-agent

It's completely open source, you can self-host it, you can contribute, you can fork it and build your own version. All I ask is that you star the repo if you think it's interesting — that helps other people find it.

## Wrapping Up

So here we are — three months and 80+ hours later, we have a working AI-powered dog walking community app that my dog actually approves of (he still sometimes refuses to move, but that's just him being a golden retriever). It's not perfect, but it works, it solves a real problem, and I had a ton of fun building it.

I think that's what side projects are supposed to be about, right? You don't have to build the next unicorn. Sometimes you just build something that makes your daily life a little better, and maybe it helps other people too.

---

## Your Turn

Have you ever built a side project to solve a really specific personal problem? Did it turn into something bigger than you expected? And if you're a dog owner — have you ever had your dog refuse to walk because they were bored of the route? Let me know in the comments below!
