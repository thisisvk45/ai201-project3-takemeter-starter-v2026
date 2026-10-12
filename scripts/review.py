"""Label and review my Hacker News posts in the terminal, then write labels.csv.

    python3 scripts/review.py           # label the 20 cold rows, then review the rest
    python3 scripts/review.py --stats   # counts so far
    python3 scripts/review.py --export  # write labels.csv once every row has a label

Cold rows come first and show no suggestion. After that each row shows the AI
pre-label: Enter keeps it, a number changes it. Progress is saved after every
row, so q is safe at any time. Standard library only, so the system python3 works.

Keys:  1-4 pick a label   Enter keep the pre-label   h flag a hard case
       b back one row     q save and quit
"""
import csv, sys, textwrap
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "labeling_queue.csv"
OUT = ROOT / "labels.csv"


def definitions():
    defs = []
    for line in (ROOT / "label_definitions.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            name, text = line.split(":", 1)
            defs.append((name.strip(), text.strip()))
    return defs


def load():
    with QUEUE.open(newline="") as f:
        return list(csv.DictReader(f))


def save(rows):
    with QUEUE.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def note_for(row):
    if row["set"] == "cold":
        note = "cold"
    elif row["label"] == row["ai_label"]:
        note = "AI pre-label, checked by me"
    else:
        note = f"AI pre-label was {row['ai_label']}, I changed it"
    if row["set"] == "extra_question":
        note = "extra question sample; " + note
    if row["hard"]:
        note += "; hard case: " + row["hard"]
    return note


def stats(rows):
    done = [r for r in rows if r["label"]]
    print(f"{len(done)} of {len(rows)} labelled")
    counts = Counter(r["label"] for r in done)
    for name, n in counts.most_common():
        print(f"  {name:<11}{n:4d}  {n / max(len(done), 1):.0%}")
    changed = sum(1 for r in done if r["set"] != "cold" and r["label"] != r["ai_label"])
    print(f"pre-labels I changed: {changed}   hard cases flagged: {sum(1 for r in rows if r['hard'])}")


def export(rows):
    missing = sum(1 for r in rows if not r["label"])
    if missing:
        sys.exit(f"{missing} rows still have no label. Finish them first.")
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "label", "note"])
        for r in rows:
            w.writerow([r["text"], r["label"], note_for(r)])
    print(f"wrote {len(rows)} rows to {OUT.name}")
    stats(rows)


def show(row, n, total, defs):
    print("\n" + "-" * 72)
    tag = "COLD, no suggestion" if row["set"] == "cold" else f"AI pre-label: {row['ai_label']}"
    print(f"{n}/{total}   thread: {row['story'][:50]}   [{tag}]\n")
    for para in row["text"].split("\n"):
        print(textwrap.fill(para, 72) if para.strip() else "")
    print()
    for i, (name, _) in enumerate(defs, 1):
        print(f"  {i} {name}", end="")
    print("    h hard case   b back   q quit")


def run(rows):
    defs = definitions()
    names = [d[0] for d in defs]
    print("\nMy definitions:")
    for name, text in defs:
        print(textwrap.fill(f"{name}: {text}", 72, subsequent_indent="    "))
    order = sorted(range(len(rows)), key=lambda i: rows[i]["set"] != "cold")
    pos = next((k for k, i in enumerate(order) if not rows[i]["label"]), None)
    if pos is None:
        print("\nEvery row has a label. Run with --export.")
        return
    while pos < len(order):
        row = rows[order[pos]]
        if row["set"] != "cold" and order[pos] == next(i for i in order if rows[i]["set"] != "cold") and not row["label"]:
            print("\nCold rows done. From here each row shows the AI pre-label.")
        show(row, pos + 1, len(order), defs)
        if row["label"]:
            print(f"  (currently {row['label']})")
        key = input("> ").strip().lower()
        if key == "q":
            break
        if key == "b":
            pos = max(pos - 1, 0)
            continue
        if key == "h":
            other = input("  which other label could it be? ").strip()
            why = input("  one line on what you chose and why: ").strip()
            row["hard"] = f"could be {other}; {why}"
            save(rows)
            continue
        if key == "" and (row["label"] or row["set"] != "cold"):
            row["label"] = row["label"] or row["ai_label"]
        elif key.isdigit() and 1 <= int(key) <= len(names):
            row["label"] = names[int(key) - 1]
        else:
            print("  pick a number" + ("" if row["set"] == "cold" else ", or Enter to keep"))
            continue
        save(rows)
        pos += 1
    print()
    stats(rows)
    if all(r["label"] for r in rows):
        export(rows)


if __name__ == "__main__":
    rows = load()
    if "--stats" in sys.argv:
        stats(rows)
    elif "--export" in sys.argv:
        export(rows)
    else:
        run(rows)
