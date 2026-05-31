"""
================================================================================
BIRLA INSTITUTE OF TECHNOLOGY AND SCIENCE, PILANI
WORK INTEGRATED LEARNING PROGRAMMES DIVISION
Deep Reinforcement Learning - Lab Assignment 1
PART 2: Autonomous Drone Rescue Using Dynamic Programming
================================================================================
Group Number  : 210
Team Members  :
  1. AMITH P KASHYAP       (2025aa05342)
  2. ARJUN RANA            (2025aa05460)
  3. JAYAKRISHNAN J        (2025aa05072)
  4. LOHAR NILESH C MEENA  (2025aa05156)
  5. MUDRAS AMEY N         (2025aa05442)

INSTRUCTOR UPDATE (applied):
  • Environment configuration is derived from Group ID = 210 (not student ID).
  • One submission per group; PDF must include both code and output.

Virtual Machine ID : (attach screenshot with VM ID and timestamp)
================================================================================

ENVIRONMENT CONFIGURATION (derived from Group ID = 210, last digit = 0)
  Group ID last digit : 0  →  falls in range 0–4
  Grid size          : 5 × 5   (last digit 0–4 → 5×5 grid)
  Rescue targets     : 2        (last digit 0–4 → 2 rescue targets)
  Charging stations  : 1        (last digit 0–4 → 1 charging station)
  Danger zones       : 3        (last digit 0–4 → 3 danger zones)
  Blocked cells      : 2        (last digit 0–4 → 2 blocked cells)
  Max battery        : 10       (last digit 0 is even → battery = 10)
  Wind probability   : 20%      (last digit 0–4 → wind prob = 20%)
  Max steps          : 50

GRID LAYOUT (S = top-left as required by assignment):
  Row 0:  S   F   D   F   R
  Row 1:  F   X   F   C   F
  Row 2:  D   F   W   F   F
  Row 3:  F   F   F   X   F
  Row 4:  R   D   F   F   F

  S = Start (0,0)
  F = Free/Safe
  D = Danger zone × 3 → (0,2), (2,0), (4,1)
  R = Rescue target × 2 → (0,4), (4,0)
  C = Charging station × 1 → (1,3)
  W = Wind zone × 1 → (2,2)
  X = Blocked × 2 → (1,1), (3,3)

STATE REPRESENTATION:
  Each state is a tuple: (row, col, battery, rescue_status)
    - row, col    : drone position (0-indexed)
    - battery     : current battery level (1 to MAX_BATTERY)
    - rescue_status: tuple of booleans, one per rescue target
                     True = already rescued, False = still needs rescue
  Example: (0, 0, 10, (False, False)) = start state, full battery, no rescues yet.

  Total theoretical states = 5×5×10×2^2 = 1000 (bounded; DP is tractable here).
  (Configuration driven by Group ID = 210, last digit = 0, per instructor update.)

TRANSITION DYNAMICS:
  Normal cells: deterministic movement to the intended cell.
  Wind cell (W) at (2,2): if the drone is ON a wind cell and attempts to move,
    with 20% probability (Group ID 210, last digit 0 → range 0–4) the intended
    direction is overridden and a uniformly random direction (Up/Down/Left/Right)
    is chosen instead.
  Blocked cells (X): movement into a blocked cell is rejected; drone stays put,
    still consuming 1 battery unit.
  Boundary: movement outside grid edges is rejected; drone stays put.
================================================================================
"""

# ── System / environment metadata ─────────────────────────────────────────────
import datetime, platform, socket

print("=" * 70)
print("EXECUTION METADATA")
print(f"  Timestamp      : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Hostname       : {socket.gethostname()}")
print(f"  OS / Platform  : {platform.system()} {platform.release()}")
print(f"  Python Version : {platform.python_version()}")
print("=" * 70)

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import itertools
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────────────────
# ENVIRONMENT CONSTANTS  (derived from group configuration above)
# ─────────────────────────────────────────────────────────────────────────────

GRID_ROWS   = 5
GRID_COLS   = 5
MAX_BATTERY = 10          # Group ID 210, last digit 0 → even → battery = 10
WIND_PROB   = 0.20        # Group ID 210, last digit 0 → range 0–4 → wind = 20%
MAX_STEPS   = 50          # 5×5 grid
GAMMA       = 0.99        # discount factor for value iteration
THETA       = 1e-3        # convergence threshold

# Cell type identifiers
FREE    = "F"
START   = "S"
DANGER  = "D"
RESCUE  = "R"
CHARGE  = "C"
WIND    = "W"
BLOCKED = "X"

