"""Stats for the Electronic Transport Properties dataset.

https://contribs.materialsproject.org/projects/carrier_transport

Available from https://contribs.materialsproject.org/projects/carrier_transport.json.gz
(see https://github.com/hackingmaterials/matminer/issues/606#issuecomment-819915362).

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
carrier_transport = load_dataframe_from_json(
    "../../data/carrier_transport_with_strucs.json.gz"
)


# %%
ptable_elemental_prevalence(carrier_transport.pretty_formula.dropna(), log=True)
plt.title("Elemental prevalence in the Ricci Carrier Transport dataset")
plt.savefig("carrier_transport-elements-log.pdf")


# %%
carrier_transport.hist(bins=50, log=True, figsize=[30, 16])
plt.tight_layout()
plt.suptitle("Ricci Carrier Transport Dataset", y=1.05)
plt.savefig("carrier_transport-hists.pdf")


# %%
carrier_transport[["S.p [µV/K]", "S.n [µV/K]"]].hist(bins=50, log=True, figsize=[18, 8])
plt.suptitle(
    "Ricci Carrier Transport dataset histograms for n- and p-type Seebeck coefficients"
)
plt.savefig("carrier_transport-seebeck-n+p.pdf")


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
plt.savefig("carrier_transport-hists-dependent-vars.pdf")