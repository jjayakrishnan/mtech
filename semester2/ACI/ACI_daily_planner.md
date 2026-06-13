# ACI Exam — 21-Day Study Planner

**Exam Date:** 28 June 2026, 1:00 PM | **Days remaining:** ~21 days | **Study hours per day:** ~3-4 hours

---

## Week 1: Foundations & Uninformed Search

### Day 1 — Agent & Environment Basics
**Goal:** Understand problem formulation and what makes an agent rational

**Tasks:**
- [ ] Read ACI_HO.pdf Session 1 (agent, environment, PEAS)
- [ ] Review CS1.pdf page 21 (game and rationality context)
- [ ] Write short notes on:
  - Agent definition
  - Environment types (observable, deterministic, static, etc.)
  - PEAS description (Performance, Environment, Actuators, Sensors)

**Practice:**
- [ ] Describe the PEAS for one example agent (e.g., chess-playing agent, self-driving car)

**Time:** 45 min reading + 30 min notes = 1h 15 min

---

### Day 2 — Problem Solving & State Space
**Goal:** Learn to formulate problems formally for search

**Tasks:**
- [ ] Continue ACI_HO.pdf Session 1 (problem formulation)
- [ ] Review CS2.pdf early pages on problem setup
- [ ] Write short notes on:
  - Initial state
  - Goal test
  - Successor function (actions)
  - Path cost
  - Search tree vs state graph

**Practice:**
- [ ] Formulate a simple problem (e.g., 8-puzzle, water jug problem) with all four components

**Time:** 1h reading + 45 min practice = 1h 45 min

---

### Day 3 — Uninformed Search: BFS & DFS
**Goal:** Understand and compare basic search strategies

**Tasks:**
- [ ] Study BFS (Breadth-First Search)
  - How it works, queue usage
  - Complete? Optimal? Time/space complexity
- [ ] Study DFS (Depth-First Search)
  - How it works, stack/recursion usage
  - Complete? Optimal? Time/space complexity
- [ ] Write comparison table: BFS vs DFS

**Practice:**
- [ ] Draw a simple search tree and trace BFS and DFS manually
- [ ] Write pseudocode for both

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 4 — Uninformed Search: IDS & UCS
**Goal:** Learn iterative deepening and uniform cost search

**Tasks:**
- [ ] Study Iterative Deepening Search (IDS)
  - Why it combines BFS and DFS advantages
  - Time/space complexity
- [ ] Study Uniform Cost Search (UCS)
  - Priority queue / min-heap usage
  - Why optimal with positive costs
- [ ] Write comparison: IDS, BFS, DFS, UCS

**Practice:**
- [ ] Trace IDS and UCS on a simple example
- [ ] Write pseudocode for UCS

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Days 5–7 — Practice Uninformed Search
**Goal:** Solidify understanding with examples and notebook code

**Day 5:**
- [ ] Review all uninformed search notes
- [ ] Create a summary table: algorithm, data structure, complete, optimal, time, space
- [ ] Practice: small problem (8-puzzle, water jug) by hand with each algorithm

**Day 6:**
- [ ] Read Webinar 1 material if available (BFS/DFS implementation context)
- [ ] Solve 2–3 example problems from handout or slides

**Day 7:**
- [ ] Review and refine notes
- [ ] Quiz yourself: what are the pros/cons of BFS vs DFS?

**Time:** 1h per day

---

## Week 2: Informed Search & Heuristics

### Day 8 — Heuristics Fundamentals
**Goal:** Understand what makes a good heuristic

**Tasks:**
- [ ] Read ACI_HO.pdf Session 2 (heuristic functions)
- [ ] Review CS2.pdf pages 41–42 (heuristic introduction)
- [ ] Write short notes on:
  - What is a heuristic?
  - Admissible heuristic (never overestimates)
  - Consistent / monotonic heuristic
  - Relationship between admissibility and consistency

**Practice:**
- [ ] For a simple problem, propose a heuristic and check if it's admissible

**Time:** 1h 30 min reading + 45 min practice = 2h 15 min

---

### Day 9 — Greedy Best-First Search
**Goal:** Learn first greedy approach and its limitations

**Tasks:**
- [ ] Study Greedy Best-First Search
  - Uses `h(n)` only
  - Not guaranteed optimal
  - Priority queue expansion
- [ ] Review CS3.pdf pages 26–30 for context

**Practice:**
- [ ] Trace greedy best-first on a small example
- [ ] Compare with BFS/DFS: when is greedy better/worse?

**Time:** 1h reading + 1h practice = 2h

---

### Day 10 — A* Search Basics
**Goal:** Understand A* search and its formula

