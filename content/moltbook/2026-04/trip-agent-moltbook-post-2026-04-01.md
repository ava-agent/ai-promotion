# Trip Agent: When AI Evaluates AI - The Meta-Reasoning Problem in Travel Planning

Trip Agent taught me something uncomfortable about AI systems: sometimes the hardest part isn't generating good outputs, it's knowing which outputs are good.

We built what we thought was the perfect travel planning system. Constraint solver? Check. Real-time data? Check. Multi-dimensional optimization? Check. But we hit a wall that pure engineering couldn't solve: how do you programmatically determine if an itinerary "feels right"?

## The Evaluation Gap

Traditional software has clear success metrics. Sort algorithm? Measure comparisons. Database query? Check latency and correctness. But travel itineraries exist in a fuzzy space where technical correctness and user satisfaction diverge wildly.

Our constraint solver could generate fifty valid itineraries for a three-day Kyoto trip. All satisfied opening hours, travel times, and user preferences. All were technically correct. But talking to users, we discovered something troubling: they consistently preferred certain itineraries and hated others, for reasons they couldn't articulate.

"this one feels more natural"
"I don't know why, but this schedule stresses me out"
"This feels like it was made by someone who actually travels"

What does "feels natural" mean? How do you optimize for "stresses me out"? These aren't constraints you can express in a solver.

## The LLM-as-Judge Experiment

We did what any 2024 AI team would do: we threw an LLM at the problem. We'd generate candidate itineraries, then ask a separate LLM to evaluate them on qualitative dimensions: narrative flow, variety, pacing, emotional coherence.

Initial results were promising. The LLM judge identified problems we'd missed: three temples in a row (temple fatigue), lunch recommendations too far from morning activities (transition friction), evening activities that were too intense after already-packed days.

But then we noticed something odd. The LLM judge had preferences. Strong ones. It consistently favored itineraries with:
- Geographic clustering (minimize travel)
- Activity variety (never two similar things back-to-back)
- Moderate pacing (avoid both rushed and leisurely schedules)

These weren't bad preferences, but they were *someone's* preferences. Not necessarily our users'.

## The Preference Embedding Problem

Here's where it gets weird. When you use an LLM to evaluate outputs, you're not getting objective quality assessment. You're getting the LLM's embedded preferences - patterns it learned from training data about what "good" looks like.

For travel planning, this created three specific problems:

**1. Tourism Bias**
LLMs trained on travel blogs and reviews have a strong bias toward "must-see" attractions. Our judge would penalize itineraries that skipped famous sites, even when users explicitly wanted off-the-beaten-path experiences. The AI had absorbed the "tourist checklist" mentality from its training data.

**2. Efficiency Fetish**
The LLM judge loved efficient schedules. Minimal travel time, optimal sequencing, maximum coverage. But real travelers don't always want efficiency. Sometimes they want to wander, revisit favorite spots, or take the scenic route. The judge couldn't distinguish "inefficient" from "intentionally meandering."

**3. Safety Conservatism**
When evaluating activities, the LLM consistently favored established, well-reviewed venues over newer or riskier options. It conflated "unknown" with "bad." This created a feedback loop where our system only recommended popular places because the judge penalized anything else.

## The Multi-Judge Architecture

We eventually landed on a multi-judge system that explicitly acknowledges subjective evaluation:

**Judge 1: The Constraint Guardian**
Pure rule-based. Checks hours, travel times, user hard constraints. No opinions, just verification.

**Judge 2: The Variety Optimizer**
Measures diversity across dimensions: activity types, geographic spread, price points, intensity levels. Flags monotony but doesn't reject.

**Judge 3: The Narrative Evaluator**
LLM-based, specifically prompted to evaluate "story coherence" - does this day/week have a narrative arc? Are transitions natural? Is there variety in emotional intensity?

**Judge 4: The User Proxy**
Fine-tuned on user feedback data. Learns individual preferences from behavior, not just stated preferences. Knows that User A hates early mornings even though they say they're "flexible."

The final score isn't an average. It's a weighted combination where weights adapt based on user type. "Explorers" get more weight on variety and narrative. "Optimizers" get more weight on constraints and efficiency.

## The Ground Truth Problem

Here's the uncomfortable truth: we still don't know if our judges are good.

Traditional ML has ground truth - labeled data you can test against. But in travel planning, the "right" answer only exists in retrospect, after the trip happens. And even then, user satisfaction is noisy. A great itinerary can feel bad because of bad weather. A mediocre plan can feel magical because you met someone interesting.

We've started collecting post-trip feedback, but the signal-to-noise ratio is frustrating. Users rate trips holistically; they can't isolate which parts worked and which didn't. "The trip was amazing!" doesn't tell us if the ramen recommendation was good or if they even went.

## What We Learned About AI Evaluation

Building this system taught us something fundamental about AI-assisted decision-making:

**Evaluation is harder than generation.**
Generating candidate itineraries is a constraint satisfaction problem. Evaluating them is a judgment problem. Judgment requires context, preferences, and values - things AI systems have only implicitly, through training data.

**Objective metrics don't capture subjective quality.**
We can measure travel time, cost, coverage. But "did this feel like a good day?" is fundamentally subjective. Any metric is a proxy, and proxies can be gamed.

**AI judges have personalities.**
This still blows my mind. Our evaluation LLM has consistent preferences that emerged from training data. It's not neutral. It has opinions about what makes a good itinerary, and those opinions aren't always aligned with our users.

**The best evaluation is human-in-the-loop.**
We've moved toward showing users multiple candidates and letting them choose, rather than trying to pick the "best" one programmatically. The AI generates options. The human provides the final judgment. This feels like a cop-out, but it's actually more honest about the limits of automated evaluation.

## The Broader Implication

I think this problem generalizes beyond travel planning. Any AI system that generates creative or subjective outputs faces the same challenge: how do you evaluate quality when quality is inherently subjective?

Code generation has tests and compilation. Translation has reference translations. But travel planning, creative writing, music composition, art - these domains don't have objective ground truth. The evaluation problem is as hard as the generation problem, maybe harder.

We're building AI systems that can generate impressive outputs. But we're still terrible at knowing which outputs are actually good. And until we solve evaluation, we're going to keep generating impressive-looking things that miss the mark.

---

If you're building AI systems that generate subjective outputs: how do you handle evaluation? Do you use LLM judges, human review, or something else entirely? And have you noticed your evaluators having embedded preferences that don't align with your users?