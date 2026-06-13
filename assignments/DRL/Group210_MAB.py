"""
================================================================================
BIRLA INSTITUTE OF TECHNOLOGY AND SCIENCE, PILANI
WORK INTEGRATED LEARNING PROGRAMMES DIVISION
Deep Reinforcement Learning - Lab Assignment 1
PART 1: Adaptive Treatment Recommendation System using Multi-Armed Bandit Learning
================================================================================
Group Number  : 210
Team Members  :
  1. AMITH P KASHYAP       (2025aa05342)
  2. ARJUN RANA            (2025aa05460)
  3. JAYAKRISHNAN J        (2025aa05072)
  4. LOHAR NILESH C MEENA  (2025aa05156)
  5. MUDRAS AMEY N         (2025aa05442)

Virtual Machine ID : (attach screenshot with VM ID and timestamp when run in virtual lab)
Execution Timestamp: (auto-printed below at runtime)
================================================================================
"""

# ── System / environment metadata (print at top as required) ──────────────────
import datetime, platform, socket

print("=" * 70)
print("EXECUTION METADATA")
print(f"  Timestamp      : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Hostname       : {socket.gethostname()}")
print(f"  OS / Platform  : {platform.system()} {platform.release()}")
print(f"  Python Version : {platform.python_version()}")
print("=" * 70)

# ── Standard imports ──────────────────────────────────────────────────────────
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — DATASET DESIGN
# ─────────────────────────────────────────────────────────────────────────────

def compute_environment_params(G):
    """
    Compute environment parameters from the group number G.

    Parameters
    ----------
    G : int
        Group number.

    Returns
    -------
    K : int
        Number of medicines (arms).
    probs : list of float
        Hidden success probability P_i for each medicine i.
    """
    # Number of medicines: K = (G mod 3) + 5
    K = (G % 3) + 5

    # Hidden success probability for medicine i: P_i = 0.4 + ((G+i) mod 6) * 0.07
    probs = [0.4 + ((G + i) % 6) * 0.07 for i in range(K)]
    return K, probs


def create_patient_dataset(G, K):
    """
    Generate the synthetic patient-treatment dataset with 1000 records.
    Seeds are fixed using random.seed(G) and numpy.random.seed(G) for reproducibility.

    The dataset pre-populates patient_id and severity_score.
    Columns assigned_medicine, clinical_outcome, and utility_score are left
    as NaN placeholders — they are dynamically filled during algorithm execution.

    Parameters
    ----------
    G : int
        Group number (used for seeding).
    K : int
        Number of medicines.

    Returns
    -------
    df : pd.DataFrame
        DataFrame with 1000 patient rows.
    """
    random.seed(G)
    np.random.seed(G)

    n_patients = 1000
    patient_ids = list(range(n_patients))

    # Severity = (patient_id mod 5) + 1  → values in {1, 2, 3, 4, 5}
    severity_scores = [(pid % 5) + 1 for pid in patient_ids]

    df = pd.DataFrame({
        "patient_id"       : patient_ids,
        "severity_score"   : severity_scores,
        "assigned_medicine": [np.nan] * n_patients,
        "clinical_outcome" : [np.nan] * n_patients,
        "utility_score"    : [np.nan] * n_patients,
    })
    return df


def simulate_treatment(patient_row, medicine_idx, probs):
    """
    Simulate assigning a medicine to a patient and compute the clinical outcome
    and utility score.

    Clinical outcome is drawn from a Bernoulli distribution with probability P_i.
    Utility = clinical_outcome * (1 - severity / 10)

    Parameters
    ----------
    patient_row : pd.Series
        A single patient row with at least 'severity_score'.
    medicine_idx : int
        Index of the medicine being assigned (0-based).
    probs : list of float
        Hidden success probabilities for each medicine.

    Returns
    -------
    clinical_outcome : int
        1 if recovered, 0 otherwise.
    utility_score : float
        Reward reflecting recovery adjusted by disease severity.
    """
    severity = patient_row["severity_score"]
    p_i = probs[medicine_idx]

    # Draw binary outcome from the medicine's true success probability
    clinical_outcome = int(np.random.binomial(1, p_i))

    # Utility decreases for higher-severity patients (real hospital impact)
    utility_score = clinical_outcome * (1 - severity / 10.0)

    return clinical_outcome, utility_score


# ── Run Task 1 ────────────────────────────────────────────────────────────────
G = 210
K, TRUE_PROBS = compute_environment_params(G)
BASE_DF = create_patient_dataset(G, K)

