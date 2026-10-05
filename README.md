HOSPITALITY AI LANDSCAPE TRACKER
================================

A small research tracker that maps companies building AI tools for hotel and
hospitality operations: who they are, what they do, who funded them, and how
well each fact is sourced.

Data as of October 2026. 21 companies. Built with AI assistance (Claude) for
the search and the script; every source was then checked by hand.


WHAT'S IN THIS FOLDER
---------------------
tracker.py      The script. Python 3 only, no extra packages to install.
companies.csv   The data. One row per company. This is the single source of truth.
README.txt      This file.


HOW TO RUN IT
-------------
1. Install Python 3 (python.org). On Windows, tick "Add python.exe to PATH".
2. Put tracker.py and companies.csv in the same folder.
3. Open a terminal in that folder and run one of these
   (on Windows, use "py" instead of "python" if "python" is not recognized):

   python tracker.py check            List rows that still need attention
   python tracker.py summary          Companies and disclosed funding by segment
   python tracker.py verify "Mews"    Mark a company as checked against a source
   python tracker.py add              Add a new company (prompts for each field)
   python tracker.py export           Print a markdown table for a report

Close companies.csv in Excel before running the script, or it cannot read it.


WHAT "CHECK" LOOKS FOR
----------------------
- Missing name, segment, stage, date, or source link
- Rows not yet marked verified
- Rows that rely only on an aggregator website
- Missing funding amount (skipped for acquisitions, joint ventures, and
  incumbents with an "n/a" stage)
- Dates not written like 2026 or 2026-03
- Rows not checked in the last 30 days

A clean run prints "0 of 21 rows need attention."


THE COLUMNS
-----------
name            Company name
segment         Category, e.g. Guest experience, Revenue management,
                PMS / operating system, Back-office, Operations / housekeeping
hq              Headquarters city, where known
stage           Funding stage (Pre-seed, Seed, Series A to D), or a label such as
                Acquired, or "n/a" where there was no funding round
amount_usd_m    Size of the disclosed round, in US dollars, millions
investors       Lead and other named investors
date            Year or year-month of the round or event (2026 or 2026-03)
status          independent, acquired, joint_venture, or incumbent
source_type     Kind of source: press release, news, aggregator, LinkedIn, etc.
source_url      Link to the source
verified        "yes" only after the fact was checked against the source
last_checked    Date the row was last reviewed
notes           Caveats, company claims, and anything unresolved


HOW SOURCES WERE HANDLED
------------------------
- Company or investor announcements are treated as primary sources.
- News articles and databases (Pitchbook, Dealroom and similar) are secondary.
  Aggregator-only rows are flagged by the script.
- A company announcement shows what the company said. Figures such as savings
  or revenue gains are company claims, not measured results, and are noted as
  such in the notes column.


KNOWN LIMITS
------------
- The list comes from web searches. It is a sample, not a complete census.
  Apaleo, Agilysys, and hotel payments companies are not covered.
- Amounts are single disclosed rounds, not lifetime funding. The "summary"
  command adds up rounds from different years, so treat its totals as rough.
- The headline figure in the accompanying one-pager (about 97% of roughly
  $883M raised in verified rounds since 2024 going to five companies) was
  calculated from the verified 2024-and-later rows, not by the summary command.
- Q Concierge's amount rests on one database source.


AUTHOR
------
Justin Maharaj, Orlando, FL
