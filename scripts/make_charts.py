# Draws docs/run_accuracy.svg and docs/label_f1.svg from the three results_three_seeds files.
# Run from the repo root: python3 scripts/make_charts.py .
import json, os, sys
R = sys.argv[1]
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Menlo, Consolas, monospace"
INK, INK2, MUTED = "#1A1A18", "#4A4A45", "#6B6B64"
ACC, GRAY, GRID, BORDER, SURF = "#4B54A8", "#9A9A92", "#EEEEEA", "#E3E3DE", "#FFFFFF"
runs = [("before", "Before", "default settings"), ("after", "After 1", "learning rate 5e-5"), ("after2", "After 2", "plus 30 experience posts")]
data = {k: json.load(open(os.path.join(R, f"results_three_seeds_{k}.json"))) for k, _, _ in runs}

def head(w, h, title, sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}" font-family="{FONT}">',
            f'  <rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{SURF}" stroke="{BORDER}"/>',
            f'  <text x="30" y="42" font-size="20" font-weight="600" fill="{INK}">{title}</text>',
            f'  <text x="30" y="66" font-size="13" fill="{MUTED}">{sub}</text>']

def t(x, y, s, size=12, fill=INK2, anchor="start", weight="400", fam=None):
    f = f' font-family="{fam}"' if fam else ""
    return f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{f}>{s}</text>'

# chart 1: accuracy and macro F1 per seed
W, H = 1000, 380
X0, X1, V0, V1 = 330, 960, 0.1, 0.9
def vx(v): return X0 + (v - V0) / (V1 - V0) * (X1 - X0)
s = head(W, H, "Accuracy and macro F1 on three seeds, three runs", "Each dot is one seed (42, 7, 2024). Lines are my targets from criteria.md: accuracy 0.65, macro F1 0.50.")
top, rowh = 112, 38
metrics = [("accuracy", "Accuracy", 0.65), ("f1_macro", "Macro F1", 0.50)]
y = top
for mk, mname, target in metrics:
    s.append(t(30, y + 4, mname.upper(), 12, MUTED, weight="600"))
    ys = []
    y += 22
    for k, name, sub in runs:
        acc = (k == "after2")
        col = ACC if acc else GRAY
        s.append(t(30, y + 4, name, 13, INK if acc else INK2, weight="600" if acc else "400"))
        s.append(t(110, y + 4, sub, 12, MUTED))
        s.append(f'  <line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{GRID}"/>')
        vals = [r[mk] for r in data[k]]
        s.append(f'  <line x1="{vx(min(vals)):.1f}" y1="{y}" x2="{vx(max(vals)):.1f}" y2="{y}" stroke="{col}" stroke-opacity="0.45" stroke-width="3"/>')
        for v in vals:
            s.append(f'  <circle cx="{vx(v):.1f}" cy="{y}" r="6" fill="{col}" stroke="{SURF}" stroke-width="2"/>')
        ys.append(y)
        y += rowh - 8
    s.append(f'  <line x1="{vx(target):.1f}" y1="{ys[0] - 16}" x2="{vx(target):.1f}" y2="{ys[-1] + 12}" stroke="{INK2}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    s.append(t(vx(target) + 6, ys[0] - 8, f"target {target:.2f}", 11, INK2))
    y += 14
for v in [0.1, 0.3, 0.5, 0.7, 0.9]:
    s.append(t(vx(v), y + 6, f"{v:.1f}", 11, MUTED, "middle"))
H = y + 50
s[0] = s[0].replace('height="380" viewBox="0 0 1000 380"', f'height="{H}" viewBox="0 0 1000 {H}"')
s[1] = s[1].replace('height="380"', f'height="{H}"')
s.append(t(30, H - 18, "Before, every seed scored the same because the model called every post opinion. After 2 is the only run that clears both lines on all three seeds.", 12, MUTED))
s.append("</svg>")
open(os.path.join(R, "docs", "run_accuracy.svg"), "w").write("\n".join(s) + "\n")

# chart 2: per-label F1
W, H = 1000, 470
X0, X1 = 330, 960
def fx(v): return X0 + v * (X1 - X0)
s = head(W, H, "F1 per label, three seeds per run", "Dots are seeds, the bar is the spread. Ticks are my criterion 3 targets. Where all three dots sit on 0 the label was never predicted.")
targets = {"question": 0.60, "evidence": 0.60, "experience": 0.35, "opinion": None}
y = 108
for lab in ["question", "experience", "evidence", "opinion"]:
    s.append(t(30, y + 4, lab, 13, INK, weight="600", fam=MONO))
    ys = []
    y += 20
    for k, name, sub in runs:
        acc = (k == "after2")
        col = ACC if acc else GRAY
        s.append(t(46, y + 4, name, 12, INK2))
        s.append(f'  <line x1="{X0}" y1="{y}" x2="{X1}" y2="{y}" stroke="{GRID}"/>')
        vals = [r["per_label"][lab]["f1"] for r in data[k]]
        s.append(f'  <line x1="{fx(min(vals)):.1f}" y1="{y}" x2="{fx(max(vals)):.1f}" y2="{y}" stroke="{col}" stroke-opacity="0.45" stroke-width="3"/>')
        for v in vals:
            s.append(f'  <circle cx="{fx(v):.1f}" cy="{y}" r="5" fill="{col}" stroke="{SURF}" stroke-width="2"/>')
        ys.append(y)
        y += 20
    tg = targets[lab]
    if tg is not None:
        s.append(f'  <line x1="{fx(tg):.1f}" y1="{ys[0] - 10}" x2="{fx(tg):.1f}" y2="{ys[-1] + 8}" stroke="{INK2}" stroke-width="1.5" stroke-dasharray="4 3"/>')
        s.append(t(fx(tg) + 6, ys[0] - 6, f"{tg:.2f}", 11, INK2))
    else:
        s.append(t(X1, ys[0] - 6, "no target", 11, MUTED, "end"))
    y += 12
for v in [0, 0.25, 0.5, 0.75, 1.0]:
    s.append(t(fx(v), y + 6, f"{v:.2f}".rstrip("0").rstrip(".") if v not in (0, 1.0) else f"{v:.0f}", 11, MUTED, "middle"))
y += 20
H = y + 34
s[0] = s[0].replace('height="470" viewBox="0 0 1000 470"', f'height="{H}" viewBox="0 0 1000 {H}"')
s[1] = s[1].replace('height="470"', f'height="{H}"')
s.append(t(30, H - 18, "experience only appears after 2. evidence is the label still under its line, which matches the error write up.", 12, MUTED))
s.append("</svg>")
open(os.path.join(R, "docs", "label_f1.svg"), "w").write("\n".join(s) + "\n")
print("ok")
