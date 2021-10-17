"""Stats for the matbench_mp_e_form dataset.

Input: Pymatgen Structure of the material.
Target variable: Formation energy in eV as calculated by the Materials Project.
Entries: 132,752

Adapted from Materials Project database. Removed entries having
formation energy more than 3.0eV and those containing noble gases.
Retrieved April 2, 2019.

https://ml.materialsproject.org/projects/matbench_mp_e_form
"""


# %%
import matplotlib.pyplot as plt
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_heatmap


# %%
mp_e_form = load_dataframe_from_json("../../data/mp_e_form.json.gz")


# %%
mp_e_form.hist(column="e_form", bins=50, log=True)
plt.savefig("mp_e_form_hist.pdf")


# %%
mp_e_form["formula"] = mp_e_form.structure.apply(lambda struct: struct.formula)


# %%
ptable_heatmap(mp_e_form.formula, log=True)
plt.title("Elemental prevalence in the Matbench formation energy dataset")
plt.savefig("mp_e_form-elements-log.pdf")