**Tasks:**
- [ ] Study A* Search
  - Formula: `f(n) = g(n) + h(n)`
  - `g(n)`: actual cost from start
  - `h(n)`: estimated cost to goal
  - Why `g(n) + h(n)` balances exploration and exploitation
- [ ] Understand optimality condition: admissible heuristic → optimal A*

**Practice:**
- [ ] Trace A* on a small problem
- [ ] Compare nodes expanded: greedy vs BFS vs A*

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 11 — A* Deep Dive & Lecture Slides
**Goal:** Deepen A* understanding with slides

**Tasks:**
- [ ] Review CS3.pdf pages 36–52 (detailed A* content)
- [ ] Review ACI_HO.pdf Session 2 more carefully (consistency, admissibility)
- [ ] Write extended notes on:
  - Admissible vs consistent heuristics
  - Why consistent heuristic is stronger
  - Proof sketch of A* optimality

**Practice:**
- [ ] Design an admissible heuristic for 8-puzzle or route planning
- [ ] Trace A* with different heuristics and compare

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 12 — Relaxed Problems & Pattern Databases
**Goal:** Learn how to derive good heuristics

**Tasks:**
- [ ] Study methods for constructing heuristics:
  - Relaxed problems (remove constraints)
  - Pattern databases (lookup precomputed values)
  - Learning heuristics (from data)
- [ ] Review CS4.pdf pages 2–25 (heuristic depth)

**Practice:**
- [ ] For 8-puzzle: propose a relaxed problem and compute its heuristic
- [ ] Compare heuristic strength: Manhattan distance vs relaxed problem

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 13 — A* Implementation & Notebooks
**Goal:** See A* in code

**Tasks:**
- [ ] Open and run `Webinar-1/A_star_implementation.ipynb`
- [ ] Read through the code:
  - How is the frontier (open set) managed?
  - How is `f(n)` calculated?
  - What is the closed set?
- [ ] Modify the notebook: change the heuristic and observe results

**Practice:**
- [ ] Run A* on the provided problem
- [ ] Trace execution: which nodes are expanded?

**Time:** 2h (code reading + experimentation)

---

### Day 14 — Practice & Revision
**Goal:** Consolidate Week 2 learning

**Tasks:**
- [ ] Review all heuristic and A* notes
- [ ] Create a one-page summary:
  - Greedy best-first vs A*
  - When is each better?
  - Why does A* need admissible heuristic?

**Practice:**
- [ ] Solve 2 practice problems using A* by hand
- [ ] Self-quiz: key concepts

**Time:** 1h 30 min

---

## Week 3: Local Search, Optimization & Game Playing

### Day 15 — Local Search & Hill Climbing
**Goal:** Shift from graph search to local search

**Tasks:**
- [ ] Read ACI_HO.pdf Session 3 (local search algorithms)
- [ ] Study Hill Climbing Search
  - Greedy improvement from current state
  - Move to best neighbor
  - Stuck in local maxima / plateaus / ridges
- [ ] Review CS4.pdf pages 33–47 (hill climbing content)

**Practice:**
- [ ] Trace hill climbing on a simple function (e.g., 2D landscape)
- [ ] Show an example where hill climbing gets stuck

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 16 — Local Beam Search & Online Search
**Goal:** Learn variants of local search

**Tasks:**
- [ ] Study Local Beam Search
  - Keep `k` best states
  - More sophisticated than basic hill climbing
- [ ] Study Online Search Agents
  - Limited lookahead
  - Safe exploration
- [ ] Review CS5.pdf pages 3–21

**Practice:**
- [ ] Compare hill climbing vs local beam: efficiency, quality of solution

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 17 — Genetic Algorithm & Overview
**Goal:** Learn evolutionary approaches

**Tasks:**
- [ ] Study Genetic Algorithm
  - Population, fitness, selection, crossover, mutation
  - Advantages: explores multiple regions of search space
- [ ] Review CS5.pdf pages 25–31, 44–45 (GA content)
- [ ] Understand when GA is useful

**Practice:**
- [ ] Trace a simple GA by hand (few generations)
- [ ] Compare GA vs hill climbing

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 18 — Ant Colony Optimization
**Goal:** Learn bio-inspired swarm intelligence

**Tasks:**
- [ ] Read ACI_HO.pdf Session 4 (ACO)
- [ ] Study Ant Colony Optimization
  - Pheromone trails
  - Probabilistic path selection
  - Swarm behavior for optimization
- [ ] Review CS4.pdf page 35, CS5.pdf page 48, CS6.pdf pages 2–4

