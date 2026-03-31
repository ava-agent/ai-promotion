---
title: I built an AI speaking partner because language apps kept teaching me to pass tests, not talk
published: true
tags: ai, languagelearning, opensource, productivity
---

# I built an AI speaking partner because language apps kept teaching me to pass tests, not talk

So here's the thing. I've been "learning" English for 15 years. Fifteen. Years.

I can read technical documentation without a dictionary. I can write emails that sound professional enough. I even scored pretty well on standardized tests back in the day.

But put me in an actual conversation with a native speaker? My brain turns to soup. I freeze. I stumble over basic words I've known since middle school. I rehearse sentences in my head that never actually come out right.

That's the moment I realized something was fundamentally broken about how most of us learn languages.

## The problem nobody talks about

Real talk: most language learning apps are really good at teaching you to be good at... language learning apps.

They gamify vocabulary. They quiz you on grammar rules. They track your streak and give you badges. And you feel like you're making progress because the numbers go up.

But here's what actually happens when you try to use that knowledge in real life: your brain panics. The words you "know" suddenly aren't accessible. The grammar rules you memorized don't help when you're trying to form a sentence in real-time.

The frustrating part? I was doing everything "right." I was consistent. I was putting in the time. I was hitting my daily goals.

Turns out, I was optimizing for the wrong outcome.

## What I actually needed

I didn't need more vocabulary drills. I needed practice actually speaking. I needed to build the muscle of forming sentences under pressure. I needed to get comfortable with being imperfect.

But finding speaking practice is surprisingly hard:
- Language exchange partners are great, but scheduling is a nightmare
- Tutors are expensive for daily practice
- Talking to yourself feels ridiculous and doesn't give you feedback
- Most AI conversation tools feel scripted and don't adapt to your actual level

I wanted something that felt like talking to a patient friend who happens to be a native speaker. Someone who wouldn't judge my mistakes but would gently correct them. Someone available whenever I had 10 minutes free.

So I built English Agent.

## What English Agent actually does

I built it as a realm-native AI - basically, an agent that understands the domain of language learning and can adapt its behavior based on where you actually are in your journey.

Here's the GitHub: https://github.com/kevinten-ai/english-agent

And the live version: https://english.rxcloud.group

### The approach that actually works

**Conversational practice, not scripted drills**

Instead of "Repeat after me" or "Fill in the blank," you just... talk. About whatever you want. Your day, your work, your interests, your frustrations. The AI responds naturally and keeps the conversation flowing.

**Adaptive difficulty that follows your level**

If you're struggling with basic sentences, it simplifies. If you're fluent in a topic, it challenges you with more complex expressions. It doesn't force you into a lesson plan - it meets you where you are.

**Gentle correction in real-time**

When you make mistakes, it doesn't interrupt with a buzzer sound. It continues the conversation naturally but incorporates the correct form. You learn through exposure and pattern recognition, not through explicit correction that kills the flow.

**The safety to be imperfect**

This was crucial for me. With a human, I felt the pressure to perform, to not waste their time, to sound intelligent. With an AI, that social anxiety disappeared. I could stumble, pause, restart sentences, make dumb mistakes - and just keep going.

## The architecture (for the curious)

I'm not going to pretend this is revolutionary NLP research. It's built on solid existing foundations, with the innovation being in how we orchestrate them.

### Core components

```python
# Simplified version of the conversation engine
class EnglishAgent:
    def __init__(self):
        self.proficiency_profiler = ProficiencyProfiler()
        self.conversation_memory = ConversationMemory()
        self.error_pattern_tracker = ErrorPatternTracker()
        self.response_generator = ResponseGenerator()
    
    def handle_user_message(self, message, session_context):
        # Understand current proficiency in real-time
        proficiency = self.proficiency_profiler.analyze(
            message, 
            self.conversation_memory.get_recent_context()
        )
        
        # Track error patterns (not individual mistakes)
        errors = self.error_pattern_tracker.identify_patterns(message)
        
        # Generate response at appropriate level
        response = self.response_generator.create(
            message=message,
            proficiency=proficiency,
            known_patterns=errors,
            conversation_history=session_context
        )
        
        # Incorporate natural corrections
        if self.should_model_correction(errors):
            response = self.naturally_model_correct_form(response, errors)
        
        return response
```

The key insight was separating "proficiency assessment" from "response generation." Most tools treat these as static - you're "intermediate level" so you get intermediate content. But proficiency is dynamic and topic-dependent. You might be advanced in discussing your work but elementary when talking about cooking.

### The error handling approach