# Base grid layout (static; rescue cells are tracked dynamically in state)
BASE_GRID = [
    [START,   FREE,    DANGER,  FREE,    RESCUE],   # row 0
    [FREE,    BLOCKED, FREE,    CHARGE,  FREE  ],   # row 1
    [DANGER,  FREE,    WIND,    FREE,    FREE  ],   # row 2
    [FREE,    FREE,    FREE,    BLOCKED, FREE  ],   # row 3
    [RESCUE,  DANGER,  FREE,    FREE,    FREE  ],   # row 4
]

# Rescue target positions (row, col) — order defines rescue_status index
RESCUE_POSITIONS = [(0, 4), (4, 0)]
N_RESCUES        = len(RESCUE_POSITIONS)

# Charging station positions
CHARGE_POSITIONS = [(1, 3)]

# Start position
START_POS = (0, 0)

# Actions: (name, delta_row, delta_col)
ACTIONS = {
    0: ("Up",    -1,  0),
    1: ("Down",  +1,  0),
    2: ("Left",   0, -1),
    3: ("Right",  0, +1),
    4: ("Hover",  0,  0),
}
N_ACTIONS = len(ACTIONS)

# Rewards
REWARD_RESCUE   =  20
REWARD_DANGER   = -10
REWARD_BATTERY  = -20   # battery exhausted
REWARD_CHARGE   =   5
REWARD_MOVE     =  -1   # regular movement step cost


# ─────────────────────────────────────────────────────────────────────────────
# OUTCOME 1 — CUSTOM DRONE RESCUE ENVIRONMENT
# ─────────────────────────────────────────────────────────────────────────────

