## Unified and cross-platform CM interface for DevOps, MLOps and MLPerf

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE.md)
[![Python Version](https://img.shields.io/badge/python-3+-blue.svg)](https://github.com/mlcommons/ck/tree/master/cm/cmind)
[![Powered by CM](https://img.shields.io/badge/Powered_by-MLCommons%20CM-blue)](https://github.com/mlcommons/ck).
[![Downloads](https://static.pepy.tech/badge/cm4mlops)](https://pepy.tech/project/cm4mlops)

[![CM script automation features test](https://github.com/mlcommons/cm4mlops/actions/workflows/test-cm-script-features.yml/badge.svg)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-cm-script-features.yml)
[![MLPerf inference bert (deepsparse, tf, onnxruntime, pytorch)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-mlperf-inference-bert-deepsparse-tf-onnxruntime-pytorch.yml/badge.svg)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-mlperf-inference-bert-deepsparse-tf-onnxruntime-pytorch.yml)
[![MLPerf inference MLCommons C++ ResNet50](https://github.com/mlcommons/cm4mlops/actions/workflows/test-mlperf-inference-mlcommons-cpp-resnet50.yml/badge.svg)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-mlperf-inference-mlcommons-cpp-resnet50.yml)
[![MLPerf inference ABTF POC Test](https://github.com/mlcommons/cm4mlops/actions/workflows/test-mlperf-inference-abtf-poc.yml/badge.svg)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-mlperf-inference-abtf-poc.yml)
[![Test Compilation of QAIC Compute SDK (build LLVM from src)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-qaic-compute-sdk-build.yml/badge.svg)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-qaic-compute-sdk-build.yml)
[![Test QAIC Software kit Compilation](https://github.com/mlcommons/cm4mlops/actions/workflows/test-qaic-software-kit.yml/badge.svg)](https://github.com/mlcommons/cm4mlops/actions/workflows/test-qaic-software-kit.yml)


# Collective Mind (CM)

**Collective Mind (CM)** is a Python package with a CLI and API designed for creating and managing automations. Two key automations developed using CM are **Script** and **Cache**, which streamline machine learning (ML) workflows, including managing Docker runs. Both Script and Cache automations are part of the **cm4mlops** repository.

The CM scripts, also housed in the **cm4mlops** repository, consist of hundreds of modular Python-wrapped scripts accompanied by `yaml` metadata, enabling the creation of robust and flexible ML workflows.

- **CM Scripts Documentation**: [https://docs.mlcommons.org/cm4mlops/](https://docs.mlcommons.org/cm4mlops/)
- **CM CLI Documentation**: [https://docs.mlcommons.org/ck/specs/cm-cli/](https://docs.mlcommons.org/ck/specs/cm-cli/)  

The `mlperf-branch` of the **cm4mlops** repository is dedicated to developments specific to MLPerf Inference. Please submit any pull requests (PRs) to this branch. For more information about using CM for MLPerf Inference, refer to the [MLPerf Inference Documentation](https://docs.mlcommons.org/inference/).

## News

* [Ongoing Discussions](https://github.com/mlcommons/cm4mlops/discussions)

## License

[Apache 2.0](LICENSE.md)

## CM concepts

Check our [ACM REP'23 keynote](https://doi.org/10.5281/zenodo.8105339).

## Authors

[Grigori Fursin](https://cKnowledge.org/gfursin) and [Arjun Suresh](https://www.linkedin.com/in/arjunsuresh)

## Major script developers

Arjun Suresh, Anandhu S, Grigori Fursin

## Funding

We thank [cKnowledge.org](https://cKnowledge.org), [cTuning foundation](https://cTuning.org)
and [MLCommons](https://mlcommons.org) for sponsoring this project!

## Acknowledgments

We thank all [volunteers, collaborators and contributors](https://github.com/mlcommons/cm4mlops/graphs/contributors) 
for their support, fruitful discussions, and useful feedback! 
