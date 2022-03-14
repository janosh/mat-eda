"""Stats for the matbench_jdft2d dataset.

Input: Pymatgen Structure of the material.
Target variable: Exfoliation energy (meV).
Entries: 636

Matbench v0.1 dataset for predicting exfoliation energies from crystal structure
(computed with the OptB88vdW and TBmBJ functionals). Adapted from the JARVIS DFT DB.


https://ml.materialsproject.org/projects/matbench_jdft2d
"""


# %%
import matplotlib.pyplot as plt
from matminer.datasets import load_dataset
from pymatviz import ptable_heatmap, spacegroup_hist, spacegroup_sunburst


# %%
(jdft2d := load_dataset("matbench_jdft2d"))


# %%
jdft2d.hist(column="exfoliation_en", bins=50, log=True)
plt.savefig("jdft2d-exfoliation-energy-hist.pdf")


# %%
jdft2d["volume"] = jdft2d.structure.apply(lambda cryst: cryst.volume)
jdft2d["formula"] = jdft2d.structure.apply(lambda cryst: cryst.formula)

ptable_heatmap(jdft2d.formula, log=True)
plt.title("Elemental prevalence in the Matbench Jarvis DFT 2D dataset")
plt.savefig("jdft2d-ptable-heatmap-log.pdf")


# %%
jdft2d[["sg_symbol", "sg_number"]] = jdft2d.apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)


# %%
spacegroup_hist(jdft2d.sg_number, log=True)
plt.savefig("jdft2d-spacegroup-hist.pdf")


# %%
fig = spacegroup_sunburst(jdft2d.sg_number, show_values="percent")
fig.update_layout(title="Spacegroup sunburst of the JARVIS DFT 2D dataset")
fig.write_image("jdft2d-spacegroup-sunburst.pdf")
fig.show()
