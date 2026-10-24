"""Figure scripts for SEML Session 2: ML in Production."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Find the skill scripts directory
_candidates = [
    "/Users/jayakrishnanj/mtech/.claude/skills/make-lecture-kit/scripts",
    os.path.normpath(os.path.join(HERE, "../../../scripts")),
    os.path.normpath(os.path.join(HERE, "../../../../.claude/skills/make-lecture-kit/scripts")),
]
for _p in _candidates:
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
        break

import figstyle as F
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# -----------------------------------------------------------------------
# Figure 1: ML pipeline stages (flow diagram)
# -----------------------------------------------------------------------
F.flow(
    ["Data\nCollection", "Data\nCleaning", "Feature\nEngineering",
     "Model\nTraining", "Model\nEvaluation", "Deployment", "Monitoring"],
    "The 7-stage ML pipeline: data work dominates stages 1–4",
    out=os.path.join(HERE, "fig_pipeline.png"),
)

# -----------------------------------------------------------------------
# Figure 2: AI paradigms bar chart (autonomy spectrum)
# -----------------------------------------------------------------------
F.bars(
    ["Predictive AI", "Generative AI", "Agentic AI"],
    [1, 2, 3],
    "AI paradigm spectrum: autonomy and complexity grow left to right",
    xlabel="Paradigm",
    ylabel="Autonomy level (relative)",
    fmt="{:.0f}",
    out=os.path.join(HERE, "fig_ai_paradigms.png"),
)

# -----------------------------------------------------------------------
# Figure 3: Apollo multi-model pipeline (flow)
# -----------------------------------------------------------------------
F.flow(
    ["Camera /\nLiDAR input", "Object\nDetection", "Classification\n& Tracking",
     "Sensor\nFusion", "Trajectory\nPrediction", "Motion\nPlanning",
     "Vehicle\nControl"],
    "Apollo’s 7-stage perception pipeline: 28 ML models work in sequence",
    out=os.path.join(HERE, "fig_apollo_pipeline.png"),
)

# -----------------------------------------------------------------------
# Figure 4: Microsoft 9-stage workflow (flow)
# -----------------------------------------------------------------------
F.flow(
    ["Model\nRequirements", "Data\nCollection", "Data\nCleaning",
     "Data\nLabelling", "Feature\nEng.", "Model\nTraining",
     "Model\nEvaluation", "Deployment", "Monitoring"],
    "Microsoft’s 9-stage ML workflow: stages 1–5 are all data work",
    out=os.path.join(HERE, "fig_ms_workflow.png"),
)

# -----------------------------------------------------------------------
# Figure 5: ML code fraction (hidden technical debt)
# -----------------------------------------------------------------------
F.bars(
    ["ML model\ncode", "Infrastructure\n(hidden)"],
    [5, 95],
    "ML code is only ~5% of a real production system (Sculley et al., 2015)",
    xlabel="System component",
    ylabel="Approximate % of codebase",
    fmt="{:.0f}%",
    out=os.path.join(HERE, "fig_ml_fraction.png"),
)

# -----------------------------------------------------------------------
# Figure 6: Production gap challenges (bar chart)
# -----------------------------------------------------------------------
F.bars(
    ["Noisy data", "Latency", "Cloud cost", "Pipeline\nfragility",
     "Team gaps", "Monitoring", "Fairness"],
    [3, 4, 4, 3, 2, 3, 2],
    "Seven production challenges Sidney faces: latency and cost hit hardest",
    xlabel="Challenge",
    ylabel="Severity (1 = minor, 4 = critical)",
    fmt="{:.0f}",
    out=os.path.join(HERE, "fig_production_gap.png"),
)

# -----------------------------------------------------------------------
# Figure 7: ML vs non-ML component roles (comparison bars)
# -----------------------------------------------------------------------
F.bars(
    ["Speech\ntranscription", "Tax audit\nrisk tool", "E-commerce\nrecommender"],
    [90, 20, 70],
    "ML component share by product type: some products are mostly ML, others are not",
    xlabel="Product",
    ylabel="Approximate % of product that is ML",
    fmt="{:.0f}%",
    out=os.path.join(HERE, "fig_ml_component_share.png"),
)