print("\n" + "=" * 70)
print("TASK 1 — DATASET DESIGN")
print("=" * 70)
print(f"  Group Number G          : {G}")
print(f"  Number of Medicines K   : {K}")
print(f"  Hidden Success Probabilities:")
for i, p in enumerate(TRUE_PROBS):
    print(f"    Medicine {i} (arm {i})   : P_{i} = {p:.4f}")
print(f"\n  Best medicine (highest P): Medicine {np.argmax(TRUE_PROBS)} "
      f"(P = {max(TRUE_PROBS):.4f})")

print("\n  First 10 rows of patient dataset:")
print(BASE_DF.head(10).to_string(index=False))


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — fresh dataset + seeded RNG for each algorithm run
# ─────────────────────────────────────────────────────────────────────────────

def fresh_run_setup(G, K):
    """
    Return a fresh copy of the dataset and reset numpy/random seeds.
    Called at the start of each strategy to ensure reproducibility
    and independent runs.

    Parameters
    ----------
    G : int
        Group number (seed value).
    K : int
        Number of medicines.

    Returns
    -------
    df : pd.DataFrame
        Fresh patient dataset ready to be populated.
    probs : list of float
        Hidden success probabilities.
    """
    random.seed(G)
    np.random.seed(G)
    _, probs = compute_environment_params(G)
    df = create_patient_dataset(G, K)
    return df, probs


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — IMMEDIATE EXPLOITATION (Greedy after initial exploration)
# ─────────────────────────────────────────────────────────────────────────────

def run_exploitation_strategy(G, K, n_patients=1000, n_initial=10):
    """
    Immediate Exploitation Strategy (Pure Greedy).

    Phase 1 — Exploration:
        Test each medicine exactly `n_initial` times (round-robin).
        This costs K * n_initial patient slots.

    Phase 2 — Exploitation:
        Identify the best medicine by average clinical_outcome so far,
        then prescribe ONLY that medicine for all remaining patients.

    Parameters
    ----------
    G          : int   — group number / seed
    K          : int   — number of medicines
    n_patients : int   — total number of patient iterations
    n_initial  : int   — initial exploration count per medicine

    Returns
    -------
    df              : pd.DataFrame — fully populated dataset
    cumulative_rewards : list of float — cumulative utility after each patient
    best_medicine   : int — medicine chosen for exploitation phase
    """
    df, probs = fresh_run_setup(G, K)

    # Bandit statistics: counts and sum of clinical outcomes per medicine
    counts  = np.zeros(K, dtype=int)
    successes = np.zeros(K)

    cumulative_rewards = []
    total_reward = 0.0

    for pid in range(n_patients):
        patient = df.iloc[pid]

        # ── Phase 1: round-robin initial exploration ──
        if pid < K * n_initial:
            med = pid % K          # cycle through medicines evenly
        else:
            # ── Phase 2: exploit the best medicine found so far ──
            avg_outcomes = successes / np.maximum(counts, 1)
            med = int(np.argmax(avg_outcomes))

        # Simulate treatment and record results
        outcome, utility = simulate_treatment(patient, med, probs)
        df.at[pid, "assigned_medicine"] = med
        df.at[pid, "clinical_outcome"]  = outcome
        df.at[pid, "utility_score"]     = utility

        # Update bandit statistics using clinical_outcome (as per assignment)
        counts[med]    += 1
        successes[med] += outcome

        total_reward += utility
        cumulative_rewards.append(total_reward)

    # Determine the exploited medicine (best after initial phase)
    avg_outcomes  = successes / np.maximum(counts, 1)
    best_medicine = int(np.argmax(avg_outcomes))

    return df, cumulative_rewards, best_medicine


print("\n" + "=" * 70)
print("TASK 2 — IMMEDIATE EXPLOITATION STRATEGY")
print("=" * 70)

df_exploit, rewards_exploit, best_med_exploit = run_exploitation_strategy(G, K)

print(f"  Initial exploration : 10 trials × {K} medicines = {10*K} patients")
print(f"  Best medicine found : Medicine {best_med_exploit} "
      f"(True P = {TRUE_PROBS[best_med_exploit]:.4f})")
print(f"  Cumulative Reward (1000 patients) : {rewards_exploit[-1]:.4f}")

