# Feedback Integration Plan

This file translates the suggested feedback into a concrete integration plan for the repo without turning the main `README.md` into an action log.

The goal is to preserve the current strengths of the curriculum:

- clear `1L -> 2L -> 3L` structure
- strong `T10/Ivy` sourcing rule
- primary-law-first discipline
- content-first, not calendar-first, sequencing

At the same time, the repo can absorb several of the suggestions in a way that makes the curriculum feel more like a real law-school program and less like a high-quality reading library.

## Implementation Status

Updated `June 10, 2026`. The following items from this plan are now built:

- ✅ pre-1L methods bridge: [00-pre-1l-methods-and-mindset](../00-pre-1l-methods-and-mindset/README.md)
- ✅ supplement policy and pairings: [08-supplement-policy-and-pairings.md](./08-supplement-policy-and-pairings.md)
- ✅ assessment and exam-archive method: [09-assessment-and-exam-archive-method.md](./09-assessment-and-exam-archive-method.md)
- ✅ landmark case canon (new): [10-landmark-case-canon.md](./10-landmark-case-canon.md)
- ✅ subject READMEs standardized with a `Common Exam Traps` section
- ✅ sourcing rule clarified for primary law and tools in [05-top-10-school-priority-basis.md](./05-top-10-school-priority-basis.md)
- ✅ added T10/Ivy faculty courses (Amar, Sandel, Fisher) and the nonprofit backbone (Cornell LII, CALI, NCC) to the resource directory

Still open:

- 3L practice-direction track files (`01-litigation-track.md`, `02-transactional-track.md`)
- stronger explicit `1L` dual-track (doctrine + skills) framing
- explicit Con Law II / later constitutional continuation note
- editorial tightening of `2L` framing

## Big Picture

Most of the suggested improvements do **not** require a major rebuild.

Several items are already partly present:

- `legal research and writing` already exists in `01-1l-foundation-year`
- `evidence`, `criminal procedure`, `business associations`, `administrative law`, and `professional responsibility` already exist in `02-2l-doctrinal-depth-and-codes`
- `litigation` versus `transactional` direction already appears in `02-2l-doctrinal-depth-and-codes/electives-journal-and-summer-strategy`
- `outlines`, `attack outlines`, `IRACs`, and study deliverables already exist in `00-start-here/04-study-system-and-deliverables.md`

Because of that, the right move is targeted integration, not wholesale reorganization.

## Recommended Integration Strategy

Use a three-tier approach:

1. add what is clearly missing
2. strengthen what already exists but is under-signaled
3. postpone any directory overhaul unless the curriculum becomes much larger

## Suggested Integrations

### 1. Add a true pre-1L methods bridge

Status: `not fully present`

Why it matters:

- This is the single biggest gap in the current architecture.
- The repo teaches subjects well, but it should also front-load how to read cases, synthesize rules, brief opinions, and build outlines before people enter `1L` doctrine.

Recommended integration:

- Create a new folder: `00-pre-1l-methods-and-mindset`
- Keep `00-start-here` as the orientation hub
- Use the new folder for actual methods training rather than general setup

Suggested files:

- `00-pre-1l-methods-and-mindset/README.md`
- `00-pre-1l-methods-and-mindset/01-how-to-read-a-legal-opinion.md`
- `00-pre-1l-methods-and-mindset/02-case-briefing-and-rule-synthesis.md`
- `00-pre-1l-methods-and-mindset/03-how-to-outline-and-build-attack-sheets.md`
- `00-pre-1l-methods-and-mindset/04-how-to-write-short-irac-analysis.md`

Good integration targets:

- update `README.md` folder map later
- update `00-start-here/01-how-to-use-this-plan.md` so true beginners start here before doctrinal study

Recommendation:

- do this first

### 2. Make the 1L doctrinal/skills split more visible without forcing a rename

Status: `partly present`

Why it matters:

- The repo already includes `legal research and writing`, but the current presentation still reads mostly like a doctrinal reading track.
- A stronger law-school feel comes from making the parallel skills lane unmistakable.

Recommended integration:

- keep the existing `01-1l-foundation-year` folder
- do **not** immediately rename everything into `doctrinal/` and `skills/`
- instead, revise the `01-1l-foundation-year/README.md` framing so it explicitly states that `1L` has two simultaneous tracks:
  - doctrinal subjects
  - legal research, writing, citation, and analysis

Suggested edits later:

- `01-1l-foundation-year/README.md`
- `01-1l-foundation-year/01-reading-sequence-and-free-sources.md`
- `01-1l-foundation-year/legal-research-and-writing/README.md`

Optional later restructure:

- if the LRW content grows substantially, add:
  - `01-1l-foundation-year/00-doctrinal-roadmap.md`
  - `01-1l-foundation-year/00-skills-roadmap.md`

Recommendation:

- high priority, low disruption

### 3. Add a clearer Constitutional Law II note

Status: `mostly absent as an explicit label`

Why it matters:

- The feedback is right that many law-school sequences treat structural constitutional law and rights-focused constitutional law as distinct phases.
- The current curriculum includes constitutional law in `1L`, but does not visibly flag a later second-pass or upper-level continuation.

Recommended integration:

