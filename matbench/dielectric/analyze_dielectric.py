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
from pymatviz import (
    ptable_heatmap,
    ptable_heatmap_plotly,
    spacegroup_hist,
    spacegroup_sunburst,
)
from pymatviz.utils import get_crystal_sys
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

df_diel["crys_sys"] = [get_crystal_sys(x) for x in df_diel.spg_num]


# %%
df_diel["volume"] = [x.volume for x in df_diel.structure]
df_diel["formula"] = [x.formula for x in df_diel.structure]

ptable_heatmap(df_diel.formula, log=True)
plt.title("Elemental prevalence in the Matbench dielectric dataset")
plt.savefig("dielectric-ptable-heatmap.pdf")


# %%
fig = ptable_heatmap_plotly(df_diel.formula)
title = "Elements in Matbench Dielectric"
fig.update_layout(title=dict(text=f"<b>{title}</b>", x=0.4, y=0.94, font_size=20))
# fig.write_image("dielectric-ptable-heatmap-plotly.pdf")


# %%
ax = spacegroup_hist(df_diel.spg_num)
ax.set_title("Space group histogram", y=1.1)
plt.savefig("dielectric-spacegroup-hist.pdf")


# %%
fig = spacegroup_sunburst(df_diel.spg_num, show_counts="percent")
fig.update_layout(title="Space group sunburst")
# fig.write_image("dielectric-spacegroup-sunburst.pdf")
fig.show()


# %%
labels = {
    "crys_sys": "Crystal system",
    "n": "Refractive index n",
    "spg_num": "Space group",
}

fig = px.violin(
    df_diel,
    color="crys_sys",
    x="crys_sys",
    y="n",
    labels=labels,
    points="all",
    hover_data=["spg_num"],
    hover_name="formula",
).update_traces(jitter=1)
fig.update_layout(
    title="Refractive index distribution by crystal system",
    margin=dict(b=10, l=10, r=10, t=50),
    showlegend=False,
)
# fig.write_image("dielectric-violin.pdf")
fig.show()


# %%
fig = px.scatter(
    df_diel.round(2),
    x="volume",
    y="n",
    color="crys_sys",
    labels=labels,
    size="n",
    hover_data=["spg_num"],
    hover_name="formula",
    range_x=[0, 1500],
)
title = "Matbench Dielectric: Refractive Index vs. Volume"
fig.update_layout(
    title=dict(text=f"<b>{title}</b>", x=0.5, font_size=20),
    legend=dict(x=1, y=1, xanchor="right"),
)

# fig.write_image("dielectric-scatter.pdf")
fig.show()
