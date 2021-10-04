"""Stats for the matbench_steels dataset.

Input: Chemical formula.
Target variable: Experimentally measured steel yield strengths in MPa.
Entries: 312

https://ml.materialsproject.org/projects/matbench_steels
"""


# %%
import matplotlib.pyplot as plt
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_heatmap


# %%
steels = load_dataframe_from_json("../../data/steels.json.gz")


# %%
steels.hist(column="yield strength", bins=50)
plt.savefig("steels-yield-strength-hist.pdf")


# %%
ptable_heatmap(steels.composition, log=True)
plt.title("Elemental prevalence in the Matbench steels dataset")
plt.savefig("steels-elements-log.pdf")
