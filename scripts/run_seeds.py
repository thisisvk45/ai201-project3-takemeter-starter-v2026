"""Run notebook section 6 one seed per process, then assemble the same file.

The VM I train in kills any job longer than three minutes, and section 6 runs
three seeds in one cell (about five minutes on CPU). So this script takes the
notebook's own code (sections 1 to 5 for the definitions, section 6 for the
loop body) and runs one seed at a time. Settings come from the notebook, so a
change made there is what gets measured.

    python scripts/run_seeds.py --label before --seed 42      # one seed
    python scripts/run_seeds.py --label before --assemble     # write results_three_seeds_before.json
    python scripts/run_seeds.py --label before --report       # sections 6 and 7 printouts
    python scripts/run_seeds.py --label after2 --seed 42 --errors   # also save every test post's guess
"""
import argparse, ast, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / ".cache" / "seeds"
SEEDS = [42, 7, 2024]


def notebook_code():
    nb = json.loads((ROOT / "takemeter.ipynb").read_text())
    cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
    return cells


def defs_only(src):
    """Keep imports and function definitions, drop top-level work."""
    tree = ast.parse(src)
    keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
    return ast.unparse(ast.Module(body=keep, type_ignores=[]))


def setup():
    cells = notebook_code()
    g = {}
    import os
    os.chdir(ROOT)
    exec(cells[0], g)          # section 1: device
    exec(cells[2], g)          # section 2: LABELS, settings, SEED
    exec(cells[3], g)          # load labels.csv
    for src in cells[4:8]:     # check, split, train, evaluate: definitions only
        exec(defs_only(src), g)
    return g, cells


def run_one(label, seed, errors=False):
    g, _ = setup()
    tr, va, te = g["split_dataset"](g["df"], seed)
    t, tok = g["train_model"](tr, va, g["LABELS"], seed, g["EPOCHS"], g["LEARNING_RATE"],
                              g["BATCH_SIZE"], g["BASE_MODEL"], quiet=True)
    r = g["evaluate"](t, tok, te, g["LABELS"], seed=seed)
    r.update(device=g["DEVICE"], device_name=g["DEVICE_NAME"],
             torch_version=g["torch"].__version__, max_length=g["MAX_LENGTH"],
             settings={"epochs": g["EPOCHS"], "learning_rate": g["LEARNING_RATE"],
                       "batch_size": g["BATCH_SIZE"], "rows": len(g["df"])})
    if errors:
        import numpy as np
        from datasets import Dataset
        ds = Dataset.from_pandas(g["to_ids"](te, g["LABELS"])).map(
            lambda b: tok(b["text"], truncation=True, padding="max_length", max_length=g["MAX_LENGTH"]), batched=True)
        pred = np.argmax(t.predict(ds).predictions, axis=-1)
        rows = [{"text": x, "gold": y, "predicted": g["LABELS"][int(p)]}
                for x, y, p in zip(te["text"], te["label"], pred)]
        (ROOT / f"predictions_{label}_seed{seed}.json").write_text(json.dumps(rows, indent=2))
    PARTS.mkdir(parents=True, exist_ok=True)
    (PARTS / f"{label}_{seed}.json").write_text(json.dumps(r, indent=2))
    print(f"seed {seed}: accuracy {r['accuracy']:.3f}   macro F1 {r['f1_macro']:.3f}")


def assemble(label):
    results = [json.loads((PARTS / f"{label}_{s}.json").read_text()) for s in SEEDS]
    out = ROOT / f"results_three_seeds_{label}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"Wrote {out.name}.")


def report(label):
    cells = notebook_code()
    g = {"all_results": json.loads((ROOT / f"results_three_seeds_{label}.json").read_text())}
    exec(cells[2].split("print(")[0], g)   # LABELS and settings only
    for src in cells[-2:]:                 # sections 6 table and 7 matrix
        exec(src, g)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--label", required=True)
    p.add_argument("--seed", type=int)
    p.add_argument("--assemble", action="store_true")
    p.add_argument("--report", action="store_true")
    p.add_argument("--errors", action="store_true")
    a = p.parse_args()
    if a.seed is not None:
        run_one(a.label, a.seed, a.errors)
    if a.assemble:
        assemble(a.label)
    if a.report:
        report(a.label)
