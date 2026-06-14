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

This is extremely helpful context. The lecturer has essentially given you the full syllabus scope for the ACI mid-semester exam. Let me break this down comprehensively.

---

# ACI Mid-Semester (EC2) Exam — Complete Preparation Guide

## Exam Parameters

| Parameter | Detail |
|-----------|--------|
| Scope | CS1 to CS8 |
| Duration | 2 hours (+15 minutes extra time mentioned) |
| Marks | 30 marks |
| Type | **Subjective** — written, not MCQ |
| Mode | Online in Exam Centre |

> **Critical insight:** Subjective format means you need to be able to *write and draw* solutions — game trees, agent diagrams, algorithm traces — not just recognize correct options. This changes preparation strategy significantly.

---

## Full Syllabus Scope (from Lecturer's Walkthrough)

### 1. Agent Theory and Representations

**What to prepare:**
- PEAS specification (Performance, Environment, Actuators, Sensors)
- Environment specification — properties: fully/partially observable, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous, single/multi-agent
- Problem-solving agents — how an agent is formally represented
- Types of agents: Simple Reflex → Model-Based → Goal-Based → Utility-Based → Learning Agent

**The sample problem directly tests this.** The sliding-tile game is a 2-player adversarial environment. You should be able to write:

*PEAS for the sliding-tile game:*
- **Performance:** Win (3 similar tiles adjacent), opponent does not win
- **Environment:** The board state (3A tiles, 3B tiles, 2 empty spaces)
- **Actuators:** Move tile into empty space (Move #1), hop over one tile (Move #2)
- **Sensors:** Current board configuration

*Environment properties:*
- Fully observable (entire board visible)
- Deterministic (moves have fixed outcomes)
- Sequential (prior moves affect future states)
- Static (board doesn't change between turns)
- Discrete (finite tile positions)
- Multi-agent (2 players, competitive)

---

### 2. Informed Search

**What to prepare:**
- A* search — f(n) = g(n) + h(n), admissibility, consistency
- Greedy Best-First Search (GBFS) — h(n) only, not optimal
- Concepts: heuristic admissibility, consistency (triangle inequality), dominance
- Pattern databases and relaxed constraints as heuristic construction methods

**Key exam-ready distinctions:**

| Property | GBFS | A* |
|----------|------|-----|
| Evaluation function | h(n) | g(n) + h(n) |
| Optimal? | No | Yes (admissible h) |
| Complete? | No (can loop) | Yes (with consistent h) |
| Speed | Faster | Slower but guaranteed |

**Relaxed constraints** — if you remove a constraint from the problem, the optimal solution cost of the relaxed problem is an admissible heuristic for the original. Example: 8-puzzle Manhattan distance ignores tile blocking.

---

### 3. Local Search

**What to prepare:**
- Hill Climbing — steepest ascent, first-choice, random restart
- Problems with Hill Climbing: local maxima, plateaus, ridges
- Simulated Annealing — escape local maxima via probabilistic acceptance
- Beam Search — keep k states, not just one

**Subjective exam likely asks:** Trace Hill Climbing on a given state space, identify where it gets stuck, explain why.

---

### 4. Evolutionary Algorithms and Nature-Inspired Search

**What to prepare (lecturer explicitly listed all of these):**

#### Genetic Algorithms
- Representation (chromosome encoding)
- Selection (tournament, roulette wheel, rank)
- Crossover (single-point, multi-point, uniform)
- Mutation
- **Generational vs. Steady-State GA** — your previously identified error area
- Fitness scaling, elitism
- **Crowding and niching** — your second error area — diversity preservation

#### Ant Colony Optimization (ACO)
- Pheromone update rule
- Evaporation coefficient role
- Positive feedback loop mechanism
- Application to TSP-style problems

#### NES (NeuroEvolution of Augmenting Topologies) — lecturer specifically named NEAT
- Why standard GA fails for neural networks (permutation problem / competing conventions)
- NEAT solution: historical markings, speciation
- Deep NEAT / CoDeep NEAT extensions
- Connection to NAS (Neural Architecture Search)

---

### 5. Adversarial Search / Game Playing

**What to prepare — and the sample problem tests this directly:**

#### Minimax Algorithm
- MAX player maximizes, MIN player minimizes
- Terminal state evaluation
- Recursive tree expansion
- **The sample problem requires you to expand 3 levels and compute utilities**

#### The Sample Problem — Worked Approach

**Board state (initial):**
```
[  ] [A ] [B ] [B ]
     [A ] [  ] [A ]
               [B ]
```

**Utility function:**
`Utility = [3×(MAX_win_chance − MIN_win_chance)] + [2×(MAX_adjacent_pairs − MIN_adjacent_pairs)]`

Where:
- **Win chance** = number of that player's tiles adjacent to an empty cell (from the note: initial state has 3 A-tiles adjacent to empty → MAX win chance = 3; 1 B-tile adjacent to empty → MIN win chance = 1)
- **Adjacent pairs** = number of same-player tiles in same row or column adjacent to each other

**To solve this in the exam:**
1. Draw the initial state clearly
2. Enumerate all legal moves from each state (Move #1: slide into adjacent empty; Move #2: hop over one tile in same row)
3. Expand the tree to exactly 3 levels (MAX moves at level 1, MIN at level 2, MAX at level 3)
4. At each leaf (level 3), calculate the utility using the formula
5. Back-propagate: MIN nodes take minimum of children, MAX nodes take maximum
6. The root MAX node selects the move with the highest backed-up value

**Alpha-Beta Pruning** — know how to apply it to prune branches that cannot affect the final decision

#### Monte Carlo Tree Search (MCTS)
- Four phases: Selection, Expansion, Simulation, Backpropagation
- UCB1 formula for node selection
- When it is preferred over Minimax (very large branching factor)

---

## Preparation Strategy for Subjective Format

This is the critical shift from your quiz preparation. Subjective questions will ask you to:

1. **Draw and label** — game trees, agent architecture diagrams, search trees
2. **Trace algorithms** — show step-by-step execution of Minimax, A*, Hill Climbing, GA crossover
3. **Write specifications** — PEAS, environment properties, agent type justification
4. **Calculate** — utility values, heuristic values, fitness scores

**Practice approach for each topic:**

| Topic | Practice Task |
|-------|---------------|
| Agent types | Given a scenario, identify agent type and justify with diagram |
| PEAS | Write full PEAS for 2–3 different problem domains |
| A* | Trace on a small graph with given heuristics, show f/g/h at each node |
| Hill Climbing | Draw a state space, trace the algorithm, identify local maxima |
| GA | Show one complete generation — selection, crossover, mutation on sample chromosomes |
| ACO | Explain pheromone update with formula, trace one ant |
| NEAT | Draw before/after speciation, explain historical markings with example |
| Minimax | Solve the sample problem fully — this is likely the 10–15 mark anchor question |
| Alpha-Beta | Apply pruning to a given game tree, mark pruned branches |

---

## Recommended Study Sequence (Remaining Days)

Given ACI is on **28 June** and SEML is on 27 June:

| Date | Focus |
|------|-------|
| 22 Jun | Agent theory, PEAS, environment specifications |
| 23 Jun | Informed search (A*, GBFS), local search (Hill Climbing) |
| 24 Jun | Genetic Algorithms — fix the two confirmed errors, crowding/niching in depth |
| 25 Jun | ACO, NEAT, NAS |
| 26 Jun | Adversarial search — solve the sample problem fully, Alpha-Beta, MCTS |
| 27 Jun | SEML exam morning → ACI light review evening only |
| 28 Jun | ACI exam |

---

## Immediate Recommended Action

Work through the sample problem completely right now — expand all 3 levels of the game tree, compute utilities at leaves, back-propagate, and identify MAX's best move. This will likely be the largest question in the actual exam (estimate 10–15 marks of the 30).

Do you want to work through the sample problem together step by step? If you share the board layout more clearly (the image grid is slightly ambiguous on exact positions), we can produce the full game tree with all utility calculations.

This is very valuable context. Let me extract the critical exam intelligence from what the lecturer said and map it to your preparation.

---

# ACI Exam — Critical Intelligence Update

## What the Lecturer Just Told You

| Point | Implication |
|-------|-------------|
| Questions from **all big picture topics** (not every small detail) | Cover all 6 branches from the mind map — none can be skipped |
| **Closed book** — no formula sheet provided | Memorize key formulas, but logic-based understanding is primary |
| **Type paper** — designed to take 1h15m to 1h55m if prepared | Speed is the constraint, not knowledge alone |
| Working professionals specifically warned about **slow solving speed** | You must practice solving, not just reading |
| Every week's slide had **sample problems** you likely haven't solved | These are your primary practice material |
| A **full fledged sample paper** will be uploaded today | This becomes your most important resource immediately |

---

## The ACI Mind Map — Full Syllabus Confirmed

From Image 1, the lecturer drew this explicitly:

```
                    ACI
                   / | \ \ \ \
         CS1      CS2    Search   Local Search   NAS(GA)    Advanced(Game)
       Basics    PEAS   Informed   Hill Climb    NEAT        Minimax
               Environ  A* GBFS   GA  ACO      DeepCONEAT  Alpha-Beta
                PSA               Pattern,Relaxed           (Alpha-Beta LR?)
```

Mapped cleanly:

| Branch | Topics |
|--------|--------|
| CS1 — Basics | AI fundamentals, agent definitions, rationality |
| CS2 — PEAS, Environment, PSA | PEAS spec, environment properties, Problem-Solving Agent formulation |
| Search — Informed | A*, GBFS, heuristics, admissibility, consistency, pattern databases, relaxed constraints |
| Local Search | Hill Climbing, GA, ACO |
| NAS (GA branch) | NEAT, Deep NEAT, CoDeep NEAT, NAS as GA application |
| Advanced — Game Playing | Minimax, Alpha-Beta pruning |

---

## The Two Practice Problems You Need to Solve Now

### Problem 1 — The Sliding Tile Minimax Problem (Image 2)

This is the sample problem. Based on the lecturer's emphasis, a question of this type **will appear in the exam**. You need to be able to solve it completely within ~20–25 minutes.

**Initial Board State:**

```
[ ]  [ ]           ← Row 0: two empty spaces (gray tiles)
[A]  [B]  [B]      ← Row 1
     [A]  [ ]  [A] ← Row 2
               [B] ← Row 3
```

Wait — let me re-read the image carefully. The board shown is:

```
[  ] ← top-left empty (gray)
[A ] [B ] [B ]     ← middle row
     [A ] [  ] [A] ← lower row (gray = empty)
               [B ] ← bottom
```

**The structure appears to be an irregular grid.** For the exam, the key is understanding the move rules and utility function regardless of exact layout.

**Utility Formula:**
```
U = [3 × (MAX_win_chance − MIN_win_chance)] + [2 × (MAX_adj_pairs − MIN_adj_pairs)]
```

Where:
- **Win chance** = number of that player's tiles adjacent to ANY empty cell
- **Adjacent pairs** = number of same-player tile pairs in same row or column, adjacent to each other

**Initial state values (given in problem):**
- MAX (A) win chance = 3 (three A tiles adjacent to empty)
- MIN (B) win chance = 1 (one B tile adjacent to empty)

**Legal moves:**
- Move #1: Slide tile into directly adjacent empty space
- Move #2: Hop over exactly one tile in the same row into empty space

---

### Problem 2 — Alpha-Beta Pruning Exercise (Image 3)

This is Exercise 1 from your slides. The tree structure is:

```
Level 0 (MAX):  ROOT [□]
Level 1 (MIN):  ○         ○
Level 2 (MAX):  □    □    □    □
Level 3 (MIN):  ○ ○  ○ ○  ○ ○  ○ ○
Leaves:    8 7  3 15  9 8  -10 5  1 4  8 9  9 9  12 -3
```

**Alpha-Beta definitions (from your slide):**
- **Alpha** = lower bound of Maximizer's value (best MAX can guarantee so far)
- **Beta** = upper bound of Minimizer's value (best MIN can guarantee so far)
- **Prune** when α ≥ β

**Let me work this through completely for you.**

**Step 1 — Compute Level 3 MIN nodes** (each MIN node takes minimum of its two children):

| MIN Node | Children | Value |
|----------|----------|-------|
| L3-1 | 8, 7 | **7** |
| L3-2 | 3, 15 | **3** |
| L3-3 | 9, 8 | **8** |
| L3-4 | -10, 5 | **-10** |
| L3-5 | 1, 4 | **1** |
| L3-6 | 8, 9 | **8** |
| L3-7 | 9, 9 | **9** |
| L3-8 | 12, -3 | **-3** |

**Step 2 — Compute Level 2 MAX nodes** (each MAX node takes maximum of its two MIN children):

| MAX Node | Children | Value |
|----------|----------|-------|
| L2-1 | 7, 3 | **7** |
| L2-2 | 8, -10 | **8** |
| L2-3 | 1, 8 | **8** |
| L2-4 | 9, -3 | **9** |

**Step 3 — Compute Level 1 MIN nodes:**

| MIN Node | Children | Value |
|----------|----------|-------|
| L1-1 | 7, 8 | **7** |
| L1-2 | 8, 9 | **8** |

**Step 4 — Root MAX node:**
- Children: 7, 8 → **Root = 8** → MAX chooses right branch

**Minimax value = 8**

**Now apply Alpha-Beta pruning** to identify which nodes get pruned:

Working left to right, tracking α (MAX's best) and β (MIN's best):

- Visit L3-1 (8), L3-1's second child (7) → L3 MIN node = 7. Root's left MIN child now has candidate = 7. β = 7.
- Visit L2-1's second subtree. α starts at -∞. First child of L3-2 = 3. Since 3 < β=7, continue. Second child = 15. L3-2 MIN = 3. L2-1 MAX = max(7,3) = 7.
- Left L1 MIN node: seen L2-1 = 7, so β = 7 for this MIN node.
- Visit L2-2. First child L3-3: values 9,8 → MIN=8. L2-2 MAX candidate = 8. Since 8 ≥ β=7 → **PRUNE L3-4** (the -10, 5 node is pruned — no need to evaluate second child of L2-2).
- Left L1 MIN = min(7, 8) = 7. Root α = 7.
- Visit right L1 MIN node. β = +∞ initially, α = 7.
- L2-3: L3-5 = min(1,4) = 1. L2-3 MAX candidate = 1. Since 1 < α=7 → **PRUNE** — but wait, need to check L3-6 first. L3-6 = min(8,9) = 8. L2-3 MAX = max(1,8) = 8. Since 8 ≥ α=7 and we're in MIN context with β=+∞, no pruning yet.
- Right L1 MIN: candidate = 8, β = 8.
- L2-4: L3-7 = min(9,9) = 9. L2-4 candidate = 9. Since 9 ≥ β=8 → **PRUNE L3-8** (the 12, -3 node — no need to evaluate).
- Right L1 MIN = min(8, 9) = 8.
- Root MAX = max(7, 8) = **8** ✓

**Pruned nodes: L3-4 (-10, 5) and L3-8 (12, -3)**

---

## Key Formulas to Memorize (Closed Book)

The lecturer said "not many formulas but wherever applicable you must know them." Here are the ones that matter:

| Formula | What it is |
|---------|------------|
| `f(n) = g(n) + h(n)` | A* evaluation function |
| `h(n) ≤ h*(n)` | Admissibility condition |
| `h(n) ≤ c(n,n') + h(n')` | Consistency condition |
| `U = [3×(MAX_wc − MIN_wc)] + [2×(MAX_ap − MIN_ap)]` | This exam's utility function |
| Prune when `α ≥ β` | Alpha-Beta condition |
| Pheromone update: `τ_ij = (1−ρ)τ_ij + Δτ_ij` | ACO pheromone rule |
| NEAT fitness sharing: `f'_i = f_i / Σ sh(d_ij)` | Speciation in NEAT |

---

## Your Action Plan for Today

1. **Check the course portal immediately** — the full sample paper is being uploaded today. That is your single most important resource.

2. **Solve the Alpha-Beta tree above yourself** from scratch on paper — time yourself. It should take under 10 minutes once you know the method.

3. **Attempt the sliding tile problem** — draw the board, enumerate all legal moves from the initial state, build level 1 of the tree. Share it here and we will complete levels 2 and 3 together.

4. **Go through every slide's end-of-class exercise** — the lecturer said these were given every week and most students haven't solved them. Those are likely the exam questions.

Do you want to work through the sliding tile game tree now, or do you want to wait until the sample paper is available and work through that instead?

This is excellent meta-information about the paper design. Let me extract the actionable exam strategy from this.

---

# ACI Exam Strategy — Bloom's Taxonomy Mapping

## Paper Design Intelligence

| Parameter | Detail |
|-----------|--------|
| Question count | 6–10 questions (mix of small, medium, one big) |
| Balance | Theory + Practical + Numerical + Formula + Code |
| Difficulty spread | Easy (recall) → Applied (class problems) → Stretch (boundary-pushing) |
| Framework | Bloom's Taxonomy |
| Sets | Different question sets possible within same exam type |
| Weight context | Midterm is lower weight than Quiz 2 and Final — don't over-stress |

---

## Bloom's Taxonomy Applied to ACI

The lecturer explicitly said he follows this. Here is what each level means for your preparation:

| Bloom's Level | What It Means | ACI Example |
|---------------|---------------|-------------|
| **Remember** | Define, list, name | Define admissible heuristic. What is PEAS? Name 5 agent types. |
| **Understand** | Explain, describe, classify | Explain why γ=1 requires episodic tasks. Describe ACO pheromone dynamics. |
| **Apply** | Solve, trace, compute | Trace A* on a graph. Compute utility for a game state. Apply GA crossover. |
| **Analyse** | Compare, differentiate, examine | Compare Minimax vs Alpha-Beta. Steady-state vs Generational GA. |
| **Evaluate** | Justify, critique, assess | Why is crowding better than generational replacement for diversity? |
| **Create** | Design, construct, formulate | Write PEAS for a new domain. Design a fitness function for a given problem. |

> The lecturer said "easy questions everybody will know" = Remember/Understand levels. "Applied" = Apply/Analyse. "Push your boundaries" = Evaluate/Create.

---

## Balanced Paper — What to Prepare Per Category

### Theory Questions (Remember + Understand)
These are the "everybody must get these" questions. Do not drop marks here.

**Must-know definitions (write these from memory right now as a test):**
- Admissible heuristic
- Consistent heuristic
- PEAS acronym and what each component means
- Environment properties (all 6 pairs)
- 5 agent types in order of complexity
- MDP components
- What NAS stands for and its connection to GA
- Speciation in NEAT and why it exists

### Practical / Trace Questions (Apply)
These consume the most time. Speed is your risk here per the lecturer's warning.

**Practice these until fast:**
- Trace Minimax on a 3-level tree with utility calculation
- Apply Alpha-Beta and mark pruned nodes
- Trace A* on a small graph (show f/g/h at every node)
- One step of Hill Climbing — identify current state, neighbors, move decision
- One generation of GA — selection, crossover, mutation on sample chromosomes

### Numerical Questions (Apply + Analyse)
- Compute utility values using the given formula (sample problem)
- Calculate heuristic values using Manhattan distance or misplaced tiles
- ACO pheromone update calculation

### Formula Questions (Remember + Apply)
Closed book — these must be memorized:

```
A*:           f(n) = g(n) + h(n)
Admissible:   h(n) ≤ h*(n)
Consistent:   h(n) ≤ c(n,n') + h(n')
Alpha-Beta:   Prune when α ≥ β
ACO:          τ_ij ← (1−ρ)·τ_ij + Δτ_ij
ACI Utility:  U = [3(MAX_wc − MIN_wc)] + [2(MAX_ap − MIN_ap)]
```

### Code Questions (Apply + Create)
The lecturer said "code" is part of the balance. Based on ACI course context, this likely means:

- Pseudocode for Minimax (with and without Alpha-Beta)
- Pseudocode for A* or Hill Climbing
- Pseudocode for a basic GA loop (initialize → evaluate → select → crossover → mutate → repeat)

**Key point:** You do not need to write Python/Java. Pseudocode that demonstrates the algorithm logic is sufficient for a subjective exam of this type.

---

## "Stretch" Questions — What Might Push Your Boundaries

Based on the syllabus and Bloom's higher levels, these are the likely candidates:

1. **Design a PEAS for an unusual domain** — not a textbook example like chess or vacuum cleaner. Something like "an AI system that recommends crop irrigation schedules" — you need to construct PEAS from scratch.

2. **Heuristic design** — given a problem, propose an admissible heuristic and prove it is admissible. The relaxed constraints method is the tool here.

3. **NEAT speciation scenario** — given two neural networks with different topologies, explain how NEAT's historical markings would handle crossover and whether they would be placed in the same species.

4. **Compare two approaches** — e.g., "When would you prefer MCTS over Minimax? Justify with an example."

5. **Failure analysis** — "Hill Climbing fails to find the global optimum in the following state space. Identify the problem and propose which algorithm would handle it better."

---

## Speed Optimization — The Lecturer's Core Warning

He said explicitly: if you have not been solving the weekly exercises, your solving speed has degraded. For a 2-hour paper with 6–10 questions, you have roughly **12–20 minutes per question**.

**Time benchmarks to hit in practice:**

| Task | Target Time |
|------|-------------|
| Write full PEAS for a domain | 3–4 minutes |
| Draw and label 5 agent types with diagram | 5 minutes |
| Trace A* on a 6-node graph | 8–10 minutes |
| Solve a 3-level Minimax tree | 10–15 minutes |
| Apply Alpha-Beta to the Exercise 1 tree | 8–10 minutes |
| One GA generation trace | 6–8 minutes |
| Write GA pseudocode | 5–6 minutes |

If any of these are taking you significantly longer, that topic needs timed practice before the exam.

---

## Immediate Action — Before the Sample Paper Arrives

Do this right now, from memory, without looking anything up. Time yourself.

**Exercise:** Write the PEAS specification and environment properties for the sliding-tile game from the sample problem.

Then share it here. I will evaluate it exactly as an examiner would — correct, complete, and appropriately detailed for a 30-mark subjective paper.

Once the full sample paper is uploaded to your course portal, share it here immediately and we will work through every question together with full worked solutions.


This confirms exactly what I outlined. Let me give you a clean, consolidated reference for the algorithm/pseudocode component since that is now confirmed as in-scope.

---

# ACI Exam — Pseudocode & Algorithm Reference

## What Is Confirmed In-Scope for "Code" Questions

- **Pseudocode** for algorithms — not Python, not Java
- **Comment on** algorithm behavior — explain what a step does, why it is there
- **Write or complete** an algorithm from understanding, not memorization

---

## Core Pseudocode You Must Know

### 1. A* Search

```
function A_STAR(start, goal):
    open_list = priority queue ordered by f(n) = g(n) + h(n)
    closed_list = empty set
    
    add start to open_list with f = h(start), g = 0
    
    while open_list is not empty:
        n = node with lowest f(n) from open_list
        
        if n == goal:
            return reconstruct_path(n)
        
        move n from open_list to closed_list
        
        for each neighbor m of n:
            if m in closed_list:
                continue
            
            tentative_g = g(n) + cost(n, m)
            
            if m not in open_list OR tentative_g < g(m):
                g(m) = tentative_g
                f(m) = g(m) + h(m)
                parent(m) = n
                add m to open_list
    
    return FAILURE
```

**What an examiner might ask you to comment on:**
- Why is the priority ordered by f(n) and not just h(n)? → Because g(n) accounts for actual cost so far, preventing A* from ignoring expensive paths
- What is the role of the closed list? → Prevents re-expanding already-optimal nodes
- What guarantee does admissibility of h(n) provide? → A* will never overestimate, so the first time goal is reached it is via optimal path

---

### 2. Minimax

```
function MINIMAX(node, depth, is_maximizing):
    if depth == 0 OR node is terminal:
        return utility(node)
    
    if is_maximizing:
        best = -infinity
        for each child of node:
            value = MINIMAX(child, depth-1, FALSE)
            best = max(best, value)
        return best
    
    else:  // minimizing
        best = +infinity
        for each child of node:
            value = MINIMAX(child, depth-1, TRUE)
            best = min(best, value)
        return best

// Call: MINIMAX(root, max_depth, TRUE)
```

---

### 3. Alpha-Beta Pruning

```
function ALPHA_BETA(node, depth, alpha, beta, is_maximizing):
    if depth == 0 OR node is terminal:
        return utility(node)
    
    if is_maximizing:
        value = -infinity
        for each child of node:
            value = max(value, ALPHA_BETA(child, depth-1, alpha, beta, FALSE))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  // Beta cutoff — MIN would never allow this
        return value
    
    else:
        value = +infinity
        for each child of node:
            value = min(value, ALPHA_BETA(child, depth-1, alpha, beta, TRUE))
            beta = min(beta, value)
            if alpha >= beta:
                break  // Alpha cutoff — MAX already has better option
        return value

// Call: ALPHA_BETA(root, max_depth, -inf, +inf, TRUE)
```

**Key comment points:**
- `alpha` tracks MAX's best guaranteed value so far
- `beta` tracks MIN's best guaranteed value so far
- Prune when `alpha >= beta` — the current branch cannot affect the final decision
- Does NOT change the final Minimax value — only skips redundant computation

---

### 4. Hill Climbing

```
function HILL_CLIMBING(problem):
    current = initial_state(problem)
    
    while TRUE:
        neighbors = generate_neighbors(current)
        best_neighbor = neighbor with highest value in neighbors
        
        if value(best_neighbor) <= value(current):
            return current  // Local maximum reached — stop
        
        current = best_neighbor
```

**What to know about its failures:**
- Returns local maximum, not guaranteed global maximum
- Gets stuck on plateaus (all neighbors equal value)
- Gets stuck on ridges (gradient direction does not align with move operators)

**Fix:** Random restart Hill Climbing — run multiple times from random starts, return best result overall

---

### 5. Genetic Algorithm

```
function GENETIC_ALGORITHM(population, fitness_fn):
    
    // Evaluate initial population
    for each individual in population:
        fitness[individual] = fitness_fn(individual)
    
    while termination condition not met:
        new_population = empty
        
        while len(new_population) < len(population):
            // Selection
            parent1 = SELECT(population, fitness)
            parent2 = SELECT(population, fitness)
            
            // Crossover
            child1, child2 = CROSSOVER(parent1, parent2)
            
            // Mutation
            child1 = MUTATE(child1, mutation_rate)
            child2 = MUTATE(child2, mutation_rate)
            
            // Evaluate
            fitness[child1] = fitness_fn(child1)
            fitness[child2] = fitness_fn(child2)
            
            add child1, child2 to new_population
        
        population = new_population  // Generational replacement
    
    return best individual in population by fitness
```

**Steady-State variant — change only the replacement step:**
```
    // Replace only worst individual(s), not entire population
    worst = individual with lowest fitness in population
    replace worst with best child
```

---

### 6. ACO (Ant Colony Optimization) — One Iteration

```
function ACO_ITERATION(graph, ants, pheromone, alpha, beta, rho):
    
    solutions = empty
    
    for each ant k in ants:
        path = construct_solution(graph, pheromone, alpha, beta)
        solutions.add(path)
    
    // Evaporate pheromone on all edges
    for each edge (i,j) in graph:
        pheromone[i][j] = (1 - rho) * pheromone[i][j]
    
    // Deposit pheromone based on solution quality
    for each ant k with path P_k:
        for each edge (i,j) in P_k:
            pheromone[i][j] += 1 / cost(P_k)
    
    return best solution found

// Key formula: τ_ij ← (1 − ρ) · τ_ij + Δτ_ij
// where ρ = evaporation rate, Δτ_ij = quality of solutions using edge (i,j)
```

---

## "Comment On" Style Questions — What to Expect

The lecturer said you might be asked to **comment on** parts of an algorithm. Practice this pattern:

**Example question format:**
> *The following pseudocode has a bug / missing step / inefficiency. Identify and explain.*

Or:

> *Line 7 of the following Minimax pseudocode reads `best = max(best, value)`. What would happen if this was changed to `best = min(best, value)` at the MAX level?*

Answer pattern: State what the line does → State what the change breaks → State the consequence on output.

---

## Quick Reference — Algorithm Comparison Table

| Algorithm | Complete? | Optimal? | Uses Heuristic? | Key Weakness |
|-----------|-----------|----------|-----------------|--------------|
| A* | Yes | Yes (admissible h) | Yes | Memory — stores all nodes |
| GBFS | No | No | Yes | Can loop, ignores path cost |
| Hill Climbing | No | No | No | Local maxima, plateaus |
| Minimax | Yes | Yes | No (uses utility) | Exponential tree size |
| Alpha-Beta | Yes | Yes | No | Same as Minimax but faster |
| GA | No | No | No (uses fitness) | Premature convergence |
| ACO | No | No | Indirect (pheromone) | Slow convergence |

---

## What to Do Right Now

The sample paper is being released today. The moment it is available on your portal, share it here. We will:

1. Categorize each question by Bloom's level
2. Identify which are the guaranteed-marks questions
3. Work through every numerical and trace question with full solutions
4. Time each solution to build your exam pace

That sample paper is your single most valuable resource between now and 28 June.


Key additional intelligence extracted. Short but important.

---

# Marking Scheme Intelligence

## How Marks Are Awarded

| Question Type | Marking Style | Implication |
|---------------|---------------|-------------|
| Numerical / Trace questions | **Step marking** — lose marks per wrong step | Show ALL working even if unsure of final answer |
| Concept / Definition questions | **Zero or one** — all or nothing | Be precise; partial answers score zero |
| Algorithm trace (e.g., Minimax) | Step marking | Each level of tree backed up correctly = marks, even if earlier error |

## Critical Exam Technique from This

**For step-marked questions (numerical, trace, algorithm):**
- Never leave blank — write every step you know
- If you make an error in step 2, you can still score steps 3, 4, 5 independently
- Label each step clearly so the examiner can award partial credit
- For game trees: even if utility calculation is wrong, correct back-propagation from those values still earns marks

**For zero-or-one questions (definitions, classifications):**
- Do not hedge or be vague — commit to a precise answer
- One wrong word in a definition can cost the full mark
- These are the "easy" questions the lecturer mentioned — cannot afford to lose these

---

## Additional Resource Confirmed — Webinar 2

The lecturer confirmed **Webinar 2 solved past exam problems**. This is your second most important resource after the sample paper.

**Action:** Access Webinar 2 recording from your course portal immediately. The past exam problems solved there are likely representative of what appears on 28 June.

---

## Regular vs Makeup — Confirmed Ambiguous

The lecturer would not confirm whether regular and makeup papers are the same or different. Treat them as potentially different — do not rely on anyone sharing questions after the regular exam on 28 June morning. Prepare for the full scope independently.

---

## Backpropagation Question from the Class

Someone asked about "backprop" in the context of this exam. The lecturer deflected — this confirms **backpropagation is NOT in scope for ACI mid-semester**. That is Deep RL / NLP territory. Do not spend time on it for this exam.

---

## Your Resource Priority List (Ranked)

| Priority | Resource | Status |
|----------|----------|--------|
| 1 | Full sample paper (being uploaded today) | Pending — check portal |
| 2 | Webinar 2 recording — past exam problems solved | Available now — watch today |
| 3 | Weekly slide end-exercises (all CS1–CS8) | Available — work through systematically |
| 4 | The Alpha-Beta Exercise 1 tree (Image 3 from earlier) | Solve from scratch, time yourself |
| 5 | The sliding tile Minimax sample problem | Full tree expansion needed |

Get Webinar 2 watched today while waiting for the sample paper to drop.


One more critical marking detail just added.

---

# Final Marking Clarification — Important Update

## Step Marking — Revised Understanding

The lecturer just clarified something that changes exam technique:

> "If you have done a wrong thing, then why would we keep on evaluating? The first mistake, we stop evaluating."

This **contradicts** the standard step-marking assumption. Here is what it actually means:

| What I Said Earlier | What the Lecturer Actually Means |
|---------------------|----------------------------------|
| "Show all working — later steps earn marks even if earlier step wrong" | **Wrong.** Evaluation stops at first error for that question |
| Partial credit for correct steps after an error | **Not guaranteed** — marking stops when error is found |

## Revised Exam Technique

This makes **accuracy more important than attempting everything.**

| Situation | What To Do |
|-----------|------------|
| Confident about a question | Attempt fully, show all steps clearly |
| Partially confident | Attempt only the steps you are certain about — do not guess mid-solution |
| Unsure of first step | **Do not bluff** — a wrong first step means zero for the rest |
| Zero-or-one question | Must be completely correct — no partial credit |

**The practical implication:** For a Minimax tree or A* trace, if you are not sure how to compute the utility correctly, do not guess the leaf values and then back-propagate. The back-propagation marks will not be awarded if the utility computation before it is wrong.

---

## Everything Else From This Segment

**Webinar location:** Same folder as all course files on the portal. Check there directly.

**Hard tickets / exam logistics:** Operations team handling — should be available within the next few days. Not the lecturer's domain.

---

## The Right Mindset Going In

The lecturer's closing advice is genuinely sound and worth internalizing:

- This is one component among many — Quiz 2 and Final carry more weight
- Learning and marks are not perfectly correlated — optimize for understanding, marks follow
- Use the exam as a forcing function to consolidate everything from CS1–CS8

The most productive thing you can do right now is pull up Webinar 2 and work through whatever past exam problems were solved there. That is your clearest signal of what the actual question style looks like.

Share the sample paper or Webinar 2 problems here the moment you have access and we will work through them completely.

this is the syllabus for midsem ACI
/Users/jayakrishnanj/mtech/semester2/exam-focused/ACI_Syllabus_MidSemester.pdf