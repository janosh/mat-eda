"""Stats for the matbench_phonons dataset.

Input: Pymatgen Structure of the material.
Target variable: Frequency of the highest frequency optical phonon mode peak
    in units of 1/cm; may be used as an estimation of dominant longitudinal
    optical phonon frequency.
Entries: 1265

Matbench v0.1 dataset for predicting vibration properties from crystal structure.
Original data retrieved from Petretto et al. Original calculations done via ABINIT
in the harmonic approximation based on density functional perturbation theory.
Removed entries having a formation energy (or energy above the convex hull) more
than 150meV.

https://ml.materialsproject.org/projects/matbench_phonons
"""


# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matminer.datasets import load_dataset
from matminer.utils.io import load_dataframe_from_json, store_dataframe_as_json
from pymatgen.ext.matproj import MPRester
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatviz import annotate_bar_heights, ptable_heatmap, spacegroup_hist
from tqdm import tqdm


tqdm.pandas()


# %%
tqdm.pandas()
phonons = load_dataset("matbench_phonons")


# %%
phonons.hist(column="last phdos peak", bins=50)
plt.savefig("phonons-last-dos-peak-hist.pdf")


# %%
phonons["formula"] = phonons.structure.apply(lambda cryst: cryst.formula)
phonons["volume"] = phonons.structure.apply(lambda cryst: cryst.volume)

ptable_heatmap(phonons.formula, log=True)
plt.title("Elemental prevalence in the Matbench phonons dataset")
plt.savefig("phonons-elements-log.pdf")


# %%
mpr = MPRester()
phonons["likely_mp_ids"] = phonons.structure.progress_apply(mpr.find_structure)


# %%
ax = phonons.likely_mp_ids.apply(len).value_counts().plot(kind="bar", log=True)
annotate_bar_heights()
plt.savefig("likely_mp_ids_lens.png", dpi=200)


# %% where there are several mp_ids, pick the one with lowest energy above convex hull
def get_e_above_hull(mp_id: str) -> float:
    return mpr.query(mp_id, ["e_above_hull"])["e_above_hull"]


phonons["es_above_hull"] = phonons.likely_mp_ids.progress_apply(
    lambda ids: [get_e_above_hull(id) for id in ids]
)

phonons["likely_mp_id"] = phonons.apply(
    lambda row: row.likely_mp_ids[np.argmin(row.es_above_hull)], axis=1
)


# %%
cols = ["structure", "last phdos peak", "likely_mp_id"]
store_dataframe_as_json(phonons[cols], "matbench-phonons-with-mp-id.json.gz")

phonons[cols] = load_dataframe_from_json("matbench-phonons-with-mp-id.json.gz")


# %%
phonons[["sg_symbol", "sg_number"]] = phonons.progress_apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

phonons["crystal_system"] = phonons.structure.progress_apply(
    lambda struct: SpacegroupAnalyzer(struct).get_crystal_system()
)

phonons[["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]].to_csv(
    "additional-df-cols.csv", index=False
)


# %%
phonons[
    ["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]
] = pd.read_csv("additional-df-cols.csv")


# %%
spacegroup_hist(phonons.sg_number)
plt.savefig("phonons-spacegroup-hist.pdf")
