"""Stats for the Electronic Transport Properties dataset.

Larger/complete version of BoltzTrap MP (data/boltztrap_mp.json.gz).

https://contribs.materialsproject.org/projects/carrier_transport

Unprocessed data available from
https://contribs.materialsproject.org/projects/carrier_transport.json.gz
(see https://git.io/JOMwY).

Reference:
Ricci, F. et al. An ab initio electronic transport database for inorganic materials.
https://nature.com/articles/sdata201785
Dryad Digital Repository. https://doi.org/10.5061/dryad.gn001

Extensive column descriptions and metadata at
https://hackingmaterials.lbl.gov/matminer/dataset_summary.html#ricci-boltztrap-mp-tabular.
"""


# %%
import matplotlib.pyplot as plt
import pandas as pd
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_elemental_prevalence, spacegroup_hist


# %%
carrier_transport = load_dataframe_from_json(
    "../../data/ricci_boltztrap_carrier_transport.json.gz"
)


# %%
ptable_elemental_prevalence(carrier_transport.pretty_formula.dropna(), log=True)
plt.title("Elemental prevalence in the Ricci Carrier Transport dataset")
plt.savefig("carrier-transport-elements-log.pdf")


# %%
carrier_transport.hist(bins=50, log=True, figsize=[30, 16])
plt.tight_layout()
plt.suptitle("Ricci Carrier Transport Dataset", y=1.05)
plt.savefig("carrier-transport-hists.pdf")


# %%
carrier_transport[["S.p [µV/K]", "S.n [µV/K]"]].hist(bins=50, log=True, figsize=[18, 8])
plt.suptitle(
    "Ricci Carrier Transport dataset histograms for n- and p-type Seebeck coefficients"
)
plt.savefig("carrier-transport-seebeck-n+p.pdf")


# %%
dependent_vars = [
    "S.p [µV/K]",
    "S.n [µV/K]",
    "Sᵉ.p.v [µV/K]",
    "Sᵉ.n.v [µV/K]",
    "σ.p [1/Ω/m/s]",
    "σ.n [1/Ω/m/s]",
    "σᵉ.p.v [1/Ω/m/s]",
    "σᵉ.n.v [1/Ω/m/s]",
    "PF.p [µW/cm/K²/s]",
    "PF.n [µW/cm/K²/s]",
    "PFᵉ.p.v [µW/cm/K²/s]",
    "PFᵉ.n.v [µW/cm/K²/s]",
    "κₑ.p [W/K/m/s]",
    "κₑ.n [W/K/m/s]",
    "κₑᵉ.p.v [W/K/m/s]",
    "κₑᵉ.n.v [W/K/m/s]",
]

carrier_transport[dependent_vars].hist(bins=50, log=True, figsize=[30, 16])
plt.tight_layout()
plt.suptitle("Ricci Carrier Transport Dataset dependent variables", y=1.05)
plt.savefig("carrier-transport-hists-dependent-vars.pdf")


# %%
# getting space group symbols and numbers takes about 2 min
# carrier_transport[["sg_symbol", "sg_number"]] = carrier_transport.apply(
#     lambda row: row.structure.get_space_group_info(), axis=1, result_type="expand"
# )


# carrier_transport[["sg_symbol", "sg_number"]].to_csv("spacegroup-cols.csv")


# %%
carrier_transport[["sg_symbol", "sg_number"]] = pd.read_csv("spacegroup-cols.csv")


# %%
spacegroup_hist(carrier_transport.sg_number)
plt.title("Spacegroup distribution in the Ricci carrier transport dataset")
plt.savefig("carrier-transport-spacegroup-hist.pdf")
