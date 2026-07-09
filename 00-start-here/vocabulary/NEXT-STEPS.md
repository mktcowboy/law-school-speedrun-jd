# Vocabulary Next Steps

Back to the [vocabulary overview](./README.md).

The first-pass buildout is populated and split across category and doctrine files. Treat the next pass as review and hardening, not raw expansion.

## Review Pass

- Check duplicate terms across cross-cutting and doctrine files; keep intentional repeats only where the subject treatment differs.
- Spot-check Wex links, especially compound terms and broader fallback links.
- Confirm each file is alphabetized by entry heading.
- Tighten weak definitions that read too generic or too bar-outline-ish.
- Move misplaced terms into the file where a student is most likely to need them first.
- Normalize related-term lists so they point to nearby useful vocabulary, not just loosely associated words.

## Structure Pass

- Add subject backlinks from each doctrine file to the matching course guide or landmark-case section.
- Decide whether cross-cutting files should have mini tables of contents once the term count settles.
- Keep `glossary.md` removed; the split files are now the source of truth.

## Verification

- Count entries and Wex lines; they should match.
- Search for stale links to `glossary.md`.
- Check relative Markdown links inside `00-start-here/vocabulary`.
- Run `git status` after fixing the safe-directory guard:

```powershell
git config --global --add safe.directory C:/Users/blake/Desktop/github/law-school-speedrun-jd
```

## Commit Candidate

Once the review pass is clean, commit this as the vocabulary architecture buildout.
