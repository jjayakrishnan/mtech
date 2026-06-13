"""
Submarine Navigation Agent — A* Informed Search
================================================
Assignment 1 | PS2 | AIMLCZG557 / AECLZG557
S2 2025-2026 | BITS Pilani WILP Division

Problem:
  Guide a submarine from a start cell to a goal cell on an ocean grid,
  minimising total movement cost while respecting terrain constraints:
    - Thermal Vents (T)  : impassable (hard wall)
    - Sonar Blackout (B) : avoid if any alternative path exists
    - Coral Reef (R)     : entry cost = 2   (double normal)
    - Current Corridor(C): entry cost = 0.5 (half normal)
    - Deep Trench (D)    : entry cost = 3   (1 base + 2 overhead)
    - Open Water (O)     : entry cost = 1
"""

import heapq
import itertools
import sys

# ─── Terrain cost table ───────────────────────────────────────────────────────

TERRAIN_COST = {
    'S': 1.0,            # Start cell — treated as Open Water
    'G': 1.0,            # Goal cell  — treated as Open Water
    'O': 1.0,            # Open Water
    'R': 2.0,            # Coral Reef   (double normal cost)
    'C': 0.5,            # Current Corridor (half normal cost)
    'D': 3.0,            # Deep Trench  (1 base + 2 fixed overhead)
    'T': float('inf'),   # Thermal Vent — ALWAYS BLOCKED
    'B': float('inf'),   # Sonar Blackout — blocked in primary pass
}

TERRAIN_NAME = {
    'S': 'Open Water (Start)',
    'G': 'Open Water (Goal)',
    'O': 'Open Water',
    'R': 'Coral Reef',
    'C': 'Current Corridor',
    'D': 'Deep Trench',
    'T': 'Thermal Vent (Blocked)',
    'B': 'Sonar Blackout Zone',
}

# 8-directional movement (4 orthogonal + 4 diagonal)
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

_TIEBREAK = itertools.count()   # breaks equal f-score ties in the heap


# ─── Heuristic ────────────────────────────────────────────────────────────────

def heuristic(pos, goal):
    """
    Chebyshev distance × 0.5 (minimum possible step cost).

    Admissible  : Chebyshev gives the fewest 8-directional steps needed;
                  every step costs at least 0.5 (Current Corridor), so
                  h(n) never overestimates the true remaining cost.

    Consistent  : For any move n → n',  h(n) ≤ cost(n,n') + h(n')
                  because Chebyshev satisfies the triangle inequality.
    """
    return max(abs(pos[0] - goal[0]), abs(pos[1] - goal[1])) * 0.5


# ─── Grid utilities ───────────────────────────────────────────────────────────

def entry_cost(symbol, sonar_ok=False):
    """Cost of entering a cell. Returns inf when the cell is impassable."""
    if symbol == 'B':
        return 1.0 if sonar_ok else float('inf')
    return TERRAIN_COST.get(symbol, 1.0)


def neighbours(row, col, rows, cols):
    """Yield in-bounds 8-directional neighbours of (row, col)."""
    for dr, dc in DIRECTIONS:
        r2, c2 = row + dr, col + dc
        if 0 <= r2 < rows and 0 <= c2 < cols:
            yield r2, c2


# ─── A* search ────────────────────────────────────────────────────────────────

