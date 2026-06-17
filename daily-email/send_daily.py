"""Send today's law-school reading assignment by email.

Designed to be run once per day by Windows Task Scheduler. It computes which
day of the 90-day program today is (based on `start_date` in config.json),
formats that day's assignment, and emails it via Gmail SMTP.

Usage:
    python send_daily.py                # send today's assignment (real email)
    python send_daily.py --preview      # print today's email to the console, no send
    python send_daily.py --preview --day 5   # preview a specific day
    python send_daily.py --day 5        # send a specific day (testing)
    python send_daily.py --config other.json

Config (config.json, see config.example.json):
    {
      "recipient": "you@example.com",
      "sender": "you@gmail.com",
      "app_password": "16-char Gmail app password (no spaces)",
      "start_date": "2026-06-16",
      "smtp_host": "smtp.gmail.com",
      "smtp_port": 587
    }
"""
import argparse
import datetime as dt
import json
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

from curriculum import build_schedule, TOTAL_DAYS, YEAR_ORDER

HERE = Path(__file__).resolve().parent
STATE_PATH = HERE / "state.json"

# Public base URL of the GitHub Pages site that build_site.py publishes. Every day
# of the plan is a page there, so each email can link to today's page, the next
# day, and the full index -- letting a fast reader "speedrun" ahead when they
# finish early. Override with the SITE_BASE_URL env var (e.g. a custom domain);
# the default is the project-site URL for this repo (https://<owner>.github.io/<repo>/).
SITE_BASE_URL = os.environ.get(
    "SITE_BASE_URL", "https://mktcowboy.github.io/law-school-speedrun-jd/"
).rstrip("/") + "/"


def day_url(n: int) -> str:
    return f"{SITE_BASE_URL}day-{n:02d}.html"


def index_url() -> str:
    return SITE_BASE_URL


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_config(path: Path) -> dict:
    """Load config from config.json if present, else from MAIL_* env vars.

    The env path is used by GitHub Actions (or any cloud cron), where the values
    come from encrypted repo secrets rather than a file on disk.
    """
    if path.exists():
        cfg = json.loads(path.read_text(encoding="utf-8"))
    else:
        cfg = {
            "recipient": os.environ.get("MAIL_RECIPIENT", ""),
            "sender": os.environ.get("MAIL_SENDER", ""),
            "app_password": os.environ.get("MAIL_APP_PASSWORD", ""),
            "start_date": os.environ.get("MAIL_START_DATE", ""),
        }
        if os.environ.get("MAIL_SMTP_HOST"):
            cfg["smtp_host"] = os.environ["MAIL_SMTP_HOST"]
        if os.environ.get("MAIL_SMTP_PORT"):
            cfg["smtp_port"] = int(os.environ["MAIL_SMTP_PORT"])
    missing = [k for k in ("recipient", "sender", "app_password", "start_date") if not cfg.get(k)]
    if missing:
        sys.exit("Missing config: " + ", ".join(missing) +
                 "\nProvide config.json (run setup.ps1) or set MAIL_* environment variables / repo secrets.")
    cfg.setdefault("smtp_host", "smtp.gmail.com")
    cfg.setdefault("smtp_port", 587)
    return cfg


def day_number(start_date: str, today: dt.date | None = None) -> int:
    today = today or dt.date.today()
    start = dt.date.fromisoformat(start_date)
    return (today - start).days + 1  # day 1 == start_date


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def goal_text_for(entry: dict) -> str:
    """The week's exit standard, phrased as today's goal.

    Study days frame it forward-looking ("By Sunday you'll be able to ..."), so
    drop the "You can " lead-in the source text is written with.
    """
    goal = entry.get("exit", "")
    if entry.get("kind") == "study" and goal.startswith("You can "):
        goal = goal[len("You can "):]
    return goal


def section_label(text: str) -> str:
    return (f'<div style="font-size:11px;letter-spacing:0.09em;text-transform:uppercase;'
            f'color:#9aa0b0;font-weight:600;margin:26px 0 10px;">{text}</div>')


