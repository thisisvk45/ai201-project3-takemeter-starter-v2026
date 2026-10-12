# TakeMeter: Hacker News comments

How to run it: [RUNNING.md](RUNNING.md). Unit 5 is the five sections below. Unit 6 adds its sections at the end.

## What This Does

My community is Hacker News, the comment threads under front page stories. Before picking labels, Claude read about 60 comments for me across 45 threads from September and early October 2026. What we noticed is that HN comments differ less in topic and more in what they lean on. Some lean on something you can check, some lean on what happened to the writer, most lean on nothing but the claim, and a few just ask. TakeMeter sorts a comment into one of those four: `evidence`, `experience`, `opinion`, `question`.

### What we noticed while reading

1. Some comments carry a thing you can check: a link, a number, a CVE, a quote from the article, a setting name. Most do not.
2. Many comments argue from "I tried it" or "at my job we". That is a different kind of support from a link, and HN readers treat it differently.
3. A lot of comments are a confident line, a joke, or a chain of reasoning with nothing checkable in it.
4. Real questions exist but are rare. Most question marks on HN are rhetorical.

### Stretch features I am adding

I declared these in my first commit, before any labelling or training.

1. A fourth label, `question`. Asking is a real move on HN that the other three do not cover.
2. 50 extra examples for my thinnest label. From my reading that is `question`, so I collect 50 more from a separate set of threads.
3. A second training run with one hyperparameter changed, and a note on what moved.

---

## Label Taxonomy

### `evidence`

Definition: backs its point with at least one specific thing a reader could check, such as a number, a link, a quote, a version, or how a product or system actually behaves.

Example 1:
> Yes, here's the graph of weekly downloads: https://stats.documentfoundation.org/downloads#week,version The 26.8 peak is within the normal range of week-to-week variation.

Example 2:
> Google is also seriously dropping the ball in terms of security. The CVE-2026-43499 root LPE (aka ghostlock) is still unpatched across all Pixel devices, on the latest """security""" update, despite weaponized exploits being public for months.

### `experience`

Definition: backs its point with something that happened to the writer or their team, first hand.

Example 1:
> i just tested and `mise bootstrap` is over twice as fast at installing when a bottle was in the cache. other commands like `status/check` are 20-30x faster. that's without spending much work at all on perf—i'm sure i could bring these numbers down much further.

Example 2:
> FWIW, I've never seen that come up on the five or six TCLs that I've owned over the last decade. I have AppleTVs connected to all of them and never connect them to the internet. So far, so good.

### `opinion`

Definition: a claim, judgment, joke, or line of reasoning with no checkable specific and no first hand experience behind it.

Example 1:
> All FOSS consumer operating systems suck. We only tolerate them because they are FOSS.

Example 2:
> Being early is the same as being wrong.  Being lucky is the same as being right.

### `question`

Definition: the main purpose is to ask for information the writer does not have and wants answered.

Example 1:
> How do I get access to that reset? I can’t find it in my app.

Example 2:
> I never understood the thinking behind the separate key query value matrixes? What are they doing exactly?

![The order of checks for every comment](docs/decision_order.svg)

### The hardest boundary

Which two labels: `evidence` and `opinion`.

The decision rule used every time: if the comment gives at least one specific thing a reader could check that supports its point, it is `evidence`, even when the rest is opinion and the tone is heated. Reasoning, analogies and general claims like "attacks get cheaper over time" stay `opinion`. A made up or joking number does not count.

Two smaller rules:

1. `experience` beats `evidence` when the support is what happened to the writer, even if it has numbers in it.
2. A rhetorical question or a challenge like "can you offer any evidence?" is `opinion`. It is `question` only when the writer actually wants the answer.

---

## The Dataset

Where the posts came from: public Hacker News comments, pulled from the Algolia HN API by `scripts/collect_hn.py`. 45 front page stories from 1 September to 10 October 2026, up to 10 comments each, 60 to 700 characters, no usernames saved. The 50 extra `question` examples come from 40 other stories in the same window, filtered to comments that ask something (`--questions`). Raw pulls are in `data/hn_raw.jsonl` and `data/hn_questions.jsonl`.

How they were labelled: I did not label these myself. I asked Claude to do it, and every row says so in the note column.

1. 20 rows were labelled by Claude blind, with no suggestion shown. They sit where the brief's 20 cold rows go, but they are not a human cold check, and the note says that.
2. 199 rows were pre-labelled by Claude from the definitions above. I did not review them, so the note reads "not checked by a human".
3. 50 extra `question` rows were labelled the same way and marked "extra question sample".
4. One comment was dropped because it made an allegation about a real person.