def astar(grid, start, goal, rows, cols, sonar_ok=False):
    """
    A* graph search on the ocean grid.

    Args:
        grid      : 2-D list of terrain symbols (strings)
        start     : (row, col) tuple of the start position
        goal      : (row, col) tuple of the goal position
        rows,cols : grid dimensions
        sonar_ok  : if True, Sonar Blackout (B) cells are traversable (cost=1)

    Returns:
        (path, total_cost) where path is an ordered list of (row,col) tuples,
        or (None, inf) when the goal is unreachable.
    """
    h0 = heuristic(start, goal)
    # Heap entries: (f_score, tie, g_score, position, path_so_far)
    heap = [(h0, next(_TIEBREAK), 0.0, start, [start])]
    best_g = {start: 0.0}

    while heap:
        f, _, g, pos, path = heapq.heappop(heap)

        if pos == goal:
            return path, g

        # Skip stale entry — we already found a cheaper route to pos
        if g > best_g.get(pos, float('inf')):
            continue

        for r2, c2 in neighbours(pos[0], pos[1], rows, cols):
            cost = entry_cost(grid[r2][c2], sonar_ok)
            if cost == float('inf'):
                continue
            ng = g + cost
            if ng < best_g.get((r2, c2), float('inf')):
                best_g[(r2, c2)] = ng
                nf = ng + heuristic((r2, c2), goal)
                heapq.heappush(
                    heap,
                    (nf, next(_TIEBREAK), ng, (r2, c2), path + [(r2, c2)])
                )

    return None, float('inf')


# ─── Two-pass navigation ──────────────────────────────────────────────────────

def navigate(grid, start, goal, rows, cols):
    """
    Pass 1 — treat Sonar Blackout as impassable (preferred safe route).
    Pass 2 — allow Sonar Blackout only when no safe route exists.

    Returns (path, total_cost, sonar_used).
    """
    path, cost = astar(grid, start, goal, rows, cols, sonar_ok=False)
    if path is not None:
        return path, cost, False

    path, cost = astar(grid, start, goal, rows, cols, sonar_ok=True)
    return path, cost, True


# ─── Input parsing ────────────────────────────────────────────────────────────

def read_input(filename):
    """
    Parse the input file.

    Required fields (order-independent, keys case-insensitive):
        GridSize: <rows> <cols>
        Source: <row> <col>
        Destination: <row> <col>
        Grid:
        <symbol> <symbol> ...    (one grid row per file line)
    """
    try:
        with open(filename) as fh:
            lines = [ln.strip() for ln in fh if ln.strip()]
    except FileNotFoundError:
        print(f"ERROR: Input file '{filename}' not found.")
        sys.exit(1)

    grid_size = source = dest = None
    grid = []
    in_grid = False

    for line in lines:
        upper = line.upper()
        val   = line.split(':', 1)[1].strip() if ':' in line else ''

        if upper.startswith('GRIDSIZE:'):
            parts = val.split()
            if len(parts) < 2:
                print("ERROR: GridSize must provide two integers (rows cols).")
                sys.exit(1)
            grid_size = (int(parts[0]), int(parts[1]))

        elif upper.startswith('SOURCE:'):
            coords = val.replace('(','').replace(')','').replace(',',' ').split()
            if len(coords) < 2:
                print("ERROR: Source must provide two integers (row col).")
                sys.exit(1)
            source = (int(coords[0]), int(coords[1]))

        elif upper.startswith('DESTINATION:'):
            coords = val.replace('(','').replace(')','').replace(',',' ').split()
            if len(coords) < 2:
                print("ERROR: Destination must provide two integers (row col).")
                sys.exit(1)
            dest = (int(coords[0]), int(coords[1]))

        elif upper.startswith('GRID:'):
            in_grid = True

        elif in_grid:
            row_syms = upper.split()
            if row_syms:
                grid.append(row_syms)

    # ── Field presence check ──
    errors = []
    if grid_size is None: errors.append("Missing 'GridSize' field.")
    if source    is None: errors.append("Missing 'Source' field.")
    if dest      is None: errors.append("Missing 'Destination' field.")
    if not grid:          errors.append("Missing 'Grid' section.")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)

    rows, cols = grid_size

    # ── Dimension check ──
    if len(grid) != rows:
        print(f"ERROR: Grid has {len(grid)} rows; GridSize specifies {rows}.")
        sys.exit(1)
    for i, r in enumerate(grid):
        if len(r) != cols:
            print(f"ERROR: Row {i} has {len(r)} cells; GridSize specifies {cols}.")
            sys.exit(1)

    # ── Bounds check ──
    sr, sc = source
    dr, dc = dest
    if not (0 <= sr < rows and 0 <= sc < cols):
        print(f"ERROR: Source {source} is outside the {rows}×{cols} grid.")
        sys.exit(1)
    if not (0 <= dr < rows and 0 <= dc < cols):
        print(f"ERROR: Destination {dest} is outside the {rows}×{cols} grid.")
        sys.exit(1)

    # ── Impassable start/goal check ──
    if grid[sr][sc] == 'T':
        print("ERROR: Source cell is a Thermal Vent — impassable.")
        sys.exit(1)
    if grid[dr][dc] == 'T':
        print("ERROR: Destination cell is a Thermal Vent — impassable.")
        sys.exit(1)

    return grid_size, source, dest, grid


