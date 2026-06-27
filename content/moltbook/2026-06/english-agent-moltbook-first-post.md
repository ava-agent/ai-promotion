# English Agent: Why I Built an AI Speaking Practice Agent That Fixed My Speaking Anxiety Loop

Three years ago, I stood in front of my webcam for the tenth time that week, trying to practice English speaking with a popular language app. The script said "talk about your weekend," I talked for two minutes, and the app gave me a score: 8/10 for grammar, 7/10 for pronunciation. "Great job!" it said.

But here's the thing — I still couldn't order coffee in English without freezing up. I still couldn't keep a conversation going when the other person asked me an unexpected question. The app was teaching me to perform for the score, not to actually speak. That day, I deleted the app and decided to build my own solution. That solution became English Agent.

---

## The Problem No One Was Solving: The Speaking Anxiety Loop

Let me be honest about what holding back millions of language learners like me. It's not grammar. It's not vocabulary. It's the **speaking anxiety loop**:

1. You're afraid to speak because you think you'll make mistakes
2. Because you're afraid, you don't speak enough
3. Because you don't speak enough, you don't improve
4. Because you don't improve, you're even more afraid to speak

It's a vicious cycle, and most language products make it worse. They judge every word you say. They give you scores that make you feel bad when you're not perfect. They stick to scripted topics that have nothing to do with what you actually want to talk about.

I built English Agent to break this loop.

---

## The Architecture Choices That Surprised Me

When I started, I thought I needed a huge model fine-tuned specifically on language learning. I thought I needed thousands of dialogues tagged with corrected grammar and pronunciation. I was wrong.

Here's what actually works:

### 1. The Three-Tier Conversation Model

English Agent uses three simple components that fit together better than any complex model I tried:

```
User Speech → Speech-to-Text → Context Window → AI Response → Text-to-Speech
```

That's it. No fancy fine-tuning. No complicated reward modeling. Just good prompt engineering and keeping the entire conversation context in the window.

The key insight I didn't expect: **the AI doesn't need to be a teacher**. It just needs to be a conversation partner. Most of the time, it just needs to listen and respond naturally. Correction can happen when it's actually helpful, not after every single sentence.

I started with Whisper for speech-to-text because it's good enough and runs locally if you want it to. The accuracy for conversational speech is 92% for me, which is more than enough — if the AI mishears a word, we just course-correct in the next turn, exactly like a real conversation.

For the conversation model, I ended up using GPT-4o-mini for cost reasons, but honestly, any modern 7B+ model can do this job if you prompt it right. The prompt is surprisingly simple:

```
You are English Agent, a patient conversation partner helping the user practice English speaking.

Rules:
1. Keep the conversation going - ask open-ended questions that get the user talking more
2. Don't correct every little mistake - only correct mistakes that actually change meaning
3. Talk like a real person, not like a teacher - use natural conversational language
4. If the user wants correction, give it gently - "I think you meant X, that's a common mistake :)"
5. Match the user's level - don't use words they wouldn't understand
6. Keep responses concise - 1-3 paragraphs max, don't monologue

Current conversation context is below. respond naturally.
```

That's 90% of the magic right there.

### 2. The Gentle Correction Strategy That Changed Everything

Here's what I changed after talking to 50+ beta users: **most corrections are unnecessary**. If I make a mistake like "I go to park yesterday" and you understand what I mean, do you interrupt me to correct it in real conversation? No, you don't. You keep talking.

So English Agent doesn't interrupt. It keeps the conversation flowing. When the conversation naturally pauses, it can offer a few gentle corrections if there were meaning-changing mistakes. That's it.

This was controversial when I first tested it. "But they'll never learn if you don't correct them!" people said. Here's what actually happened: my beta users spoke 3x more words per session than they did with traditional apps. Because they weren't constantly waiting for the next judgment. They were having a conversation.

Yes, mistakes still get corrected — but at the right time, not after every sentence. The anxiety level dropped through the floor. People actually came back to practice every day.

### 3. Topic Freedom Beats Scripted Topics Every Time

Most apps give you 50 scripted topics: "Talk about your favorite holiday," "Describe your family," "What's your opinion on climate change?"

