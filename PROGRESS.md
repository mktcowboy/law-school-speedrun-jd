# Project Progress And Status

A living status file for this curriculum. It tracks what is built, what is in flight, and what should improve next.

Last updated: `June 30, 2026`.

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
- a root [subject index](./SUBJECTS.md) for jumping into individual subjects
- a landmark-case canon and reusable templates
- an optional compressed `speedrun` path

The main work now is depth and polish, not new architecture.

## Recently Shipped

`June 30, 2026`:

- ✅ simplified the `00-start-here` area into a dashboard plus clear lanes: [methods](./00-start-here/methods/README.md), [resources](./00-start-here/resources/open-resource-library.md), [assessment](./00-start-here/assessment/exam-archive-method.md), [pathways](./00-start-here/pathways/study-pathways.md), and [maintenance](./00-start-here/maintenance/feedback-integration-plan.md)
- ✅ added the root [subject index](./SUBJECTS.md) so readers can jump directly into any `1L`, `2L`, legacy-MEE, or `3L` practice subject
- ✅ folded the old separate pre-`1L` methods folder into [00-start-here/methods](./00-start-here/methods/README.md) and updated internal links

`June 28, 2026`:

- ✅ expanded the [landmark case canon](./00-start-here/assessment/landmark-case-canon.md): added the modern personal-jurisdiction line (`Daimler`, `Ford`), the takings core (`Penn Central`, `Lucas`), `res ipsa`/proximate-cause/unconscionability staples, and split Constitutional Law into `Structure` and `Rights and Liberties` with the substantive-due-process line (`Griswold` → `Obergefell` → `Dobbs`), the Religion Clauses, and the modern Commerce Clause (`Lopez`)
- ✅ added a `Legislation and Regulation` (statutory interpretation) guide: [02-2l-doctrinal-depth-and-codes/legislation-and-regulation](./02-2l-doctrinal-depth-and-codes/legislation-and-regulation/README.md) — textualism vs. purposivism, the canons, major questions; wired into the `2L` order, root README, and resource library
- ✅ Con Law `I` (structure, `1L`) versus Con Law `II` (rights, `2L` continuation) framing added to the [constitutional-law](./01-1l-foundation-year/constitutional-law/README.md) guide — closes roadmap item 3
- ✅ relabeled the bar-coverage gap below to distinguish `NextGen`-dropped subjects from `legacy MEE` subjects
- ✅ built out the three `legacy MEE` subjects as flagged upper-level guides: [family-law](./02-2l-doctrinal-depth-and-codes/family-law/README.md), [trusts-and-estates](./02-2l-doctrinal-depth-and-codes/trusts-and-estates/README.md), and [conflict-of-laws](./02-2l-doctrinal-depth-and-codes/conflict-of-laws/README.md) — kept out of the `NextGen` core sequence and registered in the 2L README, reading sequence, resource library, and case canon
- ✅ `3L` practice-direction tracks: [01-litigation-track.md](./03-3l-practice-synthesis-and-launch/01-litigation-track.md) and [02-transactional-track.md](./03-3l-practice-synthesis-and-launch/02-transactional-track.md) — subjects to revisit, drafting exercises, research emphasis, simulations, and hiring relevance; linked from the `3L` README — closes roadmap item 1
- ✅ explicit `1L` dual-track framing (doctrine lane and legal-research-and-writing lane) added to the [1L README](./01-1l-foundation-year/README.md) — closes roadmap item 2
- ✅ reader progress tracking: new [subject-progress-checklist template](./templates/subject-progress-checklist-template.md), wired into the [study system](./00-start-here/resources/study-system-and-deliverables.md) — closes the "no progress tracking for the reader" gap
- ✅ synced the speedrun admin-law week to current law (`Loper Bright`, major questions) and added the statutory-interpretation companion
- ✅ broke the `H2O` monoculture: added a verified `CALI eLangdell` second source (or a primary-law spine where eLangdell has no title) to all 17 subject guides, wrote the "two independent sources" rule into [05](./00-start-here/resources/source-priority-rule.md), and built a consolidated [second-source map](./00-start-here/resources/open-resource-library.md) — every eLangdell URL verified against the live catalog
- ✅ goal-based study pathways: [study pathways](./00-start-here/pathways/study-pathways.md) — bar-core (NextGen 8), litigation, transactional, and con-law deep-dive routes that cut across the year structure, linked from the root README

`June 10, 2026`:

