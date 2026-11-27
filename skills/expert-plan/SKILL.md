---
name: expert-plan
description: >
  Plan a task with the user in rounds of questions, then hand back the full
  plan written to an expert's standard. First interview the user one round at
  a time over a tree of decisions (each question numbered, with a recommended
  answer), looking up facts yourself instead of asking. When nothing is left
  open and the user confirms, write the plan as a deeper prompt, not a bigger
  one: what the work is
  for, the field, done when, expert moves, raw material, methods, an external
  check, the likely failure, what stays off the table, what is unverified, and
  the first step. USE WHEN: /expert-plan, "plan this with me like an expert",
  "grill me and then write the plan", "interview me before planning". NOT FOR:
  rewriting a prompt with no questions (use expert), or only stress-testing an
  idea with no plan at the end.
metadata:
  internal: true
---

# Expert plan

Joins two methods. The rounds of questions come from the `grilling` skill by
Matt Pocock (github.com/mattpocock/skills, MIT license). The plan comes from
the `expert` skill in this collection, which grew out of a prompt shared by
Felix Rieseberg. This skill carries its own copy of both: when `expert`
changes, check whether the change belongs here too.

## Input

The task is the whole message that contains `/expert-plan`, wherever the tag
sits, together with anything attached to it. If the message holds nothing but
the tag, use the user's most recent request in this conversation. If there is
none, ask for the task in one line and stop. Calling the skill is a request
for questions and then a plan, not for the work: do not start editing or
running the task. Read-only looks at files and tools to find facts are fine.

## Deeper, not bigger

Keep the user's goal and scope. Depth means a higher standard for the same
outcome: better sources, sharper methods, real verification. Do not add
deliverables, features or side quests, in the questions or in the plan. If a
question or a suggestion would make the job larger rather than better, drop
it.

## Part 1: the rounds

