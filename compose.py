#!/usr/bin/env python3
"""Compose front-page.png: a newspaper front page for Wednesday 25 Nov 2026.

Fresh build for the make.fun news-image-20261125 bounty.
All stories verified against dated reporting (see ../news-image-20261125-research.md).
Output: 1024x1024 PNG, well under 1 MiB.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 46
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
INK = (12, 12, 12)
GREY = (90, 90, 90)
RULE = (30, 30, 30)

def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)

def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    right = W - MARGIN
    content_w = right - MARGIN
    warnings = []

    def check(lines, max_lines, what):
        if len(lines) > max_lines:
            warnings.append(f"{what}: {len(lines)} lines, max {max_lines}")

    # ---- Masthead ----
    mast = "THE WORLD TODAY"
    f_mast = SERIF_B(78)
    mw = d.textlength(mast, font=f_mast)
    d.text(((W - mw) / 2, 26), mast, font=f_mast, fill=INK)
    rule(d, MARGIN, right, 132, 3)

    # ---- Date line (prominent) ----
    f_date = SANS_B(34)
    date = "WEDNESDAY 25 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 146), date, font=f_date, fill=INK)
    rule(d, MARGIN, right, 196, 3)
    rule(d, MARGIN, right, 201, 1)

    # ---- Tagline ----
    f_tag = SERIF(19)
    tag = "One day in world news — from the Pacific to the markets"
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 214), tag, font=f_tag, fill=GREY)

    # ---- Lead story ----
    y = 252
    f_kick = SANS_B(17)
    d.text((MARGIN, y), "THE PACIFIC  •  LEAD STORY", font=f_kick, fill=INK)
    y += 30
    f_lead = SERIF_B(46)
    lead_head = ["Solomon Islands pick Australia", "as defence partner of choice"]
    for line in lead_head:
        lw = d.textlength(line, font=f_lead)
        if lw > content_w:
            warnings.append(f"lead headline too wide: {line}")
        d.text((MARGIN, y), line, font=f_lead, fill=INK)
        y += 56
    y += 4
    f_lead_sum = SERIF(21)
    lead_sum = ("Canberra signs a security pact making it the islands' defence "
                "partner of choice, in a shift away from Beijing. Australian "
                "media report the earlier deal with China has been scrapped.")
    lead_lines = wrap(d, lead_sum, f_lead_sum, content_w)
    check(lead_lines, 3, "lead summary")
    y = draw_wrapped(d, MARGIN, y, lead_lines, f_lead_sum, leading=28)
    rule(d, MARGIN, right, y + 14, 2)

    # ---- Grid of six stories: 2 columns x 3 rows ----
    stories = [
        ("CYBER",
         "Hack hits CIA network",
         "Unclassified open-source system breached, officials say; "
         "no classified data was taken and no culprit named yet."),
        ("HEALTH",
         "WHO pulls staff from Ebola hospital",
         "Health workers leave a hospital in Akwe, DR Congo, after "
         "sheltering there for three days amid fierce fighting."),
        ("MARKETS",
         "Anthropic sinks below its IPO price",
         "Claude maker's shares close at $81.91, under the $83 debut "
         "price, as worries over AI valuations deepen."),
        ("EUROPE",
         "Sweden sets vote to end 72-day deadlock",
         "Parliament will vote on 30 November on whether Ulf "
         "Kristersson stays prime minister."),
        ("INDIA",
         "BJP and Akali Dal reunite for Punjab",
         "The allies announce a pact for the 2027 Punjab polls, "
         "six years after their split."),
        ("SPORT",
         "Teen, 15, smashes cricket records",
         "Vaibhav Sooryavanshi hits the fastest List A hundred "
         "(28 balls) and double hundred (52 balls) — 204 off 53."),
    ]
    gap = 28
    col_w = (content_w - gap) // 2
    grid_top = y + 32
    row_h = 148
    f_label = SANS_B(15)
    f_head = SERIF_B(24)
    f_sum = SANS(16)
    for i, (label, head, summ) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + gap)
        cy = grid_top + row * row_h
        d.text((x, cy), label, font=f_label, fill=GREY)
        cy += 24
        head_lines = wrap(d, head, f_head, col_w)
        check(head_lines, 2, f"headline {label}")
        cy = draw_wrapped(d, x, cy, head_lines, f_head, leading=29)
        cy += 3
        sum_lines = wrap(d, summ, f_sum, col_w)
        check(sum_lines, 3, f"summary {label}")
        draw_wrapped(d, x, cy, sum_lines, f_sum, leading=21)
        # vertical divider between columns
        if col == 0:
            d.line([(MARGIN + col_w + gap // 2, grid_top - 4),
                    (MARGIN + col_w + gap // 2, grid_top + 3 * row_h - 16)],
                   fill=(200, 200, 200), width=1)

    foot_y = grid_top + 3 * row_h + 6
    rule(d, MARGIN, right, foot_y, 2)
    f_foot = SANS(16)
    foot1 = "25 November is the International Day for the Elimination of Violence against Women."
    d.text((MARGIN, foot_y + 12), foot1, font=f_foot, fill=INK)
    f_src = SANS(14)
    foot2 = "Sources: Reuters  •  AP  •  CNN  •  ICC  •  WHO  —  Compiled 25 November 2026"
    d.text((MARGIN, foot_y + 38), foot2, font=f_src, fill=GREY)

    if warnings:
        for w in warnings:
            print("WARNING:", w, file=sys.stderr)
        sys.exit(1)

    img.save("front-page.png", optimize=True)
    print("wrote front-page.png")

if __name__ == "__main__":
    main()