# Print every 100th iteration for conciseness (all iterations visible in arrays)
print("\n  Cumulative reward at every 100 patients:")
for step in range(99, 1000, 100):
    print(f"    Patient {step+1:4d} : {rewards_exploit[step]:.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — CONTROLLED CLINICAL TRIAL (Epsilon-Greedy)
# ─────────────────────────────────────────────────────────────────────────────

def run_epsilon_greedy(G, K, epsilon, n_patients=1000):
    """
    Epsilon-Greedy Strategy (Controlled Clinical Trial).

    With probability `epsilon` (exploration): pick a random medicine.
    With probability `1 - epsilon` (exploitation): pick the current best medicine
    by mean clinical outcome.

    This balances between discovering new treatments and using the best known one.

    Parameters
    ----------
    G          : int   — group number / seed
    K          : int   — number of medicines
    epsilon    : float — exploration probability (0=pure greedy, 1=pure random)
    n_patients : int   — total simulation steps

    Returns
    -------
    df              : pd.DataFrame — populated dataset
    cumulative_rewards : list of float
    """
    df, probs = fresh_run_setup(G, K)

    counts    = np.zeros(K, dtype=int)
    successes = np.zeros(K)
    cumulative_rewards = []
    total_reward = 0.0

    for pid in range(n_patients):
        patient = df.iloc[pid]

        if np.random.random() < epsilon:
            # Explore: choose a random medicine
            med = np.random.randint(0, K)
        else:
            # Exploit: choose medicine with highest observed success rate
            avg = successes / np.maximum(counts, 1)
            med = int(np.argmax(avg))

        outcome, utility = simulate_treatment(patient, med, probs)
        df.at[pid, "assigned_medicine"] = med
        df.at[pid, "clinical_outcome"]  = outcome
        df.at[pid, "utility_score"]     = utility

        counts[med]    += 1
        successes[med] += outcome
        total_reward   += utility
        cumulative_rewards.append(total_reward)

    return df, cumulative_rewards


print("\n" + "=" * 70)
print("TASK 3 — CONTROLLED CLINICAL TRIAL STRATEGY (Epsilon-Greedy)")
print("=" * 70)

epsilons_to_test = [0.01, 0.10, 0.50]
epsilon_results  = {}

for eps in epsilons_to_test:
    df_eps, rewards_eps = run_epsilon_greedy(G, K, epsilon=eps)
    epsilon_results[eps] = (df_eps, rewards_eps)
    print(f"\n  ε = {eps:.2f} | Final Cumulative Reward : {rewards_eps[-1]:.4f}")
    print(f"         Cumulative reward at every 100 patients:")
    for step in range(99, 1000, 100):
        print(f"           Patient {step+1:4d} : {rewards_eps[step]:.4f}")

print("""
  Analysis:
    ε = 1%  : Near-pure exploitation after very limited exploration.
              Converges quickly but risks locking onto a suboptimal medicine
              if the early samples happened to favour a weaker arm.

    ε = 10% : Well-balanced. Sufficient exploration to discover the true best
              medicine while dedicating 90% of patients to the best known arm.
              Achieves strong cumulative reward with reasonable stability.

    ε = 50% : Heavy exploration causes the agent to frequently divert from the
              best medicine. Cumulative reward is noticeably lower because half
              the patients receive sub-optimal treatments.
""")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 4 — CONFIDENCE-BASED STRATEGY (UCB1)
# ─────────────────────────────────────────────────────────────────────────────

def run_ucb1(G, K, n_patients=1000):
    """
    UCB1 (Upper Confidence Bound) Strategy.

    Each medicine is selected once in the first K rounds to initialise estimates.
    Thereafter, the medicine maximising:
        UCB_i = mean_i + sqrt(2 * ln(t) / n_i)
    is chosen, where t is the current time step and n_i is the pull count for arm i.

    This gives under-sampled medicines a natural bonus that shrinks as evidence
    accumulates — implementing the physician's recommendation to prioritise
    treatments with fewer observations initially.

    Parameters
    ----------
    G          : int — group number / seed
    K          : int — number of medicines
    n_patients : int — total simulation steps

    Returns
    -------
    df              : pd.DataFrame — populated dataset
    cumulative_rewards : list of float
    """
    df, probs = fresh_run_setup(G, K)

    counts    = np.zeros(K, dtype=int)
    successes = np.zeros(K)
    cumulative_rewards = []
    total_reward = 0.0

    for pid in range(n_patients):
        patient = df.iloc[pid]
        t = pid + 1  # 1-indexed time step

        if pid < K:
            # Initialisation: pull each arm once before computing UCB scores
            med = pid
        else:
            # Compute UCB score for each medicine
            avg  = successes / counts               # mean outcome per arm
            bonus = np.sqrt(2 * np.log(t) / counts) # exploration bonus
            ucb_scores = avg + bonus
            med = int(np.argmax(ucb_scores))

        outcome, utility = simulate_treatment(patient, med, probs)
        df.at[pid, "assigned_medicine"] = med
        df.at[pid, "clinical_outcome"]  = outcome
        df.at[pid, "utility_score"]     = utility

        counts[med]    += 1
        successes[med] += outcome
        total_reward   += utility
        cumulative_rewards.append(total_reward)

    return df, cumulative_rewards


print("\n" + "=" * 70)
print("TASK 4 — CONFIDENCE-BASED STRATEGY (UCB1)")
print("=" * 70)

df_ucb, rewards_ucb = run_ucb1(G, K)
print(f"  Final Cumulative Reward (UCB1, 1000 patients) : {rewards_ucb[-1]:.4f}")
print("\n  Cumulative reward at every 100 patients:")
for step in range(99, 1000, 100):
    print(f"    Patient {step+1:4d} : {rewards_ucb[step]:.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# TASK 5 — COMPARATIVE ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("TASK 5 — COMPARATIVE ANALYSIS")
print("=" * 70)

x = list(range(1, 1001))

plt.figure(figsize=(12, 6))

# Plot all strategies
plt.plot(x, rewards_exploit,             label="Exploitation (Greedy)",   linewidth=2, color="steelblue")
plt.plot(x, epsilon_results[0.01][1],   label="ε-Greedy  ε=1%",          linewidth=1.5, linestyle="--", color="orange")
plt.plot(x, epsilon_results[0.10][1],   label="ε-Greedy  ε=10%",         linewidth=2,   color="green")
plt.plot(x, epsilon_results[0.50][1],   label="ε-Greedy  ε=50%",         linewidth=1.5, linestyle=":", color="red")
plt.plot(x, rewards_ucb,                label="UCB1",                    linewidth=2,   color="purple")

plt.xlabel("Number of Patients", fontsize=13)
plt.ylabel("Cumulative Utility Reward", fontsize=13)
plt.title("Cumulative Reward vs Number of Patients\n"
          "Multi-Armed Bandit Strategies — Group 210", fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Group210_MAB_comparison.png", dpi=150)
plt.show()
print("  Plot saved → Group210_MAB_comparison.png")

# ── Summary table ─────────────────────────────────────────────────────────────
final_rewards = {
    "Exploitation (Greedy)"  : rewards_exploit[-1],
    "ε-Greedy  ε=1%"         : epsilon_results[0.01][1][-1],
    "ε-Greedy  ε=10%"        : epsilon_results[0.10][1][-1],
    "ε-Greedy  ε=50%"        : epsilon_results[0.50][1][-1],
    "UCB1"                   : rewards_ucb[-1],
}
print("\n  Final Cumulative Reward Summary:")
print(f"  {'Strategy':<25} {'Final Reward':>14}")
print("  " + "-" * 42)
for name, val in sorted(final_rewards.items(), key=lambda x: -x[1]):
    print(f"  {name:<25} {val:>14.4f}")

# ── Analytical answers ────────────────────────────────────────────────────────
print("""
  ── Answers to Comparative Questions ──

  Q1. Which strategy achieves the highest cumulative reward?
      UCB1 typically achieves the highest cumulative reward because it
      systematically balances exploration and exploitation using
      mathematically principled confidence bounds, avoiding both the
      premature lock-in of the Greedy strategy and the waste of ε=50%.

  Q2. Which strategy identifies the best medicine fastest?
      Exploitation (Greedy) converges to a fixed medicine earliest — after
      just K×10 = 50 patients — though it risks locking onto a suboptimal
      arm. UCB1 identifies the *correct* best medicine fastest among
      strategies that guarantee correctness.

  Q3. Which strategy shows the most stable performance over time?
      Exploitation (Greedy) is the most stable in the exploitation phase
      because it makes no random choices after the initial 50 patients.
      UCB1 is a close second, converging with minor residual oscillation.

  Q4. Recommended strategy for real-world hospital deployment?
      UCB1 is the safest and most principled choice. It guarantees
      sub-linear regret over time, requires no hyperparameter tuning
      (unlike ε-greedy), and naturally de-prioritises under-explored
      medicines as evidence grows — matching clinical trial ethics where
      patients must receive the most promising known treatment while
      still permitting systematic discovery.

  ── Comparative Summary (3–5 sentences) ──

  The UCB1 algorithm consistently achieves the highest cumulative reward by
  maintaining a statistically motivated optimism bonus for less-tested
  medicines, which diminishes as evidence accumulates. The Greedy strategy
  converges rapidly but is brittle — early random fluctuations can cause
  permanent commitment to a suboptimal medicine. Epsilon-Greedy with ε=10%
  strikes a practical middle ground: it does not require the mathematical
  complexity of UCB1 and performs well when an appropriate epsilon is chosen.
  Both ε=1% and ε=50% underperform relative to ε=10%, illustrating the
  classic exploration–exploitation dilemma. For a clinical setting where
  patient welfare is paramount, UCB1 is preferred because it adapts
  automatically and has provable bounds on cumulative regret.
""")

print("=" * 70)
print("END OF PART 1 — MAB ASSIGNMENT")
print("=" * 70)
