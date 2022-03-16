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
from matminer.datasets import load_dataset
from pymatgen.core import Structure
from pymatviz import ptable_heatmap, spacegroup_hist, spacegroup_sunburst
from tqdm import tqdm


# %%
df_grvh = load_dataset("matbench_log_gvrh")
df_kvrh = load_dataset("matbench_log_kvrh")

# getting space group symbols and numbers for 10,987 structures takes about 4 min
print("getting spacegroups for log_gvrh")
df_grvh[["sg_symbol", "sg_number"]] = [
    struct.get_space_group_info() for struct in tqdm(df_grvh.structure)
]


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
df_grvh["volume"] = df_grvh.structure.apply(lambda struct: struct.volume)

df_grvh.hist(column="volume", bins=50, log=True, alpha=0.8)
plt.savefig("log_gvrh-volume-hist.pdf")


# %%
start = perf_counter()
radius = 5
df_grvh[f"neighbor_list_r{radius}"] = df_grvh.structure.apply(
    lambda crystal: crystal.get_neighbor_list(r=radius),
)
print(f"took {perf_counter() - start:.3f} sec")

df_kvrh[f"neighbor_list_r{radius}"] = df_kvrh.structure.apply(
    lambda crystal: crystal.get_neighbor_list(r=radius),
)


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
structure.make_supercell([2, 2, 2])
view = nv.show_pymatgen(structure)
view.add_unitcell()
structure.get_primitive_structure()
view


# %%
df_grvh["volume"] = df_grvh.structure.apply(lambda struct: struct.volume)

df_grvh.hist(column="volume", bins=50, log=True)


# %%
df_grvh["formula"] = df_grvh.structure.apply(lambda struct: struct.formula)

ptable_heatmap(df_grvh.formula, log=True)
plt.title("Elemental prevalence in the Matbench bulk/shear modulus datasets")
plt.savefig("log_gvrh-ptable-heatmap-log.pdf")


# %%
spacegroup_hist(df_grvh.sg_number)
plt.savefig("log_gvrh-spacegroup-hist.pdf")


# %%
fig = spacegroup_sunburst(df_grvh.sg_number, show_values="percent")
fig.update_layout(title="Spacegroup sunburst of the JARVIS DFT 2D dataset")
fig.write_image("log_gvrh-spacegroup-sunburst.pdf")
fig.show()