def speedrun_html(n: int) -> str:
    """The "finished early? keep going" panel: a button to the next day's page
    plus a link to the index, so a fast reader can run the plan ahead at will."""
    if n < TOTAL_DAYS:
        button = (
            f'<div style="text-align:center;margin:4px 0 10px;">'
            f'<a href="{day_url(n + 1)}" style="display:inline-block;background:#3b5bdb;'
            f'color:#ffffff;text-decoration:none;padding:13px 26px;border-radius:8px;'
            f'font-weight:600;font-size:15px;">Finished early? Continue to Day {n + 1} &rarr;</a></div>'
        )
        sub = (
            f'<div style="text-align:center;font-size:13px;color:#888;">Keep going as far as you '
            f'like &mdash; <a href="{index_url()}" style="color:#3b5bdb;text-decoration:none;">'
            f'jump to any of the {TOTAL_DAYS} days</a>.</div>'
        )
    else:
        button = ('<div style="text-align:center;margin:4px 0 10px;font-weight:600;font-size:15px;'
                  'color:#2f9e44;">That was Day 90 &mdash; the final day. \U0001f389</div>')
        sub = (f'<div style="text-align:center;font-size:13px;color:#888;">'
               f'<a href="{index_url()}" style="color:#3b5bdb;text-decoration:none;">'
               f'Revisit any of the {TOTAL_DAYS} days</a>.</div>')
    return ('<div style="background:#f7f9fc;border:1px solid #e9edf4;border-radius:10px;'
            'padding:16px 18px;margin:26px 0 6px;">' + button + sub + '</div>')


def content_html(entry: dict) -> str:
    """Inner HTML for one day: year rail, focus, today, reads, week arc and the
    closing panels. Shared by the email body (render) and the published day page
    (build_site.py) so the two always stay in sync."""
    n = entry["day"]
    year = entry.get("year")
    goal_text = goal_text_for(entry)

    pills = []
    for y in YEAR_ORDER:
        if y == year:
            pills.append(f'<span style="background:#3b5bdb;color:#fff;font-size:12px;font-weight:600;'
                         f'padding:2px 10px;border-radius:999px;">{esc(y)}</span>')
        else:
            pills.append(f'<span style="background:#eef0f7;color:#8a90a2;font-size:12px;'
                         f'padding:2px 10px;border-radius:999px;">{esc(y)}</span>')
    rail = ('<span style="color:#c2c7d6;font-size:12px;">&nbsp;&rarr;&nbsp;</span>').join(pills)

    # Week arc: a compact stepper showing where today sits in the 7-day week.
    arc_html = ""
    if entry.get("week_arc"):
        diw = entry.get("day_in_week", 0)
        steps = list(enumerate(entry["week_arc"], start=1))
        steps.append((len(entry["week_arc"]) + 1, "Review & build the week's artifacts"))
        rows = []
        for idx, topic in steps:
            if idx == diw:
                circle = ('<span style="display:inline-block;width:24px;height:24px;line-height:24px;'
                          'text-align:center;border-radius:50%;background:#3b5bdb;color:#fff;'
                          f'font-size:12px;font-weight:600;">{idx}</span>')
                text_style = "color:#16203a;font-weight:600;"
                tag = ('<span style="background:#3b5bdb;color:#fff;font-size:9px;font-weight:600;'
                       'letter-spacing:0.06em;padding:2px 7px;border-radius:999px;margin-left:8px;'
                       'vertical-align:1px;">TODAY</span>')
            elif idx < diw:
                circle = ('<span style="display:inline-block;width:24px;height:24px;line-height:24px;'
                          'text-align:center;border-radius:50%;background:#e7eaf3;color:#9aa0b0;'
                          'font-size:12px;font-weight:600;">&#10003;</span>')
                text_style = "color:#a2a8b6;"
                tag = ""
            else:
                circle = ('<span style="display:inline-block;width:22px;height:22px;line-height:22px;'
                          'text-align:center;border-radius:50%;background:#ffffff;color:#aeb4c2;'
                          f'border:1px solid #d8dce8;font-size:12px;font-weight:600;">{idx}</span>')
                text_style = "color:#5a6072;"
                tag = ""
            rows.append(
                f'<tr><td valign="top" style="padding:5px 0;width:36px;">{circle}</td>'
                f'<td valign="top" style="padding:6px 0 6px 4px;font-size:14px;line-height:1.4;{text_style}">'
                f'{esc(topic)}{tag}</td></tr>'
            )
        arc_html = (
            '<div style="background:#fafbfd;border:1px solid #eef0f5;border-radius:10px;padding:12px 18px;">'
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
            'style="width:100%;border-collapse:collapse;">' + "".join(rows) + '</table></div>'
        )

    parts = [
        f'<p style="color:#888;font-size:13px;margin:0 0 4px;">{esc(entry.get("year_label", entry["phase"]))}</p>',
        f'<h2 style="margin:0 0 4px;">{esc(entry["title"])}</h2>',
        f'<p style="color:#666;margin:0 0 10px;">Day {n} of {TOTAL_DAYS}</p>',
        f'<div style="margin:0 0 20px;">{rail}</div>',
        f'<p style="margin:0 0 4px;"><strong>Focus.</strong> {esc(entry["focus"])}</p>',
        '<div style="background:#f4f6fb;border-left:4px solid #3b5bdb;padding:12px 16px;margin:18px 0;">'
        '<div style="font-size:11px;letter-spacing:0.09em;text-transform:uppercase;color:#3b5bdb;'
        'font-weight:600;margin-bottom:4px;">Today</div>'
        f'<div style="color:#16203a;">{esc(entry["topic"])}</div></div>',
    ]
    if entry.get("reads"):
        parts.append(section_label("Read &mdash; and what to do"))
        parts.append('<ol style="padding-left:22px;margin:0;">')
        for r in entry["reads"]:
            parts.append(
                f'<li style="margin-bottom:14px;padding-left:4px;">'
                f'<a href="{esc(r["url"])}" style="font-weight:600;color:#2952cc;text-decoration:none;">{esc(r["label"])}</a>'
                f'<div style="color:#555;font-size:14px;margin-top:3px;">{esc(r["do"])}</div></li>'
            )
        parts.append("</ol>")
    if arc_html:
        parts.append(section_label(f"This week &middot; {esc(entry['subject'])}"))
        parts.append(arc_html)
    if entry.get("canon"):
        items = "".join(f'<li style="margin-bottom:5px;">{esc(c)}</li>' for c in entry["canon"])
        parts.append(section_label("This week's canon &mdash; recall from memory"))
        parts.append(f'<ul style="margin:0;padding-left:22px;color:#333;font-size:14px;">{items}</ul>')
    if entry.get("build"):
        items = "".join(f'<li style="margin-bottom:5px;">{esc(b)}</li>' for b in entry["build"])
        parts.append(section_label("Build"))
        parts.append(f'<ul style="margin:0;padding-left:22px;color:#333;font-size:14px;">{items}</ul>')
    if entry.get("writing"):
        items = "".join(f'<li style="margin-bottom:5px;">{esc(w)}</li>' for w in entry["writing"])
        parts.append(section_label("Writing assignment"))
        parts.append(f'<ul style="margin:0;padding-left:22px;color:#333;font-size:14px;">{items}</ul>')
    if entry.get("exit"):
        goal_label = "By Sunday you'll be able to" if entry.get("kind") == "study" else "Week exit standard"
        parts.append(
            '<div style="background:#f0fdf4;border-left:4px solid #2f9e44;padding:12px 16px;margin:18px 0;">'
            '<div style="font-size:11px;letter-spacing:0.09em;text-transform:uppercase;color:#2f9e44;'
            f'font-weight:600;margin-bottom:4px;">{goal_label}</div>'
            f'<div style="color:#1f5132;font-size:14px;">{esc(goal_text)}</div></div>'
        )
    if entry.get("connect"):
        parts.append(
            '<div style="background:#fff8ec;border-left:4px solid #e8a13a;padding:12px 16px;margin:18px 0;">'
            '<div style="font-size:11px;letter-spacing:0.09em;text-transform:uppercase;color:#c77f1a;'
            'font-weight:600;margin-bottom:4px;">How this connects</div>'
            f'<div style="color:#5a4a2a;font-size:14px;">{esc(entry["connect"])}</div></div>'
        )
    if entry.get("source_links"):
        links = " &nbsp;·&nbsp; ".join(f'<a href="{esc(u)}">{esc(l)}</a>' for l, u in entry["source_links"])
        parts.append(f'<p style="color:#888;font-size:13px;margin-top:18px;"><strong>Teaching source (T10/Ivy):</strong> {links}</p>')
    return "\n".join(parts)