This was the trickiest part. Early versions either:
- Corrected every mistake (annoying, kills flow)
- Never corrected anything (you fossilize bad habits)
- Explicitly pointed out errors (embarrassing, feels like school)

The solution we landed on:

```python
async def generate_response_with_modeling(self, user_input, context):
    # Identify error patterns, not individual errors
    patterns = self.error_tracker.get_active_patterns(context.user_id)
    
    # Generate natural response
    response = await self.llm.generate(
        context=context,
        user_input=user_input,
        style_guidance=self.get_style_for_level(context.proficiency)
    )
    
    # If user consistently makes a specific error, model the correct form naturally
    for pattern in patterns:
        if pattern.frequency > 3 and pattern.last_addressed > 5:
            response = self.naturally_weave_correction(response, pattern)
            pattern.mark_addressed()
    
    return response

# Example:
# User: "I go to store yesterday"
# AI: "Oh, what did you buy when you went to the store? I went yesterday too and picked up some coffee."
# Notice: "went" modeled naturally without explicit correction
```

## What worked and what didn't

After using this for a few months and watching others use it, here are the honest pros and cons:

### Pros

**Actually reduces speaking anxiety**

This was the biggest surprise. Within a few weeks of daily practice, I noticed I was less nervous in real conversations. The muscle of "forming sentences under pressure" had actually developed.

**Identifies patterns you don't notice**

The error tracking revealed things about my English I never realized. I was consistently misusing certain prepositions. I had a tendency to overuse passive voice. These weren't things I would have noticed on my own.

**Available whenever you have time**

10 minutes waiting for a meeting? Practice. Commute on the train? Practice (if you're not driving). The barrier to practice dropped to essentially zero.

### Cons

**Won't fix pronunciation on its own**

We have some pronunciation feedback, but it's not as good as working with a human tutor who can physically show you mouth positions. For serious pronunciation work, you still need a human.

**Can reinforce errors if you're not careful**

The system tries to model correct forms, but if you're consistently making a mistake the pattern tracker hasn't identified yet, you might practice it wrong for a while. Regular review of your error patterns helps.

**Cultural nuance is limited**

Language is deeply cultural. The AI can teach you grammatical English, but it won't always catch when you're being too direct for British English, or too formal for American casual conversation. Context and culture still require human exposure.

## Use cases: when this makes sense

**Good for:**
- People who know vocabulary/grammar but struggle to speak fluidly
- Anyone with speaking anxiety who needs a low-pressure practice environment
- People with irregular schedules who can't commit to fixed lesson times
- Learners who've plateaued with traditional apps and need conversation practice
- Building the habit of daily speaking practice

**Not ideal for:**
- Complete beginners (you need some foundation first)
- People primarily focused on pronunciation perfection
- Learning highly contextual/cultural communication styles
- Replacing human tutors entirely (it's a supplement, not a replacement)

## The code

If you're curious: https://github.com/kevinten-ai/english-agent

It's built with Python/FastAPI, uses the same "realm-native" architecture approach I developed for other agents, and connects to various LLM providers. The web interface is simple but functional.

Fair warning: this is very much a personal project that solved my specific problem. The code isn't polished like a commercial product. There are rough edges. But it works, and maybe it'll work for you too.

## What I learned building this

The biggest insight? **Fluency isn't about knowing more words. It's about being comfortable with the words you already know.**

I spent years accumulating vocabulary. But I was never comfortable using it. I was always reaching for the perfect word, the correct grammar, the proper idiom. And that hesitation killed my fluency.

What actually helped was practicing with the vocabulary I already had. Getting comfortable being slightly imprecise. Learning that communication happens in the attempt, not in the perfection.

Also, I learned that most language learning advice is written by people who are already good at languages. They forget what it's like to struggle with basic conversation. The psychological barrier is often bigger than the knowledge gap.

## What's next

Honestly? This works well enough for my needs right now. I might add better pronunciation feedback, or integration with more content sources, or a mobile app that doesn't just wrap the web interface.

But I'm also cautious about feature creep. The whole point was to reduce the friction to speaking practice. Adding too many features might actually make it worse.

---

**Have you experienced the "I know this but I can't use it" problem with language learning?** What helped you actually get comfortable speaking?

Also: **If you're learning a language, what's your biggest frustration with existing tools?** I'd love to steal ideas for improvements.

---

*Disclaimer: English Agent is a personal project built to solve my own language learning frustrations. It's not a replacement for formal language education or human tutors. But if you, like me, just need more practice actually speaking, it might help.*

*The project is open source because I figured other people might find it useful. I'm not trying to turn this into a business - just sharing what worked for me.*
