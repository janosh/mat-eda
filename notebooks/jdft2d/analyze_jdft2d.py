"""Stats for the matbench_jdft2d dataset.

Input: Pymatgen Structure of the material.
Target variable: Exfoliation energy (meV).
Entries: 636

Matbench v0.1 dataset for predicting exfoliation energies from crystal structure (computed
with the OptB88vdW and TBmBJ functionals). Adapted from the JARVIS DFT database.


https://ml.materialsproject.org/projects/matbench_jdft2d
"""


# %%
import matplotlib.pyplot as plt
import pandas as pd
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_elemental_prevalence, spacegroup_hist
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from tqdm import tqdm

# %%
tqdm.pandas()
(jdft2d := load_dataframe_from_json("../../data/jdft2d.json.gz"))


# %%
jdft2d.hist(column="exfoliation_en", bins=50, log=True)
plt.savefig("jdft2d-last-dos-peak-hist.pdf")


# %%
jdft2d["volume"] = jdft2d.structure.apply(lambda cryst: cryst.volume)
jdft2d["formula"] = jdft2d.structure.apply(lambda cryst: cryst.formula)

ptable_elemental_prevalence(jdft2d.formula, log=True)
plt.title("Elemental prevalence in the Matbench Jarvis DFT 2D dataset")
plt.savefig("jdft2d-elements-log.pdf")


# %%
jdft2d[["sg_symbol", "sg_number"]] = jdft2d.progress_apply(
    lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
)

jdft2d["crystal_system"] = jdft2d.structure.progress_apply(
    lambda struc: SpacegroupAnalyzer(struc).get_crystal_system()
)

jdft2d[["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]].to_csv(
    "additional-df-cols.csv", index=False
)


# %%
jdft2d[["sg_symbol", "sg_number", "crystal_system", "volume", "formula"]] = pd.read_csv(
    "additional-df-cols.csv"
)


# %%
spacegroup_hist(jdft2d.sg_number, log=True)
plt.savefig("jdft2d-spacegroup-hist.pdf")


# %%
jdft2d.value_counts("crystal_system").plot.pie(
    autopct=lambda val: f"{val:.1f}% ({int(round(val * len(jdft2d) / 100)):,})"
)
plt.title("Crystal systems in Matbench jdft2d")

plt.yticks(None)
plt.xlabel(f"{len(jdft2d):,} total samples")
plt.ylabel(None)
plt.savefig("jd2dft-crystal-system-pie.pdf")
