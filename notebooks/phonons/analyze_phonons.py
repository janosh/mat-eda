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
from matminer.utils.io import load_dataframe_from_json, store_dataframe_as_json
from mlmatrics import (
    annotate_bar_heights,
    ptable_elemental_prevalence,
    spacegroup_hist,
)
from pymatgen.ext.matproj import MPRester
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from tqdm import tqdm

tqdm.pandas()


# %%
tqdm.pandas()
phonons = load_dataframe_from_json("../../data/phonons.json.gz")


# %%
phonons.hist(column="last phdos peak", bins=50)
plt.savefig("phonons-last-dos-peak-hist.pdf")


# %%
phonons["formula"] = phonons.structure.apply(lambda cryst: cryst.formula)
phonons["volume"] = phonons.structure.apply(lambda cryst: cryst.volume)

ptable_elemental_prevalence(phonons.formula, log=True)
plt.savefig("phonons-elements-log.pdf")


# %%
mpr = MPRester()
phonons["likely_mp_ids"] = phonons.structure.progress_apply(mpr.find_structure)


# %%
ax = phonons.likely_mp_ids.apply(len).value_counts().plot(kind="bar", log=True)
annotate_bar_heights()
plt.savefig("likely_mp_ids_lens.png", dpi=200)


# %% where there are several mp_ids, pick the one with lowest energy above the convex hull
def get_e_above_hull(mp_id):
    return mpr.query(mp_id, ["e_above_hull"])["e_above_hull"]


phonons["es_above_hull"] = phonons.likely_mp_ids.progress_apply(
    lambda ids: [get_e_above_hull(id) for id in ids]
)

phonons["likely_mp_id"] = phonons.apply(
    lambda row: row.likely_mp_ids[np.argmin(row.es_above_hull)], axis=1
)


# %%
store_dataframe_as_json(
    phonons[["structure", "last phdos peak", "likely_mp_id"]],
    "matbench-phonons-with-mp-id.json.gz",
    compression="gz",
)


# %% sort of a dumb test but check for 5 % of entries that
# formulas of first found and original structures match
for _, (struc, _, id) in phonons.sample(frac=0.05).iterrows():
    print(f"{id=}")
    struc = mpr.get_structure_by_material_id(phonons["likely_mp_id"].iloc[0])
    assert struc.formula == phonons.structure.iloc[0].formula


# %%
phonons[["sg_symbol", "sg_number"]] = phonons.progress_apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

phonons["crystal_system"] = phonons.structure.progress_apply(
    lambda struc: SpacegroupAnalyzer(struc).get_crystal_system()
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
