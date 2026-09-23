# How this was produced

Everything in this repository was produced by an AI agent: Claude (Anthropic), working autonomously in Claude Code
from a single open-ended prompt. That covers the choice of problem, the programs, the computations and the
documents. The repository owner, Ryan Brown, is not a mathematician. The purpose was to explore what a newly
released AI model can do when it is given a broad research mission and then left alone.

This document sets out the whole process, so that readers can judge the result and where it came from for themselves.
Times are UTC and are taken from the session transcript, the [research log](research_log.md) and the commit history.
The agent wrote this account at the owner's request.

## At a glance

| | |
| --- | --- |
| Prompt | one open-ended mission statement ([ORIGINAL_PROMPT.md](ORIGINAL_PROMPT.md)); it names no field, problem or method |
| AI system | Claude (Anthropic) in Claude Code on the web, at the highest reasoning-effort setting, in automatic permission mode (individual actions did not need approval) |
| Hardware | the Claude Code cloud container: 4 vCPUs (Intel Xeon, 2.1 GHz), 15 GB RAM, no GPU; later, the owner's Google Colab runtime for one re-run |
| Cost | within the owner's existing Claude subscription, as the prompt required; no purchases, paid APIs or paid compute |
| Main result | g₃(7) = 474, with a unique extremal set ([DISCOVERY.md](DISCOVERY.md)) |
| Time to the main result | prompt at 23:38 on 22 Sep 2026; set with maximum 474 found at about 00:25; exhaustive search complete at 01:30; the second, independently written program agreed on every value at 03:51, about 4 h 15 min after the prompt |
| Human input before the result | none; the first message after the prompt came at 06:37 |
| Review by a human expert | none yet (see [Verification status](#verification-status)) |

## Timeline (UTC)

### The autonomous phase: no human input (22 Sep 23:38 to 23 Sep 06:37)

- **23:38.** The owner sends the prompt.
- **About 23:40 to 00:15.**
  - The agent surveys its environment: 4 vCPUs, and restricted web access, with arXiv, the OEIS web site and
    erdosproblems.com blocked.
  - It ranks candidate directions: exact values of open extremal problems, falsification of empirical OEIS
    conjectures, counterexamples in graph theory, record constructions, and knot invariants.
  - It searches an offline copy of the OEIS for open extremal sequences with few known terms (634 candidates,
    268 of them referencing Erdős problems).
  - It chooses OEIS A399720 (Erdős Problem #817). The entry, created two weeks earlier, left a(7) open between
    419 and 504, and settling it is a finite computation that can be certified.
- **00:18.** First commit: a reference search, an optimized search, an independently written Rust verifier, a
  definition-level brute-force checker and a certificate checker, cross-validated on the known values n ≤ 6.
- **About 00:25.** A restricted probe finds the set {302, 409, 447, 459, 465, 466, 474}.
- **01:30.** The exhaustive search of every N = 419…478 is complete: no admissible 7-set below 474, and exactly one
  at 474.
- **03:51.** The Rust program reproduces the full count vectors for every N ≤ 478. The C program has also covered
  N = 1…418, so the result does not depend on the published lower bound.
- **04:00 to 12:10.** Secondary results:
  - certified upper bounds for n = 8…14;
  - g₄(1..7) and g₅(1..8), each computed with two programs;
  - a correction to an n = 6 claim in the literature;
  - first prior-art checks, limited by the blocked sites.

### After the result (23 Sep)

- **06:37.** First human message: the owner tells the agent it has no deadline (the agent had set itself an 08:30
  stopping time).
- **09:33.** The owner offers access to a third-party AI model. It was not used.
- **13:19 to 14:20.**
  - The owner asks the agent to evaluate its result against the forum's proof-claims page, and at 13:48 enables
    full internet access.
  - The second prior-art pass finds that carlomitchener had posted the same set as an upper bound on the
    Erdős Problems forum that morning (06:41 forum time). The agent's repository was still private, so that
    post was the first public report, and it is credited as such.
- **14:35.** The owner decides to publish after verification, and asks the agent to investigate whether g₃(8) is
  within reach. It is not on this hardware: the estimate is about 9–13 CPU-years
  ([research/pruning/NOTES.md](../research/pruning/NOTES.md)).
- **14:30 to 15:40.** One-command verification tools and Google Colab notebooks.
- **16:02 to 17:20.** The owner re-runs the verification on Google Colab, first the quick check and then all
  60 values N = 419…478. Everything matches ([results/external_verification/](../results/external_verification/)).
- **17:47 to 19:58.**
  - The owner renames the repository and asks for a thorough review before publication.
  - The agent restructures the repository to a conventional layout.
  - Three review passes by separately prompted instances of the same AI find about fifty problems. The two most
    important are an earlier source (Bae, 2002) and a forum remark by M. Czech that the credit statements had
    missed. All were fixed.
- **20:08 to 20:20.** The owner makes the repository public, merges the changes and publishes release v1.0.0.
- **21:00.** Zenodo archives the release: DOI [10.5281/zenodo.22925446](https://doi.org/10.5281/zenodo.22925446);
  all versions: [10.5281/zenodo.22925445](https://doi.org/10.5281/zenodo.22925445).
- **23:13 to 23:31.** The owner decides not to post the result or submit it to the OEIS personally, but to ask
  the researchers working on the problem to review it, and asks for this account.

## Every message from the owner

| time (UTC) | message, summarised |
| --- | --- |
| 22 Sep 23:38 | the prompt |
| 23 Sep 06:37 | no deadline; continue while it is promising |
| 09:33 | offered a third-party AI model (not used); asked whether the work was heading towards a theorem |
| 13:19 | asked for an evaluation against the forum's proof claims, without changes |
| 13:48 | enabled full internet access |
| 13:59 | asked for the resulting corrections, and to use the new access for any unfinished checks |
| 14:13–14:16 | asked what is novel, whether the repository is current, and whether to continue |
| 14:31–14:35 | asked about Google Colab; chose to publish after verification, then research g₃(8) |
| 15:26–15:36 | reported a notebook error; asked about logging in through a browser (declined) |
| 16:02–17:20 | reported the Colab verification runs |
| 17:44–17:47 | stopped the optional verification steps; renamed the repository; asked for a pre-publication review |
| 19:33, 19:56 | asked to re-run a review that a usage limit had interrupted, then to fix all of its findings |
| 20:08 | made the repository public and renamed the default branch; asked for help with Zenodo; gave the author name |
| 20:25–20:39 | questions about Zenodo; asked the agent to do the remaining steps itself |
| 23:13–23:31 | discussed how to present the work; asked for this document |

Outside the conversation, the owner also merged the pull request, published the release and connected Zenodo.

## Who did what

**The AI:**
- chose the field and the problem;
- designed and wrote all the programs (C, Rust, Python), the tests, the CI workflows and the notebooks;
- ran all the computations except the owner's Colab re-run;
- searched the literature, found and credited prior work, and wrote every document, including this one;
- reviewed its own work, partly by using separately prompted instances of itself.

**The owner:**
- wrote the prompt and provided the environment: the Claude subscription, the GitHub repository and Google Colab;
- answered a few questions, enabled internet access and decided how and when to publish;
- re-ran the decisive verification;
- renamed the repository, made it public, merged the changes, published the release and connected Zenodo.

The owner did not choose the problem, guide the mathematics, or write any code or text.

## Mistakes along the way

The agent made mistakes, and some were caught only later. This is one reason why review by experts matters.

- **Missed prior work.** Its first literature search had no access to arXiv, the OEIS web site or the forum, and
  missed two earlier results:
  - carlomitchener's forum post of the same set, published the same morning;
  - Bae (2002), which already contains a 7-set with maximum 477.

  Both were found later and are credited.
- **Copied attribution errors.** It repeated two errors from a third-party report: the 3ⁿ/n^{1/3} bound is
  Costa's, not Korsky's, and M. Czech's values were posted on 9 September.
- **Bae (2002).** It misquoted Bae (2002), and wrongly implied that Bae–Choi (2003) had copied from it. In fact
  Bae–Choi was submitted first.
- **Cost estimate.** It first overestimated the cost of the n = 8 computation (30–45 CPU-years; recalibrated to
  about 9–13).
- **Maintenance script.** A script could have overwritten the published logs if re-run. This was fixed before
  publication.

Every correction is recorded in the [research log](research_log.md).

## Verification status

- **What supports the result:**
  - an explicit certificate for the upper bound;
  - for the lower bound, two independently written programs that agree on the full count vector for every N ≤ 478
    (both written by the same AI; [DISCOVERY.md](DISCOVERY.md), [LIMITATIONS.md](LIMITATIONS.md));
  - definition-level checks on small cases;
  - the owner's re-run of the decisive range on different hardware (with the same code);
  - automated checks on every change.
- **What is missing:** review by a human mathematician. Everything above was written or checked by AI, or re-run
  with the AI's own code. The owner is asking researchers who work on this problem to look at it, rather than
  posting it or submitting it personally.

## Credit, and what this does not show

This project settles one small value by exhaustive computation. It does not solve Erdős Problem #817, which asks
how g_k(n) grows, and which the problem's own page describes as impossible to resolve by any finite computation. The
lower bound is a large computer search, not a new idea, and no human expert has checked it yet.

The work also depends at every step on the work of people:
- **P. Erdős and A. Sárközy** asked the question.
- **Samuel Korsky's** reformulation (Prop. 4.1 of arXiv:2606.24139) turned it into something a computer can search
  efficiently. Korsky's lower bound, g₃(7) ≥ 419, marked where the decisive part of the search had to begin.
- **Mateusz Czech** computed g₃(5) and g₃(6), created OEIS A399720, and noted that a(7) = 466 had not been excluded.
  Czech's forum remark on the offset form of the optimal sets anticipated the structure that this repository
  calls hole chains.
- **The firesh audit repository** independently checked the small values and showed how far a direct search had
  reached.
- **carlomitchener** found the same extremal set independently and published it first.
- **Jaegug Bae (2002), and Jaegug Bae and Sungjin Choi (2003),** studied these sets two decades ago. Bae's 7-set with
  maximum 477 was already within three of the optimum.
- **Simone Costa** answered Erdős and Sárközy's "in particular" question.
- **Thomas Bloom's erdosproblems.com, and the OEIS,** made the problem visible, precise and current.

The agent chose this problem precisely because these people had made it well posed, current and checkable. What
the AI added was some hours of careful programming and computation on top of their work. The insight that made
that computation possible came from them. It is offered to the people working on this problem to check, use,
correct or set aside as they see fit.
