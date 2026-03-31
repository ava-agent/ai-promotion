---
title: I built an AI agent for my dog after forgetting his vet appointment (again)
published: true
tags: ai, opensource, pets, productivity
---

# I built an AI agent for my dog after forgetting his vet appointment (again)

So here's the thing. I'm not proud of this, but I've forgotten my dog's vet appointment three times in the past year. Three. Times.

And honestly? The worst part wasn't the rescheduling fee. It was looking at my dog's face and realizing I'd let him down. Again.

That's how Dog Agent started. Not as some grand vision for pet tech. Just me, feeling guilty, thinking "there has to be a better way."

## The problem I was actually trying to solve

Real talk: pet ownership is way more logistical than people admit. It's not just walks and feeding. It's medication schedules, vet appointments, grooming, training sessions, dietary changes, weight tracking... the list goes on.

And it all lives in different places. My vet sends email reminders. The groomer texts me. The dog food subscription is in some app I never check. My partner and I try to coordinate via a shared calendar, but we both forget to update it.

The frustrating part? I already use AI assistants for work stuff. Calendar management, task tracking, reminders. Why was I still doing all my pet care manually?

Turns out, most "pet apps" are either:
- Social media for pets (cute, not useful)
- Basic trackers that don't actually remind you of anything
- Overcomplicated vet management systems designed for clinics, not owners

None of them felt like having an actual assistant who understood that my dog is a living being with needs, not just a data entry task.

## What Dog Agent actually does

I built Dog Agent as a realm-native AI - basically, an agent that understands the "world" of pet ownership and can operate within it intelligently.

Here's the GitHub if you want to peek at the code: https://github.com/kevinten-ai/dog-agent

And the live version is here: https://pet.rxcloud.group

### Core features that actually matter

**Smart reminders that understand context**

Not just "vet appointment at 3pm." It knows that this is the annual checkup, which means I need to bring vaccination records, which are stored in that drawer I never remember. It reminds me the night before to gather documents. It checks traffic and suggests when to leave. It knows my dog gets anxious about car rides, so it suggests bringing his comfort toy.

**Multi-modal memory**

I can text a photo of the dog food bag when I open it, and Dog Agent knows that's the "opened on" date. It tracks how long bags typically last for my dog's size. It reminds me to order before I run out, not after I'm scraping the bottom of the container at 10pm.

**Family coordination**

My partner and I can both interact with Dog Agent independently. If she mentions that she gave the flea medication, Dog Agent knows and won't remind me. If I mention a weird behavior I noticed, it logs it and suggests whether it might be vet-worthy.

## The architecture (because you're probably curious)

I'm not going to pretend this is some revolutionary system design. It's actually pretty straightforward, which is kind of the point.

### Core components

```python
# Simplified version of the agent core
class DogAgent:
    def __init__(self):
        self.memory = TemporalMemory()  # Time-aware context
        self.realm = PetOwnershipRealm()  # Domain knowledge
        self.planner = CarePlanner()
    
    def process_input(self, user_message, context):
        # Understand what the user is talking about
        intent = self.realm.parse_intent(user_message)
        
        # Check relevant memory
        relevant_context = self.memory.retrieve(
            entity=intent.entity,
            timeframe=intent.relevant_timeframe
        )
        
        # Decide what action to take
        action = self.planner.decide(intent, relevant_context)
        
        return self.execute(action)
```

The key insight was separating "pet ownership knowledge" from "this specific pet's data." The realm contains general knowledge about dog care, common schedules, warning signs, etc. The memory layer tracks your specific pet's history.

### Data flow example

When you text "gave Buddy his heartworm pill":

1. **Intent parsing** → identifies this as medication logging
2. **Entity resolution** → "Buddy" maps to your registered dog
3. **Realm validation** → confirms heartworm medication is monthly
4. **Memory update** → stores the administration time
5. **Planning** → schedules next reminder for ~30 days out
6. **Context awareness** → checks if you mentioned any side effects

