"""Stats for the matbench_log_gvrh and matbench_log_kvrh datasets.

Input: Pymatgen Structure of the material.
Target variable(s): Base 10 logarithm of the DFT Voigt-Reuss-Hill average shear (g_vrh)
    and bulk (k_vrh) moduli in GPa.
Entries: 10987 (each)

https://ml.materialsproject.org/projects/matbench_log_gvrh
https://ml.materialsproject.org/projects/matbench_log_kvrh
"""


# %%
from time import perf_counter

import matplotlib.pyplot as plt
import nglview as nv
import numpy as np
import pandas as pd
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_heatmap, spacegroup_hist
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from tqdm import tqdm


# %%
log_gvrh = load_dataframe_from_json("../../data/log_gvrh.json.gz")
log_kvrh = load_dataframe_from_json("../../data/log_kvrh.json.gz")

tqdm.pandas()


# %%
print("Number of materials with shear modulus of 0:")
print(sum(log_gvrh["log10(G_VRH)"] == 0))  # sum is 31


# %%
print("Number of materials with bulk modulus of 0:")
print(sum(log_kvrh["log10(K_VRH)"] == 0))  # sum is 14


# %%
ax = log_kvrh.hist(column="log10(K_VRH)", bins=50, alpha=0.8)

log_gvrh.hist(column="log10(G_VRH)", bins=50, ax=ax, alpha=0.8)
plt.savefig("log_g+kvrh-target-hist.pdf")


# %%
log_gvrh["volume"] = log_gvrh.structure.apply(lambda struct: struct.volume)

log_gvrh.hist(column="volume", bins=50, log=True, alpha=0.8)
plt.savefig("log_gvrh-volume-hist.pdf")


# %%
start = perf_counter()
radius = 5
log_gvrh[f"neighbor_list_r{radius}"] = log_gvrh.structure.apply(
    lambda crystal: crystal.get_neighbor_list(r=radius),
)
print(f"took {perf_counter() - start:.3f} sec")

log_kvrh[f"neighbor_list_r{radius}"] = log_kvrh.structure.apply(
    lambda crystal: crystal.get_neighbor_list(r=radius),
)


# %%
start = perf_counter()


def has_isolated_atom(crystal: Structure, radius: float = 5) -> bool:
    dists = crystal.distance_matrix
    np.fill_diagonal(dists, np.inf)
    return (dists.min(1) > radius).any()


log_gvrh["isolated_r5"] = log_gvrh.structure.apply(has_isolated_atom)
print(f"took {perf_counter() - start:.3f} sec")


# %%
log_gvrh["graph_size"] = log_gvrh[f"neighbor_list_r{radius}"].apply(
    lambda lst: len(lst[0])
)


# %%
for idx, (structure, target, *_) in log_gvrh[log_gvrh.graph_size == 0].iterrows():
    print(f"\n{idx = }")
    print(f"{structure = }")
    print(f"{target = }")


# %%
structure.make_supercell([2, 2, 2])
view = nv.show_pymatgen(structure)
view.add_unitcell()
structure.get_primitive_structure()
view


# %%
log_gvrh["volume"] = log_gvrh.structure.apply(lambda struct: struct.volume)

log_gvrh.hist(column="volume", bins=50, log=True)


# %%
log_gvrh["formula"] = log_gvrh.structure.apply(lambda struct: struct.formula)

ptable_heatmap(log_gvrh.formula, log=True)
plt.title("Elemental prevalence in the Matbench bulk/shear modulus datasets")
plt.savefig("log_gvrh-elements-log.pdf")


# %% getting space group symbols and numbers for 10,987 structures takes about 4 min
print("getting spacegroups for log_gvrh")
log_gvrh[["sg_symbol", "sg_number"]] = log_gvrh.progress_apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

print("getting crystal systems for log_gvrh")
log_gvrh["crystal_system"] = log_gvrh.structure.progress_apply(
    lambda struct: SpacegroupAnalyzer(struct).get_crystal_system()
)

log_gvrh[["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]].to_csv(
    "additional-df-cols.csv", index=False
)


# %%
log_gvrh[
    ["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]
] = pd.read_csv("additional-df-cols.csv")


# %%
spacegroup_hist(log_gvrh.sg_number)
plt.savefig("log_gvrh-spacegroup-hist.pdf")


# %%
log_gvrh.crystal_system.value_counts().plot.pie(autopct="%1.1f%%")
