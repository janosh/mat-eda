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
from matminer.datasets import load_dataset
from pymatgen.ext.matproj import MPRester
from pymatviz import annotate_bars, ptable_heatmap, spacegroup_hist
from tqdm import tqdm


# %%
df_phonon = load_dataset("matbench_phonons")

df_phonon[["spg_symbol", "spg_num"]] = [
    struct.get_space_group_info() for struct in tqdm(df_phonon.structure)
]


# %%
df_phonon.hist(column="last phdos peak", bins=50)
plt.savefig("phonons-last-dos-peak-hist.pdf")


# %%
df_phonon["formula"] = df_phonon.structure.apply(lambda cryst: cryst.formula)
df_phonon["volume"] = df_phonon.structure.apply(lambda cryst: cryst.volume)

ptable_heatmap(df_phonon.formula, log=True)
plt.title("Elemental prevalence in the Matbench phonons dataset")
plt.savefig("phonons-ptable-heatmap.pdf")


# %%
mpr = MPRester()
df_phonon["likely_mp_ids"] = [mpr.find_structure(x) for x in tqdm(df_phonon.structure)]


# %%
ax = df_phonon.likely_mp_ids.apply(len).value_counts().plot(kind="bar", log=True)
annotate_bars()
plt.savefig("likely_mp_ids_lens.pdf")


# %% where there are several mp_ids, pick the one with lowest energy above convex hull
def get_e_above_hull(mp_id: str) -> float:
    return mpr.query(mp_id, ["e_above_hull"])["e_above_hull"]


df_phonon["es_above_hull"] = df_phonon.likely_mp_ids.apply(
    lambda ids: [get_e_above_hull(id) for id in ids]
)

df_phonon["likely_mp_id"] = df_phonon.apply(
    lambda row: row.likely_mp_ids[np.argmin(row.es_above_hull)], axis=1
)


# %%
spacegroup_hist(df_phonon.spg_num)
plt.savefig("phonons-spacegroup-hist.pdf")
