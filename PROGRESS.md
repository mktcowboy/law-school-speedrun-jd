# Project Progress And Status

A living status file for this curriculum. It tracks what is built, what is in flight, and what should improve next.

Last updated: `June 10, 2026`.

## North Star

Keep this repo a `free-first`, `primary-law-first`, self-study JD curriculum that is `very aligned with T10/Ivy material`.

That means:

- teaching materials come from the current `top-10 / Ivy` band first
- primary law and core tools come from the best free host regardless of rank
- every external resource is verified before it ships, not guessed
- the structure mirrors a real `1L -> 2L -> 3L` arc, not a random reading list

## Where This Stands

The curriculum is structurally complete and usable end to end:

- a methods bridge for true beginners
- full `1L`, `2L`, and `3L` reading tracks with subject guides
- a verified `T10/Ivy` resource directory
- study-system, supplement, and assessment guidance
- a landmark-case canon and reusable templates
- an optional compressed `speedrun` path

The main work now is depth and polish, not new architecture.

## Recently Shipped

`June 10, 2026`:

- ✅ pre-1L methods bridge: [00-pre-1l-methods-and-mindset](./00-pre-1l-methods-and-mindset/README.md) — read an opinion, brief and synthesize, outline and attack-sheet, write `IRAC`
- ✅ assessment and exam-archive loop: [09-assessment-and-exam-archive-method.md](./00-start-here/09-assessment-and-exam-archive-method.md)
- ✅ supplement policy and pairings: [08-supplement-policy-and-pairings.md](./00-start-here/08-supplement-policy-and-pairings.md)
- ✅ landmark case canon: [10-landmark-case-canon.md](./00-start-here/10-landmark-case-canon.md)
- ✅ `Common Exam Traps` section added to all 13 doctrinal subject READMEs; `Landmark Cases` added to evidence
- ✅ sourcing rule clarified: top-10 band governs teaching materials; primary law and tools use the best free host — see [05-top-10-school-priority-basis.md](./00-start-here/05-top-10-school-priority-basis.md)
- ✅ added `T10/Ivy` faculty courses (Amar/Yale, Sandel/Harvard, Fisher/Harvard) and the nonprofit backbone (Cornell LII, CALI, NCC) to [03](./00-start-here/03-open-resource-library.md) and [06](./00-start-here/06-top-tier-school-resource-directory.md)
- ✅ fixed corruption in [01-how-to-use-this-plan.md](./00-start-here/01-how-to-use-this-plan.md) (leftover patch text and duplicated READMEs)

## Roadmap / Open Work

Prioritized. The first three come straight from [07-feedback-integration-plan.md](./00-start-here/07-feedback-integration-plan.md).

1. `3L` practice-direction tracks — `01-litigation-track.md` and `02-transactional-track.md` under [03-3l-practice-synthesis-and-launch](./03-3l-practice-synthesis-and-launch/README.md): core subjects to revisit, drafting exercises, research emphasis, simulations, hiring relevance
2. explicit `1L` dual-track framing — make the doctrine lane and the legal-research-and-writing lane visibly parallel in [01-1l-foundation-year/README.md](./01-1l-foundation-year/README.md)
3. Con Law II continuation note — flag structure/separation-of-powers as `1L` and rights/First Amendment as a later `2L` continuation
4. editorial tightening of the `2L` framing as the bar-core upper-level foundation
5. optional spaced-repetition / flashcard guidance tied to the rule sheets and attack outlines

## What Could Be Better

Honest gaps and risks to watch:

- `link rot` — there are 50+ external URLs verified by hand on a date stamp. There is no automated check. A simple link-checker (CI or a script) would catch breakage before a reader hits it.
- `casebook monoculture` — first-pass doctrine leans heavily on Harvard `H2O`. It is the best open platform, but adding `eLangdell` open casebooks and more faculty-produced material would reduce single-source dependence.
- `speedrun drift` — [99-optional-speedrun](./99-optional-speedrun/README.md) re-derives the main curriculum in its own words. As the main guides change, the speedrun can fall out of sync. Tightening it toward cross-references would prevent contradictions.
- `gated practice` — the assessment loop leans on outside question banks. `NCBE NextGen` samples are free, but `CALI` lessons need a school authorization code, which a pure self-studier may not have. Worth listing more fully open practice sources.
- `subject breadth` — upper-level subjects beyond the bar core (remedies, federal courts, trusts and estates, tax, bankruptcy) appear only as expansion paths, not full guides. Fine for now; revisit if the repo's scope grows.
- `no progress tracking for the reader` — the plan defines deliverables but gives the reader no checklist artifact to mark a subject "done." A per-subject progress checklist template could help.

## Repo Map

- [00-start-here](./00-start-here) — orientation, sourcing rules, resource library, study system, supplements, assessment, case canon
- [00-pre-1l-methods-and-mindset](./00-pre-1l-methods-and-mindset/README.md) — the methods bridge to do first
- [01-1l-foundation-year](./01-1l-foundation-year/README.md) — civ pro, torts, contracts, property, criminal law, con law, legal research and writing
- [02-2l-doctrinal-depth-and-codes](./02-2l-doctrinal-depth-and-codes/README.md) — evidence, criminal procedure, business associations, UCC, admin law, professional responsibility
- [03-3l-practice-synthesis-and-launch](./03-3l-practice-synthesis-and-launch/README.md) — clinics, trial advocacy, advanced writing, bar bridge and career
- [99-optional-speedrun](./99-optional-speedrun/README.md) — compressed timeline version
- [templates](./templates) — case brief, statute brief, reading log, subject review, weekly review

## Ground Rules For Edits

- verify any new external URL before adding it; this repo is "verified"-stamped
- keep teaching materials inside the `T10/Ivy` band; use best-free-host for primary law and tools
- match the house voice: terse, backtick-wrapped terms, relative markdown links
- when you change a guide, check whether the `speedrun` mirror needs the same change
