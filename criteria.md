# Acceptance criteria: TakeMeter

Disclosure: Claude drafted these five at my request, before any training run on my data. The brief asks students to write their own, so I am saying so plainly here and in the README.

Five criteria for what "working" means, filed before training. Next unit each target has to hold across all three seeds.

---

## 1. Overall accuracy is at least 0.65 on the held-out test split.

Why this target: `opinion` is about 51% of my data, so a model that always says `opinion` already gets about 0.51. 0.65 means it beats that guesser by a clear margin on roughly 40 test posts, which is about six more posts right, not one lucky one.

---

## 2. Macro F1 is at least 0.50.

Why this target: macro F1 weights my four labels equally, so a model that only learns `opinion` cannot pass it. I set it lower than accuracy because `experience` is my smallest label and will drag the average down.

---

## 3. `question` and `evidence` each have an F1 of at least 0.60, and `experience` has an F1 of at least 0.35.

Why this target: `question` and `evidence` carry surface signals the model can see (question openers and a question mark; links, numbers, version names). `experience` has only 29 examples, so about 4 land in the test split, and one miss moves its F1 a lot. Its target is looser on purpose.

---

## 4. Accuracy on the model's most confident third of test posts is at least 0.15 higher than on its least confident third.

Why this target: if confidence means anything, the posts it is sure about should be right more often. 0.15 on about 13 posts per third is two posts, which is the smallest gap I would not call noise. `results.json` records both numbers.

---

## 5. At most 30% of the true `evidence` and `experience` posts in the test split are predicted as `opinion`.

Why this target: `evidence` against `opinion` is my hardest boundary, and `opinion` is half the data, so the likely failure is the model swallowing the other two into it. This checks that direction directly. 30% is about 3 of the roughly 11 such posts.

---

<!-- Your criterion. -->



**Why this target:**



---

## 3.

<!-- Your criterion. -->



**Why this target:**



---

## 4.

<!-- Your criterion. -->



**Why this target:**



---

## 5.

<!-- Your criterion. -->



**Why this target:**



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
