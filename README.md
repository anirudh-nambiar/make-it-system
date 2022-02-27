## Description

This repository contains code accompanying the following paper on the Make-It robotic flow chemistry platform developed by the Jensen Research Group at MIT:

*Bayesian Optimization of Computer-Proposed Multistep Synthetic Routes on an Automated Robotic Flow Platform* ([preprint](https://doi.org/10.26434/chemrxiv-2022-xl27m))

## Contents

The code is organized into two main folders:
-	`hardware_control` contains Python classes developed to interface with common lab equipment (e.g., pumps, valves, HPLC) for chemical synthesis
-	`dragonfly_bayesopt_demo` contains an example Jupyter notebook demonstrating how to use the Dragonfly Bayesian optimization algorithm (developed by Kandasamy et al., [paper](https://jmlr.org/papers/v21/18-223.html)) for single- and multi-objective optimization and to visualize response surfaces

Additional documentation is provided in each folder.

Significant contributions to the hardware control code were made by authors of the previous [report](https://doi.org/10.1126/science.aax1566) on this platform.

## Funding

This work was funded by the DARPA Make-It and Accelerated Molecular Discovery programs under contracts ARO W911NF-16-2-0023 and HR00111920025, respectively.
