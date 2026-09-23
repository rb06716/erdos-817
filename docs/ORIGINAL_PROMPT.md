# The original prompt

This is the complete task prompt that started the work, exactly as the repository owner, Ryan Brown, sent it to
Claude Code at 23:38 UTC on 22 September 2026 (7,601 characters, reproduced verbatim from the session transcript).
It names no field, problem or method: choosing Erdős Problem #817 was the agent's own decision. The full account of
what happened next is in [HOW_THIS_WAS_PRODUCED.md](HOW_THIS_WAS_PRODUCED.md).

Claude Code also supplies its own standard operating instructions to the agent (for example, which git branch to
push to and how to format commit messages). Those come with the product and were not written by the owner.

````text
Your mission is to make one genuinely novel, useful, provable, and reproducible discovery.

You have broad autonomy to choose the field, formulate hypotheses, write and run code, obtain freely available public data, search literature and the web, construct simulations, perform mathematical or statistical analysis, use automated hypothesis generation, falsification, exhaustive search, theorem/proof techniques, counterexample search, optimization, or any other legitimate research method available to you.

SUCCESS CRITERIA

The project is successful only when you produce a concrete result that:

1. Appears genuinely novel after a serious prior-art and literature search.
2. Can be independently reproduced by another person.
3. Has strong evidence, a proof, a computational certificate, or another objective verification method.
4. Has a plausible beneficial application or advances useful human knowledge.
5. Requires little or no money to reproduce.
6. Does not depend on trusting your interpretation alone.
7. Survives deliberate attempts by you to falsify it.

Do not stop at an interesting idea, hypothesis, correlation, proposal, or literature review. The objective is an actual result.

RESEARCH STRATEGY

Optimize for probability of success, not prestige.

Prefer domains where a single researcher with coding ability and modest compute can establish novelty and correctness, including:

- mathematics and combinatorics
- algorithms and data structures
- optimization
- numerical methods
- graph theory
- information theory
- error detection/correction
- computational science
- open scientific datasets
- overlooked relationships between existing public datasets
- reproducible empirical regularities
- counterexamples to published conjectures or assumptions
- improved bounds
- new heuristics with measurable performance improvements
- small but useful scientific or engineering discoveries

Avoid projects whose validation requires expensive laboratories, proprietary datasets, large GPU clusters, paid APIs, specialized physical equipment, or human/animal experimentation.

Do not conduct work involving weapons, harmful biological or chemical experimentation, malware, unauthorized access, privacy invasion, or other dangerous or illegal activity.

OPERATING METHOD

Act as an autonomous research scientist.

Begin by generating multiple candidate research directions and rank them internally by:

novelty potential × tractability × verifiability × usefulness ÷ computational cost.

Investigate the strongest candidates quickly. Kill weak directions aggressively. Do not spend most of the budget pursuing one attractive idea before testing whether it is likely to work.

Use literature searches early enough to avoid rediscovering known results, but do not allow literature review to consume the project.

Look specifically for research spaces with:

- enormous searchable combinatorial spaces
- old conjectures that can now be computationally tested farther
- published algorithms with obvious unexplored parameter regimes
- datasets collected for different purposes that have rarely been analyzed together
- papers containing assumptions that can be systematically stress-tested
- small optimization problems where exhaustive search can establish an exact result
- empirical rules accepted from limited historical data that can now be tested against larger public datasets

Build tools and scripts whenever automation increases the number of hypotheses you can test.

Maintain a research log containing hypotheses, experiments, failures, evidence, sources, code, and decisions so the final result has a complete provenance trail.

RESOURCE CONSTRAINT

This project must remain comfortably within a Claude Max $200/month subscription and should incur essentially no additional monetary cost.

Treat Claude usage as a scarce research resource.

Prefer scripts, local computation, cached data, efficient searches, summarized intermediate state, and inexpensive deterministic computation over repeatedly spending model tokens on work that code can perform.

Do not purchase datasets, APIs, compute, subscriptions, or services.

Periodically evaluate whether the current direction justifies additional model usage. If it does not, pivot.

DISCOVERY LOOP

Repeat this loop until a defensible discovery emerges:

OBSERVE
Identify an unexplored question, discrepancy, optimization opportunity, conjecture, unexplained pattern, or search space.

HYPOTHESIZE
State a precise claim that could be true or false.

TEST
Design the cheapest decisive experiment or computation.

FALSIFY
Actively search for counterexamples, confounders, data leakage, numerical artifacts, multiple-testing effects, alternative explanations, and known prior work.

ITERATE
Improve, abandon, or replace the hypothesis.

VERIFY
Once something survives, reproduce it independently using a second implementation, alternate method, held-out data, formal proof, exhaustive enumeration, or another appropriate verification technique.

NOVELTY CHECK
Search academic papers, preprints, patents where relevant, GitHub, technical literature, and the broader web using multiple descriptions of the result. Search both the exact result and the underlying concept because terminology may differ.

If prior work contains the same result, it is not the discovery. Determine whether your result extends it in a genuinely new way or move on.

Do not weaken the novelty standard simply to finish.

FINAL ADVERSARIAL PHASE

When you believe you have discovered something, temporarily switch roles and try to destroy the result.

Assume it is wrong.

Attempt:

- independent reimplementation
- randomized tests
- boundary cases
- adversarial examples
- alternative datasets
- alternative statistical tests
- exact arithmetic where numerical precision matters
- comparison against strong baselines
- leakage checks
- sensitivity analysis
- exhaustive verification where feasible
- deeper prior-art searches

Only advance a result that survives.

DELIVERABLE

Create a self-contained research package containing:

README.md
DISCOVERY.md
METHODS.md
PRIOR_ART.md
REPRODUCE.md
LIMITATIONS.md
research_log.md

and all source code, tests, data-download scripts, checksums or source URLs, generated results, and verification tools needed for reproduction.

DISCOVERY.md must clearly state:

- the discovery in one sentence
- why it appears novel
- why it matters
- exact evidence supporting it
- how it can be falsified
- independent verification performed
- remaining uncertainty

REPRODUCE.md should allow a technically competent stranger on an ordinary computer to reproduce the central result from scratch with as few commands as practical.

Where possible, create a machine-verifiable artifact such as a proof certificate, exhaustive-search certificate, deterministic test suite, independently generated result file, or cryptographic hash of the verified output.

FINAL STANDARD

Do not confuse novelty with complexity.

A small previously unknown theorem, counterexample, algorithmic improvement, exact optimum, useful empirical relationship, or reproducible scientific observation counts if it is genuinely new and defensible.

Relentlessly pursue the mission, pivot when necessary, and use the full range of reasoning, coding, research, experimentation, and verification available to you.

Do not prematurely conclude that the task is impossible.

Continue searching for increasingly tractable discovery spaces until you obtain the strongest genuinely novel and independently verifiable result achievable within the available resources.
````
