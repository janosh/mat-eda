"""Stats for the boltztrap_mp dataset.

Input: Pymatgen Structure of the material.
Columns:
  - mpid: Materials Project identifier
  - formula: Chemical formula of the entry
  - m_n: n-type/conduction band effective mass. Units: m_e (electron mass),
    i.e. m_n is a unitless ratio
  - m_p: p-type/valence band effective mass.
  - pf_n: n-type thermoelectric power factor in uW/cm2.K
    where uW is microwatts and a constant relaxation time of 1e-14 assumed.
  - pf_p: p-type power factor in uW/cm2.K
  - s_n: n-type Seebeck coefficient in micro Volts per Kelvin
  - s_p: p-type Seebeck coefficient in micro Volts per Kelvin
Entries: 8924

Effective mass and thermoelectric properties of 8924 MP compounds calculated
by the BoltzTraP software package run on the GGA-PBE or GGA+U DFT results.
The properties are reported at 300 Kelvin and carrier concentration of 1e18/cm3.

Reference:
Ricci, F. et al. An ab initio electronic transport database for inorganic materials.
https://nature.com/articles/sdata201785
Dryad Digital Repository. https://doi.org/10.5061/dryad.gn001

https://hackingmaterials.lbl.gov/matminer/dataset_summary.html
"""


# %%
import matplotlib.pyplot as plt
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_elemental_prevalence


# %%
(boltztrap_mp := load_dataframe_from_json("../../data/boltztrap_mp.json.gz"))


# %%
ptable_elemental_prevalence(boltztrap_mp.formula, log=True)
plt.title("Elemental prevalence in the BoltzTraP MP dataset")
plt.savefig("boltztrap_mp-elements-log.pdf")


# %%
ptable_elemental_prevalence(boltztrap_mp.sort_values("pf_n").tail(100).formula)
plt.title("Elemental prevalence of top 100 n-type powerfactors in BoltzTraP MP dataset")
plt.savefig("boltztrap_mp-elements-top-100-nPF.pdf")


# %%
boltztrap_mp.hist(bins=50, log=True, layout=[2, 3], figsize=[18, 8])
plt.suptitle("BoltzTraP MP")
plt.savefig("boltztrap_mp-hists.pdf")


# %%
boltztrap_mp.sort_values("pf_n", ascending=False).head(1000).hist(
    bins=50, log=True, layout=[2, 3], figsize=[18, 8]
)
plt.suptitle("BoltzTraP MP")
