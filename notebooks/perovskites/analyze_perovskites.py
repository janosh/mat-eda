"""Stats for the matbench_perovskites dataset.

Input: Pymatgen Structure of the material.
Target variable: Heat of formation of the entire 5-atom perovskite cell in eV
    as calculated by RPBE GGA-DFT. Note the reference state for oxygen was
    computed from oxygen's chemical potential in water vapor, not as oxygen
    molecules, to reflect the application which these perovskites were studied for.
Entries: 18,928

Matbench v0.1 dataset for predicting formation energy from crystal structure.
Adapted from an original dataset generated by Castelli et al.

https://ml.materialsproject.org/projects/matbench_perovskites
"""


# %%
import matplotlib.pyplot as plt
import pandas as pd
from matminer.datasets import load_dataset
from ml_matrics import annotate_bar_heights, ptable_heatmap, spacegroup_hist
from pymatgen.ext.matproj import MPRester
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from tqdm import tqdm


# %%
tqdm.pandas()
perovskites = load_dataset("matbench_perovskites")


# %%
perovskites.hist(column="e_form", bins=50)
plt.savefig("perovskites-e_form-hist.pdf")


# %%
perovskites["formula"] = perovskites.structure.apply(lambda cryst: cryst.formula)

ptable_heatmap(perovskites.formula, log=True)
plt.title("Elemental prevalence in the Matbench perovskites dataset")
plt.savefig("perovskites-elements-log.pdf")


# %%
perovskites["volume"] = perovskites.structure.apply(lambda struct: struct.volume)

perovskites.hist(column="volume", bins=50, log=True)


# %%
mpr = MPRester()
perovskites["likely_mp_ids"] = perovskites.structure.progress_apply(mpr.find_structure)


# %%
mp_ids = perovskites.likely_mp_ids.explode().value_counts().index.to_list()

es_above_hull = mpr.query({"material_id": {"$in": mp_ids}}, ["e_above_hull"])


# %%
ax = perovskites.likely_mp_ids.apply(len).value_counts().plot(kind="bar", log=True)
annotate_bar_heights()
plt.savefig("likely_mp_ids_lens.pdf")


# %%
perovskites[["sg_symbol", "sg_number"]] = perovskites.progress_apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

perovskites["crystal_system"] = perovskites.structure.progress_apply(
    lambda struct: SpacegroupAnalyzer(struct).get_crystal_system()
)

perovskites[["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]].to_csv(
    "additional-df-cols.csv", index=False
)


# %%
perovskites[
    ["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]
] = pd.read_csv("additional-df-cols.csv")


# %%
spacegroup_hist(perovskites.sg_number)
plt.savefig("perovskites-spacegroup-hist.pdf")


# %%
perovskites["crystal_system"].value_counts().plot.bar()

plt.title("Crystal systems in Matbench Perovskites")
plt.xticks(rotation="horizontal")

annotate_bar_heights(voffset=250)

plt.savefig("perovskites-crystal-system-counts.pdf")


# %%
perovskites.plot.scatter(x="volume", y="e_form", c="sg_number", colormap="viridis")


# %%
perovskites.value_counts(["crystal_system", "sg_number"]).sort_index().plot.pie(
    autopct="%1.1f%%"
)

plt.title("Crystal systems and space groups in Matbench Perovskites")
plt.ylabel(None)
plt.savefig("perovskites-crystal-system-pie.pdf")
