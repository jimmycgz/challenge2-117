# Submission checklist

Navigation: [3-minute video script](VIDEO-SCRIPT-3MIN.md) · [long demo script](DEMO-SCRIPT.md) · [deck outline](DECK-OUTLINE.md) · [captured evidence](evidence/README.md) ·
[agent README](../agent/food_broker/README.md).

Submit at <http://goo.gle/A4I-Submission> by 16:59 EDT. The organizers' notice names four items: the Pitch Deck, the
Environment Link, the Pitch Video (under 3 minutes) and the GitHub Link. Edits are allowed before the deadline through
the link in the confirmation email. Judges read these after the event and cannot ask questions. Someone on the team
pastes them; nothing here submits.

## Before pasting anything

1. **Merge the pull request.** The default branch is what a judge sees at the repository link. Squash-merge pull request 1
   in the browser as the repository owner. The sandbox's `gh` login is read-only on this repository, so it cannot merge.
2. **Pin the commit.** After the merge, from a clone of the repository:

   ```bash
   git checkout main && git pull
   git tag submission && git push origin submission
   ```

   Submit the repository link together with the tag, so what judges read does not move if someone pushes later.
3. **Check the root page.** The repository's front page now starts with a pointer to the agent README. Open it logged out
   and read it as a judge would.
4. **Freeze the live service at 16:00.** No redeploys after that unless something is broken.

## The four fields

| Field (the organizers' name) | Draft answer |
|---|---|
| GitHub Link | <https://github.com/jimmycgz/challenge2-117> (tag `submission` once merged) |
| Environment Link | Paste the lab link from the Skills page. It names the lab project, so it goes in the portal, not in this repository |
| Pitch Deck | The team's deck, built from the [outline](DECK-OUTLINE.md). It must answer the rigor questions in its own slides |
| Pitch Video (under 3 minutes) | A screen share with a person on camera at the start, following the [3-minute script](VIDEO-SCRIPT-3MIN.md). The [long script](DEMO-SCRIPT.md) is the fuller version |

## Extra links, if the portal has a notes field

- Live service, with ADK's chat page: <https://food-broker-817377390808.us-east1.run.app/dev-ui/>. **This may expire with
  the lab.** It is open to anyone, and the chat page lists test sessions, so do not type anything personal into it.
- Output captured from the live service on the day: the [evidence folder](evidence/README.md). It stays after the lab is gone.
- [Equity audit](../agent/food_broker/EQUITY-AUDIT.md) and the [README](../agent/food_broker/README.md).

## Open items that only the team can close

- The organizers' answer on whether the judging URL must survive past today, and the lab timer.
- A screenshot or recording of one full answer on the chat page, added to the evidence folder.
- The deck and the video.

## Draft one-line description, if asked

A food-rescue broker for Chicago: a coordinator describes a surplus offer, and the agent finds recipients by meaning with
BigQuery vector search, removes the ones that cannot store or collect it in time, and returns a Match Brief with a
message ready to send. Recipient names and addresses are real; their storage, capacity and pickup times are generated.
