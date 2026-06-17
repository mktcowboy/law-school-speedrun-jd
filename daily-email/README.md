# Daily Reading Email

A daily email that walks you through a 90-day JD reading plan built on **Ivy
League and T10 law-school teaching materials** — Harvard, Yale, Columbia, and
Penn — paired with canonical primary law. One focused assignment per day from the
12-week speedrun curriculum (`99-optional-speedrun`).

Each email contains:

- the day's focus and the exact rules/cases to read — each linked, with what to do;
- a one-line thread tying the day to what came before and after;
- a school-tagged **T10/Ivy teaching source** for context.
- a speedrun link to the current day online, the next day, and the full index so
  you can keep going when you finish early.

Every 7th day reviews and builds; the final 6 bridge into bar prep.

## Sourcing

Per the repo's own rule (`00-start-here/05-top-10-school-priority-basis.md`):

- **Teaching → T10/Ivy, Ivy-first.** Harvard H2O casebooks plus Yale, Columbia,
  and Penn guides (Duke and Stanford only where the Ivies lack a strong public
  option). Every teaching link is tagged with its school.
- **The law itself → canonical free hosts.** Cornell LII for rules, statutes, the
  Constitution, and Supreme Court opinions (each SCOTUS link verified
  individually); CourtListener for other cases; ABA Model Rules for ethics.

## What you need

A **Gmail account to send from**, with an **app password**: enable
[2-Step Verification](https://myaccount.google.com/security), then create one
under [App passwords](https://myaccount.google.com/apppasswords) ("Mail" → 16
letters). The recipient can be any address.

## Setup

**Cloud — GitHub Actions (recommended; runs even when your PC is off).**
Workflow: [`.github/workflows/daily-reading-email.yml`](../.github/workflows/daily-reading-email.yml).

1. In the repo: **Settings → Secrets and variables → Actions → New repository
   secret**, add three: `MAIL_RECIPIENT`, `MAIL_SENDER`, `MAIL_APP_PASSWORD`.
2. (Optional) Add a `MAIL_START_DATE` (`YYYY-MM-DD`) **Variable** for Day 1; else
   the workflow default applies.
3. In **Settings → Pages**, set the build/deploy source to **GitHub Actions** so
   the click-through day pages can publish.
4. Push `daily-email/` and `.github/` to the default branch.
5. Test: **Actions → Daily reading email → Run workflow**, then check your inbox.

Runs daily at `0 11 * * *` = 11:00 UTC = **6 AM US Central** (daylight months; use
`0 12` for 6 AM CST in winter). A tiny `[skip ci]` keepalive commit each run
prevents GitHub's 60-day pause — so `git pull` before your next local push.

**Local — Windows (alternative).** Needs Python 3.10+. In PowerShell, from this
folder: `powershell -ExecutionPolicy Bypass -File .\setup.ps1` — it prompts for
your details, writes `config.json`, sends a Day 1 test, and registers a daily task.

## Reference

```powershell
python send_daily.py --preview            # print today's email, no send
python send_daily.py --preview --day 30   # preview any day 1-90
python send_daily.py --day 1              # send a specific day (test)
```

- Day number = `(today - start_date) + 1`; before the start it waits, after Day 90 it stops.
- **Stop/change (cloud):** Actions → the workflow → `...` → Disable; edit `cron:`
  to retime; `MAIL_START_DATE` to reset Day 1.
- **Stop/change (local):** `Unregister-ScheduledTask -TaskName LawSchoolDailyReading -Confirm:$false`.
- **Non-Gmail:** set `smtp_host`/`smtp_port` in `config.json`, or
  `MAIL_SMTP_HOST`/`MAIL_SMTP_PORT` env in the workflow.
- **Edit the plan:** change `WEEKS`/`BAR_BRIDGE_TAIL` in `curriculum.py`, then run
  `python curriculum.py` to confirm it still totals 90 days.

| File | Purpose |
|------|---------|
| `curriculum.py` | The 90-day schedule (data + builder). |
| `send_daily.py` | Builds and sends today's email (config.json locally, `MAIL_*` secrets in the cloud). |
| `build_site.py` | Publishes the linked day pages and full index used by the email speedrun links. |
| `../.github/workflows/daily-reading-email.yml` | Cloud daily schedule. |
| `setup.ps1`, `config.example.json` | Local setup. `config.json` / `state.json` are git-ignored. |
