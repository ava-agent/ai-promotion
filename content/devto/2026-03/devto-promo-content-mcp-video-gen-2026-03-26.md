---
title: "I got tired of paying for AI video generators, so I built one that uses free tiers instead"
published: false
description: "A multi-provider MCP server that routes video generation to free tiers - because my wallet couldn't handle another $50/month subscription"
tags: ai, opensource, video, mcp
---

## So here's the thing

I was spending way too much money on AI video generators.

Like, embarrassingly too much. We're talking $49/month for one tool, another $39 for another, plus API calls that somehow always cost more than expected. At one point I was paying over $120/month just to generate short video clips for side projects.

The worst part? I wasn't even using them that much. I'd get excited about a project, generate maybe five videos, then forget about it for weeks. But those subscriptions kept charging me anyway.

Yeah, I know. Not my smartest financial move.

## The breaking point

Last month I wanted to create a short demo video for a hackathon project. Just something simple - 5 seconds, text-to-video, nothing fancy.

I checked my usual tool. Subscription expired. Fine, I'll renew. But then I saw the new pricing: $59/month minimum for video generation. For five seconds of video?

I sat there staring at the checkout page thinking, "There's got to be a better way."

## Turns out, there is

I'd been following the AI video space and noticed something interesting: almost every provider offers some kind of free tier or trial credits.

- CogVideoX (智谱清影): **Completely free, no daily limits**
- Alibaba's Wan model: **50 seconds free for new users**
- Kling AI: **66 credits/day on their web UI**
- SiliconFlow: **$1 signup bonus**

The problem was managing all of them. Each has its own API, its own documentation, its own quirks. I didn't want to write integration code for seven different providers just to make a demo video.

So I built something to solve that.

## What I built

**mcp-video-gen** is a Model Context Protocol (MCP) server that acts as a unified interface for multiple AI video, speech, and music generation providers.

GitHub: https://github.com/kevinten-ai/mcp-video-gen

The idea is simple: you describe what video you want, and it routes your request to the most appropriate provider based on availability, quality needs, and - importantly - whether you have free credits left.

## The architecture (because you're probably curious)

Honestly, I started with a mess of if-statements. Don't judge me - I was prototyping. But once it grew beyond three providers, I had to actually think about the design.

Here's what I landed on:

```
┌─────────────────────────────────────────┐
│           MCP Server Layer              │
│  - Tool definitions                     │
│  - Request routing                      │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────┐           ┌────▼────┐
│ Video  │           │ Audio   │
│Router  │           │Router   │
└───┬────┘           └────┬────┘
    │                     │
    │    ┌──────────────┐ │
    └───►│  Providers   │◄┘
         │              │
         │ • CogVideoX  │
         │ • Wan/DashScope│
         │ • Kling AI   │
         │ • SiliconFlow│
         │ • Vidu       │
         │ • MiniMax    │
         │ • Google Veo │
         └──────────────┘
```

Each provider implements a common `BaseProvider` interface. The router picks the best available provider based on:

1. **Cost priority** (free tiers first)
2. **Quality requirements** (some providers support 1080p)
3. **Provider availability** (some get overloaded)

## Code that actually works

Here's how simple it is to use from Claude Code:

```bash
# Add the MCP server
claude mcp add -s user mcp-video-gen \
  --env COGVIDEO_API_KEY=your_key \
  --env DASHSCOPE_API_KEY=your_key \
  --env SILICONFLOW_API_KEY=your_key \
  -- uv --directory /path/to/mcp-video-gen run video-gen
```

Then in Claude:

```
> Generate a 5-second video of a cat typing on a laptop

I'll generate that video using the most cost-effective available provider.

[Uses CogVideoX-Flash - free tier]

Your video is ready: output/cat_typing_20240326.mp4
Resolution: 1440x960, Duration: 6 seconds
Provider: CogVideoX-Flash (free tier)
Cost: $0.00
```

The code behind the video generation is straightforward Python:

```python
async def generate_video(
    prompt: str,
    provider: Optional[str] = None,
    width: int = 720,
    height: int = 480,
    duration: int = 5
) -> str:
    """Generate video using the best available provider."""
    
    # If no provider specified, pick the cheapest available
    if provider is None:
        provider = router.select_provider(
            width=width,
            height=height,
            duration=duration,
            priority="cost"  # Free tiers first
        )
    
    # Generate and download
    result = await providers[provider].generate(
        prompt=prompt,
        width=width,
        height=height,
        duration=duration
    )
    
    return result.video_path
```

## What about audio?

I ended up adding TTS and music generation too, because why not? MiniMax has decent speech synthesis and their music model is surprisingly good.

```python
# Generate speech
await generate_speech(
    text="Welcome to my presentation",
    voice_id="affectionate_girl",
    speed=1.0
)

# Generate background music
await generate_music(
    prompt="Upbeat electronic music for a tech demo",
    lyrics="[Verse]\nBuilding the future..."
)
```

## Honest pros and cons

**Pros:**
- Actually saves money (I've generated 30+ videos this month, total cost: $0)
- No vendor lock-in - switch providers anytime
- Claude Code integration means I can describe videos in natural language
- All providers use the same interface

**Cons:**
- Free tiers have limitations (CogVideoX gets overloaded during peak hours)
- Video quality varies by provider (CogVideoX is good, MiniMax is better but paid)
- Some providers require Chinese phone numbers for registration
- You need to manage multiple API keys
- Free credits expire (Alibaba's 50s expires after 90 days)

## When should you use this?

**Good for:**
- Side projects and prototypes
- Content creators on a budget
- Developers who want to experiment with AI video
- Anyone tired of subscription fatigue

**Not ideal for:**
- Production systems requiring consistent quality
- High-volume commercial use (respect rate limits)
- When you need guaranteed 1080p output (some free tiers cap at 720p)
- If you hate managing API keys

## The real reason I built this

Honestly? I was frustrated.

Every AI video tool wants $40-60/month. That's $500-700 per year just for occasional video generation. For hobby projects and experiments, that's absurd.

The providers offer free tiers because they want users to try their services. But accessing those free tiers requires jumping through hoops - different APIs, different auth methods, different quirks.

This MCP server is basically a bridge. It lets me (and now you) access all those free tiers through a single, consistent interface.

## Fair warning

This isn't a magic bullet. Free tiers have limits:

- CogVideoX is free but can be slow during peak times
- Alibaba's Wan gives you 50 seconds, then you pay
- Kling's free credits only work on their web UI, not API
- Google Veo is expensive (but high quality)

If you're generating hundreds of videos per month, you'll eventually hit limits or need to pay. But for side projects? This has saved me hundreds of dollars.

## Try it yourself

If you're curious:

```bash
git clone https://github.com/kevinten-ai/mcp-video-gen.git
cd mcp-video-gen

# Install dependencies
uv sync

# Set up at least one provider API key
export COGVIDEO_API_KEY="your_key_here"

# Run the server
uv run video-gen
```

Or just add it to Claude Code and start generating videos through conversation.

## What do you think?

Am I being too cheap? Or is $50/month for occasional video generation actually unreasonable?

I'd love to hear about your experience with AI video tools. Have you found any hidden free gems? Hit me up in the comments.

---

*P.S. - If this saves you money, consider starring the repo. It helps other people find it, and honestly, that feels pretty good.*
