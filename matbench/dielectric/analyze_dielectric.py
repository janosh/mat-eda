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
import plotly.express as px
import plotly.io as pio
from matminer.datasets import load_dataset
from pymatviz import ptable_heatmap, spacegroup_hist, spacegroup_sunburst
from tqdm import tqdm


pio.templates.default = "plotly_white"

plt.rc("font", size=14)
plt.rc("savefig", bbox="tight", dpi=200)
plt.rc("axes", titlesize=16, titleweight="bold")
plt.rcParams["figure.constrained_layout.use"] = True


# %%
df_diel = load_dataset("matbench_dielectric")

df_diel[["spg_symbol", "spg_num"]] = [
    struct.get_space_group_info() for struct in tqdm(df_diel.structure)
]


# %%
df_diel["volume"] = [x.volume for x in df_diel.structure]
df_diel["formula"] = [x.formula for x in df_diel.structure]

ptable_heatmap(df_diel.formula, log=True)
plt.title("Elemental prevalence in the Matbench dielectric dataset")
plt.savefig("dielectric-ptable-heatmap.pdf")


# %%
df_diel.hist(bins=80, log=True, figsize=(20, 4), layout=(1, 3))
plt.savefig("dielectric-hists.pdf")


# %%
ax = spacegroup_hist(df_diel.spg_num)
ax.set_title("Space group histogram", y=1.1)
plt.savefig("dielectric-spacegroup-hist.pdf")


# %%
fig = spacegroup_sunburst(df_diel.spg_num, show_counts="percent")
fig.update_layout(title="Space group sunburst")
fig.write_image("dielectric-spacegroup-sunburst.pdf")
fig.show()


# %%
labels = {"crys_sys": "Crystal system", "n": "Refractive index n"}

fig = px.violin(df_diel, color="crys_sys", x="crys_sys", y="n", labels=labels)
fig.update_layout(
    title="Refractive index distribution by crystal system",
    margin=dict(b=10, l=10, r=10, t=50),
    showlegend=False,
)
fig.write_image("dielectric-violin.pdf")
fig.show()


# %%
fig = px.scatter(
    df_diel,
    x="volume",
    y="n",
    color="crys_sys",
    labels=labels,
    size="n",
    hover_data=["spg_symbol", "spg_num"],
    hover_name="formula",
    log_x=True,
    log_y=True,
)

fig.write_image("dielectric-scatter.pdf")
fig.show()