`scripts/review.py` is the tool for the human pass the brief asks for: cold rows first, then Enter to keep or a number to change each pre-label. It rewrites the notes as rows are checked.

Counts per label:

| Label | Count | Share |
|---|---|---|
| `opinion` | 136 | 50.6% |
| `question` | 57 | 21.2% |
| `evidence` | 47 | 17.5% |
| `experience` | 29 | 10.8% |
| Total | 269 | 100% |

No label is above 70%. Before the extra 50, `question` had only 7 rows, which is why it got the extra examples.

### Three hard cases

1. The post:
> The reset stuff is incredibly tiresome. We all know that it's all built into an internal number they are tracking (just like e.g. company benefits that are just part of your compensation calculation), and all it does is obscure the value the subscription provides and make planning impossible. It's the poorest service experience I can remember having, ever.

Could have been `experience` or `opinion`. Labelled `opinion`, because the personal line is a verdict on the service, not something that happened.

2. The post:
> When I hear people making these claims (all unproven theories, or misrepresentation of what really happens), I want to know: what happened in democratic administrations that went in favor of a large corporate donor and against the public? Any specific example where they diverged, and a politician ruled in favor of the corp, and against their constituents?

Could have been `question` or `opinion`. Labelled `opinion`. It is phrased as a question, but it is a challenge and the writer does not expect an answer.

3. The post:
> If China keeps training AI off the web while US companies have to negotiate with  7,383,654 different rights holders, it's going to handicap the US companies a bit.

Could have been `evidence` or `opinion`. Labelled `opinion`, because 7,383,654 is a made up number used for effect. This is where the rule about joking numbers came from.

Every hard case is marked "hard case" in the note column, six in all.

---

## The Training Run

Base model: `distilbert-base-uncased`, the notebook default.

Settings: 3 epochs, learning rate 2e-5, batch size 16, 128 tokens per post, seed 42.

Device: `cpu`, recorded in `results.json`. It ran inside the Linux VM that Claude uses on my MacBook Pro, not on the Mac's own GPU, so someone running this on `mps` may get different numbers.

Split sizes: train 187, validation 41, test 41. Test per label: `opinion` 21, `question` 9, `evidence` 7, `experience` 4. `evidence` and `experience` are under 8 in the test split, so their F1 will jump between seeds next unit.

Anything changed from the defaults: nothing in the main run. `results.json` and `test_split.csv` come from the defaults above.

### Second run, one hyperparameter changed (stretch)

The default run predicted `opinion` for all 41 test posts. Its accuracy of 0.512 is exactly the always-`opinion` guesser. The loss was still falling at epoch 3, so the model had not moved far enough from its starting point. I changed one thing, the learning rate from 2e-5 to 5e-5, and kept the same seed, split and everything else. The output is `results_run2_lr5e-5.json`.

| Measure | lr 2e-5 (default) | lr 5e-5 |
|---|---|---|
| Accuracy | 0.512 | 0.780 |
| Macro F1 | 0.169 | 0.598 |
| F1 `evidence` | 0.000 | 0.727 |
| F1 `experience` | 0.000 | 0.000 |
| F1 `opinion` | 0.677 | 0.840 |
| F1 `question` | 0.000 | 0.824 |

What moved: `question` and `evidence` were learned, `experience` was not. All 4 `experience` test posts still went to `opinion`. One seed is not a result I would stand on. Next unit's three seeds will show whether this holds.

---

## How I Used AI

Moment 1

1. What I asked for: I asked Claude to pick and read Hacker News threads, propose labels and a decision rule, and collect the posts.
2. What came back: four labels, the order of checks in the diagram above, and the collector script.
3. What I changed: nothing. I accepted the taxonomy as written.

Moment 2

1. What I asked for: I asked Claude to run the notebook, sections 1 to 5, end to end.
2. What came back: the default run collapsed to `opinion` on every test post.
3. What I changed: I had Claude run a second time with only the learning rate raised to 5e-5. That was the declared stretch run. The default run stays as `results.json`.

Pre-labelling disclosure: Claude labelled all 269 rows, including the 20 in the cold slot. I did not read or correct them. Claude also drafted the five criteria in `criteria.md` before training, and that file says so at the top. The brief asks for a human cold pass, a human review of every pre-label and criteria written by the student. None of those happened here. `scripts/review.py` is ready if I do that pass before the deadline.

<!-- UNIT 6 sections (Baseline vs. Trained, Run Log Before, Verdicts and
     Diagnoses, Agreement Report, The Improvement, What's Still Broken) are
     added next unit. The starter template is in git history. -->
