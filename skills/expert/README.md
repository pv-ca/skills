# expert

Rewrite a task the way a top professional in its field would ask for it: deeper, not bigger.

## What it does

Add `/expert` to a message and the agent does not start the work. It hands the task back as a prompt rewritten to an expert's standard, then stops so you can read it and decide whether to run it.

The rewrite names the field whose standard applies and answers nine lines for it: done when, expert moves, raw material, methods, external check, likely failure, off the table, not checked, and first step. It keeps your goal and scope: a suggestion that would make the job larger rather than better is dropped.

The session that runs the rewritten prompt acts on it without checking it again, so a guess written as a fact becomes a false premise there. Every technical claim in the rewrite is therefore marked `(checked: <command or file>)` or `(not checked: <where it came from>)`, and an unknown base rate is said to be unknown rather than invented.

## When to reach for it

Type `/expert` anywhere in the message, usually at the end. A message holding only `/expert` rewrites your previous request. Attached screenshots and files count as part of the task. The agent can also reach for it when you ask to make a prompt deeper or what an expert would do.

Reach for it before work where doing the obvious thing well is not enough: a fix whose cause you have not confirmed, a decision with money or users behind it, research where the easy sources are summaries. To have a plan questioned rather than rewritten, use a grilling skill instead.

## Example

You type:

```text
I want to add a cache to my web app's product search endpoint because it feels slow. /expert
```

Without the skill, the agent picks Redis and starts writing cache code. With it, you get back a prompt that starts like this (shortened; full output in [example.md](example.md)):

> I want to make product search feel fast to the people using it. [...] Before I add a cache, I want to find out where the time goes.
>
> **Field:** web backend performance engineering.
>
> **Expert moves:** treat "feels slow" as a hypothesis and measure first. Take the hit rate from the real query logs, not from an assumption. Decide the staleness budget before writing code.
>
> **External check:** "replay the same query sample against the endpoint before and after. Pass means p95 improves by a margin we agree on in advance and the cached responses are byte-identical to uncached ones for the same query." Then an automated staleness test, and production p95 after rollout.
>
> **Likely failure:** the hit rate is low because queries are mostly unique, and p95 barely moves.
>
> **First step:** time one slow request stage by stage, before touching any caching code.

## It's working if

- The reply is one fenced prompt you can copy, then two to four bullets on what was raised, then an offer to run it.
- Methods are named by their proper names, and the external check does not depend on you or the model.
- It is not working if the agent starts editing files, or if a line would read the same for any other task.

## Tests

[evals.json](evals.json) holds the cases: the tag at the end, the tag at the start, a task in Portuguese, a churn analysis, a cause the user already assumed, a slide deck, and a question about experts that must not fire it. Run them with `python3 scripts/eval.py expert`. The last result is in [CHANGELOG.md](../../CHANGELOG.md).

## Credits

Inspired by a prompt shared by Felix Rieseberg and DannyMac180's `be-ambitious` skill. The outside view comes from Kahneman and Lovallo, the premortem from Gary Klein.
