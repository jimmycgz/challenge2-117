# Deck outline

Navigation: [demo script](DEMO-SCRIPT.md) · [submission checklist](SUBMISSION.md) ·
[agent README](../agent/food_broker/README.md) · [equity audit](../agent/food_broker/EQUITY-AUDIT.md).

Eight slides. Judges score the deck and the video after the event with no questions, so the rigor answers are on the
slides, in these words, not only in the repo. Front-load it: assume nobody reaches the last slide.

## 1. The situation

We coordinate food rescue in Chicago. A grocer has just offered ten crates of spinach and it has to leave in six
hours. Here is who we would call, and what we do not know about them.

## 2. The problem

Food that could be eaten is thrown away a few miles from people who need it. It is a matching problem under a clock:
what just became available, who could use it, what they can store, and how long the food has left. Four questions in
the same minute.

## 3. What we built

A posting goes in. A Match Brief comes out, in six parts: who and why, what they can take, the clock and the margin,
whose neighborhood it helps, a message ready to send, and the next two options. Under it: BigQuery vector search to find
candidates by meaning, hard filters for cold storage, capacity and collection time, then a ranking. Gemini on Vertex AI
writes the answer; ADK runs the agent; Google's managed BigQuery MCP server answers free-form data questions; it runs
on Cloud Run.

## 4. Why meaning is not enough

For the spinach offer, the three closest recipients by meaning were all wrong. Two could not collect in time. One,
ranked third, wrote that its families ask for fresh greens and that it has no refrigeration of any kind. The nearest
one that passes is 11th by meaning; the three our ranking puts first sit at 50th, 54th and 63rd, because it prefers
sturdier cold storage and a comfortable margin over closeness. Pool of 15 left 1 viable recipient, 40 left 3, 80 left 12.
Sources: [pool study](evidence/pool-study.txt) for the pool numbers, [demo-tracks.txt](evidence/demo-tracks.txt) for the ranks.
Use the captured output as the screenshot. The rule that always shows a cold-storage rejection is
tested with a case that fails when the rule is switched off; our first version had a sorting bug and that test caught it. Say so in one line.

## 5. One corpus, three tracks

Retail spinach, five tons of farm potatoes and sealed infant formula went through the same corpus, the same search and
the same filters, with no rulebook per track. Show the three blocks of [demo-tracks.txt](evidence/demo-tracks.txt).

## 6. What the agent decides for itself

It says when nobody can take the load and shows why. It caught that the shelf-life table gave sealed formula one hour (an
opened-container figure) and now trusts the donor's expiry. The BigQuery tools are read-only and never used to match a
posting. A guard refuses to run under any account but the lab's.

## 7. The equity audit

Did the food go where the need is, or where the loading docks are? Counted per posting, the matches have more poverty
than the corpus and the other two measures are mixed. Counted per recipient, they sit lower, because one pantry won three postings. Weighted by volume,
assistance is 9% against 20%, because the big farm loads can only go to the 17 recipients with room, who sit in
somewhat lower-need areas (weighted figures are compared with the corpus as means). The audit searches with the raw
posting text; the live agent searches with a rewrite Gemini writes. Ten postings cannot separate a real skew from noise. We found this by having the first version
reviewed cold: it counted one recipient three times and reversed our own headline. Table: [equity audit](../agent/food_broker/EQUITY-AUDIT.md).

## 8. Limits and what is next

Recipient names and addresses are real; their storage, capacity and pickup times are generated. Shelf life is consumer
guidance. Locations are ZIP-level. One metro, ten postings. Next: remember who received food recently so one pantry is
not asked every time, and split a load no single recipient can take.

## Where each scoring dimension is answered

| Dimension | Answered on |
|---|---|
| Impact and insight | Slides 1 to 3, and the Match Brief in the video |
| Technical execution | Slides 3 to 5: vector search used and shown to matter; live service |
| Rigor and judgment | Slides 4, 6, 7 and 8: the decoy, the data bug, the audit, the limits |
| Craft and communication | The demo script, one moment that lands (slide 4) |
| Bonus, range | Managed MCP server, Cloud Run, Vertex AI, Cloud Build |