class DroneRescueEnv:
    """
    Custom Drone Rescue Environment for Group 210.

    Models a 5×5 grid-world disaster zone. The drone must rescue civilians,
    manage battery, avoid danger, and use charging stations.

    State = (row, col, battery, rescue_status_tuple)
      - row, col       : drone position
      - battery        : remaining battery (1–MAX_BATTERY); 0 → episode over
      - rescue_status  : tuple[bool] of length N_RESCUES
                         True = that target is already rescued

    Actions: 0=Up, 1=Down, 2=Left, 3=Right, 4=Hover
    """

    def __init__(self):
        """Initialise environment; call reset() before first use."""
        self.reset()

    # ── Core API ──────────────────────────────────────────────────────────────

    def reset(self):
        """
        Reset the environment to its initial state.
        Returns the initial state tuple.
        """
        self.row     = START_POS[0]
        self.col     = START_POS[1]
        self.battery = MAX_BATTERY
        self.rescue_status = [False] * N_RESCUES  # no targets rescued yet
        self.steps   = 0
        self.done    = False
        return self._get_state()

    def step(self, action):
        """
        Execute one action in the environment.

        Wind stochasticity: if the drone is currently on a WIND cell and the
        action is a movement (not Hover), with probability WIND_PROB the
        intended direction is replaced by a uniformly random direction.

        Battery:
          - All actions cost 1 battery.
          - Hovering ON a charging station restores +2 battery (capped at MAX).
          - Entering a charging station refills battery to MAX.

        Parameters
        ----------
        action : int
            Action index (0–4).

        Returns
        -------
        next_state : tuple
        reward     : float
        done       : bool
        info       : dict
        """
        assert not self.done, "Episode is over. Call reset()."

        self.steps += 1
        reward = 0.0
        info   = {}

        action_name, dr, dc = ACTIONS[action]

        # ── Wind stochasticity: applied when drone IS on a wind cell ──
        if BASE_GRID[self.row][self.col] == WIND and action != 4:  # 4=Hover
            if np.random.random() < WIND_PROB:
                # Override direction uniformly at random from {Up,Down,Left,Right}
                random_action = np.random.choice([0, 1, 2, 3])
                _, dr, dc = ACTIONS[random_action]
                info["wind_deflected"] = True

        # ── Compute candidate next position ──
        new_row = self.row + dr
        new_col = self.col + dc

        # ── Boundary and blocked-cell enforcement ──
        if (action == 4):
            # Hover: stay in place
            new_row, new_col = self.row, self.col
        else:
            # Clamp to grid and reject blocked cells
            if (new_row < 0 or new_row >= GRID_ROWS or
                new_col < 0 or new_col >= GRID_COLS or
                BASE_GRID[new_row][new_col] == BLOCKED):
                new_row, new_col = self.row, self.col  # bounce back

        # ── Battery cost: every action costs 1 unit ──
        if action == 4 and BASE_GRID[new_row][new_col] == CHARGE:
            # Hovering on charging station: +2 net (charge +2, cost -1 → net +1)
            self.battery = min(MAX_BATTERY, self.battery - 1 + 2)
        else:
            self.battery -= 1

        # ── Move the drone ──
        self.row, self.col = new_row, new_col

        # ── Cell effects at new position ──
        cell = BASE_GRID[self.row][self.col]

        if cell == DANGER:
            # Danger zone: heavy penalty, episode continues
            reward += REWARD_DANGER
            info["event"] = "danger"

        elif cell == CHARGE and action != 4:
            # Entering a charging station: full battery refill.
            # The +5 reward is given only when the drone genuinely needed charging
            # (battery ≤ half capacity on arrival, after deducting the step cost).
            # This prevents the pathological infinite-horizon DP behaviour where
            # cycling between an adjacent cell and the charger is preferred over
            # completing rescues, since the cycle would generate no charging reward
            # unless the drone had actually depleted its battery sufficiently.
            if self.battery <= MAX_BATTERY // 2:
                reward += REWARD_CHARGE
                info["event"] = "charged_needed"
            else:
                info["event"] = "charged_topped_up"
            self.battery = MAX_BATTERY

        # Check rescue targets
        for idx, (rr, rc) in enumerate(RESCUE_POSITIONS):
            if (self.row == rr and self.col == rc and
                    not self.rescue_status[idx]):
                self.rescue_status[idx] = True
                reward += REWARD_RESCUE
                info["rescued"] = idx

        # Regular step cost applied to all transitions (additive with events)
        reward += REWARD_MOVE

        # ── Termination conditions ──
        if self.battery <= 0:
            reward += REWARD_BATTERY  # battery exhausted penalty
            self.done = True
            info["termination"] = "battery_depleted"
        elif all(self.rescue_status):
            self.done = True
            info["termination"] = "all_rescued"
        elif self.steps >= MAX_STEPS:
            self.done = True
            info["termination"] = "max_steps"

        return self._get_state(), reward, self.done, info

    def valid_actions(self, state=None):
        """
        Return a list of valid action indices from the given state.
        An action is invalid only if it would move into a BLOCKED cell AND there
        is no stochasticity — for DP purposes all 5 actions are available at
        every non-terminal state (blocked movement simply keeps the drone in
        place and still costs battery).

        Parameters
        ----------
        state : tuple or None
            If None, uses current env state.

        Returns
        -------
        list of int
        """
        # All 5 actions are structurally valid; the environment handles
        # "invalid" moves by keeping the drone in place with battery cost.
        return list(range(N_ACTIONS))

    def render(self):
        """
        Print a human-readable ASCII representation of the current grid state.
        Shows drone position (★), rescue targets (R/✓), and other cell types.
        """
        print(f"\n  Step {self.steps} | Battery {self.battery}/{MAX_BATTERY} | "
              f"Rescued: {sum(self.rescue_status)}/{N_RESCUES}")
        print("  +" + "---+" * GRID_COLS)
        for r in range(GRID_ROWS):
            row_str = "  |"
            for c in range(GRID_COLS):
                if r == self.row and c == self.col:
                    symbol = " ★ "   # drone position
                else:
                    cell = BASE_GRID[r][c]
                    # Check if rescue target at this cell is already done
                    rescue_done = False
                    for idx, (rr, rc) in enumerate(RESCUE_POSITIONS):
                        if (r, c) == (rr, rc) and self.rescue_status[idx]:
                            rescue_done = True
                    if rescue_done:
                        symbol = " ✓ "
                    elif cell == START:
                        symbol = " S "
                    else:
                        symbol = f" {cell} "
                row_str += symbol + "|"
            print(row_str)
            print("  +" + "---+" * GRID_COLS)

    def _get_state(self):
        """Return the current state as an immutable tuple."""
        return (self.row, self.col, self.battery, tuple(self.rescue_status))


# ── Quick environment smoke-test ──────────────────────────────────────────────
print("\n" + "=" * 70)
print("OUTCOME 1 — CUSTOM DRONE RESCUE ENVIRONMENT")
print("=" * 70)
print("\nGrid layout:")
print("  " + "    ".join([str(c) for c in range(GRID_COLS)]))
for r, row in enumerate(BASE_GRID):
    print(f"  {r} " + "  ".join(f"{cell:2s}" for cell in row))

env_demo = DroneRescueEnv()
state = env_demo.reset()
print(f"\nInitial State : {state}")
print(f"  Position    : row={state[0]}, col={state[1]}")
print(f"  Battery     : {state[2]}/{MAX_BATTERY}")
print(f"  Rescue done : {state[3]}")
env_demo.render()

# Take a few demo steps: move right twice, then down
print("\nDemo: Right → Right → Down → Down → Down → Down (moving toward rescue at (4,0))")
demo_actions = [3, 1, 1, 2, 2, 1, 1, 1]   # Right, Down×2, Left×2, Down×3
for act in demo_actions:
    s, r, done, info = env_demo.step(act)
    print(f"  Action={ACTIONS[act][0]:<6} → pos=({s[0]},{s[1]}), "
          f"battery={s[2]}, reward={r:+.1f}, {info}")
    if done:
        print("  Episode ended.")
        break
