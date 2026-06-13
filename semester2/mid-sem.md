Good — I have your full picture from past sessions. Here is a structured, realistic study plan built around your exam schedule, your existing progress, and the knowledge gaps we have already identified together.

---

# Mid-Semester Exam Study Plan

## Exam Schedule at a Glance

| Date | Time | Course | Type | Gap from Today |
|------|------|--------|------|----------------|
| 20 Jun 2026 | 09:00 AM | AIMLCZG530 — NLP | Regular | ~7 days |
| 21 Jun 2026 | 09:00 AM | AIMLCZG512 — Deep RL | Regular | ~8 days |
| 27 Jun 2026 | 01:00 PM | AIMLCZG546 — SEML | Makeup | ~14 days |
| 28 Jun 2026 | 01:00 PM | AIMLCZG557 — ACI | Makeup | ~15 days |

> **Key observation:** NLP and Deep RL are back-to-back on consecutive mornings. These need the most intensive preparation *first*. SEML and ACI have more runway, and given your prior quiz work on both, you are in a better position there.

---

## Phase 1 — NLP Intensive (13–17 June)

**Priority: Highest. Exam is first, on 20 June.**

From your NLP quiz session, you covered these topics correctly and understand them:
- Preprocessing pipeline order
- Language model definition (conditional probability / chain rule)
- Word embedding taxonomy (frequency-based vs. learned)
- Distributional Hypothesis
- N-gram trade-offs and Markov assumption
- GloVe vs. Word2Vec distinction
- Statistical machine translation (noisy channel / argmax formulation)
- VAD affective model, dense vector properties

**What to focus on for the exam (gaps and extension topics):**

| Topic Area | Focus |
|------------|-------|
| Transformer architecture | Attention mechanism, self-attention, positional encoding — likely to appear at mid-sem depth |
| BERT / GPT distinctions | Encoder-only vs. decoder-only, masked LM vs. causal LM |
| Fine-tuning vs. feature extraction | When to use each, task-specific embeddings |
| Named Entity Recognition / POS tagging | Sequence labeling framing |
| Evaluation metrics | BLEU (MT), perplexity (LM), F1 (classification tasks) |
| Seq2Seq and attention | Encoder-decoder with attention vs. vanilla Seq2Seq |

**Daily plan:**

- **Day 1 (13 Jun):** Revisit preprocessing, LM, N-grams. Consolidate what you already know. Quick self-test.
- **Day 2 (14 Jun):** Word embeddings deep dive — Word2Vec training objective (CBOW vs. Skip-gram), GloVe objective function details, contextual embeddings (ELMo conceptually).
- **Day 3 (15 Jun):** Transformer — attention mechanism, multi-head attention, BERT vs. GPT. This is the most likely mid-sem stretch topic.
- **Day 4 (16 Jun):** Evaluation metrics. Practice past questions. Identify any remaining weak spots.
- **Day 5 (17 Jun):** Full mock revision. Work through any question sets available for NLP. Rest by evening.

---

## Phase 2 — Deep RL Intensive (15–19 June)

**Priority: High. Exam is 21 June, the morning after NLP.**

From your Deep RL quiz session, you demonstrated solid understanding of:
- Discount rate validity (γ = 1 in episodic tasks)
- Bellman Optimality Equation (recursive definition)
- MDP formulation

**What to extend and consolidate:**

| Topic Area | Focus |
|------------|-------|
| MDP components | State space, action space, transition function, reward function, policy |
| Value functions | V(s), Q(s,a), advantage function A(s,a) |
| Dynamic programming | Value Iteration, Policy Iteration — convergence conditions |
| Model-free methods | Monte Carlo, TD(0), TD(λ), SARSA vs. Q-learning (on-policy vs. off-policy) |
| Deep Q-Network (DQN) | Experience replay, target network, ε-greedy exploration |
| Policy gradient methods | REINFORCE, Actor-Critic, A3C/A2C — why policy gradients over value methods |
| Exploration vs. exploitation | ε-greedy, UCB, Thompson sampling |
| Convergence and stability | Deadly triad in Deep RL |

**Daily plan:**

- **Day 3 (15 Jun, shared with NLP morning):** MDP formulation and value functions — evening slot dedicated to RL.
- **Day 4 (16 Jun, evening):** Dynamic programming methods. Value Iteration vs. Policy Iteration clearly differentiated.
- **Day 5 (17 Jun, evening):** TD methods — SARSA vs. Q-Learning distinction is a common exam question.
- **Day 6 (18 Jun):** DQN architecture. Policy gradient methods. Actor-Critic framing.
- **Day 7 (19 Jun):** Full RL mock revision. Focus on Bellman equations under different algorithms. Rest early — NLP exam is next morning.

---

