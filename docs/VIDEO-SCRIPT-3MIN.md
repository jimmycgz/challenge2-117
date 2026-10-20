# Pitch video script, 2:45

Navigation: [long demo script](DEMO-SCRIPT.md) · [deck outline](DECK-OUTLINE.md) · [submission checklist](SUBMISSION.md) ·
[captured evidence](evidence/README.md) · [equity audit](../agent/food_broker/EQUITY-AUDIT.md).

The organizers want a pitch video under 3 minutes. This script runs about 2:30 and stops at 2:45 at the latest. Judges
watch it after the event and cannot ask questions, so anything not said or shown here counts as unanswered. The long
version, with the farm, formula, no-match postings and the follow-up questions, is [DEMO-SCRIPT.md](DEMO-SCRIPT.md).

Presenter: ______ (write the name here, and use it in the opening line).

## Before you record

- Open the chat page: the service address, then `/dev-ui/`. Pick the `food_broker` agent and start a new session.
- The page lists everyone's test sessions. Type nothing personal.
- An answer takes about 13 seconds on Cloud Run and about 22 locally. The table says which waits you talk over and
  which the editor cuts.
- Answers vary from run to run: Gemini rewrites the search, so the recipient names and ranks on screen can change.
  Read names off the screen. The only recipient this script names is from a saved run, and it says so.
- Keep a second window open on the evidence folder with [demo-tracks.txt](evidence/demo-tracks.txt),
  [pool-study.txt](evidence/pool-study.txt), [mcp-walk-in-answer.md](evidence/mcp-walk-in-answer.md) and the
  [equity audit](../agent/food_broker/EQUITY-AUDIT.md) open, ready to switch to.

## The plan

Segments 4 and 9 are in your own words: the cell gives the facts to land, and the count is for those facts said
plainly. Everything else may be read as written, or said your way with the same facts and numbers.

| # | Segment | Seconds | What is on screen | Words to say | Spoken words | Live wait included |
|---|---|---|---|---|---|---|
| 1 | The problem | 15 | Presenter on camera | "I'm [your name]. Our track is retail and grocer rescue, in Chicago. A grocer has ten crates of spinach that must leave in six hours and stay cold. Who can store it, and get there in time?" | 37 | None |
| 2 | Paste the spinach offer | 22 | Chat page. Paste posting 1 (below), press enter, tool calls appear | "The agent pulls the eighty closest Chicago recipients by meaning with BigQuery vector search, then drops anyone who can't keep it cold, take the load or collect in time. Names and addresses are real, from IRS records; storage, capacity and pickup times are generated; shelf life is consumer guidance; locations are ZIP-level." | 52 | Yes, about 13 s on Cloud Run, talked over. Locally about 22 s: the editor cuts what the talk doesn't cover |
| 3 | The Match Brief | 9 | The answer, scrolled slowly from the summary to part 5 | "Six parts: who and why, what they can take, the clock and margin, and a message ready to send." If you name the recipient, read it off the screen | 19 | None |
| 4 | The decoy | 32 | Part 6 of the live answer ("rejected but close"), then [demo-tracks.txt](evidence/demo-tracks.txt) (retail block), then [pool-study.txt](evidence/pool-study.txt) | In your own words. Facts in the section below | about 78 | None |
| 5 | "They said no" | 14 | Same session. Paste posting 2 (below); the new brief appears | "Say they turn it down. It searches again, skips whoever said no, and briefs the next one." Read the new name off the screen if you say it | 17 | Yes, about 13 s. Talk over the first 7 s; the editor cuts the rest (about 6 s, or 15 s locally). Uncut, this segment is 20 s |
| 6 | Other tracks | 9 | [demo-tracks.txt](evidence/demo-tracks.txt), farm and essentials blocks | "The same corpus and search also handled five tons of farm potatoes and sealed infant formula, with no rules per track." | 21 | None |
| 7 | The data question | 9 | [mcp-walk-in-answer.md](evidence/mcp-walk-in-answer.md), the saved answer | "Data questions go through Google's managed BigQuery MCP server, read-only: thirteen of a hundred and ninety-two have a walk-in cooler." | 20 | None: the saved answer is shown. Typing it live adds about 13 s |
| 8 | The audit | 26 | The group table in the [equity audit](../agent/food_broker/EQUITY-AUDIT.md) | "Did the food go where the need is? Counted per posting, our matches have more poverty than the corpus, and the other two measures are mixed. Counted per recipient they sit lower, because one pantry won three of the four retail offers. Weighted by estimated volume, assistance is nine percent against a corpus mean of twenty. Ten postings can't separate a real skew from noise." | 65 | None |
| 9 | The close | 14 | Presenter on camera, or the repository's front page | In your own words. Facts in the section below | about 34 | None |
| | **Total** | **150** | | | **about 343** | Two live answers, 26 s of waiting: 20 s talked over, 6 s cut |