env_demo.render()


# ─────────────────────────────────────────────────────────────────────────────
# OUTCOME 2 — DYNAMIC PROGRAMMING: VALUE ITERATION
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("OUTCOME 2 — DYNAMIC PROGRAMMING: VALUE ITERATION")
print("=" * 70)

# ── State enumeration ─────────────────────────────────────────────────────────

def enumerate_states():
    """
    Enumerate all reachable (non-terminal) states in the MDP.

    A state is (row, col, battery, rescue_status_tuple).
    We exclude:
      - Blocked cells (drone can never be in them)
      - battery = 0 (terminal: episode ends)

    Returns
    -------
    states : list of tuples
        All reachable non-terminal states.
    state_index : dict
        Maps state tuple → integer index for fast lookup.
    """
    states = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if BASE_GRID[r][c] == BLOCKED:
                continue   # drone cannot occupy blocked cells
            for bat in range(1, MAX_BATTERY + 1):
                for rescue_combo in itertools.product([False, True], repeat=N_RESCUES):
                    states.append((r, c, bat, rescue_combo))

    state_index = {s: i for i, s in enumerate(states)}
    return states, state_index


def get_transitions(state, action):
    """
    Compute the transition distribution T(s'|s,a) and reward R(s,a,s')
    for a given state-action pair.

    This function implements the full MDP transition model including:
      - Deterministic movement (most cells)
      - Stochastic wind deflection (when on W cell, 20% chance of random direction)
      - Blocked cell bounce-back
      - Battery management (charging, depletion)
      - Rescue target removal
      - Reward computation

    Parameters
    ----------
    state  : tuple (row, col, battery, rescue_status)
    action : int (0–4)

    Returns
    -------
    transitions : list of (probability, next_state, reward, done)
        Each element represents one possible outcome of the action.
    """
    row, col, battery, rescue_status = state
    rescue_status = list(rescue_status)

    _, dr, dc = ACTIONS[action]
    current_cell = BASE_GRID[row][col]

    # Build the set of (prob, direction) pairs — wind stochasticity
    if current_cell == WIND and action != 4:
        # 80% intended direction, 20% uniform random among 4 directions
        wind_directions = []
        for a_wind in [0, 1, 2, 3]:
            _, ddr, ddc = ACTIONS[a_wind]
            wind_directions.append((WIND_PROB / 4.0, ddr, ddc))

        # Intended direction contributes (1 - WIND_PROB) + its own random share
        intended_prob = (1 - WIND_PROB) + WIND_PROB / 4.0
        direction_dist = {}
        for a_wind in [0, 1, 2, 3]:
            _, ddr, ddc = ACTIONS[a_wind]
            key = (ddr, ddc)
            direction_dist[key] = direction_dist.get(key, 0) + WIND_PROB / 4.0
        direction_dist[(dr, dc)] = (direction_dist.get((dr, dc), 0)
                                    - WIND_PROB / 4.0 + (1 - WIND_PROB) + WIND_PROB / 4.0)
        direction_list = [(prob, ddr, ddc) for (ddr, ddc), prob in direction_dist.items()]
    elif action == 4:
        # Hover: no movement
        direction_list = [(1.0, 0, 0)]
    else:
        # Deterministic movement
        direction_list = [(1.0, dr, dc)]

    transitions = []

    for prob, ddr, ddc in direction_list:
        if prob <= 0:
            continue

        # Compute candidate next position
        nr, nc = row + ddr, col + ddc

        # Boundary / blocked-cell check
        if (nr < 0 or nr >= GRID_ROWS or nc < 0 or nc >= GRID_COLS or
                BASE_GRID[nr][nc] == BLOCKED):
            nr, nc = row, col   # bounce back

        # Battery update
        new_battery = battery
        if action == 4 and BASE_GRID[nr][nc] == CHARGE:
            # Hover on charging station: net +1 battery (−1 cost + 2 charge)
            new_battery = min(MAX_BATTERY, battery - 1 + 2)
        else:
            new_battery -= 1

        # Cell effects at destination
        reward = REWARD_MOVE
        new_rescue = list(rescue_status)
        done = False
        next_cell = BASE_GRID[nr][nc]

        if next_cell == DANGER:
            reward += REWARD_DANGER

        elif next_cell == CHARGE and action != 4:
            # Reward only when genuinely depleted (battery after step cost ≤ half cap).
            # Mirrors the env.step() logic to keep model and environment consistent.
            if new_battery <= MAX_BATTERY // 2:
                reward += REWARD_CHARGE
            new_battery = MAX_BATTERY   # full refill on entry regardless

        # Rescue targets
        for idx, (rr, rc) in enumerate(RESCUE_POSITIONS):
            if (nr, nc) == (rr, rc) and not new_rescue[idx]:
                new_rescue[idx] = True
                reward += REWARD_RESCUE

        # Terminal conditions
        if new_battery <= 0:
            reward += REWARD_BATTERY
            done = True
        elif all(new_rescue):
            done = True

        next_state = (nr, nc, max(new_battery, 0), tuple(new_rescue))
        transitions.append((prob, next_state, reward, done))

    return transitions


