"""Pull public Hacker News comments from the Algolia API into data/hn_raw.jsonl.

I take front page stories from a fixed window, walk each comment tree, and keep
comments between 60 and 700 characters so a post can be read and labelled in
one go. Usernames are not saved.

--questions pulls from a different set of stories and keeps only comments that
ask something (a question mark plus a question opener). I used it for the 50
extra examples of my thinnest label, written to data/hn_questions.jsonl.
"""
import html, json, random, re, sys, time, urllib.request
from pathlib import Path

API = "https://hn.algolia.com/api/v1"
DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "hn_raw.jsonl"
ASKS = re.compile(r"(^|[.!?]\s+)(does|do|is|are|can|could|how|what|why|which|where|has|have|any|anyone|would|will|should)\b[^.!?]*\?", re.I)
PER_STORY = 10
STORIES = 45


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def clean(text):
    text = re.sub(r"<p>", "\n\n", text or "")
    text = re.sub(r"<a [^>]*>(.*?)</a>", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def walk(node, story, out, questions=False):
    for child in node.get("children") or []:
        body = clean(child.get("text"))
        if questions and not ASKS.search(body):
            walk(child, story, out, questions)
            continue
        if child.get("type") == "comment" and (40 if questions else 60) <= len(body) <= 700:
            out.append({"id": child["id"], "story_id": story["objectID"],
                        "story": story["title"], "text": body})
        walk(child, story, out, questions)


def main():
    questions = "--questions" in sys.argv
    out_path = DATA / "hn_questions.jsonl" if questions else OUT
    per_story = 4 if questions else PER_STORY
    random.seed(5)
    start = int(time.mktime((2026, 9, 1, 0, 0, 0, 0, 0, -1)))
    end = int(time.mktime((2026, 10, 10, 0, 0, 0, 0, 0, -1)))
    hits = get(f"{API}/search?tags=story&numericFilters=created_at_i>{start},created_at_i<{end},num_comments>80&hitsPerPage=200")["hits"]
    random.shuffle(hits)
    rows = []
    picked = hits[STORIES:STORIES + 40] if questions else hits[:STORIES]
    for story in picked:
        found = []
        walk(get(f"{API}/items/{story['objectID']}"), story, found, questions)
        random.shuffle(found)
        rows += found[:per_story]
        print(f"{len(found):4d} kept {min(len(found), per_story):2d}  {story['title'][:70]}", file=sys.stderr)
    seen, unique = set(), []
    for r in rows:
        if r["text"] not in seen:
            seen.add(r["text"]); unique.append(r)
    out_path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in unique))
    print(f"wrote {len(unique)} comments from {len(picked)} stories to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
