"""Build the static web version of the 90-day daily reading plan.

The email points readers at the current day page, the next day page, and an
index. This script publishes those pages from the same renderer used by the
email body so the web and inbox versions stay in sync.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from curriculum import TOTAL_DAYS, build_schedule
from send_daily import content_html, esc, speedrun_html


HERE = Path(__file__).resolve().parent
DEFAULT_OUT = HERE.parent / "site"


def page_shell(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      background: #f3f5f9;
      color: #1a1a1a;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.55;
    }}
    main {{
      max-width: 720px;
      margin: 0 auto;
      padding: 28px 18px 48px;
    }}
    .page {{
      background: #ffffff;
      border: 1px solid #e8ebf2;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 10px 30px rgba(22, 32, 58, 0.06);
    }}
    .topnav {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
      font-size: 14px;
    }}
    .topnav a {{
      color: #3b5bdb;
      text-decoration: none;
      font-weight: 600;
    }}
    @media (max-width: 560px) {{
      main {{ padding: 14px 10px 32px; }}
      .page {{ padding: 18px 14px; border-radius: 8px; }}
      .topnav {{ flex-wrap: wrap; }}
    }}
  </style>
</head>
<body>
  <main>{body}</main>
</body>
</html>
"""


def day_nav(day: int) -> str:
    previous_link = (
        f'<a href="day-{day - 1:02d}.html">&larr; Day {day - 1}</a>'
        if day > 1
        else "<span></span>"
    )
    next_link = (
        f'<a href="day-{day + 1:02d}.html">Day {day + 1} &rarr;</a>'
        if day < TOTAL_DAYS
        else "<span></span>"
    )
    return (
        '<nav class="topnav" aria-label="Day navigation">'
        f"{previous_link}"
        '<a href="index.html">All days</a>'
        f"{next_link}"
        "</nav>"
    )


def render_day(entry: dict) -> str:
    day = entry["day"]
    body = (
        day_nav(day)
        + '<article class="page">'
        + content_html(entry)
        + speedrun_html(day)
        + "</article>"
    )
    return page_shell(f"Law Speedrun Day {day}: {esc(entry['subject'])}", body)


def render_index(schedule: list[dict]) -> str:
    items = []
    for entry in schedule:
        day = entry["day"]
        items.append(
            '<li style="margin:0 0 10px;">'
            f'<a href="day-{day:02d}.html" style="color:#3b5bdb;font-weight:600;text-decoration:none;">'
            f"Day {day}: {esc(entry['subject'])}</a>"
            f'<div style="color:#555;font-size:14px;">{esc(entry["topic"])}</div>'
            "</li>"
        )
    body = (
        '<article class="page">'
        '<p style="color:#888;font-size:13px;margin:0 0 4px;">90-day JD reading plan</p>'
        '<h1 style="margin:0 0 10px;">Law School Speedrun</h1>'
        '<p style="margin:0 0 22px;color:#555;">Open any day, then keep moving forward when you finish early.</p>'
        f'<ol style="padding-left:22px;margin:0;">{"".join(items)}</ol>'
        "</article>"
    )
    return page_shell("Law School Speedrun Daily Reading", body)


def build(out_dir: Path) -> None:
    schedule = build_schedule()
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "index.html").write_text(render_index(schedule), encoding="utf-8")
    for entry in schedule:
        day = entry["day"]
        (out_dir / f"day-{day:02d}.html").write_text(render_day(entry), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static daily reading pages.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output directory")
    args = parser.parse_args()

    build(args.out)
    print(f"Built {TOTAL_DAYS} day pages plus index in {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