## Phase 3 — SEML Consolidation (22–26 June)

**Priority: Medium-high. Makeup exam, more time available.**

From your SEML quiz work (all 20 questions covered), your confirmed error was **Question 2** — RAG selected instead of Feature Store for training-serving skew. All other answers were correct.

**Focus areas for exam depth (not just quiz recall):**

| Topic Area | Focus |
|------------|-------|
| Feature Store pattern | Architecture, purpose, how it eliminates training-serving skew specifically |
| GR4ML framework | Analytics Design View, SoftGoals, HardGoals, Tasks — be able to apply, not just recall |
| MLOps pipeline stages | Data ingestion → feature engineering → training → evaluation → deployment → monitoring |
| Deployment strategies | Real-time vs. batch vs. edge — trade-offs, use cases |
| IEEE architecture definition | Be able to quote and apply the definition |
| Data drift types | Covariate drift vs. concept drift — detection and mitigation strategies |
| ML complexity variables | Data, Model, Code — how each contributes to engineering complexity |
| SMART requirements | Applied to ML systems specifically |
| Responsible ML | Post-hoc explainability, SHAP, fairness concepts |

**Daily plan:**

- **Day 9 (22 Jun):** Feature Store deep dive — correct the one confirmed gap. Review RAG vs. Feature Store boundary clearly.
- **Day 10 (23 Jun):** GR4ML framework, MLOps pipeline. Practice applying to scenario questions.
- **Day 11 (24 Jun):** Deployment strategies, drift types, monitoring approaches.
- **Day 12 (25 Jun):** Responsible ML, SMART requirements, IEEE definition. Full SEML mock revision.
- **Day 13 (26 Jun):** Light review only. Rest.

---

## Phase 4 — ACI Consolidation (22–27 June, parallel with SEML)

**Priority: Medium. Your AI/ML course mock exam showed strong breadth.**

From your ACI mock exam session, you covered and understood: heuristic search (A*, admissibility, consistency), game trees (minimax, horizon effect), genetic algorithms (selection, elitism, NEAT, No Free Lunch), ACO, NAS/DARTS, CSP/AC-3, and agent architectures.

**Your two confirmed errors to fix:**
1. Steady-state GA — not "entire population replaced every generation" (that is generational GA). Steady-state replaces only a few individuals incrementally.
2. Diversity-maximizing replacement — crowding methods, not generational replacement.

**Additional depth topics for mid-semester:**

| Topic Area | Focus |
|------------|-------|
| Genetic algorithms | Steady-state vs. generational — crystal clear distinction |
| Crowding and niching | Fitness sharing, crowding distance, deterministic crowding |
| NEAT specifics | Speciation mechanism, historical markings, why it solves the permutation problem |
| Multi-agent systems | Coordination, communication, emergent behavior |
| Constraint propagation | AC-3 complexity, forward checking vs. arc consistency |
| Local search | Hill climbing variants, simulated annealing, beam search |
| Utility-based agents | Expected utility maximization, decision theory connection |

**Daily plan (parallel with SEML, evening slots):**

- **22 Jun (evening):** Correct the two GA/crowding errors. Full re-review of evolutionary algorithms.
- **23 Jun (evening):** Search algorithms — local search, constraint propagation.
- **24 Jun (evening):** Agent architectures — utility-based and learning agents in depth.
- **25 Jun (evening):** NEAT, ACO, NAS — advanced topics review.
- **26 Jun (evening):** ACI mock pass — full question set.
- **27 Jun (after SEML exam):** Light ACI review only. Rest.

---

## Recommended Daily Time Budget

Given you are working full-time as Lead Architect alongside this program, a realistic allocation:

| Time Slot | Activity |
|-----------|----------|
| 06:00–07:30 AM | Primary study (high-focus slot before work) |
| 07:00–09:00 PM | Secondary study / problem solving |
| Weekends | Extended 3–4 hour revision blocks |

---

## Preparation Strategy — What Works Based on Your Pattern

From all our sessions, you consistently perform best when you:

1. **Work through actual questions, not just notes** — Submit questions here and we evaluate them together with full reasoning for all options.
2. **Use comparative tables** — You retain information better when correct vs. incorrect options are laid out side by side.
3. **Cross-reference related concepts** — E.g., connecting crowding in GAs to diversity maintenance as a principle that also appears in multi-objective optimization.

For each subject, I recommend dedicating at least two sessions to question practice — one mid-phase to identify gaps, one at the end as a full mock.

---

## Immediate Next Step

Given today is 13 June and NLP is first on 20 June, I'd suggest we start a focused NLP revision session today or tomorrow — working through topic areas systematically, with any question sets you have from your course material.

Do you have access to past papers or question banks for any of these four subjects? If yes, share them and we can run structured mock sessions for each.