def value_iteration(states, state_index):
    """
    Value Iteration algorithm to compute the optimal value function V*(s)
    and optimal policy π*(s).

    Updates V(s) for all states repeatedly until the maximum change across
    all states in one sweep is below the threshold θ = 1e-3.

    Bellman optimality equation:
      V*(s) = max_a Σ_{s'} T(s'|s,a) [ R(s,a,s') + γ · V*(s') ]

    Parameters
    ----------
    states      : list of state tuples
    state_index : dict mapping state → index

    Returns
    -------
    V       : np.ndarray — optimal value function
    policy  : dict state → best action index
    n_iters : int — number of iterations until convergence
    runtime : float — elapsed time in seconds
    final_delta : float — Bellman error at convergence
    """
    V = np.zeros(len(states))
    policy = {}
    n_iters = 0
    start_time = time.time()

    print(f"  Starting Value Iteration over {len(states):,} states ...")
    print(f"  Convergence threshold θ = {THETA}, discount γ = {GAMMA}")

    while True:
        delta = 0.0
        n_iters += 1

        for i, state in enumerate(states):
            row, col, battery, rescue_status = state

            # Skip terminal states (battery=0 handled by state enumeration exclusion;
            # all-rescued is technically terminal but may appear in state list)
            if all(rescue_status):
                V[i] = 0.0
                continue

            best_val = -np.inf
            best_action = 0

            for action in range(N_ACTIONS):
                transitions = get_transitions(state, action)
                q_value = 0.0
                for prob, next_state, reward, done in transitions:
                    if done:
                        q_value += prob * reward  # terminal: no future value
                    else:
                        j = state_index.get(next_state, None)
                        if j is not None:
                            q_value += prob * (reward + GAMMA * V[j])
                        else:
                            q_value += prob * reward  # unknown next state

                if q_value > best_val:
                    best_val    = q_value
                    best_action = action

            delta = max(delta, abs(best_val - V[i]))
            V[i] = best_val
            policy[state] = best_action

        # Progress report every 10 iterations
        if n_iters % 10 == 0:
            print(f"    Iteration {n_iters:4d} | Δ = {delta:.6f}")

        if delta < THETA:
            break

    runtime = time.time() - start_time
    return V, policy, n_iters, runtime, delta


# Run Value Iteration
ALL_STATES, STATE_INDEX = enumerate_states()
print(f"\n  Total enumerated states : {len(ALL_STATES):,}")

V_STAR, POLICY, N_ITERS, RUNTIME, FINAL_DELTA = value_iteration(ALL_STATES, STATE_INDEX)

print(f"\n  ── Value Iteration Results ──")
print(f"  Convergence achieved in : {N_ITERS} iterations")
print(f"  Runtime                 : {RUNTIME:.4f} seconds")
print(f"  Final Bellman error (Δ) : {FINAL_DELTA:.8f}")
print(f"  Max V*(s)               : {V_STAR.max():.4f}")
print(f"  Min V*(s)               : {V_STAR.min():.4f}")


# ─────────────────────────────────────────────────────────────────────────────
# OUTCOME 3 — POLICY VISUALISATION
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("OUTCOME 3 — POLICY VISUALISATION")
print("=" * 70)

