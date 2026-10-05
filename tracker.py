#!/usr/bin/env python3
"""
Hospitality AI landscape tracker.

Keeps one CSV (companies.csv) as the single source of truth and gives you
four commands. Standard library only, so it runs anywhere Python 3 does.

    python tracker.py check            # list data-quality problems
    python tracker.py summary          # companies and disclosed funding by segment
    python tracker.py verify "Mews"    # mark a row as checked against a primary source
    python tracker.py add              # add a company interactively
    python tracker.py export           # print a markdown table for the one-pager
"""
import csv
import re
import sys
from datetime import date, datetime
from pathlib import Path

FILE = Path(__file__).with_name("companies.csv")
REQUIRED = ["name", "segment", "stage", "date", "source_url"]
STALE_DAYS = 30


def load():
    with open(FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def save(fields, rows):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_day(text):
    """Accept 2026-10-04 (what the script writes) or 10/4/2026 (what Excel writes)."""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError(text)


def check():
    """Flag rows a careful reader would not trust yet."""
    _, rows = load()
    problems = 0
    for r in rows:
        issues = [f"missing {k}" for k in REQUIRED if not r[k].strip()]
        if r["verified"] != "yes":
            issues.append("not verified against a primary source")
        if r["source_type"] == "aggregator":
            issues.append("aggregator source only" + (" (but marked verified)" if r["verified"] == "yes" else ""))
        if r["date"].strip() and not re.fullmatch(r"\d{4}(-\d{2}){0,2}", r["date"].strip()):
            issues.append(f"date '{r['date']}' should look like 2026 or 2026-03")
        if r["status"] not in ("acquired", "joint_venture", "merged") and not r["stage"].lower().startswith("n/a") and not r["amount_usd_m"].strip():
            issues.append("no disclosed amount")
        try:
            age = (date.today() - parse_day(r["last_checked"])).days
            if age > STALE_DAYS:
                issues.append(f"stale ({age} days since last check)")
        except ValueError:
            issues.append("bad last_checked date")
        if issues:
            problems += 1
            print(f"{r['name']}: " + "; ".join(issues))
    print(f"\n{problems} of {len(rows)} rows need attention.")


def summary():
    """Count companies and add up disclosed funding per segment."""
    _, rows = load()
    seg = {}
    for r in rows:
        s = seg.setdefault(r["segment"], {"n": 0, "funding": 0.0, "acquired": 0})
        s["n"] += 1
        s["acquired"] += r["status"] == "acquired"
        if r["amount_usd_m"].strip():
            s["funding"] += float(r["amount_usd_m"])
    print(f"{'Segment':28}{'Cos':>5}{'Acquired':>10}{'Disclosed $M':>15}")
    for name, s in sorted(seg.items(), key=lambda kv: -kv[1]["funding"]):
        print(f"{name:28}{s['n']:>5}{s['acquired']:>10}{s['funding']:>15,.1f}")
    print("\nNote: amounts are single disclosed rounds, not lifetime funding, and mix dates.")


def verify(name):
    """Mark a company as verified and reset its last_checked date."""
    fields, rows = load()
    hit = [r for r in rows if r["name"].lower() == name.lower()]
    if not hit:
        sys.exit(f"No company named '{name}'.")
    hit[0]["verified"] = "yes"
    hit[0]["last_checked"] = date.today().isoformat()
    save(fields, rows)
    print(f"{hit[0]['name']} marked verified.")


def add():
    fields, rows = load()
    new = {k: "" for k in fields}
    for k in fields:
        if k in ("verified", "last_checked"):
            continue
        new[k] = input(f"{k}: ").strip()
    new["verified"] = "no"
    new["last_checked"] = date.today().isoformat()
    rows.append(new)
    save(fields, rows)
    print("Added. Run 'check' to see what still needs sourcing.")


def export():
    """Markdown table, grouped by segment, ready to paste into the brief."""
    _, rows = load()
    print("| Company | Segment | Stage | $M | Date |\n|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r["segment"], r["name"])):
        print(f"| {r['name']} | {r['segment']} | {r['stage']} | {r['amount_usd_m']} | {r['date']} |")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        check()
    elif cmd == "summary":
        summary()
    elif cmd == "verify" and len(sys.argv) > 2:
        verify(sys.argv[2])
    elif cmd == "add":
        add()
    elif cmd == "export":
        export()
    else:
        print(__doc__)
