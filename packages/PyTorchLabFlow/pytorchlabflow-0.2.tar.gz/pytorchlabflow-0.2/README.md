# PyTorchLabFlow

[![PyPI version](https://badge.fury.io/py/pytorchlabflow.svg)](https://badge.fury.io/py/pytorchlabflow)
[![Downloads](https://static.pepy.tech/badge/Pytorchlabflow)](https://pepy.tech/project/Pytorchlabflow)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black?style=flat&logo=github)](https://github.com/BBEK-Anand/PyTorchLabFlow)

---

**PyTorchLabFlow** simplifies managing deep learning experiments, tracking models, components, performance, and configurations, letting you focus on research.

For end to end use case check [Military_AirCraft_Classification](https://github.com/BBEK-Anand/Military_AirCraft_Classification)

## Features
These are not all features that **PyTorchLabFlow** provides, here are ony few. Read more features with more detailing at[![GitHub](https://img.shields.io/static/v1?label=&message=GitHub&color=black&logo=github&logoColor=white&style=flat-square)](https://github.com/BBEK-Anand/PyTorchLabFlow)

### Setting up project
    - use `setup_project` for initiate a project.
   [Read more at github](https://github.com/BBEK-Anand/PyTorchLabFlow#setup_project)
    
### Training multiple experiments sequentialy
    - use `multi_train` to train multiple experiments to a specified epoch (`last_epoch`).
   [Read more at github](https://github.com/BBEK-Anand/PyTorchLabFlow#multi_train)

### Test model dataset compactibility at the time of model designing
    - use `test_mods` to check model's compactibility to dataset.
   [Read more at github](https://github.com/BBEK-Anand/PyTorchLabFlow#test_mods)
   
### Transfer experiment to a high-end system
    - use `transfer` to make all nessessary files of experiments to `internal/Transfer` folder, and then copy the folder to other system.
   [Read more at github](https://github.com/BBEK-Anand/PyTorchLabFlow#transfer)

### Use previous experiment configurations
    - use `use_ppl` to initiate a new experiment with some modified configurations generaly for hyperparameter tuning.
   [Read more at github](https://github.com/BBEK-Anand/PyTorchLabFlow#use_ppl)

### Plot performance of multiple experiments at a time
    - use `performance_plot` to plot experiments' performance over epochs individualy but at a time.
   [Read more at github](https://github.com/BBEK-Anand/PyTorchLabFlow#performance_plot)


# License
This project is licensed under the MIT License.