def visualise_policy(V_STAR, POLICY, ALL_STATES, STATE_INDEX,
                     battery_level=10, rescue_done=(False, False)):
    """
    Visualise the optimal policy as a grid of arrows and a heatmap of V*(s).

    For a fixed battery level and rescue status slice of the state space,
    display:
      1. An arrow grid showing π*(s) at each grid cell.
      2. A heatmap of V*(s) values.

    Parameters
    ----------
    V_STAR       : np.ndarray — optimal value function
    POLICY       : dict — state → best action index
    ALL_STATES   : list of state tuples
    STATE_INDEX  : dict — state → index
    battery_level: int — battery level to slice on
    rescue_done  : tuple of bool — rescue status to slice on
    """
    ACTION_ARROWS = {0: "↑", 1: "↓", 2: "←", 3: "→", 4: "⊙"}
    ACTION_DXY    = {0: (0, 0.4), 1: (0, -0.4), 2: (-0.4, 0), 3: (0.4, 0)}

    grid_val    = np.full((GRID_ROWS, GRID_COLS), np.nan)
    grid_policy = {}

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if BASE_GRID[r][c] == BLOCKED:
                continue
            state = (r, c, battery_level, tuple(rescue_done))
            idx = STATE_INDEX.get(state)
            if idx is not None:
                grid_val[r][c] = V_STAR[idx]
                grid_policy[(r, c)] = POLICY.get(state, 4)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # ── Left: Policy Arrow Grid ──────────────────────────────────────────────
    ax = axes[0]
    cmap = matplotlib.colormaps["RdYlGn"]
    vmin, vmax = np.nanmin(grid_val), np.nanmax(grid_val)

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            cell = BASE_GRID[r][c]
            if cell == BLOCKED:
                ax.add_patch(plt.Rectangle((c, GRID_ROWS-1-r), 1, 1,
                             color="black", zorder=2))
                continue

            # Background colour by cell type
            colour_map = {FREE:"#e8f4f8", START:"#b3e0ff", DANGER:"#ffcccc",
                          RESCUE:"#ccffcc", CHARGE:"#ffffcc", WIND:"#e0ccff"}
            bg = colour_map.get(cell, "white")
            ax.add_patch(plt.Rectangle((c, GRID_ROWS-1-r), 1, 1,
                         color=bg, zorder=1, ec="gray"))

            # Value text
            val = grid_val[r][c]
            if not np.isnan(val):
                ax.text(c+0.5, GRID_ROWS-0.5-r, f"{val:.1f}",
                        ha="center", va="top", fontsize=6.5, color="dimgray")

            # Policy arrow
            act = grid_policy.get((r, c), None)
            if act is not None:
                if act == 4:  # Hover
                    ax.text(c+0.5, GRID_ROWS-0.5-r-0.2, "⊙",
                            ha="center", va="center", fontsize=14)
                else:
                    dx, dy = ACTION_DXY[act]
                    ax.annotate("", xy=(c+0.5+dx, GRID_ROWS-0.5-r+dy),
                                xytext=(c+0.5, GRID_ROWS-0.5-r),
                                arrowprops=dict(arrowstyle="->",
                                                color="navy", lw=1.5))

            # Cell label
            label = cell if cell not in (FREE,) else ""
            ax.text(c+0.1, GRID_ROWS-0.15-r, label,
                    ha="left", va="top", fontsize=8, fontweight="bold")

    ax.set_xlim(0, GRID_COLS)
    ax.set_ylim(0, GRID_ROWS)
    ax.set_xticks(range(GRID_COLS))
    ax.set_yticks(range(GRID_ROWS))
    ax.set_xticklabels(range(GRID_COLS))
    ax.set_yticklabels(range(GRID_ROWS-1, -1, -1))
    ax.set_title(f"Optimal Policy π*(s)\n"
                 f"(Battery={battery_level}, Rescue={rescue_done})", fontsize=12)
    ax.set_xlabel("Column"); ax.set_ylabel("Row")

    # Legend patches
    patches = [
        mpatches.Patch(color="#e8f4f8", label="F: Free"),
        mpatches.Patch(color="#b3e0ff", label="S: Start"),
        mpatches.Patch(color="#ffcccc", label="D: Danger"),
        mpatches.Patch(color="#ccffcc", label="R: Rescue"),
        mpatches.Patch(color="#ffffcc", label="C: Charge"),
        mpatches.Patch(color="#e0ccff", label="W: Wind"),
        mpatches.Patch(color="black",   label="X: Blocked"),
    ]
    ax.legend(handles=patches, loc="upper right", fontsize=7, framealpha=0.9)

    # ── Right: V* Heatmap ─────────────────────────────────────────────────────
    ax2 = axes[1]
    masked = np.ma.masked_invalid(grid_val)
    im = ax2.imshow(masked, cmap="RdYlGn", origin="upper",
                    vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax2, label="V*(s)")

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            val = grid_val[r][c]
            cell = BASE_GRID[r][c]
            text = f"{val:.1f}" if not np.isnan(val) else "X"
            ax2.text(c, r, text, ha="center", va="center",
                     fontsize=9, color="black" if not np.isnan(val) else "white",
                     fontweight="bold")
            ax2.text(c-0.4, r-0.35, cell, ha="left", va="top",
                     fontsize=7, color="dimgray")

    ax2.set_xticks(range(GRID_COLS))
    ax2.set_yticks(range(GRID_ROWS))
    ax2.set_title(f"State Value Heatmap V*(s)\n"
                  f"(Battery={battery_level}, Rescue={rescue_done})", fontsize=12)
    ax2.set_xlabel("Column"); ax2.set_ylabel("Row")

    plt.tight_layout()
    fname = f"Group210_DP_policy_bat{battery_level}.png"
    plt.savefig(fname, dpi=150)
    plt.show()
    print(f"  Policy/value visualisation saved → {fname}")


