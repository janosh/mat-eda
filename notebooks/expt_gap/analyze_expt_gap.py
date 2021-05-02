"""Stats for the matbench_expt_gap dataset.

Input: Chemical formula.
Target variable: Experimentally measured band gap (E_g) in eV.
Entries: 4604

Matbench v0.1 dataset for predicting experimental band gaps from composition alone.
Retrieved from Zhuo et al. supplementary information. Deduplicated according to
composition, removing compositions with reported band gaps spanning more than a 0.1 eV
range; remaining compositions were assigned values based on the closest experimental
value to the mean experimental value for that composition among all reports.

To get likely MP IDs for each chemical formula, see https://git.io/JmpVe:

Likely mp-ids were chosen from among computed materials in the MP database (version 2021.03)
that were 1) not marked 'theoretical', 2) had structures matching at least one ICSD material,
and 3) were within 200 meV of the DFT-computed stable energy hull (e_above_hull < 0.2 eV).
Among these candidates, we chose the mp-id with the lowest e_above_hull.

https://ml.materialsproject.org/projects/matbench_expt_gap
"""


# %%
import matplotlib.pyplot as plt
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_elemental_prevalence


# %%
expt_gap = load_dataframe_from_json("../../data/expt_gap.json.gz")


# %%
expt_gap.hist(column="gap expt", bins=50, log=True)
plt.savefig("expt_gap_hist.pdf")


# %%
ptable_elemental_prevalence(expt_gap.composition, log=True)
plt.title("Elemental prevalence in the Matbench experimental band gap dataset")
plt.savefig("expt_gap-elements-log.pdf")