# ─── Output formatting ────────────────────────────────────────────────────────

def display_grid(grid, path_set, rows, cols):
    """Print the grid to stdout, marking path cells with brackets."""
    print("\nGrid layout  ( [X] = path cell ):")
    print("     " + "  ".join(f"{c}" for c in range(cols)))
    for r in range(rows):
        row_str = f"  {r}  "
        for c in range(cols):
            sym = grid[r][c]
            row_str += f"[{sym}]" if (r, c) in path_set else f" {sym} "
        print(row_str)
    print()


def build_report(path, grid, total_cost, sonar_used):
    """Return the formatted result string (printed and saved to file)."""
    SEP = "=" * 70
    lines = [SEP,
             "   SUBMARINE NAVIGATION  —  A* SEARCH RESULTS",
             SEP, ""]

    if sonar_used:
        lines += [
            "  WARNING: No sonar-free path exists.",
            "           Path traverses Sonar Blackout Zone(s).",
            ""
        ]

    lines.append("  Best Path:")
    lines.append("  " + " -> ".join(f"({r},{c})" for r, c in path))
    lines.append("")

    lines.append("  Step-by-step breakdown:")
    hdr = (f"  {'Step':<6}  {'Cell':<9}  {'Terrain Type':<28}"
           f"  {'Step Cost':>10}  {'Cumul. Cost':>12}")
    lines += [hdr, "  " + "-" * (len(hdr) - 2)]

    cumul = 0.0
    for i, (r, c) in enumerate(path):
        sym   = grid[r][c]
        scost = 0.0 if i == 0 else (1.0 if sym == 'B' else TERRAIN_COST.get(sym, 1.0))
        cumul += scost
        lines.append(
            f"  {i:<6}  ({r},{c}){'':<4}  {TERRAIN_NAME.get(sym, sym):<28}"
            f"  {scost:>10.1f}  {cumul:>12.1f}"
        )

    lines += [
        "",
        f"  Total Grid Cells Traversed : {len(path)}",
        f"  Total Movement Cost        : {total_cost}",
        SEP
    ]
    return "\n".join(lines)


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    INPUT_FILE  = 'inputPS2.txt'
    OUTPUT_FILE = 'outputPS2.txt'

    # ── Load problem ──
    (rows, cols), start, goal, grid = read_input(INPUT_FILE)

    print(f"Grid Size   : {rows} x {cols}")
    print(f"Source      : {start}")
    print(f"Destination : {goal}")

    # ── Run A* ──
    path, total_cost, sonar_used = navigate(grid, start, goal, rows, cols)

    if path is None:
        msg = ("ERROR: Destination is completely unreachable "
               "(all routes are blocked by Thermal Vents).")
        print(msg)
        with open(OUTPUT_FILE, 'w') as fh:
            fh.write(msg + "\n")
        sys.exit(0)

    # ── Console output ──
    display_grid(grid, set(path), rows, cols)
    report = build_report(path, grid, total_cost, sonar_used)
    print(report)

    # ── File output ──
    with open(OUTPUT_FILE, 'w') as fh:
        fh.write(report + "\n")
    print(f"\nOutput saved to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
