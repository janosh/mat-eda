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
from matminer.datasets import load_dataset
from pymatviz import (
    annotate_bars,
    plot_structure_2d,
    ptable_heatmap,
    spacegroup_sunburst,
)
from pymatviz.utils import get_crystal_sys
from tqdm import tqdm


plt.rc("font", size=14)
plt.rc("savefig", bbox="tight", dpi=200)
plt.rc("axes", titlesize=16, titleweight="bold")
plt.rcParams["figure.constrained_layout.use"] = True


# %%
df_perov = load_dataset("matbench_perovskites")

df_perov[["spg_symbol", "spg_num"]] = [
    struct.get_space_group_info() for struct in tqdm(df_perov.structure)
]
df_perov["volume"] = df_perov.structure.map(lambda struct: struct.volume)

df_perov["formula"] = df_perov.structure.map(lambda cryst: cryst.formula)

df_perov["crys_sys"] = [get_crystal_sys(x) for x in df_perov.spg_num]


# %%
fig, axs = plt.subplots(3, 4, figsize=(12, 12))

for struct, ax in zip(df_perov.structure.head(12), axs.flat):
    ax = plot_structure_2d(struct, ax=ax)
    ax.set_title(struct.composition.reduced_formula, fontsize=14)

plt.savefig("perovskite-structures-2d.pdf")


# %%
df_perov.hist(column="e_form", bins=50)
plt.savefig("perovskites-e_form-hist.pdf")


# %%
ax = ptable_heatmap(df_perov.formula, log=True)
plt.title("Elements in Matbench Perovskites dataset")
plt.savefig("perovskites-ptable-heatmap.pdf")


# %%
df_perov["crys_sys"].value_counts().plot.bar()

plt.title("Crystal systems in Matbench Perovskites")
plt.xticks(rotation="horizontal")

annotate_bars(v_offset=250)

plt.savefig("perovskites-crystal-system-counts.pdf")


# %%
df_perov.plot.scatter(x="volume", y="e_form", c="spg_num", colormap="viridis")


# %%
fig = spacegroup_sunburst(df_perov.spg_num, show_counts="percent")
fig.update_layout(title="Matbench Perovskites spacegroup sunburst")
fig.write_image("perovskite-spacegroup-sunburst.pdf")
fig.show()
