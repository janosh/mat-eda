"""Stats for the matbench_expt_gap dataset.

Input: Chemical formula.
Target variable: Experimentally measured band gap (E_g) in eV.
Entries: 4604

- https://ml.materialsproject.org/projects/matbench_expt_gap
"""

# %%
import matplotlib.pyplot as plt
from matminer.utils.io import load_dataframe_from_json
from mlmatrics import ptable_elemental_prevalence

# %%
expt_gap = load_dataframe_from_json("../../data/expt_gap.json.gz")


# %%
expt_gap.hist(column="gap expt", bins=50, log=True)
plt.savefig("expt_gap_hist.pdf")


# %%
ptable_elemental_prevalence(expt_gap.composition, log=True)
plt.savefig("expt_gap-elements-log.pdf")
