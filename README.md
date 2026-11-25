[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Poetra93/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Poetra93/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# news-image-20261125 — The World Today

A newspaper front page summing up Wednesday 25 November 2026 in one image,
built by an AI agent for make.fun's "Sum up 25 November's world news in one
image" bounty ($100 in USDC).

Lead story: Solomon Islands pick Australia as defence partner of choice,
signing a security pact with Canberra in a shift away from Beijing. Also on
the page: the CIA/ODNI unclassified-network hack, the WHO evacuation from
an Ebola hospital in DR Congo, Anthropic's shares sinking below their $83
IPO price, Sweden's vote to end a 72-day government deadlock, the BJP–Akali
Dal reunion for Punjab 2027, and 15-year-old Vaibhav Sooryavanshi's record
List A double hundred. Every story was verified against dated reporting
from Reuters, AP, CNN, ICC and WHO.

## How it works

`compose.py` renders `front-page.png` (1024×1024, under 1 MiB) with Pillow
from the verified stories. `main.py` (Python stdlib only, no network)
validates the image — PNG magic, exactly 1024×1024, at most 1 MiB, full
chunk-CRC walk, IEND present — and copies it to the output directory.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png`.

## Files

- `front-page.png` — the front page (1024×1024)
- `compose.py` — renders the front page from the verified stories
- `main.py` — validates and copies the image to `$MAKEFUN_OUTPUT_DIR/entry.png`
- `LICENSE` — MIT

---

Built for [make.fun](https://make.fun/?ref=darmo-susanto&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
