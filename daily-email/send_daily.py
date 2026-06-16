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

from curriculum import build_schedule, TOTAL_DAYS

HERE = Path(__file__).resolve().parent
STATE_PATH = HERE / "state.json"


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


def render(entry: dict) -> tuple[str, str, str]:
    """Return (subject, plaintext, html) for the day's email."""
    n = entry["day"]
    subject = f"[Law Speedrun] Day {n}/{TOTAL_DAYS} - {entry['subject']}"

    # ---- Plain text ----
    lines = [
        entry["title"],
        entry["phase"],
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
        lines.append("WEEK EXIT STANDARD")
        lines.append(f"  {entry['exit']}")
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
    lines.append("-" * 60)
    lines.append(f"Day {n} of {TOTAL_DAYS} - keep going.")
    plain = "\n".join(lines)

    # ---- HTML ----
    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    html_parts = [
        '<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;'
        'max-width:640px;margin:0 auto;color:#1a1a1a;line-height:1.55;">',
        f'<p style="color:#888;font-size:13px;margin:0 0 4px;">{esc(entry["phase"])}</p>',
        f'<h2 style="margin:0 0 4px;">{esc(entry["title"])}</h2>',
        f'<p style="color:#666;margin:0 0 18px;">Day {n} of {TOTAL_DAYS}</p>',
        f'<p><strong>Focus.</strong> {esc(entry["focus"])}</p>',
        f'<div style="background:#f4f6fb;border-left:4px solid #3b5bdb;padding:12px 16px;'
        f'margin:16px 0;"><strong>Today</strong><br>{esc(entry["topic"])}</div>',
    ]
    if entry.get("reads"):
        html_parts.append('<p style="margin:18px 0 8px;"><strong>Read (and what to do)</strong></p>')
        html_parts.append('<ol style="padding-left:20px;margin:0;">')
        for r in entry["reads"]:
            html_parts.append(
                f'<li style="margin-bottom:12px;"><a href="{esc(r["url"])}" '
                f'style="font-weight:500;">{esc(r["label"])}</a>'
                f'<br><span style="color:#444;font-size:14px;">{esc(r["do"])}</span></li>'
            )
        html_parts.append("</ol>")
    if entry.get("canon"):
        items = "".join(f"<li>{esc(c)}</li>" for c in entry["canon"])
        html_parts.append(f'<p style="margin:18px 0 8px;"><strong>This week\'s canon (recall from memory)</strong></p><ul>{items}</ul>')
    if entry.get("build"):
        items = "".join(f"<li>{esc(b)}</li>" for b in entry["build"])
        html_parts.append(f"<p><strong>Build</strong></p><ul>{items}</ul>")
    if entry.get("writing"):
        items = "".join(f"<li>{esc(w)}</li>" for w in entry["writing"])
        html_parts.append(f"<p><strong>Writing assignment</strong></p><ul>{items}</ul>")
    if entry.get("exit"):
        html_parts.append(
            f'<p style="background:#f0fdf4;border-left:4px solid #2f9e44;padding:10px 14px;">'
            f'<strong>Week exit standard.</strong> {esc(entry["exit"])}</p>'
        )
    if entry.get("connect"):
        html_parts.append(
            f'<p style="background:#fff8ec;border-left:4px solid #e8a13a;padding:10px 14px;'
            f'color:#5a4a2a;font-size:14px;"><strong>How this connects.</strong> {esc(entry["connect"])}</p>'
        )
    if entry.get("source_links"):
        links = " &nbsp;·&nbsp; ".join(f'<a href="{esc(u)}">{esc(l)}</a>' for l, u in entry["source_links"])
        html_parts.append(f'<p style="color:#888;font-size:13px;margin-top:18px;"><strong>Teaching source (T10/Ivy):</strong> {links}</p>')
    html_parts.append('<hr style="border:none;border-top:1px solid #eee;margin:20px 0;">')
    html_parts.append('<p style="color:#999;font-size:12px;">Automated daily reading from your '
                      'law-school-speedrun-jd plan.</p></div>')
    html = "\n".join(html_parts)
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
