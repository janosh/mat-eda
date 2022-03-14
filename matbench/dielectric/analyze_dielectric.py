"""matbench_dielectric dataset

Input: Pymatgen Structure of the material.
Target variable: refractive index.
Entries: 636

Matbench v0. 1 test dataset for predicting refractive index from structure. Adapted from
Materials Project database. Removed entries having a formation energy (or energy above
the convex hull) more than 150meV and those having refractive indices less than 1 and
those containing noble gases. Retrieved April 2, 2019.

https://ml.materialsproject.org/projects/matbench_dielectric
"""


# %%
import matplotlib.pyplot as plt
from matminer.datasets import load_dataset
from pymatviz import ptable_heatmap, spacegroup_hist, spacegroup_sunburst


# %%
dielectric = load_dataset("matbench_dielectric")


# %%
dielectric["volume"] = dielectric.structure.apply(lambda cryst: cryst.volume)
dielectric["formula"] = dielectric.structure.apply(lambda cryst: cryst.formula)

ptable_heatmap(dielectric.formula, log=True)
plt.title("Elemental prevalence in the Matbench dielectric dataset")
plt.savefig("dielectric-ptable-heatmap-log.pdf")


# %%
dielectric[["sg_symbol", "sg_number"]] = dielectric.apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

# %%
dielectric.hist(bins=80, log=True, figsize=(20, 4), layout=(1, 3))
plt.savefig("dielectric-hists.pdf")


# %%
ax = spacegroup_hist(dielectric.sg_number)
ax.set_title("Space group histogram", y=1.1)
plt.savefig("dielectric-spacegroup-hist.pdf")


# %%
fig = spacegroup_sunburst(dielectric.sg_number, show_values="percent")
fig.update_layout(title="Space group sunburst")
fig.write_image("dielectric-spacegroup-sunburst.pdf")
fig.show()
