# %%
from matminer.datasets import get_available_datasets, load_dataset
from matminer.utils.io import store_dataframe_as_json

# %%
matminer_datasets = get_available_datasets()

matbench_datasets = [dset for dset in matminer_datasets if dset.startswith("matbench_")]


print(f"total datasets = {len(matbench_datasets)}\n{matbench_datasets=}")
# 13 datasets in Matbench v0.1 as of Mar 2021:
#   dielectric, expt_gap, expt_is_metal, glass,
#   jdft2d, log_gvrh, log_kvrh, mp_e_form, mp_gap,
#   mp_is_metal, perovskites, phonons, steels",

# %% https://hackingmaterials.lbl.gov/automatminer/datasets.html#down-loading-datasets
# Load all MatBench datasets. Will be cached and faster to load next time.
for dataset in matbench_datasets:
    df = load_dataset(dataset)
    store_dataframe_as_json(df, f"../data/{dataset}.json.gz", compression="gz")


# %%
df = load_dataset("boltztrap_mp")
store_dataframe_as_json(df, "../data/boltztrap_mp.json.gz", compression="gz")
