# %%
from matminer.datasets import get_available_datasets, load_dataset

# %%
get_available_datasets()


# %%
# https://hackingmaterials.lbl.gov/automatminer/datasets.html#down-loading-datasets
# Load all MatBench datasets. Will be cached and faster to load next time.

for dataset in [
    "matbench_dielectric",
    "matbench_expt_gap",
    "matbench_expt_is_metal",
    "matbench_glass",
    "matbench_jdft2d",
    "matbench_log_gvrh",
    "matbench_log_kvrh",
    "matbench_mp_e_form",
    "matbench_mp_gap",
    "matbench_mp_is_metal",
]:
    load_dataset(dataset)