def render(entry: dict) -> tuple[str, str, str]:
    """Return (subject, plaintext, html) for the day's email."""
    n = entry["day"]
    subject = f"[Law Speedrun] Day {n}/{TOTAL_DAYS} - {entry['subject']}"

    year = entry.get("year")
    year_rail = "  ->  ".join(f"[{y}]" if y == year else y for y in YEAR_ORDER)
    goal_text = goal_text_for(entry)

    # ---- Plain text ----
    lines = [
        entry["title"],
        entry.get("year_label", entry["phase"]),
        f"JD year: {year_rail}",
        "=" * 60,
        "",
        "FOCUS",
        f"  {entry['focus']}",
        "",
        "TODAY",
        f"  {entry['topic']}",
        "",
    ]
    if entry.get("reads"):
        lines.append("READ (and what to do)")
        for i, r in enumerate(entry["reads"], start=1):
            lines.append(f"  {i}. {r['label']}")
            lines.append(f"     {r['do']}")
            lines.append(f"     {r['url']}")
        lines.append("")
    if entry.get("week_arc"):
        diw = entry.get("day_in_week", 0)
        lines.append(f"THIS WEEK ({entry['subject']})")
        for idx, t in enumerate(entry["week_arc"], start=1):
            if idx == diw:
                lines.append(f"  > Day {idx}: {t}   <- you are here")
            elif idx < diw:
                lines.append(f"  x Day {idx}: {t}")
            else:
                lines.append(f"    Day {idx}: {t}")
        lines.append(f"  + Day {len(entry['week_arc']) + 1}: Review & build the week's artifacts")
        lines.append("")
    if entry.get("canon"):
        lines.append("THIS WEEK'S CANON (recall from memory)")
        for c in entry["canon"]:
            lines.append(f"  - {c}")
        lines.append("")
    if entry.get("build"):
        lines.append("BUILD")
        for b in entry["build"]:
            lines.append(f"  - {b}")
        lines.append("")
    if entry.get("writing"):
        lines.append("WRITING ASSIGNMENT")
        for w in entry["writing"]:
            lines.append(f"  - {w}")
        lines.append("")
    if entry.get("exit"):
        lines.append("BY SUNDAY YOU'LL BE ABLE TO" if entry.get("kind") == "study" else "WEEK EXIT STANDARD")
        lines.append(f"  {goal_text}")
        lines.append("")
    if entry.get("connect"):
        lines.append("HOW THIS CONNECTS")
        lines.append(f"  {entry['connect']}")
        lines.append("")
    if entry.get("source_links"):
        lines.append("TEACHING SOURCE (T10/IVY)")
        for label, url in entry["source_links"]:
            lines.append(f"  - {label}: {url}")
        lines.append("")
    lines.append("SPEEDRUN (finished early? keep going)")
    lines.append(f"  Read this day online:  {day_url(n)}")
    if n < TOTAL_DAYS:
        lines.append(f"  Next -> Day {n + 1}:       {day_url(n + 1)}")
    lines.append(f"  Jump to any of {TOTAL_DAYS} days: {index_url()}")
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"Day {n} of {TOTAL_DAYS} - keep going.")
    plain = "\n".join(lines)

    # ---- HTML ----  (content_html is shared with the published day pages)
    html = (
        '<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;'
        'max-width:640px;margin:0 auto;color:#1a1a1a;line-height:1.55;">'
        f'<p style="text-align:right;font-size:12px;margin:0 0 12px;">'
        f'<a href="{day_url(n)}" style="color:#b3b8c4;text-decoration:none;">View online &rarr;</a></p>'
        + content_html(entry)
        + speedrun_html(n)
        + '<hr style="border:none;border-top:1px solid #eee;margin:22px 0;">'
        '<p style="color:#999;font-size:12px;">Automated daily reading from your '
        'law-school-speedrun-jd plan.</p></div>'
    )
    return subject, plain, html


