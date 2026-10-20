# Demo script for the pitch video

Navigation: [submission checklist](SUBMISSION.md) · [agent README](../agent/food_broker/README.md) ·
[equity audit](../agent/food_broker/EQUITY-AUDIT.md) · [captured evidence](evidence/README.md).

Plan for about three minutes of screen share with one person talking. Judges watch the recording after the event and
cannot ask questions, so every point below has to be said out loud or shown on screen.

## Before you record

- Open the service's chat page: the service address, then `/dev-ui/`. Pick the `food_broker` agent if it is not
  already selected and start a new session for each posting. Nobody here has tried this in a browser yet, so do one
  dry run first.
- The page lists everyone's test sessions. Type nothing personal.
- Answers vary a little from run to run: the Gemini model rewrites the search and estimates the load, so the top
  recipient's name and the pallet estimate can change. Point at the structure, not at a name you expect.
- Each answer takes 10 to 20 seconds. Say something while it works, or cut the wait when you edit.
- Keep a second window open on [the evidence folder](evidence/README.md). If the live page is slow or gone, show the
  same answers from there (see the fallback at the end).

## The opening line (15 seconds)

Say it as one sentence, in your own words:

> We coordinate food rescue in Chicago. A grocer has just offered us ten crates of spinach and it has to leave within
> six hours. Here is who we would call, and here is what we don't know about them.

## Posting 1: retail, the clock (60 seconds)

Type:

```text
A grocer in Chicago has ten crates of spinach, harvested yesterday, that must leave the dock within 6 hours and stay cold.
```

Point at, in this order:

1. The one-line summary, then part 1: a named organization and its address, and why it fits.
2. Part 3, the clock: hours the food has, the recipient's collection time and the margin. Say what the margin means:
   a match with 20 minutes of slack is a warning, not a win.
3. Part 6, the next two options and the "closest rejected matches", each with its rank by meaning. This is the moment
   to slow down, and to say it in your own words. The facts to land: in the saved run, the three nearest recipients by
   meaning were all removed; two could not collect in time; one, Greenline Community Pantry at rank 3, writes that its
   families ask for fresh greens and that it has no refrigeration of any kind; the nearest recipient that works is
   11th by meaning, and the ranking's top three sit at 50th to 63rd. A live run can pick a different recipient for the rejected list, so read what is on screen;
   the saved version is in [demo-tracks.txt](evidence/demo-tracks.txt).
4. Part 5, the outreach message: ready to send, with the driver sentence if the recipient has no cold transport.

## Posting 2: farm, same corpus (30 seconds)

Type:

```text
A farm south of Chicago has 5 tons of potatoes still in the field. They can load pallets if someone collects within 3 days.
```

Point at: the capacity in part 2 (a recipient with room for the whole load, and whether it has a dock and its own
transport) and the margin in part 3. Say: this is a different track, handled by the same corpus and the same search, with no separate
rulebook. Be honest that splitting a load across several recipients is not built.

## Posting 3: essentials, a data problem the agent caught (30 seconds)

Type:

```text
48 cases of sealed infant formula with 8 months to expiry from a distributor in Chicago, 2 pallets, can sit at room temperature.
```

Point at: the clock in part 3 is the donor's eight months, not an hour. Say: the shelf-life table gave sealed formula
one hour, which is FoodKeeper's figure for an opened container. We found it while auditing, and the agent now warns on
very short figures and trusts the donor's expiry.

## "They said no" (30 seconds)

Stay in the same session as posting 1 and type:

```text
They said no. Who's next?
```

Point at: it skips the recipient who declined and briefs the next one, with a new message ready to send. Then type:

```text
Why them and not the big food bank downtown?
```

Point at: it searches for "food bank" (and "food depository"), finds a large food bank, says where it ranked by meaning
and why it was removed (for example, no room for the load, or a collection time of 36 or 41 hours against 6). Which
organization it finds varies run to run (the Greater Chicago Food Depository in some runs, Americas Food Bank in the
saved one); read what is on screen. Saved version: [follow-ups transcript](evidence/follow-ups-transcript.md).

## When nobody can take it (20 seconds)

Type:

```text
A bakery has 40 trays of cream-filled pastries that must stay refrigerated and leave their dock within 1 hour.
```

Point at: it says there is no match and shows the closest rejections with the reason for each (they need many hours
to collect). Say: an agent that recommends a recipient who cannot store the food is worse than one that says nobody
can.

## A question that is not a posting (20 seconds)

Type:

```text
How many recipients in the corpus have walk-in cold storage, and what share of all recipients is that?
```

Point at: it answers 13 of 192, about 6.8%, and states the query. Say: this goes through Google's managed BigQuery MCP
server, read-only. Matching a posting never goes through free-form SQL, so the filters cannot be skipped.

## The audit (20 seconds, one slide or the audit page)

Show the group table in [the equity audit](../agent/food_broker/EQUITY-AUDIT.md). Say the honest result: counted per
posting, the matches have more poverty than the corpus and the other two measures are mixed; counted per recipient, they sit lower, because one
pantry won three postings; weighted by volume, assistance is 9% against 20% (compared as means). The audit searches with
the raw posting text, while the live agent searches with a rewrite Gemini writes. Ten postings cannot separate a real
skew from noise. The big farm loads can only go to the 17 recipients with room, who sit in somewhat lower-need areas.

## The close (15 seconds)

Say what is real and what is generated: recipient names and addresses are real, their storage, capacity and pickup times
are generated, shelf life is consumer guidance, and locations are ZIP-level. Then say what comes next: remembering who
received food recently so one pantry is not asked every time.

## If the live page is slow or gone

The lab project is temporary. Show the saved answers instead, and say they were captured from the live service:

- Spinach: [answer](evidence/spinach-answer.md) and [structured brief](evidence/spinach-brief.json)
- Sealed formula: [answer](evidence/sealed-formula-answer.md)
- Free-form question: [answer](evidence/mcp-walk-in-answer.md)
- Potatoes: [answer](evidence/farm-potatoes-answer.md)
- No match: [answer](evidence/no-match-bakery-answer.md)
- Three tracks through one search: [demo-tracks.txt](evidence/demo-tracks.txt)
- The service answering with no credentials: [transcript](evidence/curl-transcript.md)
