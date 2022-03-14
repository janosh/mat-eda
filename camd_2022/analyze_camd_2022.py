"""Rhys received this dataset from Joseph Montoya at Toyota Research Institute (TRI)
via email on 2022-01-12.

Download link: https://data.matr.io/7
GitHub repo: https://github.com/TRI-AMDD/CAMD

DFT calculations are unfortunately OQMD based, i.e. not Materials Project compatible.

Description:
TRI's second active learning crystal discovery dataset from Computational Autonomy for
Materials Discovery (CAMD). The dataset has ~100k crystal structures, 25k of which are
within 20 meV of the hull and ~1k of which are on the hull. They organized all of the
campaigns by chemical system.
"""


# %%
import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
from pymatgen.symmetry.groups import SpaceGroup
from pymatviz import (
    annotate_bar_heights,
    count_elements,
    ptable_heatmap,
    spacegroup_sunburst,
)


# %% Download data (if needed)
if os.path.isfile("camd-2022-wo-features.csv.bz2"):
    print("Loading local data...")
    df = pd.read_csv("camd-2022-wo-features.csv.bz2")
else:
    print("Fetching data from AWS...")
    url = "https://s3.amazonaws.com/publications.matr.io/7/deployment/data/files"
    with_feat = False
    dataset = f"/camd_data_to_release_{'w' if with_feat else 'wo'}features.json"
    data = requests.get(url + dataset).json()
    df = pd.DataFrame(data)
    df = pd.to_csv(f"camd-2022-{'w' if with_feat else 'wo'}-features.csv.bz2")


# %%
df.hist(bins=50)


# %%
elem_counts = count_elements(df.reduced_formula)
ptable_heatmap(elem_counts, log=True)
plt.title("Elemental prevalence of CAMD 2022 dataset", fontsize=16)
plt.savefig("camd-2022-ptable-heatmap-log.pdf")


# %%
df.data_source.value_counts().plot.bar(fontsize=18, rot=0)
annotate_bar_heights(voffset=3e3)


# %%
spgs = df.space_group.apply(SpaceGroup)

df["sg_number"] = [x.int_number for x in spgs]

fig = spacegroup_sunburst(df.sg_number, show_values="percent")
fig.show()
fig.write_image("camd-2022-spacegroup-sunburst.pdf")
fig.show()