def send_email(cfg: dict, subject: str, plain: str, html: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = cfg["sender"]
    msg["To"] = cfg["recipient"]
    msg.set_content(plain)
    msg.add_alternative(html, subtype="html")
    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"], timeout=30) as server:
        server.starttls()
        server.login(cfg["sender"], cfg["app_password"])
        server.send_message(msg)


def main() -> int:
    ap = argparse.ArgumentParser(description="Send today's law-school reading assignment.")
    ap.add_argument("--config", default=str(HERE / "config.json"), help="path to config.json")
    ap.add_argument("--preview", action="store_true", help="print the email instead of sending")
    ap.add_argument("--day", type=int, default=None, help="override which day to send (1-90)")
    ap.add_argument("--force", action="store_true", help="send even if today's day was already sent")
    args = ap.parse_args()

    schedule = build_schedule()

    if args.preview:
        # Preview never sends, so it only needs config to resolve "today".
        if args.day is not None:
            cfg, n = None, args.day
        else:
            try:
                cfg = load_config(Path(args.config))
                n = day_number(cfg["start_date"])
            except SystemExit:
                n = 1  # no config/env and no --day: preview day 1
    else:
        cfg = load_config(Path(args.config))
        n = args.day if args.day is not None else day_number(cfg["start_date"])

    if n < 1:
        print(f"Program has not started yet (computed day {n}). Start date is in the future.")
        return 0
    if n > TOTAL_DAYS:
        print(f"Program complete: day {n} is past the {TOTAL_DAYS}-day plan. Nothing to send.")
        return 0

    entry = schedule[n - 1]
    subject, plain, html = render(entry)

    if args.preview:
        print(f"SUBJECT: {subject}\n")
        print(plain)
        return 0

    # Idempotency: do not send the same day twice unless --force.
    state = load_state()
    if not args.force and state.get("last_sent_day") == n and args.day is None:
        print(f"Day {n} already sent on {state.get('last_sent_at')}. Use --force to resend.")
        return 0

    send_email(cfg, subject, plain, html)
    if args.day is None:
        state["last_sent_day"] = n
        state["last_sent_at"] = dt.datetime.now().isoformat(timespec="seconds")
        save_state(state)
    print(f"Sent day {n}/{TOTAL_DAYS} to {cfg['recipient']}: {entry['subject']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
