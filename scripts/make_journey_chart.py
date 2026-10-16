# Draws docs/what_changed.svg. Run from the repo root: python3 scripts/make_journey_chart.py .
import os, sys
R = sys.argv[1]
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
INK, INK2, MUTED = "#1A1A18", "#4A4A45", "#6B6B64"
ACC, ACC_BG, ACC_INK = "#4B54A8", "#EEF0FB", "#2A2F6B"
GRAY, GRAY_BG, BORDER = "#8A8A82", "#F4F4F1", "#E3E3DE"
W, H = 1000, 360
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="What went wrong in unit 6 and what I changed" font-family="{FONT}">',
     '  <defs>',
     f'    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="{ACC}" stroke-width="1.6"/></marker>',
     '  </defs>',
     f'  <rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="#FFFFFF" stroke="{BORDER}"/>',
     f'  <text x="30" y="42" font-size="20" font-weight="600" fill="{INK}">What went wrong, and what I changed</text>',
     f'  <text x="30" y="66" font-size="13" fill="{MUTED}">One change at a time, each measured on seeds 42, 7 and 2024. Accuracy is the range across the three seeds.</text>']
steps = [
    ("Before", "default settings", "0.512 on every seed", ["Every post called opinion.", "Loss still falling at epoch 3,", "so the model had barely moved."], False),
    ("Fix 1", "learning rate 0.00005", "0.610 to 0.780", ["question learned on all seeds.", "experience still 0.00 everywhere:", "only 21 training examples."], False),
    ("Fix 2", "30 more experience posts", "0.733 to 0.778", ["experience up to 0.62 to 0.67.", "Criteria 1 and 2 met on all", "three seeds. Spread now 0.044."], True),
    ("Still broken", "not fixed", "F1 0.44 to 0.55", ["It learned links and tables,", "not facts in plain prose.", "Next: 30 prose evidence posts."], False),
]
BW, BH, GAP, X0, Y = 215, 230, 27, 30, 92
for i, (title, sub, metric, lines, main) in enumerate(steps):
    x = X0 + i * (BW + GAP)
    fill, stroke, tcol = (ACC_BG, ACC, ACC_INK) if main else (("#FFFFFF", BORDER, INK) if title == "Still broken" else (GRAY_BG, GRAY, INK))
    dash = ' stroke-dasharray="5 4"' if title == "Still broken" else ""
    s.append(f'  <rect x="{x}" y="{Y}" width="{BW}" height="{BH}" rx="10" fill="{fill}" stroke="{stroke}"{dash}/>')
    s.append(f'  <text x="{x+18}" y="{Y+32}" font-size="15" font-weight="600" fill="{tcol}">{title}</text>')
    s.append(f'  <text x="{x+18}" y="{Y+52}" font-size="12" fill="{MUTED}">{sub}</text>')
    s.append(f'  <text x="{x+18}" y="{Y+90}" font-size="11" fill="{MUTED}" letter-spacing="0.4">{"ACCURACY" if i < 3 else "WORST LABEL: EVIDENCE"}</text>')
    s.append(f'  <text x="{x+18}" y="{Y+114}" font-size="17" font-weight="600" fill="{ACC if main else INK}">{metric}</text>')
    for j, line in enumerate(lines):
        s.append(f'  <text x="{x+18}" y="{Y+152+j*19}" font-size="12.5" fill="{INK2}">{line}</text>')
    if i < 3:
        s.append(f'  <path d="M{x+BW+3} {Y+BH/2} H{x+BW+GAP-3}" stroke="{ACC}" stroke-width="1.5" fill="none" marker-end="url(#a)"/>')
s.append(f'  <text x="30" y="{H-18}" font-size="12" fill="{MUTED}">Labels, taxonomy and criteria stayed as filed in unit 5. Only the two declared changes moved.</text>')
s.append("</svg>")
open(os.path.join(R, "docs", "what_changed.svg"), "w").write("\n".join(s) + "\n")
print("ok")