- ✅ pre-1L methods bridge: [methods bridge](./00-start-here/methods/README.md) — read an opinion, brief and synthesize, outline and attack-sheet, write `IRAC`
- ✅ assessment and exam-archive loop: [assessment and exam archive method](./00-start-here/assessment/exam-archive-method.md)
- ✅ supplement policy and pairings: [supplement policy and pairings](./00-start-here/resources/supplement-policy-and-pairings.md)
- ✅ landmark case canon: [landmark case canon](./00-start-here/assessment/landmark-case-canon.md)
- ✅ `Common Exam Traps` section added to all 13 doctrinal subject READMEs; `Landmark Cases` added to evidence
- ✅ sourcing rule clarified: top-10 band governs teaching materials; primary law and tools use the best free host — see [source priority rule](./00-start-here/resources/source-priority-rule.md)
- ✅ added `T10/Ivy` faculty courses (Amar/Yale, Sandel/Harvard, Fisher/Harvard) and the nonprofit backbone (Cornell LII, CALI, NCC) to [03](./00-start-here/resources/open-resource-library.md) and [06](./00-start-here/resources/ivy-t10-resource-directory.md)
- ✅ fixed corruption in [quick start](./00-start-here/quick-start.md) (leftover patch text and duplicated READMEs)

## Roadmap / Open Work

Prioritized. The original [feedback-plan](./00-start-here/maintenance/feedback-integration-plan.md) items — `3L` practice tracks, `1L` dual-track framing, and the Con Law II split — are now shipped; what remains is polish and reinforcement.

1. automated `link check` in CI to protect the verified-URL stamp (see `link rot` below) — now the highest-value reliability item, with 90+ verified URLs
2. editorial tightening of the `2L` framing as the bar-core upper-level foundation
3. optional spaced-repetition / flashcard guidance tied to the rule sheets and attack outlines

## What Could Be Better

Honest gaps and risks to watch:

- `link rot` — there are 50+ external URLs verified by hand on a date stamp. There is no automated check. A simple link-checker (CI or a script) would catch breakage before a reader hits it.
- `casebook monoculture` — addressed: every subject now carries a verified `CALI eLangdell` second source, or a primary-law spine where eLangdell has no title (business associations, administrative law, professional responsibility, family law, conflict of laws). The "two independent sources" rule is in [05](./00-start-here/resources/source-priority-rule.md). Remaining upside: more faculty-produced material per subject.
- `speedrun drift` — [99-optional-speedrun](./99-optional-speedrun/README.md) re-derives the main curriculum in its own words. As the main guides change, the speedrun can fall out of sync. Tightening it toward cross-references would prevent contradictions.
- `gated practice` — the assessment loop leans on outside question banks. `NCBE NextGen` samples are free, but `CALI` lessons need a school authorization code, which a pure self-studier may not have. Worth listing more fully open practice sources.
- `subject breadth` — the doctrinal guides now cover the `NextGen UBE` foundational set, the traditional upper-level codes, and the three `legacy MEE` subjects `NextGen` drops (`family law`, `trusts and estates`, `conflict of laws`), each built as a flagged upper-level guide outside the `NextGen` core. Subjects beyond any bar core (remedies, federal courts, tax, bankruptcy) stay as expansion-path mentions by design; revisit if the repo's scope grows.
- `no progress tracking for the reader` — the plan defines deliverables but gives the reader no checklist artifact to mark a subject "done." A per-subject progress checklist template could help.

## Repo Map

- [00-start-here](./00-start-here/README.md) — launch dashboard, quick start, methods, resources, assessment, pathways, and maintenance
- [SUBJECTS.md](./SUBJECTS.md) — direct subject jump index
- [01-1l-foundation-year](./01-1l-foundation-year/README.md) — civ pro, torts, contracts, property, criminal law, con law, legal research and writing
- [02-2l-doctrinal-depth-and-codes](./02-2l-doctrinal-depth-and-codes/README.md) — evidence, criminal procedure, business associations, UCC, legislation and regulation, admin law, professional responsibility; plus legacy MEE guides (family law, trusts and estates, conflict of laws)
- [03-3l-practice-synthesis-and-launch](./03-3l-practice-synthesis-and-launch/README.md) — clinics, trial advocacy, advanced writing, bar bridge and career; plus litigation and transactional practice-direction tracks
- [99-optional-speedrun](./99-optional-speedrun/README.md) — compressed timeline version
- [templates](./templates) — case brief, statute brief, reading log, subject review, weekly review, subject progress checklist

## Ground Rules For Edits

- verify any new external URL before adding it; this repo is "verified"-stamped
- keep teaching materials inside the `T10/Ivy` band; use best-free-host for primary law and tools
- match the house voice: terse, backtick-wrapped terms, relative markdown links
- when you change a guide, check whether the `speedrun` mirror needs the same change
