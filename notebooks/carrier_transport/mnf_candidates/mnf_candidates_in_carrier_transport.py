# %%
import matplotlib.pyplot as plt
import pandas as pd
from matminer.utils.io import load_dataframe_from_json
from ml_matrics import ptable_elemental_prevalence

# %%
carrier_transport = load_dataframe_from_json(
    "../../../data/carrier_transport_with_strucs.json.gz"
)
carrier_transport.index.name = "mp_id"


# %%
mnf_candidates = pd.read_csv("mnf-candidates-with-mp-id.csv")


# %% 269 out of 446 MNF candidates
mnf_candidates.mp_id.isin(carrier_transport.index).sum()


# %%
mnf_in_carrier = carrier_transport.loc[
    mnf_candidates[mnf_candidates.mp_id.isin(carrier_transport.index)].mp_id
]


# %%
ptable_elemental_prevalence(mnf_in_carrier.pretty_formula.dropna(), log=True)
plt.title(
    "Elemental prevalence of MNF candidates in the Ricci Carrier Transport dataset"
)
plt.savefig("mnf-in-carrier-elements-log.pdf")


# %%
mnf_in_carrier.hist(bins=50, log=True, figsize=[30, 16])
plt.tight_layout()
plt.suptitle(
    "Properties of MNF Candidates according to Ricci Carrier Transport Dataset", y=1.05
)
plt.savefig("mnf-candidates-in-carrier-transport-hists.pdf")


# %%
dependent_vars = [
    "Sᵉ.p.v [µV/K]",
    "Sᵉ.n.v [µV/K]",
    "σᵉ.p.v [1/Ω/m/s]",
    "σᵉ.n.v [1/Ω/m/s]",
    "PFᵉ.p.v [µW/cm/K²/s]",
    "PFᵉ.n.v [µW/cm/K²/s]",
    "κₑᵉ.p.v [W/K/m/s]",
    "κₑᵉ.n.v [W/K/m/s]",
]

mnf_in_carrier[dependent_vars].hist(bins=50, log=True, figsize=[15, 15], layout=[4, 2])
plt.tight_layout()
plt.suptitle(
    "Carrier transport property distributions of MNF candidates "
    "present in Ricci Carrier Transport Dataset",
    y=1.05,
)
plt.savefig("mnf-candidates-carrier-transport-hists-dependent-vars.pdf")


# %%
mnf_in_carrier[dependent_vars].describe()


# %%
carrier_transport[dependent_vars].describe()


# %%
carrier_transport["zT_el"] = (
    (carrier_transport.dropna()["Sᵉ.p.v [µV/K]"] * 1e-6) ** 2
    * carrier_transport.dropna()["σᵉ.p.v [1/Ω/m/s]"]
    / carrier_transport.dropna()["κₑᵉ.p.v [W/K/m/s]"]
    * 300
)


# %%
mnf_in_carrier["zT_el"] = (
    (mnf_in_carrier["Sᵉ.p.v [µV/K]"] * 1e-6) ** 2
    * mnf_in_carrier["σᵉ.p.v [1/Ω/m/s]"]
    / mnf_in_carrier["κₑᵉ.p.v [W/K/m/s]"]
    * 300
)

# %%
carrier_transport.zT_el.describe()
