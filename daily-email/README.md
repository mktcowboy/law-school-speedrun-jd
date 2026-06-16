# Daily Reading Email

Emails you one short reading assignment per day for 90 days, walking through the
12-week speedrun curriculum (`99-optional-speedrun`). Each email contains the
day's focus, the specific task, the open-source reading links, and the key
cases/rules for that week. Review days add the build artifacts and writing
assignments; the last 6 days bridge into bar prep.

## What you need

- **Python 3.10+** (already installed on this machine).
- A **Gmail account** to send from, with a **Gmail App Password**:
  1. Enable 2-Step Verification: <https://myaccount.google.com/security>
  2. Create an app password: <https://myaccount.google.com/apppasswords>
     (pick "Mail" / any device name). You'll get a 16-letter password.
  - The recipient can be any email address; the sender must be Gmail.

> Don't have/want a Gmail sender? Any SMTP provider works — set `smtp_host`,
> `smtp_port`, `sender`, and `app_password` in `config.json` accordingly.

## Two ways to run it

| | Local (Windows Task Scheduler) | Cloud (GitHub Actions) |
|---|---|---|
| Runs when PC is off | No (catches up at next wake) | Yes |
| Cost | Free | Free |
| Credentials live in | `config.json` (git-ignored) | encrypted repo secrets |
| Setup | run `setup.ps1` | add 3 secrets, push, done |

The same `send_daily.py` powers both: it reads `config.json` if present, else
falls back to `MAIL_*` environment variables (which Actions supplies from secrets).

## Option A — Cloud (GitHub Actions, runs even when your PC is off)

Workflow: [`.github/workflows/daily-reading-email.yml`](../.github/workflows/daily-reading-email.yml).

1. Create a Gmail app password (see "What you need" above).
2. In the GitHub repo: **Settings -> Secrets and variables -> Actions -> New
   repository secret**, add three secrets:
   - `MAIL_RECIPIENT` — where the daily email goes
   - `MAIL_SENDER` — your Gmail address
   - `MAIL_APP_PASSWORD` — the 16-letter app password
3. (Optional) Set Day 1: add a repository **Variable** `MAIL_START_DATE`
   (`YYYY-MM-DD`). If omitted, it uses the default in the workflow file.
4. Commit and push `daily-email/` and `.github/` to the repo's default branch.
5. Test now: **Actions tab -> Daily reading email -> Run workflow**. Check your inbox.

After that it runs daily on the cron in the workflow (default `0 12 * * *` =
12:00 UTC). Change the time by editing that `cron:` line (GitHub cron is UTC).

Notes:
- GitHub pauses scheduled workflows after 60 days with no repo commits, which
  would otherwise stop this near day 60. The workflow's "keepalive commit" step
  writes `daily-email/last_run.txt` each run to reset that clock (it uses
  `[skip ci]` so it never re-triggers itself). After it runs, `git pull` before
  your next local push. If your default branch is protected, the push is skipped
  — either allow it or push any commit manually within each 60-day window.
- Cron runs are best-effort and can be delayed a few minutes under load.

## Option B — Local (Windows Task Scheduler)

Open **PowerShell in this folder** and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

It asks for your recipient email, Gmail sender + app password, start date, and
daily send time; writes `config.json`; sends a **test email (Day 1)** so you can
confirm delivery; and registers a Windows Scheduled Task
(`LawSchoolDailyReading`) that runs every day at your chosen time.

If your PC is asleep or off at send time, the task runs at the next wake
(`StartWhenAvailable`), so you won't silently skip a day.

## Manual use / testing

```powershell
py send_daily.py --preview            # print today's email, no send
py send_daily.py --preview --day 30   # preview any day 1-90
py send_daily.py --day 1              # actually send a specific day (test)
py send_daily.py                      # send today's assignment
```

- The day number is computed as `(today - start_date) + 1`. Day 1 == `start_date`.
- Before the start date it does nothing; after Day 90 it reports "complete".
- `state.json` records the last day sent so a double-run won't email twice
  (override with `--force`).

## Files

| File | Purpose |
|------|---------|
| `curriculum.py` | The 90-day schedule (data + builder). Run it to print the full plan. |
| `send_daily.py` | Computes today's day, formats the email, sends via SMTP. |
| `setup.ps1` | Interactive setup + scheduled-task registration. |
| `config.example.json` | Template; `setup.ps1` writes the real `config.json`. |
| `config.json` / `state.json` | Local only — git-ignored (the app password lives here). |

## How the reading links work

This follows the repo's own sourcing rule (`00-start-here/05-top-10-school-priority-basis.md`),
which has two layers:

1. Teaching materials are T10/Ivy, Ivy-first. Each email's "Teaching source
   (T10/Ivy)" line uses the repo's directory (`00-start-here/06`): Harvard H2O
   casebook spines plus Yale, Columbia, Penn, and (where Ivies lack a strong
   public option) Duke and Stanford guides. Every link is tagged with its school.
2. Primary law and case-reading use the nonprofit backbone the same rule names
   as best-in-class regardless of rank:
   - Rules, statutes, Constitution, and Supreme Court opinions → Cornell LII
     (`law.cornell.edu`). Every SCOTUS link was verified individually.
   - Non-Supreme-Court cases → CourtListener search links (open the opinion).
   - ABA Model Rules → the Model Rules table of contents (open the named rule).

So each day points you to elite teaching for context and to canonical free hosts
for the law itself, exactly as the curriculum prescribes.

## Editing the curriculum

Edit the `WEEKS` and `BAR_BRIDGE_TAIL` data in `curriculum.py`, then run
`py curriculum.py` to confirm it still totals 90 days.

## Stop or change the schedule

```powershell
# Stop daily emails
Unregister-ScheduledTask -TaskName LawSchoolDailyReading -Confirm:$false

# Change the time / restart: just re-run setup.ps1
```