**Practice:**
- [ ] Understand ACO for Traveling Salesman Problem
- [ ] Compare ACO vs GA vs hill climbing

**Time:** 1h 30 min reading + 1h practice = 2h 30 min

---

### Day 19 — Game Playing: Minimax & Alpha-Beta
**Goal:** Learn adversarial search

**Tasks:**
- [ ] Read ACI_HO.pdf Session 6 (game playing, minimax)
- [ ] Study Minimax Algorithm
  - Max and min nodes
  - Recursive backup of values
  - Time complexity (exponential in depth)
- [ ] Study Alpha-Beta Pruning
  - How to cut branches safely
  - Alpha (best for maximizer), beta (best for minimizer)

**Practice:**
- [ ] Trace minimax on a small game tree (tic-tac-toe or simple game)
- [ ] Show where alpha-beta pruning saves computation

**Time:** 1h 45 min reading + 1h 15 min practice = 3h

---

### Day 20 — Monte Carlo Tree Search & Stochastic Games
**Goal:** Learn modern game-playing techniques

**Tasks:**
- [ ] Study Monte Carlo Tree Search (MCTS)
  - Selection, expansion, simulation, backpropagation
  - Why it works well for complex games (Go, chess engines)
- [ ] Study Stochastic Games
  - Chance nodes
  - Expectimax algorithm
- [ ] Review ACI_HO.pdf Session 7

**Practice:**
- [ ] Understand MCTS conceptually
- [ ] Compare minimax vs MCTS: when is each better?

**Time:** 1h 45 min reading + 1h practice = 2h 45 min

---

### Day 21 — Final Review & Mock Exam
**Goal:** Comprehensive revision and self-assessment

**Tasks:**
- [ ] Review all seven sessions from notes
- [ ] Go through the revision checklist in the study plan
- [ ] Create final summary sheet (one page per major topic):
  - Uninformed search
  - Heuristics and A*
  - Local search and optimization
  - Game playing

**Mock exam practice:**
- [ ] Solve 3–5 example problems covering different topics
- [ ] Write quick essays: explain A* optimality, compare HC vs GA, etc.
- [ ] Self-quiz on definitions and key algorithms

**Time:** 3h

---

## Daily Study Tips

1. **Start each day with a 5-min overview** of what you'll learn
2. **Take brief notes** (not everything—key points only)
3. **Do one practical exercise per day** (pseudocode, trace by hand, or notebook)
4. **End with a 5-min summary** of what you learned
5. **Keep a glossary** of algorithms and their properties
6. **Sleep well**—rest is essential for retention

---

## Exam Preparation Checklist

### Last 3 days before exam (25–27 June)
- [ ] Review summary sheet one more time
- [ ] Do one final practice problem per algorithm
- [ ] Get good sleep

### Day before exam (27 June)
- [ ] Light review of definitions only
- [ ] No new material
- [ ] Prepare: ID card, pens, paper for rough work

### Exam day (28 June)
- [ ] Arrive 15 min early
- [ ] Read questions carefully
- [ ] Allocate time: ~2 min per mark
- [ ] Answer easy questions first

---

## Resources at a glance

| Topic | Primary Source | Slides | Notebook |
|-------|---|---|---|
| Agents & environments | ACI_HO.pdf S1 | CS1.pdf | — |
| Problem formulation | ACI_HO.pdf S1 | CS2.pdf | — |
| BFS, DFS, IDS, UCS | ACI_HO.pdf S1 | CS2.pdf | — |
| Heuristics & A* | ACI_HO.pdf S2 | CS2.pdf, CS3.pdf | A_star_implementation.ipynb |
| Heuristic design | ACI_HO.pdf S2 | CS4.pdf | — |
| Hill climbing | ACI_HO.pdf S3 | CS4.pdf, CS5.pdf | HillClimb.ipynb |
| Local beam search | ACI_HO.pdf S3 | CS5.pdf | — |
| Genetic algorithm | ACI_HO.pdf S4 | CS5.pdf | — |
| Ant colony opt. | ACI_HO.pdf S4 | CS4.pdf, CS5.pdf, CS6.pdf | — |
| Minimax & alpha-beta | ACI_HO.pdf S6 | CS1.pdf–CS6.pdf | — |
| Monte Carlo tree search | ACI_HO.pdf S7 | CS1.pdf–CS6.pdf | — |

---

## Notes
- Adjust pace based on how fast you learn each topic
- If a day feels too long, spread across 1.5 days
- If you finish early, do extra practice or review the previous day's material
- Use webinar notebooks to solidify implementation understanding
- DSAD.pdf should be reviewed alongside each data structure mention (queue, priority queue, tree, etc.)