Map the task as a **design tree**: every decision branches into the decisions
that hang off it. Sort its decisions the way a decision hierarchy does
(Spetzler, Winter and Meyer, *Decision Quality*): **given** (already settled
in this conversation: skip them, and keep the user's wording for the plan),
**focus** (what this plan must decide now: these are the rounds) and
**deferred** (what can wait for the work itself: name them in the plan, do
not ask). A hope outside the user's control ("customers will love it") is not
a given; it is an assumption to test.

Seed the focus decisions with what only the user can tell you:

- What the work is for: the decision it serves or the change it must cause,
  and what is in and out of scope.
- What "done" looks like, and who or what will judge it.
- Who will carry out the work and who can block it, if that is not the user
  alone (*Decision Quality*: much of a decision's value is lost in the
  handoff to the people who execute it). A plan the doers did not agree to
  fails at the handoff.
- What must stay untouched, and why.
- What the plan has to fit: what the user already knows and uses, the
  resources they have (time, money, people), the systems, processes or
  audience it must work with, and the scale it must handle.
- What is needed now and what is expected later. Ask about later only so the
  plan does not block it, never to build it now.
- The load-bearing premises: a cause stated in the request, or a prerequisite
  of your own approach, that would change the plan if it were false.

### Ask like an expert planner

A competent planner asks the checklist above. An expert asks the few
questions whose answers decide the plan, in words simple enough to answer in
one line.

Before the first round, map what the plan takes for granted (assumption
mapping, David Bland and Alex Osterwalder, *Testing Business Ideas*, adapted
from Gothelf and Seiden's *Lean UX*). For each assumption, ask whether the
people involved want it, whether it can be done, and whether it is worth
doing (desirability, feasibility, viability). Rank it by importance (if it is
wrong, the plan fails and the rest no longer matters) and by evidence
(relevant, observable and recent, or none). The rounds go to the important
assumptions with no evidence; for an important one that already has some,
ask whether that evidence is good enough.

Then pick and word the questions with these moves:

- **Ask only what changes the plan** (Ronald Howard, "Information Value
  Theory", 1966). Test each question: if the user could answer it with
  certainty, would the plan change, and by how much? An answer is worth what
  the plan can do with it, not how uncertain it is. Write what the plan does
  under each likely answer; if every answer leads to the same plan, drop the
  question and state your default. Skip a lookup that costs more than the
  difference it could make.
- **Ask about their life and the past, not about your idea** (Rob
  Fitzpatrick, *The Mom Test*). Opinions and hypotheticals ("would you...?",
  "will you...?") get hopes; specifics in the past ("talk me through the last
  time that happened", "what have you already tried?") get facts. If they
  never looked for a fix, the problem may not matter to them. When the
  request names a feature or a tool, ask what it is for: a request is
  understood, not obeyed.
- **Do not let your recommendation do the answering.** People say what they
  think you want to hear (Fitzpatrick), and a model's suggestion can change
  with one word of the question. Ask a question about the user's facts or
  context openly, and give your recommendation only as the assumption the
  plan will use if they do not know. For a choice of approach or tool, ask
  the context questions first and put the choice itself in the next round,
  once those answers are in, so it never goes out without a recommendation
  or with one picked before the context. Every recommendation
  says what it rests on: an answer the user gave, or a fact you found; if it
  rests on neither, say it is your default ("the first step checks it" says
  how it gets tested, not what it rests on). A recommendation is a value a
  "yes" settles: a number, a date, a named option, never "low", "a few" or
  "months", and never "tell me the number". Where the value comes from
  depends on the kind of fact. A fact the work can measure (how many rows,
  how long a script runs) gets a value the plan assumes and its first step
  checks. A fact that lives only with the user (how long something took them
  or people they know, why an earlier attempt failed, a date they have not
  set) is never invented: recommend what they already said or what you
  found, or else a neutral default the plan does not lean on, worded as a
  named option and marked as your default ("no date yet: the plan sets one
  once the first area is measured"; "no comparable case: the plan starts
  with no base rate").
- **Offer real alternatives for the key choice** (*Decision Quality*: a
  decision cannot be better than the best alternative considered). For the
  one or two choices the plan turns on, give two or three distinct options
  instead of one proposal to accept or reject, and recommend one.
- **Force the trade-off** (*Decision Quality*, clear values and trade-offs).
  When two goals can collide (the date and the scope, speed and polish), ask
  how much of one the user will give up to get more of the other; "both" is
  how plans fail quietly.
- **Calibrate by reversibility** (Annie Duke, *How to Decide*). If a choice
  can be undone and replaced at a reasonable cost, or the options are close
  enough that any of them would do, give your default and no question. To
  tell whether they are close enough, use Duke's Only-Option Test: if each
  one were the only option, would the user be happy with it? If yes for all,
  pick one and move on. Ask about what is costly to undo: deleting data, a
  public launch, a contract.
- **Take the user's outside view** (Kahneman and Lovallo, "Timid Choices and
  Bold Forecasts", 1993). Ask them to think of others who did something
  comparable, from a point like theirs, and ask one thing only: how long it
  took them from there, in plain words with no label of its own. Whether
  some gave up is a cause of failure, so it belongs to the premortem; what
  makes this case better or worse goes to the next round, once the time is
  in, and only if its answer would change the plan. People who know the
  answer still plan from the inside unless asked this way. Ask it in the
  first round, since its answer sets the scale of the rest; use it in the
  plan even when it is discouraging.
- **Ask the question you would rather not ask** (Fitzpatrick). Most plans
  have one question whose answer could sink them; ask it.
- **Run the premortem with the user, after a sketch of the plan** (Gary
  Klein, "Performing a Project Premortem", 2007). Klein runs it once people
  know the plan, so in the last round sketch the plan in two or three lines,
  then say that the time the work should take has passed and the plan
  failed, and ask for every reason they can think of (counting what made
  people they know stop, if any tried something comparable and gave up),
  above all the ones they
  would not usually say out loud. Then ask for a kill criterion in Annie
  Duke's "states and dates" form (*Quit*): "if by <date> I have not <reached
  this state>, I stop." Recommend a criterion that tests the likeliest cause
  of failure (people going back to the old way, say), not a step of the work
  that a script already checks. Then the backcast, Duke's companion to the
  premortem (*How to Decide*): the work succeeded; what is the one thing
  that most made it work? It names what must go right, which the premortem
  does not. Their answers feed Likely failure, External check and First
  step.

Keep each number to one decision and plain words: the depth is in what you
ask, not in how long the question is. Different decisions get their own numbers, even if
the round grows long: "have they agreed?" and "if one refuses, who decides?"
are two. Test it: if the user could say "yes" to one part and "no" to
another, split it. A part you split off goes to one of three places, never
dropped silently: its own number in this round; the next round, if it only
matters after another answer still open; or, if no answer would change the
plan, a default the plan states.

### The rounds

Work the tree in **rounds**. The **frontier** is every focus decision whose
prerequisites are already settled: the questions you can ask now without
guessing at answers you haven't heard yet. Ask the whole frontier in one
round, number each question and give your recommended answer, then wait for
the answers.

Format a round like so, in plain Markdown with no emoji:

```
**1. <question title>**

<one or two sentences of context, if needed> <the question: one decision>

*Changes the plan:* <if A, the plan does X; if B, it does Y>

> **Recommended:** <your recommended answer>, because <what it rests on>

---

**2. <question title>**

<context> <the question>

*Changes the plan:* <...>

> **Recommended:** <...>, because <...>
```

Word each question so "yes" accepts your recommended answer: never ask "Is
there X?" while recommending "no X". Write the round, labels included, in the
user's language (in Portuguese: *Muda o plano:* and **Recomendação:**).
Number questions across rounds, so a later round continues from the last
number and the user can answer "3: no, ..." without ambiguity. End each round
with one line on how to answer (by number, or "yes to all", which accepts
every recommendation, defaults included) and what the next turn does. Before
sending a round, check it number by number:

- Split test: could the user say "yes" to one part and "no" to another? Then
  it is two decisions; split it into two numbers, or move the later part to
  the next round if it only matters after the first is answered. Run it on
  the recommendation too: one that adds a choice the question did not ask
  ("yes, and the base components can start now") holds a second decision.
- Every number has a recommendation, and it answers every part of its
  number, so a "yes" settles the whole number.
- Read the recommendations as if the user answered "yes to all": they must
  agree with each other (a target of 50 next to a base rate of 10 to 30 does
  not). A default says it is a default; "you did not mention it" is not what
  it rests on. Since every number has one, "yes to all" is always a valid
  answer: never say in the same round that some numbers only the user can
  answer.

Each round of answers reshapes the tree: settled decisions push the frontier
outward and unblock the questions that depended on them. Recompute the
frontier and ask the next round. A question whose answer depends on another
question still open in this round belongs to a later round.

Finding **facts** is your job, never the user's. When a question needs a fact
from the environment (the code, the files, the data, what a tool can do), look
it up; do the quick lookups (is the file here, what does it contain) before
the first round, so no question asks what a look would have answered. For a
wide search, start a subagent with a fresh context. Don't block
on it: only the questions downstream of a running search wait for it; ask the
rest of the frontier now. The **decisions** are the user's: put each to them
and wait. A fact you cannot reach (it lives only with the user, outside this
environment) may be asked once, with the kind of recommendation given above
for a fact that lives only with the user.

Once the purpose, what done looks like, what stays untouched and what the plan
has to fit are settled, the next round is the last one: the sketch (it
assumes your recommended option for any choice still open in that round), the
premortem, the kill criterion and the backcast, plus only the questions still blocking the
plan. Details the first step can check are assumptions, not another round.
This holds even when a tool or approach choice is still open: its context is
in by now, so the choice goes in this same round with its alternatives, and a
part that this section or the outside view would send to "the next round"
becomes a default the plan states. Never add a round before the last one
just for more context.

The rounds are done when the frontier is empty: every branch visited, nothing
left silently assumed. Before saying so, check the weakest link (*Decision
Quality*: a decision is only as good as the weakest of its six requirements):
the frame, the alternatives, the information, the values and trade-offs, the
reasoning, and the commitment of the people who will act. If one that only
the user can fill (the frame, the values, the commitment) has nothing from
the rounds behind it and would change the plan, ask one question about the
weakest, never a new round; anything else becomes a default in the plan.
If you ask it, say you will ask before writing the plan once it is answered;
if not, say in one line that you have what you need and ask whether to write
the plan. Do not write it until the user confirms: a
"yes" to the questions, even "yes to all", answers the questions, not this.

## Part 2: the plan

The plan is read by a session that acts on it and does not re-check it, so a
guess written as a fact becomes a false premise there. Three habits keep it
honest:

- **Specific.** Name the actual thing, not the category. A line that would
  read the same for any task is not answered yet.
- **Provenance.** Every specific claim (a behavior of the code, a fact about
  a system or the data, a command, flag, default or version) is marked
  `(checked: <command or file>)` or `(not checked: <where it came from>)`.
  Before writing, do the quick lookups from Part 1 that this conversation
  has not done yet (list the folder, open the files the plan rests on), even
  when the user goes straight to "write the plan". When a quick read-only
  command can check a claim, run it and write `checked`; `checked` names a
  command you ran or a file you read in this conversation, and a claim
  remembered and not run is `not checked`. If a command was blocked, try a
  file read; if nothing worked, mark the claim `(not checked: not run)`. A fact the user stated and
  nobody verified is `(not checked: stated by me, not measured)`, and an
  assumption accepted in the rounds is `(not checked: assumed; the first step
  checks it)`. A decision the user made in the rounds is settled, not a fact
  to verify: it never takes a mark. A well-known framework or practice named
  from memory needs no mark either; a specific claim about it (a number, a
  version, a quote) does. A tool or approach that no answer from the rounds
  and no fact found supports is a model default, and a model's pick can
  change with one word of the question: mark it `(default: <the answer that
  would change it>)`.
- **Honest gaps.** Write `none`, with the reason, when a line does not apply,
  and `I don't know` rather than naming a source or tool you are not sure
  exists.

First restate the deliverable's noun as the verb it must accomplish. The
deliverable stays the same; the verb says what it is for: a quarterly review
deck is there for "getting busy people to believe a story about cause and
effect, and to decide under uncertainty, in 30 minutes" (a trick from Tom
Kelley and Jonathan Littman's The Art of Innovation). Use the purpose the user
gave in the rounds.

Then name the **field**: the profession whose standard applies (e.g.
"investigative journalism", "SRE incident response", "clinical pharmacology",
"essay editing"). Then answer these lines for that field. They appear once in
the reply, inside the plan; do not print them a second time before it:

1. **Done when.** One sentence on the finished state a third party could
   observe, built from the standard the user chose. How to verify it goes in
   External check, not here.
2. **Expert moves.** The two or three things that separate expert work from
   competent work here and that the user did not ask for, such as stating the
   decision the work serves, reproducing before fixing, or writing the
   counter-argument. Take the outside view before the inside one (Kahneman and
   Lovallo's reference class): name the class of similar jobs and what usually
   happens in it (how long it takes, how often it meets its goal; failure
   causes belong in Likely failure, not here), starting from the user's own
   outside view from the rounds, then adjust for what is really different
   here. With no user answer and no named source, say in one clause that the
   base rate is unknown; don't invent one.
3. **Raw material.** The primary sources to start from instead of summaries:
   the dataset, not the chart; the filing, not the article; the logs and the
   code, not the bug report. Say where it lives if you found it; if you did
   not, say so and what the first step must get. The plan holds no open
   questions: an unknown is stated as an assumption marked `not checked`.
4. **Methods.** The heart of the plan: the working frameworks that the best
   people in this field actually use for this kind of job. Name each one by
   its proper name, say who it comes from or where it is documented, and say
   why it fits this task better than the obvious approach. Pick the one or two
   that fit and write this line as their steps in order, applied to this task
   (the tool, query or artifact at each step), so the plan walks through the
   framework instead of mentioning it. For the key choice, name in one
   sentence the alternatives compared in the rounds and why this one won, so
   the session does not reopen it. If the rounds compared none, name the ones
   you considered, say they are yours, and mark the pick `default`; never
   write that the rounds compared what they did not. Then the named techniques,
   instruments, libraries or commands that serve it. A generic label ("best
   practices", "a structured approach") is not an answer.
5. **External check.** What, other than the user or the model, would show the
   result is right, with the judge and the pass the user chose. Say what
   counts as a pass and what counts as a failure. Where the work allows it,
   include at least one check the session can run itself and get a pass or
   fail at once (a script, a test, a recomputation from the raw data, a
   held-out sample the work was not tuned on), and a person's judgment on top
   of it. The runnable check must test what matters for this task, not a proxy
   made up to have something to run; if no such check exists, say so and rely
   on the person.
6. **Likely failure.** Start from the user's premortem in the rounds (Gary
   Klein): the work is done and has failed; write the most plausible cause for
   this task, and the kill criterion as a state and a date ("if by <date>
   <this state> is not reached, stop and re-plan").
7. **Off the table.** What must stay untouched even if it looks helpful, each
   with its reason. A limit with its reason gets applied correctly to cases it
   did not foresee. Then the deferred decisions from the tree, each with when
   it gets decided, so the work does not settle them by default.
8. **Not checked.** The assumptions still open, numbered, riskiest as 1:
   the ones that matter most and have the least evidence, as in the map from
   the rounds, not the ones easiest to measure. End with the one observation
   that would overturn the task's premise.
9. **First step.** One concrete action on the hardest, most uncertain part,
   not the easy part that only looks like progress (Annie Duke's monkeys and
   pedestals, *Quit*). If a single prerequisite would make the whole task
   worthless when false, verifying it is the first step.

Read the answers against every decision from the rounds: each move and limit
agrees with them. When the user stated a decision in their own words, keep
their wording; translating it changes it.

Write the plan in a single fenced block the user can copy: one paragraph
stating the task and what it is for in the user's terms (the verb goes in
this paragraph, in plain words with no "Verb:" label), then **Field:** and the nine
lines, each as a bold label with a colon (**Done when:** through **First
step:**), unnumbered so no one reads them as steps, and in the language of
the user's messages (a phrase they quote in another language stays as quoted
and does not switch the plan). Add no other sections: a settled limit such as a deadline or a
budget goes in the opening paragraph or under Off the table, so the plan
keeps the same shape every time. Keep the provenance marks in it. Write it
from the user ("I") to the session that will run it ("you"): "I don't
want...", "check this before you...". Never write as the planner ("you told
me", "I haven't seen your files") and never name the user or write "the user
said". Make it as long as it needs to be.

After the block, in two to four bullets, say what the plan contains that the
user did not ask for, and what in it is still unverified.

Stop there. Offer in one line to run it now; don't start the task unless the
user says so.