150 seconds is 2:30, which leaves 15 seconds for a slow answer or a stumble before the 2:45 line. If the editor does
not cut the wait in segment 5, the total is 156. Recorded against the local server with no cuts at all, it is about
165, so cut the waits.

343 words in 150 seconds is about 137 words a minute, in the planned range once the waiting is paid for. The two
own-words counts (segments 4 and 9) are the facts below said plainly; a longer telling eats the 15-second margin.

## What to type

Posting 1, in a new session (segment 2):

```text
A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.
```

Posting 2, in the same session, after the spinach answer (segment 5):

```text
They said no. Who's next?
```

Only if you have the time and choose to run segment 7 live, in the same session:

```text
How many recipients in the corpus have walk-in cold storage, and what share of all recipients is that?
```

## Segment 4: the decoy, in your own words

Slow down here; this is the beat judges should remember. Say these facts, in this order, in your own words:

1. On screen, part 6: the closest recipients the agent removed, each with its rank by meaning and the reason. Read
   the names and ranks off the screen; they change from run to run.
2. Switch to [demo-tracks.txt](evidence/demo-tracks.txt) and say it is a saved run: the three nearest by meaning were
   all removed.
3. One of them, Greenline Community Pantry, is an invented case in the challenge data. It writes that its families ask
   for fresh greens, and that it has no refrigeration of any kind.
4. The nearest recipient that passes the filters is eleventh by meaning.
5. Switch to [pool-study.txt](evidence/pool-study.txt): a pool of fifteen left one viable recipient, forty left three,
   eighty left twelve.
6. Only if there is time, and the first thing to drop here: the agent still picks a safer recipient than the nearest
   passing one, which has a household fridge and one hour of slack, while its picks have two or three hours.
7. One line: the rule that always shows a cold-storage rejection is tested with a case that fails when the rule is
   switched off, and that test caught a sorting bug in our first version.

Leave out where the agent's own top three sit. In the saved run they are 50th, 54th and 63rd by meaning, because the
ranking puts a comfortable margin and sturdier cold storage ahead of closeness. Those are easy to mistake for the
first recipients that pass, which start at 11th.

## Segment 9: the close, in your own words

1. The limits: one city, ten postings, and generated profiles, so the agent tells the coordinator to confirm by
   phone.
2. Not built yet: splitting a load across several recipients, and remembering who received food recently so one
   pantry isn't asked every time.

## If you run long

Decide this now, not while recording. Drop in this order, and stop dropping as soon as you are under 2:45:

1. Segment 6, the other-tracks line (saves about 9 s).
2. Segment 7, the data question (saves about 9 s).
3. Segment 3, cut to "Six parts, and a message ready to send" (saves about 5 s).
4. In the edit, cut every wait that nobody is talking over.

Never drop segment 1 (the track), the real-or-generated sentence in segment 2, the decoy, "they said no", the audit or
the limits in the close.

## If the live page is slow or gone

Say once that these were captured from the live service earlier today, then show them in place of the live steps:

- Segments 2 to 4: [evidence/spinach-answer.md](evidence/spinach-answer.md), then
  [evidence/demo-tracks.txt](evidence/demo-tracks.txt) and [evidence/pool-study.txt](evidence/pool-study.txt).
- Segment 5: [evidence/follow-ups-transcript.md](evidence/follow-ups-transcript.md), the second turn.
- Segment 6: [evidence/demo-tracks.txt](evidence/demo-tracks.txt).
- Segment 7: [evidence/mcp-walk-in-answer.md](evidence/mcp-walk-in-answer.md).

The saved spinach answer ranks its rejections differently from demo-tracks.txt. Read what each file shows.

## Where each number comes from

| Said in segment | Figure | Source |
|---|---|---|
| 2 | Pool of eighty | [agent README](../agent/food_broker/README.md), "How it works", step 1 |
| 4 | Three nearest removed; Greenline's profile text; nearest viable 11th by meaning | [demo-tracks.txt](evidence/demo-tracks.txt), retail block |
| 4 | Greenline is an invented case | [agent README](../agent/food_broker/README.md), "Why a plain top-k search is not enough" |
| 4 | Pool 15 left 1, 40 left 3, 80 left 12 | [pool-study.txt](evidence/pool-study.txt) |
| 4 | The test and the sorting bug | [deck outline](DECK-OUTLINE.md), slide 4; the test is in [selfcheck.py](../agent/food_broker/selfcheck.py) |
| 7 | 13 of 192 | [mcp-walk-in-answer.md](evidence/mcp-walk-in-answer.md) |
| 8 | Per posting, per recipient, three of four retail offers, 9% against a mean of 20%, ten postings | [equity audit](../agent/food_broker/EQUITY-AUDIT.md), group table and "What the numbers say" |
| Before you record | About 13 s on Cloud Run, about 22 s locally | [agent README](../agent/food_broker/README.md), "Speed" |