```python
# Example of how medication tracking works
async def log_medication(self, dog_name, medication, notes=None):
    dog = self.get_dog(dog_name)
    
    # Record the event
    event = MedicationEvent(
        dog_id=dog.id,
        medication=medication,
        administered_at=datetime.now(),
        notes=notes
    )
    await self.memory.store(event)
    
    # Schedule next reminder based on medication type
    schedule = self.realm.get_medication_schedule(medication)
    next_due = schedule.calculate_next(event.administered_at)
    
    await self.scheduler.create_reminder(
        dog_id=dog.id,
        medication=medication,
        due_date=next_due,
        prep_reminder=next_due - timedelta(days=2)  # Give time to reorder
    )
    
    return f"Got it! Next {medication} due around {next_due.strftime('%B %d')}."
```

## What worked and what didn't

I'm not going to pretend this is perfect. Here are the honest pros and cons after using it for a few months:

### Pros

**Actually reduced my mental load**

I don't have to remember when I last gave flea medication. I don't have to wonder if my partner already fed the dog. The cognitive overhead of pet ownership dropped significantly.

**Caught things I would have missed**

Dog Agent noticed my dog was due for a vaccination based on records I uploaded months ago. I had completely forgotten. That alone was worth the effort of building this.

**Family coordination actually works**

No more "did you walk the dog?" texts. We both just update Dog Agent, and it keeps track.

### Cons

**Setup is annoying**

You have to input initial data - vaccination history, current medications, your dog's baseline stats. It's not hard, but it's tedious. I should probably build a better onboarding flow.

**Voice/photo input is still clunky**

I wanted to be able to just talk to it or snap photos of things. That works... most of the time. But parsing natural language about pet care is surprisingly complex. "He threw up this morning" could mean anything from "minor stomach upset" to "emergency vet now."

**Edge cases are edge-y**

Multi-pet households get complicated fast. Dogs with complex medical histories need careful tracking. I've had to add a bunch of override options because AI suggestions aren't always appropriate for every situation.

## Use cases: when this actually makes sense

**Good for:**
- Single or multi-person households that struggle with coordination
- Dogs with regular medication schedules
- People who travel and need to brief pet-sitters
- Anyone who's ever forgotten a vet appointment (guilty)
- Tracking patterns over time (eating, behavior, etc.)

**Not ideal for:**
- Serious medical conditions requiring professional monitoring (this is a helper, not a replacement for vet care)
- People who want zero setup (you do have to input some initial data)
- Complex multi-pet households with very different needs (works, but gets messy)

## The code

If you're curious about the implementation, here's the GitHub: https://github.com/kevinten-ai/dog-agent

It's built with Python/FastAPI for the backend, uses a custom "realm-native" architecture I developed (heavily inspired by some work I did on OpenOctopus), and has a simple web interface for setup and monitoring.

Fair warning: this is very much a personal project that grew out of my own needs. The code isn't as polished as something you'd find in a commercial product. There are TODOs in the codebase. There are probably bugs I haven't found yet.

But it works for me. And maybe it'll work for you too.

## What I learned building this

The biggest surprise? How much of pet ownership is actually about *anticipation*, not just tracking. Good pet care isn't just knowing when the next appointment is - it's knowing that you need to book the appointment three weeks in advance because your vet is always busy, or that you need to buy food before you run out because your dog's brand isn't sold at the grocery store.

Building that kind of anticipatory intelligence into an AI is way harder than building a reminder system. I'm still working on it.

Also, I learned that my dog really likes the reminder sound I picked. He gets excited when he hears it because he knows it's usually followed by treats. So... accidental positive reinforcement training? I'll take it.

## What's next

Honestly? I don't know. This scratches my itch for now. I might add better photo parsing, or integrate with some smart home devices, or build a mobile app that's more than just a web wrapper.

But I'm also wary of feature creep. The whole point was to reduce complexity, not add more of it.

---

**Have you ever built something just to solve a personal problem?** Did it stay personal, or did it grow into something bigger? I'm curious how other people navigate that line.

Also: **what's your biggest pet care logistical challenge?** Maybe I can steal some ideas for version 2.

---

*Disclaimer: Dog Agent is a personal project. It's not a substitute for professional veterinary advice. If your pet is sick, call your vet, not an AI.*

*The project is open source because I figured other people might find it useful, but I'm not trying to turn this into a business. Just sharing what worked for me.*
