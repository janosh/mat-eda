# MatBench v0.1

## Overview

> MatBench is an [ImageNet](http://www.image-net.org) for materials science; a set of 13 supervised, pre-cleaned, ready-to-use ML tasks for benchmarking and fair comparison. The tasks span across the domain of inorganic materials science applications.

The datasets in this repo are available at <https://hackingmaterials.lbl.gov/matbench/#all-matbench-datasets>.
To browse these datasets online, go to <https://ml.materialsproject.org> and log in.
Datasets were originally published in <https://nature.com/articles/s41524-020-00406-3>.

Detailed information about how each dataset was created and prepared for use is available at <https://hackingmaterials.lbl.gov/matminer/dataset_summary.html>

## Full list of the 13 Matbench datasets in v0.1

| task name                | target column (unit)         | number of samples | task type      | links                             |
| ------------------------ | ---------------------------- | ----------------- | -------------- | --------------------------------- |
| `matbench_dielectric`    | `n` (unitless)               | 4764              | regression     | [download][1], [interactive][2]   |
| `matbench_expt_gap`      | `gap expt` (eV)              | 4604              | regression     | [download][3], [interactive][4]   |
| `matbench_expt_is_metal` | `is_metal` (unitless)        | 4921              | classification | [download][5], [interactive][6]   |
| `matbench_glass`         | `gfa` (unitless)             | 5680              | classification | [download][7], [interactive][8]   |
| `matbench_jdft2d`        | `exfoliation_en` (meV/atom)  | 636               | regression     | [download][9], [interactive][10]  |
| `matbench_log_gvrh`      | `log10(G_VRH)` (log(GPa))    | 10987             | regression     | [download][11], [interactive][12] |
| `matbench_log_kvrh`      | `log10(K_VRH)` (log(GPa))    | 10987             | regression     | [download][13], [interactive][14] |
| `matbench_mp_e_form`     | `e_form` (eV/atom)           | 132752            | regression     | [download][15], [interactive][16] |
| `matbench_mp_gap`        | `gap pbe` (eV)               | 106113            | regression     | [download][17], [interactive][18] |
| `matbench_mp_is_metal`   | `is_metal` (unitless)        | 106113            | classification | [download][19], [interactive][20] |
| `matbench_perovskites`   | `e_form` (eV, per unit cell) | 18928             | regression     | [download][19], [interactive][20] |

[1]: https://ml.materialsproject.org/projects/matbench_dielectric.json.gz
[2]: https://ml.materialsproject.org/projects/matbench_dielectric
[3]: https://ml.materialsproject.org/projects/matbench_expt_gap.json.gz
[4]: https://ml.materialsproject.org/projects/matbench_expt_gap
[5]: https://ml.materialsproject.org/projects/matbench_expt_is_metal.json.gz
[6]: https://ml.materialsproject.org/projects/matbench_expt_is_metal
[7]: https://ml.materialsproject.org/projects/matbench_glass.json.gz
[8]: https://ml.materialsproject.org/projects/matbench_glass
[9]: https://ml.materialsproject.org/projects/matbench_jdft2d.json.gz
[10]: https://ml.materialsproject.org/projects/matbench_jdft2d
[11]: https://ml.materialsproject.org/projects/matbench_log_gvrh.json.gz
[12]: https://ml.materialsproject.org/projects/matbench_log_gvrh
[13]: https://ml.materialsproject.org/projects/matbench_log_kvrh.json.gz
[14]: https://ml.materialsproject.org/projects/matbench_log_kvrh
[15]: https://ml.materialsproject.org/projects/matbench_mp_e_form.json.gz
[16]: https://ml.materialsproject.org/projects/matbench_mp_e_form
[17]: https://ml.materialsproject.org/projects/matbench_mp_gap.json.gz
[18]: https://ml.materialsproject.org/projects/matbench_mp_gap
[19]: https://ml.materialsproject.org/projects/matbench_mp_is_metal.json.gz
[20]: https://ml.materialsproject.org/projects/matbench_mp_is_metal

## Leaderboard

| task name                | verified top score (MAE or ROCAUC) | algorithm name, config,             | general purpose algorithm? |
| ------------------------ | ---------------------------------- | ----------------------------------- | -------------------------- |
| `matbench_dielectric`    | 0.299 (unitless)                   | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_expt_gap`      | 0.416 eV                           | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_expt_is_metal` | 0.92                               | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_glass`         | 0.861                              | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_jdft2d`        | 38.6 meV/atom                      | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_log_gvrh`      | 0.0849 log(GPa)                    | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_log_kvrh`      | 0.0679 log(GPa)                    | Automatminer express v1.0.3.2019111 | yes                        |
| `matbench_mp_e_form`     | 0.0327 eV/atom                     | MEGNet v0.2.2                       | yes, structure only        |
| `matbench_mp_gap`        | 0.228 eV                           | CGCNN (2019)                        | yes, structure only        |
| `matbench_mp_is_metal`   | 0.977                              | MEGNet v0.2.2                       | yes, structure only        |
| `matbench_perovskites`   | 0.0417                             | MEGNet v0.2.2                       | yes, structure only        |
| `matbench_phonons`       | 36.9 cm^-1                         | MEGNet v0.2.2                       | yes, structure only        |
| `matbench_steels`        | 95.2 MPa                           | Automatminer express v1.0.3.2019111 | yes                        |

## Files of Interest

Everything in the [`notebooks`](/notebooks) directory.

## How to load Matbench Datasets

The simplest way to load Matbench datasets is with `matminer` (`pip install matminer`):

```py
from matminer.datasets import load_dataset

df = load_dataset("matbench_<dataset_name>")
```

`load_dataset` fetches and caches the dataset locally and automatically hydrates Pymatgen objects like `Structure` and `Composition` in the returned dataframe.

## Interesting Datasets in MPContribs

- [**Electronic Transport Properties** by F. Ricci et al.](https://contribs.materialsproject.org/projects/carrier_transport) contains 48,000 DFT Seebeck coefficients ([Paper](https://nature.com/articles/sdata201785))
