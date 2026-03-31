# English Agent: What I Learned Building an AI Language Tutor That Actually Teaches

Six months ago, I shipped my first AI-powered language learning app. I thought it would be simple—hook up an LLM, add some conversation prompts, done. What I didn't expect was to spend the next half year deep in the weeds of context management, real-time adaptation, and the surprisingly complex problem of making AI feedback feel... human.

This is the story of building English Agent, and the architectural decisions that kept me up at night.

---

## The Illusion of Simplicity

The initial prototype took a weekend. A Next.js app, a chat interface, some hardcoded conversation scenarios. "You're a barista in London, the user orders coffee." Simple, right?

The first users exposed the cracks immediately. The AI would forget what they ordered two turns ago. It would correct grammar in the middle of a sentence, breaking immersion. And worst of all—it couldn't tell when someone was struggling versus when they were just being brief.

The core problem: **language learning isn't just conversation**. It's a multi-layered feedback loop where timing, context, and adaptation matter as much as content.

---

## Architecture Evolution: From Chatbot to Learning System

### Layer 1: Conversation State Management

The naive approach stores messages in an array. The sophisticated approach realizes that language learning conversations have semantic states that transcend individual messages.

I ended up with what I call a "layered context architecture":

- **Immediate context**: Last 3-5 exchanges (what's being discussed right now)
- **Session context**: Current scenario, learning objectives, difficulty level
- **User context**: Historical vocabulary gaps, persistent weaknesses, learning velocity
- **Meta context**: Time of day, streak status, engagement signals

Each layer has different retention policies and weights in prompt construction. The immediate context gets full attention, session context gets summarized injection, user context gets selective retrieval based on relevance scoring.

The breakthrough came when I stopped treating context as a flat array and started treating it as a **hierarchical memory system with garbage collection**.

### Layer 2: The Feedback Timing Problem

When should an AI language tutor correct mistakes?

Correct immediately → breaks conversation flow, kills confidence
Correct at the end → user forgets what they said, feedback feels disconnected
Never correct → user doesn't learn

My solution: **deferred, categorized feedback with natural breakpoints**.

The system classifies errors into three tiers:
1. **Critical** (wrong word choice that changes meaning) → gentle inline hint
2. **Moderate** (grammar issues) → accumulate, deliver at scene transition
3. **Minor** (pronunciation hints, style suggestions) → optional end-of-session summary

This required building a real-time error classification layer that runs parallel to the conversation. The AI doesn't just respond—it annotates its own understanding of the user's input with error metadata that gets queued for appropriate delivery.

### Layer 3: Difficulty Adaptation Without Frustration

Traditional adaptive learning uses right/wrong ratios. That's too crude for conversation.

I implemented what I call **micro-readiness signals**:
- Response latency (are they taking time to think, or stuck?)
- Message length patterns (confident users write more)
- Backtrack frequency (self-corrections indicate awareness)
- Vocabulary overlap with previous sessions (are they reusing learned words?)

These signals feed into a dynamic difficulty adjuster that tunes:
- AI vocabulary complexity
- Response length expectations
- Correction frequency
- Scenario cognitive load

The key insight: **adaptation should feel invisible**. Users should feel "I'm getting better" not "the system got easier."

---

## The Real-Time Response Pipeline

Streaming responses changed everything. Not just for UX, but for system architecture.

### Why Streaming Matters for Language Learning

In a traditional request-response model, users wait 2-4 seconds for a complete response. In language learning, this creates anxiety—"Did I say something wrong? Is it thinking?"

Streaming addresses this psychologically and technically:

1. **Psychological**: Immediate feedback reduces anxiety. The first tokens appear in ~300ms, signaling "I heard you, I'm responding."

2. **Technical**: Enables real-time processing pipeline where vocabulary extraction, error classification, and adaptation scoring happen during generation, not after.

The pipeline:
```
User Input → Intent Classification → Context Assembly → 
LLM Stream Generation → [Parallel: Vocab Extraction + Error Detection] → 
Streaming Response → Post-Response: Feedback Queue Update
```

The parallel processing during streaming was the hardest part. Extracting vocabulary while the AI is still generating requires careful token buffering and partial content analysis.

---

## The Mobile Optimization Journey

60% of usage happens on mobile. This created unexpected challenges.

### Challenge 1: Context Persistence Across Sessions

Mobile users don't have linear sessions. They chat for 2 minutes, close the app, return 4 hours later. Traditional session management assumes continuous interaction.

Solution: **state serialization with semantic compression**.

Instead of storing raw conversation history, I serialize:
- Current scenario state (where in the conversation we are)
- Pending feedback queue
- Vocabulary exposure log
- Engagement trajectory (were they improving or plateauing?)

When they return, the system reconstructs context from this compressed state plus the last N messages. It's not perfect restoration, but it's good enough—and it keeps localStorage usage under control.

### Challenge 2: Network Resilience

Mobile networks are unreliable. Streaming responses break mid-way. Users lose connection during generation.

I implemented a **resumable stream protocol**:
- Each response gets a unique ID
- Server maintains response buffer for 60 seconds after completion
- Client can request continuation from any checkpoint
- Graceful degradation: if streaming fails, fall back to chunked delivery

The retry logic alone took two weeks to get right. The edge cases are endless: what if they reconnect after the server evicted the buffer? What if they got part of the response but the feedback metadata didn't make it?

---

## The Ethics of AI Language Education

This kept me up more than any technical challenge.

### The Competence Illusion

LLMs are confident. They'll teach you wrong grammar with total assurance. They'll invent word origins, misattribute idioms, and make up usage patterns.

I had to build a **confidence calibration layer**:
- Grammar explanations get cross-referenced with rule databases
- Vocabulary definitions get validated against corpus frequency data
- Cultural context claims get flagged for human review

This doesn't catch everything, but it reduces hallucination-induced learning errors by roughly 70% (based on user correction reports).

### The Dependency Problem

AI tutors can become crutches. Users stop struggling through difficult expressions because the AI will always understand and respond.

My approach: **controlled friction injection**.
- Occasionally pretend to misunderstand unclear input
- Require users to rephrase instead of accepting ambiguous statements
- Introduce communication breakdowns that require repair strategies

This simulates real-world conversation where communication isn't perfect. The goal isn't to frustrate, but to build resilience.

### Data Privacy in Learning Contexts

Language learning data is intimate. It reveals education level, cultural background, cognitive patterns, even emotional states through word choice.

I implemented:
- **Local-first processing** where possible (vocabulary extraction can happen client-side)
- **Ephemeral session data** for unauthenticated users
- **Granular consent** for different data types (conversation content vs. learning metrics)
- **Export and deletion APIs** that actually work

The hardest part was explaining to users what they were consenting to. Privacy policies are useless if no one reads them. I ended up building interactive consent flows that explain data usage in context.

---

## What I'd Do Differently

1. **Started with the feedback system, not the conversation system**. The conversation part was easy; meaningful feedback is the real product.

2. **Built for offline-first from the start**. Retrofitting mobile resilience into an online-first architecture was painful.

3. **Invested more in evaluation infrastructure**. I spent months building features before I had robust ways to measure if they actually improved learning outcomes.

4. **Thought harder about the business model earlier**. AI API costs scale with usage in ways that traditional SaaS doesn't. The unit economics of language learning apps are brutal.

---

## The Open Questions

Six months in, I have more questions than answers:

- **How do you measure language learning success in weeks, not months?** Traditional metrics assume semester-long evaluation cycles. AI enables daily iteration, but we don't have good short-term proxies for long-term retention.

- **What's the right balance between adaptation and consistency?** If the AI adapts too much, users game the system. If it doesn't adapt enough, they get frustrated. The equilibrium is personal and shifts over time.

- **Can AI language tutors ever replace the social motivation of real conversation partners?** I've built something that teaches effectively, but I'm not sure I've built something that motivates consistently. The students who succeed are already motivated; the ones who need motivation still drift away.

- **How do you build for the long tail of languages and learning contexts?** English is well-resourced. The same architecture for, say, learning Tamil or adapting to learners with dyslexia requires fundamentally different approaches.

I don't have answers to these. But I've learned that asking the right questions is more valuable than optimizing the wrong metrics.

---

Building English Agent taught me that AI education products aren't AI products—they're education products that happen to use AI. The technology is the easy part. The pedagogy, the psychology, the ethics... that's where the real work lives.

The code is open source. The architecture is documented. The mistakes are preserved in the commit history. If you're building something similar, maybe this saves you a few wrong turns.

Or maybe you'll make entirely new mistakes. That's how we learn, after all.