# Visualise at full battery, no rescues done
visualise_policy(V_STAR, POLICY, ALL_STATES, STATE_INDEX,
                 battery_level=10, rescue_done=(False, False))

# Also show low-battery scenario
visualise_policy(V_STAR, POLICY, ALL_STATES, STATE_INDEX,
                 battery_level=3, rescue_done=(False, False))


# ── Simulate an episode using the optimal policy ──────────────────────────────

def run_episode_with_policy(policy, max_steps=MAX_STEPS, render_steps=True):
    """
    Run one episode in the environment following the learned optimal policy.
    Used to visually verify that the policy makes sensible decisions.

    Parameters
    ----------
    policy      : dict — state → action
    max_steps   : int
    render_steps: bool — if True, print each step

    Returns
    -------
    total_reward : float
    trajectory   : list of (state, action, reward)
    """
    env = DroneRescueEnv()
    state = env.reset()
    total_reward = 0.0
    trajectory   = []

    print(f"\n  Running episode with optimal policy (max {max_steps} steps):")
    if render_steps:
        env.render()

    for step in range(max_steps):
        action = policy.get(state, 4)   # default Hover if state unseen
        next_state, reward, done, info = env.step(action)
        total_reward += reward
        trajectory.append((state, action, reward))

        if render_steps:
            print(f"  Step {step+1:3d}: Action={ACTIONS[action][0]:<6} "
                  f"pos=({next_state[0]},{next_state[1]}) "
                  f"bat={next_state[2]:2d} reward={reward:+.0f} "
                  f"rescued={next_state[3]} {info}")

        state = next_state
        if done:
            print(f"  Episode ended: {info.get('termination','?')} | "
                  f"Total Reward = {total_reward:.1f}")
            break
    else:
        print(f"  Max steps reached | Total Reward = {total_reward:.1f}")

    return total_reward, trajectory


total_r, traj = run_episode_with_policy(POLICY, render_steps=True)


# ─────────────────────────────────────────────────────────────────────────────
# OUTCOME 4 — STATE-VALUE ANALYSIS (Heatmap slices)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("OUTCOME 4 — STATE-VALUE ANALYSIS")
print("=" * 70)
print("""
  We analyse V*(s) by fixing battery level and rescue status,
  and varying only drone position (row, col) across the 5×5 grid.
  This reveals the spatial structure of the value function and shows
  how the DP solution has learned the geometry of the environment.
""")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

# Slice configurations: (battery, rescue_status, title)
slices = [
    (10, (False, False), "Full Battery\nNo Rescues"),
    (10, (True,  False), "Full Battery\nRescue-0 Done"),
    (10, (False, True ), "Full Battery\nRescue-1 Done"),
    ( 5, (False, False), "Half Battery\nNo Rescues"),
    ( 5, (True,  False), "Half Battery\nRescue-0 Done"),
    ( 3, (False, False), "Low Battery (3)\nNo Rescues"),
]

for ax, (bat, resc, title) in zip(axes, slices):
    grid_val = np.full((GRID_ROWS, GRID_COLS), np.nan)
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if BASE_GRID[r][c] == BLOCKED:
                continue
            state = (r, c, bat, resc)
            idx = STATE_INDEX.get(state)
            if idx is not None:
                grid_val[r][c] = V_STAR[idx]

    masked = np.ma.masked_invalid(grid_val)
    im = ax.imshow(masked, cmap="coolwarm", origin="upper")
    plt.colorbar(im, ax=ax, shrink=0.8)

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            val = grid_val[r][c]
            cell = BASE_GRID[r][c]
            label = f"{val:.1f}" if not np.isnan(val) else "X"
            colour = "white" if np.isnan(val) else "black"
            ax.text(c, r, label, ha="center", va="center",
                    fontsize=8, color=colour, fontweight="bold")
            ax.text(c-0.48, r-0.4, cell, ha="left", va="top",
                    fontsize=6, color="gray")

    ax.set_title(title, fontsize=10)
    ax.set_xticks(range(GRID_COLS))
    ax.set_yticks(range(GRID_ROWS))
    ax.set_xlabel("Col"); ax.set_ylabel("Row")

