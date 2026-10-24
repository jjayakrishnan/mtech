# Mission: Advanced Computing for AI (ACI)

## Why
Pass the BITS Pilani WILP mid-semester exam for AIMLCZG557. The exam is subjective (written), 2 hours, 30 marks, 6-10 questions. Closed book — no formula sheet.

## Success looks like
- Can write PEAS specification and environment properties for any given domain in under 4 minutes
- Can trace A* on a graph showing f/g/h at each step
- Can expand a 3-level Minimax tree, compute utility at leaves, back-propagate values
- Can apply Alpha-Beta pruning and identify pruned nodes
- Can trace one generation of GA (selection → crossover → mutation)
- Can explain NEAT speciation with historical markings
- Can write pseudocode for: A*, Minimax, Alpha-Beta, Hill Climbing, GA
- Can distinguish: Generational vs Steady-State GA, crowding vs fitness sharing

## Exam Parameters
- **Date:** 28 Jun 2026, 01:00 PM (Makeup)
- **Scope:** CS1 to CS8 (all sessions)
- **Format:** Subjective — draw diagrams, trace algorithms, compute values
- **Marking:** Evaluation stops at first error (accuracy > coverage)
- **Bloom's levels:** Remember → Understand → Apply → Analyse → Evaluate → Create

## Key Topics (Mind Map from Lecturer)
1. **CS1-2: Agent Theory** — AI basics, PEAS, environment properties, 5 agent types, Problem-Solving Agents
2. **Informed Search** — A*, GBFS, heuristics (admissibility, consistency), relaxed constraints
3. **Local Search** — Hill Climbing (variants), Simulated Annealing, Beam Search
4. **Evolutionary/Nature-Inspired** — GA (generational vs steady-state, crowding), ACO (pheromone), NEAT (speciation)
5. **NAS** — Neural Architecture Search as GA application, DeepNEAT, CoDeepNEAT
6. **Adversarial Search** — Minimax, Alpha-Beta pruning, MCTS (UCB1)

## Formulas to Memorize (Closed Book)
- A*: f(n) = g(n) + h(n)
- Admissible: h(n) ≤ h*(n)
- Consistent: h(n) ≤ c(n,n') + h(n')
- Alpha-Beta: Prune when α ≥ β
- ACO: τ_ij ← (1−ρ)·τ_ij + Δτ_ij
- NEAT fitness sharing: f'_i = f_i / Σ sh(d_ij)

## Confirmed Errors to Fix
1. **Steady-state GA** — replaces only a few individuals incrementally (NOT entire population like generational GA)
2. **Crowding** — diversity-preserving replacement mechanism (NOT generational replacement)

## Constraints
- WILP student: full-time professional, limited daily study time
- Exam uses step-marking but stops at first error — accuracy over coverage
- Backpropagation is NOT in scope (that's DRL/NLP territory)

## Out of scope (for now)
- Deep learning / neural network training (separate from NAS as search)
- Multi-agent RL (that's DRL comprehensive exam)
