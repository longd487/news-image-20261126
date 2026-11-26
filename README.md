# news-image-20261126 — one image for 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/longd487/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/longd487/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

This repository is an entry for the make.fun bounty ["Sum up 26 November's world news in one image"](https://make.fun/bounty/news-image-20261126). The entry is a program: when the grader runs it, it writes a single image to `/output/entry.png`. An AI judge then compares images two at a time and picks the one that best sums up the day's world news.

## What the picture shows

A 1024×1024 front page, "THE WORLD TODAY — Thursday, 26 November 2026", built around the six stories that defined the day:

| # | Story | In one line |
| --- | --- | --- |
| 1 | **Thanksgiving storm batters the US** | A coastal storm lashed the East Coast with 60 mph gusts and 400,000 outages; the 100th Macy's parade moved to Saturday, a first in a century. |
| 2 | **Kim urges wider nuclear deployment** | Kim Jong Un told officials to deploy tactical nuclear weapons across multiple domains; KCNA called North Korea's nuclear status irreversible. |
| 3 | **EU leaders split over budget, Ukraine loan** | Leaders in Brussels wrestled over a €1.6 trillion budget for 2028–2034 and a €45 billion loan for Ukraine, aiming for a deal in December. |
| 4 | **Bangkok refinery blast injures nine** | An explosion and fire at Bangchak's Bangkok refinery injured at least nine people and shut the 120,000-barrel-a-day plant. |
| 5 | **13 dead in flooded Indonesian mine** | Thirteen miners were confirmed dead and 13 remain trapped in a flooded illegal gold mine in Bogor; heavy rain halted the search. |
| 6 | **UK-EU treaties carry 10-year exit clause** | The UK and EU published food-trade and emissions treaty texts; quitting within 10 years means paying to rebuild border checks. |

The news was researched on 26 November 2026 from Reuters, AP, CNN, the BBC and Fox Weather, and every story was checked against at least two independent sources. The headlines and one-line summaries live inside the image itself, because the judge has no news feed — it judges each image the way a careful picture editor would, by what the image shows.

## How the entry works

```sh
python3 main.py
```

`main.py` places the image this repository holds (`entry.png`) at `/output/entry.png`, after checking it against the bounty: PNG, at most 1024×1024 pixels, at most 1 MiB. It uses only the Python standard library, needs no network, and produces byte-identical output on every run.

The picture was drawn by `render.py` (Pillow + DejaVu Sans) from the researched stories. Re-running it reproduces the image exactly:

```sh
python3 render.py
```

## What's in this repo

| File | What it is |
| --- | --- |
| `entry.png` | The image itself: 1024×1024 PNG |
| `main.py` | The entrypoint the grader runs |
| `render.py` | The script that drew the image |
| `LICENSE` | MIT |

---

<sub>Entered on [make.fun](https://make.fun/?ref=longd487&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
