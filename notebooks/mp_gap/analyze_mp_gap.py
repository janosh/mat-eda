"""Stats for the matbench_mp_gap dataset.

Input: Pymatgen Structure of the material.
Target variable: The band gap (E_g) as calculated by PBE DFT from the Materials Project in eV.
Entries: 106113

https://ml.materialsproject.org/projects/matbench_mp_gap
"""

# %%
import matplotlib.pyplot as plt
from matminer.utils.io import load_dataframe_from_json
from mlmatrics import ptable_elemental_prevalence

# %%
mp_gap = load_dataframe_from_json("../../data/mp_gap.json.gz")


# %%
mp_gap.hist(column="gap pbe", bins=50, log=True)
plt.xlabel("eV")
plt.savefig("pbe_gap_hist.pdf")


# %%
mp_gap["volume/atom"] = mp_gap.structure.apply(
    lambda cryst: cryst.volume / cryst.num_sites
)
mp_gap["num_sites"] = mp_gap.structure.apply(lambda cryst: cryst.num_sites)

mp_gap["formula"] = mp_gap.structure.apply(lambda cryst: cryst.formula)


# %%
ptable_elemental_prevalence(mp_gap.formula, log=True)
plt.savefig("mp_gap-elements-log.pdf")


# %%
mp_gap.hist(column="volume/atom", bins=50, log=True)
plt.savefig("volume_per_atom_hist.pdf")
