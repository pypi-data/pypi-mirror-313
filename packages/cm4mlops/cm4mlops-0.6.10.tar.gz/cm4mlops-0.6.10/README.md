# MLPerf Automations and Scripts

This repository contains the automations and scripts used to run MLPerf benchmarks, primarily focusing on MLPerf inference benchmarks. The automations used here are largely based on and extended from the [Collective Mind script automations](https://github.com/mlcommons/cm4mlops/tree/main/automation/script).


## Collective Mind (CM)

**Collective Mind (CM)** is a Python package with a CLI and API designed for creating and managing automations. Two key automations developed using CM are **Script** and **Cache**, which streamline machine learning (ML) workflows, including managing Docker runs. Both Script and Cache automations are extended as part of this repository.

The CM scripts housed in this repository consist of hundreds of modular Python-wrapped scripts accompanied by `yaml` metadata, enabling the creation of robust and flexible ML workflows.

- **CM Scripts Documentation**: [https://docs.mlcommons.org/cm4mlops/](https://docs.mlcommons.org/cm4mlops/)


## License

[Apache 2.0](LICENSE.md)
