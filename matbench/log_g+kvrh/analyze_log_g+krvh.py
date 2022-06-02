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
import numpy as np
from aviary.wren.utils import count_wyks, get_aflow_label_spglib
from matminer.datasets import load_dataset
from pymatgen.core import Structure
from pymatviz import ptable_heatmap, spacegroup_hist, spacegroup_sunburst
from pymatviz.utils import get_crystal_sys
from tqdm import tqdm


plt.rc("font", size=14)
plt.rc("savefig", bbox="tight", dpi=200)
plt.rc("axes", titlesize=16, titleweight="bold")
plt.rcParams["figure.constrained_layout.use"] = True


# %%
df_grvh = load_dataset("matbench_log_gvrh")
df_kvrh = load_dataset("matbench_log_kvrh")

# getting space group symbols and numbers for 10,987 structures takes about 45 sec
df_grvh[["spg_symbol", "spg_num"]] = [
    struct.get_space_group_info()
    for struct in tqdm(df_grvh.structure, desc="Getting matbench_log_gvrh spacegroups")
]
df_grvh["crystal_sys"] = [get_crystal_sys(x) for x in df_grvh.spg_num]

df_grvh["wyckoff"] = [
    get_aflow_label_spglib(struct)
    for struct in tqdm(df_grvh.structure, desc="Getting Wyckoff strings for log_gvrh")
]
df_grvh["n_wyckoff"] = df_grvh.wyckoff.map(count_wyks)
df_grvh["formula"] = [x.formula for x in df_grvh.structure]


# %%
print("Number of materials with shear modulus of 0:")
print(sum(df_grvh["log10(G_VRH)"] == 0))  # sum is 31


# %%
print("Number of materials with bulk modulus of 0:")
print(sum(df_kvrh["log10(K_VRH)"] == 0))  # sum is 14


# %%
ax = df_kvrh.hist(column="log10(K_VRH)", bins=50, alpha=0.8)

df_grvh.hist(column="log10(G_VRH)", bins=50, ax=ax, alpha=0.8)
plt.savefig("log_g+kvrh-target-hist.pdf")


# %%
df_grvh["volume"] = [x.volume for x in df_grvh.structure]
df_grvh["formula"] = [x.formula for x in df_grvh.structure]

df_grvh.hist(column="volume", bins=50, log=True, alpha=0.8)
plt.savefig("log_gvrh-volume-hist.pdf")


# %%
start = perf_counter()
radius = 5
df_grvh[f"neighbor_list_r{radius}"] = [
    x.get_neighbor_list(r=radius) for x in df_grvh.structure
]
print(f"took {perf_counter() - start:.3f} sec")

df_kvrh[f"neighbor_list_r{radius}"] = [
    x.get_neighbor_list(r=radius) for x in df_kvrh.structure
]


# %%
start = perf_counter()


def has_isolated_atom(crystal: Structure, radius: float = 5) -> bool:
    dists = crystal.distance_matrix
    np.fill_diagonal(dists, np.inf)
    return (dists.min(1) > radius).any()


df_grvh["isolated_r5"] = df_grvh.structure.apply(has_isolated_atom)
print(f"took {perf_counter() - start:.3f} sec")


# %%
df_grvh["graph_size"] = df_grvh[f"neighbor_list_r{radius}"].apply(
    lambda lst: len(lst[0])
)


# %%
for idx, structure, target, *_ in df_grvh.query("graph_size == 0").itertuples():
    print(f"\n{idx = }")
    print(f"{structure = }")
    print(f"{target = }")


# %%
df_grvh["volume"] = df_grvh.structure.apply(lambda struct: struct.volume)

df_grvh.hist(column="volume", bins=50, log=True)


# %%
df_grvh["formula"] = df_grvh.structure.apply(lambda struct: struct.formula)

ptable_heatmap(df_grvh.formula, log=True)
plt.title("Elemental prevalence in the Matbench bulk/shear modulus datasets")
plt.savefig("log_gvrh-ptable-heatmap.pdf")


# %%
spacegroup_hist(df_grvh.spg_num)
plt.savefig("log_gvrh-spacegroup-hist.pdf")


# %%
fig = spacegroup_sunburst(df_grvh.spg_num, show_counts="percent")
fig.update_layout(title="Spacegroup sunburst of the JARVIS DFT 2D dataset")
fig.write_image("log_gvrh-spacegroup-sunburst.pdf")
fig.show()
