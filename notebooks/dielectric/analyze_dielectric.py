"""Stats for the matbench_dielectric dataset.

Input: Pymatgen Structure of the material.
Target variable: Exfoliation energy (meV).
Entries: 636

Matbench v0.1 dataset for predicting exfoliation energies from crystal structure
(computed with the OptB88vdW and TBmBJ functionals). Adapted from the JARVIS DFT
database.


https://ml.materialsproject.org/projects/matbench_dielectric
"""


# %%
import matplotlib.pyplot as plt
import pandas as pd
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_heatmap, spacegroup_hist
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from tqdm import tqdm


# %%
tqdm.pandas()
(dielectric := load_dataframe_from_json("../../data/dielectric.json.gz"))


# %%
dielectric.hist(column="n", bins=50, log=True)
plt.savefig("dielectric-last-dos-peak-hist.pdf")


# %%
dielectric["volume"] = dielectric.structure.apply(lambda cryst: cryst.volume)
dielectric["formula"] = dielectric.structure.apply(lambda cryst: cryst.formula)

ptable_heatmap(dielectric.formula, log=True)
plt.title("Elemental prevalence in the Matbench dieletric dataset")
plt.savefig("dielectric-elements-log.pdf")


# %%
dielectric[["sg_symbol", "sg_number"]] = dielectric.progress_apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

dielectric["crystal_system"] = dielectric.structure.progress_apply(
    lambda struct: SpacegroupAnalyzer(struct).get_crystal_system()
)

dielectric[["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]].to_csv(
    "additional-df-cols.csv", index=False
)


# %%
dielectric[
    ["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]
] = pd.read_csv("additional-df-cols.csv")


# %%
spacegroup_hist(dielectric.sg_number)
plt.savefig("dielectric-spacegroup-hist.pdf")


# %%
dielectric.value_counts("crystal_system").plot.pie(
    autopct=lambda val: f"{val:.1f}% ({round(val * len(dielectric) / 100):,})"
)
plt.title("Crystal systems in Matbench dielectric")

plt.yticks(None)
plt.xlabel(f"{len(dielectric):,} total samples")
plt.ylabel(None)
plt.savefig("dielectric-crystal-system-pie.pdf")