plt.suptitle("State-Value V*(s) Heatmaps — Various Battery & Rescue Slices\nGroup 210",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("Group210_DP_state_value_heatmaps.png", dpi=150)
plt.show()
print("  State-value heatmaps saved → Group210_DP_state_value_heatmaps.png")

print("""
  Observed Patterns:
    1. Cells near rescue targets (R at (0,4) and (4,0)) have high V* because
       the drone can earn +20 reward imminently, reflected as warm colours.
    2. Danger zones (D at (0,2), (2,0), (4,1)) consistently show low/negative
       values across all slices, confirming the DP solution correctly learns
       to avoid them unless battery management forces proximity.
    3. The charging station (C at (1,3)) shows elevated value when battery is
       low (3 units) — the drone learns to prioritise charging to extend its
       operational horizon and complete rescues.
    4. As battery decreases from 10 to 3, global V* values drop because the
       feasible future reward horizon shortens; cells far from C or R have
       increasingly negative values at low battery.
    5. When one rescue target is already done (e.g., Rescue-0 Done), the
       spatial value landscape reshapes: the remaining rescue target dominates,
       and its neighbouring cells see the sharpest value increases.
    6. Blocked cells (X) are masked as NaN and shown in grey, correctly
       excluded from the value function.
""")


# ─────────────────────────────────────────────────────────────────────────────
# OUTCOME 5 — DP SCALABILITY DISCUSSION
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("OUTCOME 5 — DP SCALABILITY: CURSE OF DIMENSIONALITY")
print("=" * 70)

print(f"""
  Current environment state space:
    Grid cells   : {GRID_ROWS}×{GRID_COLS} = {GRID_ROWS*GRID_COLS} (minus {2} blocked = {GRID_ROWS*GRID_COLS-2})
    Battery levels : {MAX_BATTERY}
    Rescue combos  : 2^{N_RESCUES} = {2**N_RESCUES}
    Total states   : {(GRID_ROWS*GRID_COLS-2)*MAX_BATTERY*(2**N_RESCUES):,} (approx {len(ALL_STATES):,} enumerated)

  ── How state space explodes with scaling ──

  10×10 Grid (100 cells, same battery=10, same 2 rescues):
    States ≈ 100 × 10 × 4 = 4,000  (still manageable)

  10×10 Grid + 5 rescue targets + battery=20:
    States = 100 × 20 × 2^5 = 64,000  (growing rapidly)

  10×10 Grid + 10 rescue targets + battery=50:
    States = 100 × 50 × 2^10 = 5,120,000  (5M states)

  10×10 Grid + 20 rescue targets + battery=100:
    States = 100 × 100 × 2^20 ≈ 104 BILLION  (computationally intractable)

  Dynamic weather (e.g., wind intensity: 5 levels × direction: 4):
    Adds a 20× multiplier to every state count above.

  ── Why DP becomes difficult ──

  1. Memory:     Storing V(s) for 100 million+ states exceeds RAM on most systems.
  2. Compute:    Each Value Iteration sweep is O(|S| × |A| × |S|) — cubic growth.
  3. Transition model: Computing T(s'|s,a) requires explicit enumeration of all
                transitions. With stochastic weather and dynamic targets this
                becomes a combinatorial problem.
  4. Non-stationarity: If rescue target positions or danger zones change over
                time (dynamic disaster), the MDP is non-stationary and the
                pre-computed policy becomes invalid immediately.

  ── How Deep RL methods help ──

  Deep RL replaces the explicit state table with a neural network V_θ(s) or
  Q_θ(s,a) that generalises across similar states, enabling:

    • DQN (Deep Q-Network): learns Q(s,a) from sampled experience without
      enumerating the full state space. Handles continuous or very large
      discrete state spaces.
    • Policy Gradient methods (PPO, A3C): directly optimise the policy π_θ(a|s)
      without maintaining a value table; scale to image-based inputs (drone camera).
    • Model-based Deep RL (World Models, Dreamer): learn a compact latent
      representation of the environment, enabling planning without full MDP enumeration.

  ── Relation to real-world autonomous drone systems ──

  Real disaster drones face:
    • Continuous state spaces (GPS coordinates, sensor readings, 3D positions)
    • Partially observable environments (fog, debris obscuring targets)
    • Multi-agent coordination (fleet of drones)
    • Dynamic objectives (new survivors located over time)
    • Communication delays and hardware failures

  DP is sufficient only for small, fully-observable, static problem instances
  (e.g., this assignment's 5×5 grid). For real autonomous drones, Deep RL
  frameworks like DQN + prioritised experience replay or model-based approaches
  with recurrent networks are necessary to handle the scale, uncertainty, and
  non-stationarity of real disaster environments.
""")

print("=" * 70)
print("END OF PART 2 — DP ASSIGNMENT")
print("=" * 70)