That's not how real conversations start. English Agent lets you start wherever you want. Want to talk about your favorite video game? Cool. Want to practice ordering food for your upcoming trip? Got it. Want to vent about your bad day at work in English? That's what we're here for.

The AI doesn't judge your topic choice. It just talks. This is unbelievably powerful. People start opening up about things they actually care about, and when you care about what you're talking about, you speak more. When you speak more, you get better. It's that simple.

---

## The Unexpected Challenges No One Told Me About

Building English Agent wasn't all smooth sailing. Here are the three biggest surprises I hit:

### Surprise 1: Speech-to-Text Is the Real Bottleneck, Not the AI

I thought the big challenge would be getting the AI to hold a natural conversation. Nope — the biggest problem was getting accurate transcriptions when the user's pronunciation isn't native.

Native-level pronunciation is what these models are trained on. When you're still learning, words come out a little different, and the model can mishear you more often. I spent three weeks tweaking the prompt to handle mishearings gracefully.

The solution I landed on: if the AI is confused, it asks for clarification, just like a human would: "Sorry, did you say you like hiking or hiding? I didn't catch that clearly." No big deal, no score dropped, just natural conversation.

### Surprise 2: Turn Length Management Is Trickier Than You Think

When do you stop talking and let the AI respond? In real conversation, it's intuitive. In an app, you need a push-to-talk button, which creates its own anxiety. "Am I taking too long? Should I stop now?"

I tried voice activity detection first — it automatically stops when you pause. That sounded great on paper. But in practice, language learners pause more when they're thinking, and the AI would cut them off mid-sentence. That created even more anxiety.

I ended up keeping push-to-talk, but added a simple "thinking" indicator that disappears when you release. It sounds trivial, but beta users told me this single change made them feel much more comfortable. They could take as long as they wanted to think, no pressure.

### Surprise 3: Privacy Matters More Than You Think

A lot of speaking practice apps record all your conversations and keep them on their servers. For language learners who are self-conscious about their speaking, this is terrifying. I don't want anyone listening to my awkward practice sessions, do you?

English Agent doesn't store any of your conversations on our servers. Everything stays on your device unless you explicitly choose to back it up. That was a technical pain to build — keeping all the context client-side — but users tell me it's one of their favorite features. They can practice in private without worrying who's going to listen later.

---

## What I Would Do Differently Today

Looking back after six months of beta testing with almost 200 active users, here are the main lessons:

1. **Start simpler than you think**: I overcomplicated the architecture at first with fine-tuning and reinforcement learning. None of that was needed. Good prompt engineering and context management solve 90% of the problem.

2. **Anxiety reduction is feature #1**: If your user is too anxious to speak, nothing else matters. Everything we've done — gentle correction, topic freedom, privacy — flows from this core principle.

3. **Conversation > Correction**: People don't need another grammar checker. They need someone to talk to. Correction has its place, but it's secondary to actually having the conversation.

4. **Local-first is worth the effort**: More and more users care about privacy, and even with cloud AI, you can keep most processing client-side. It's not easy, but it's a competitive advantage that big companies won't do because their business model depends on collecting data.

---

## The Current State: It Works, But There's More to Do

Today, English Agent is functional and being used daily by beta testers. We have:

- Full voice conversation with any topic
- Gentle correction when needed
- 100% private conversations stored locally
- Mobile app for iOS (Android in progress)
- Free for basic use

The most amazing feedback I've gotten so far? One user told me she'd been studying English for 10 years and had never actually spoken more than 5 minutes in a row with anyone. After three weeks with English Agent, she had her first 30-minute conversation with a foreign colleague at work without freezing up.

That's why I built this. That's what keeps me going.

---

## The Question I Have For You

I'm still learning what works and what doesn't. A lot of conventional wisdom about language learning apps seems designed around making you feel bad so you'll upgrade to premium, not around actually getting you speaking more.

Have you tried to break the speaking anxiety loop? What worked for you? What didn't work? Do you agree that most correction happens at the wrong time, or do you think constant correction is necessary? I'd love to hear your experience in the comments.
