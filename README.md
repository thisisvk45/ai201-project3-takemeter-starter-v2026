# TakeMeter: Hacker News comments

How to run it: [RUNNING.md](RUNNING.md). Unit 5 is the five sections below. Unit 6 adds its sections at the end.

## What This Does

My community is Hacker News, the comment threads under front page stories. I read about 60 comments across 45 threads from September and early October 2026 before picking labels. What I noticed is that HN comments differ less in topic and more in what they lean on. Some lean on something you can check, some lean on what happened to the writer, most lean on nothing but the claim, and a few just ask. TakeMeter sorts a comment into one of those four: `evidence`, `experience`, `opinion`, `question`.

### What I noticed while reading

1. Some comments carry a thing you can check: a link, a number, a CVE, a quote from the article, a setting name. Most do not.
2. Many comments argue from "I tried it" or "at my job we". That is a different kind of support from a link, and HN readers treat it differently.
3. A lot of comments are a confident line, a joke, or a chain of reasoning with nothing checkable in it.
4. Real questions exist but are rare. Most question marks on HN are rhetorical.

### Stretch features I am adding

I declared these before labelling or training anything.

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

### The hardest boundary

Which two labels: `evidence` and `opinion`.

The decision rule I used every time: if the comment gives at least one specific thing a reader could check that supports its point, it is `evidence`, even when the rest is opinion and the tone is heated. Reasoning, analogies and general claims like "attacks get cheaper over time" stay `opinion`. A made up or joking number does not count.

Two smaller rules I also used:

1. `experience` beats `evidence` when the support is what happened to the writer, even if it has numbers in it.
2. A rhetorical question or a challenge like "can you offer any evidence?" is `opinion`. It is `question` only when the writer actually wants the answer.

---

## The Dataset

To be filled in after labelling.

---

## The Training Run

To be filled in after training.

---

## How I Used AI

To be filled in after labelling and training.

<!-- UNIT 6 sections (Baseline vs. Trained, Run Log Before, Verdicts and
     Diagnoses, Agreement Report, The Improvement, What's Still Broken) are
     added next unit. The starter template is in git history. -->