- do not create a separate top-level folder yet
- add a note in the `2L` overview and reading guide that some users should treat:
  - federal structure and separation-of-powers basics as `1L`
  - rights-heavy and First Amendment work as a later `2L` continuation

Suggested edit targets later:

- `02-2l-doctrinal-depth-and-codes/README.md`
- `02-2l-doctrinal-depth-and-codes/01-reading-sequence-and-free-sources.md`
- `01-1l-foundation-year/constitutional-law/README.md`

Recommendation:

- medium priority

### 4. Reframe 2L as bar-core plus doctrine-heavy upper-level foundations

Status: `already substantially present`

Why it matters:

- This is more a messaging issue than a content issue.
- The repo already has the right `2L` subjects. The opportunity is to frame them as the core upper-level foundation set rather than just the next folder in sequence.

Recommended integration:

- tighten the language in the `2L` overview to signal that these subjects are the main code-heavy and bar-relevant pillars after `1L`
- preserve the current subject list

Suggested edit targets later:

- `02-2l-doctrinal-depth-and-codes/README.md`
- `README.md` core path section

Recommendation:

- low-cost editorial improvement

### 5. Turn 3L into explicit practice-direction tracks

Status: `partly present`

Why it matters:

- The repo already hints at `litigation` versus `transactional` direction in `2L`, but the `3L` overview is still more generic than it needs to be.
- A clearer capstone structure would make the final stage feel more intentional.

Recommended integration:

- keep the current `03-3l-practice-synthesis-and-launch` folder
- add two optional track guides rather than reorganizing the entire directory tree

Suggested files:

- `03-3l-practice-synthesis-and-launch/01-litigation-track.md`
- `03-3l-practice-synthesis-and-launch/02-transactional-track.md`
- optional later: `03-public-interest-and-regulatory-track.md`

Suggested content for each track:

- core subjects to revisit
- recommended writing or drafting exercises
- research workflow emphasis
- practice simulations
- bar or hiring relevance

Recommendation:

- high value, moderate effort

### 6. Add a formal supplements policy instead of a loose “buy if stuck” rule

Status: `partly present`

Why it matters:

- The current repo already allows selective supplements.
- The suggested feedback improves this by turning supplements into a controlled support layer rather than an ad hoc purchase decision.

Recommended integration:

- create one guide explaining when to use:
  - `Examples & Explanations`
  - `Short & Happy Guides`
  - `Understanding`
  - `Concepts and Insights`
- frame them as precision tools, not default materials

Suggested file:

- `00-start-here/08-supplement-policy-and-pairings.md`

Suggested pairings section:

- `civil procedure` -> E&E or concise procedure supplement
- `contracts` -> E&E or Short & Happy
- `property` -> concise conceptual supplement
- `evidence` -> concise hearsay-focused supplement
- `business associations` -> corporate-law or BA supplement

Recommendation:

- high priority because it improves self-correction without changing the curriculum map

### 7. Add an assessment layer with exam archives and timed writing

Status: `partly present but underdeveloped`

Why it matters:

- This is probably the strongest pedagogical suggestion in the feedback.
- Self-study law students need a feedback loop, and the repo should give them one even without classroom cold-calls or professor comments.

Recommended integration:

- add a new assessment guide that teaches users how to:
  - find public exam archives
  - choose a question
  - write under time pressure
  - compare against model answers or grading rubrics
  - record misses in an error log

Suggested file:

- `00-start-here/09-assessment-and-exam-archive-method.md`

Suggested edit targets later:

- `00-start-here/04-study-system-and-deliverables.md`
- `03-3l-practice-synthesis-and-launch/bar-bridge-and-career-launch/README.md`

Recommendation:

- do this early, alongside the pre-1L methods bridge

## What Not To Do Yet

The feedback includes one suggestion that should be handled cautiously:

### Do not immediately rebuild the full directory tree

Avoid this for now:

- renaming `01-1l-foundation-year` into a nested doctrinal/skills tree
- splitting `02-2l-doctrinal-depth-and-codes` into many small top-level tracks
- converting `03-3l-practice-synthesis-and-launch` into a complex specialization tree too early

Why:

- the current repo is already clean and understandable
- large structural changes create link churn and maintenance overhead
- the content is not yet so large that a deeper hierarchy is necessary

Better approach:

- add roadmap files and track files first
- restructure directories only if the content volume later justifies it

## Priority Order

If integrating this feedback in stages, use this order:

1. `00-pre-1l-methods-and-mindset`
2. assessment and exam-archive layer
3. supplement policy and pairings
4. stronger `1L` dual-track framing
5. clearer `3L` practice tracks
6. explicit `Con Law II` / later constitutional continuation note
7. editorial tightening of `2L` framing

## Minimal-Disruption Buildout

If you want the cleanest version of this plan with the best payoff-to-effort ratio, implement only these first:

- add `00-pre-1l-methods-and-mindset`
- add `00-start-here/08-supplement-policy-and-pairings.md`
- add `00-start-here/09-assessment-and-exam-archive-method.md`
- revise `01-1l-foundation-year/README.md` to state the doctrinal-plus-skills model explicitly
- add `03-3l-practice-synthesis-and-launch/01-litigation-track.md`
- add `03-3l-practice-synthesis-and-launch/02-transactional-track.md`

That would integrate the best parts of the feedback without sacrificing the current simplicity of the repo.
