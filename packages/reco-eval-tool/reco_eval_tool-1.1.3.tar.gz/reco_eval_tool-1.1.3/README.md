# Reco Evaluation Tool

The Reco Evaluation Tool simplifies result evaluation by offering the following functions:

1. reading results from file or directory
2. analyzing features (including single feature distribution, pivot tables, feature shifts, correlation  coeficient and threshold selection)
3. calculating PR numbers
4. sample cases

All functions are achievable with a single line of code.

## Overview

Reco Evaluation Tool is a Python library that consists of the following components:


| Component                          | Description                                                                                                                |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [**reco_eval_tool.datasets**]      | Read results from file or directory then return a dataframe                                                                |
| [**reco_eval_tool.metrics**]       | Calculate pr numbers                                                                                                       |
| [**reco_eval_tool.statistics**]    | Analyze single feature; Analyze feature shift; Generate pivot table; Feature correlation  coeficient; mthreshold selection |
| [**reco_eval_tool.visualization**] | Visualize evaluation result                                                                                                |
| [**reco_eval_tool.sample**]        | Sample cases to check                                                                                                      |

# Installation

To install the current release:

```shell
$ pip install --upgrade reco_eval_tool
```

# Getting Started

## Minimal Example

```python
import os
import reco_eval_tool as ret

ret.set_output_dir("./eval_results")
all_df = ret.datasets.load_dir("demo")
per_language_prf = ret.metrics.calculate_prf(all_df, 'HumanIsLimitedUse', 'GPTIsLimitedUseV6', 'Language')
```

![1728654952757](images/README/1728654952757.png)

Please go this below file for more details: [demo.ipynb - Repos (azure.com)](https://dev.azure.com/msasg/ContentServices/_git/RecoNF?path=/users/mingleiguo/reco_eval_tool/official/examples/demo.ipynb&_a=preview)

# Update

1.0.5: Onboard correlavance cofficient, predict positive, sample

1.0.6: Update sample function

1.0.9: Update calculate_prf to calculate prf between GroundTruth list and Predict list

1.1.1 Add threshold selection

1.1.2 Update visualization function

1.1.3 Support to calculate weighted pr;  Support to calculate AUC and draw ROC curve
