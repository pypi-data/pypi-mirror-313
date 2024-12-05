E2Clab (Edge-to-Cloud lab)
==========================

* Website: https://team.inria.fr/kerdata/e2clab/
* Documentation: https://e2clab.gitlabpages.inria.fr/e2clab/
* Main publication: https://hal.archives-ouvertes.fr/hal-02916032


Why E2Clab?
===========
Distributed digital infrastructures for computation and analytics are now evolving towards an interconnected ecosystem
allowing to execute complex application workflows from IoT Edge devices to the HPC Cloud (aka the Computing Continuum,
the Digital Continuum, or the Transcontinuum). **Understanding end-to-end performance** in such a complex continuum is
challenging. This breaks down to conciliating many, typically contradicting application requirements and constraints with
low-level infrastructure design choices. One important  **challenge** is to accurately reproduce relevant behaviors of a
given application workflow and representative settings of the physical infrastructure underlying this complex continuum.


What is E2Clab?
===============
E2Clab is a **framework** that implements a rigorous **methodology** that provides guidelines to move from
real-life application workflows to representative settings of the physical infrastructure underlying this application in
order to accurately reproduce its relevant behaviors and therefore **understand end-to-end performance**. Understanding
end-to-end performance means rigorously mapping the scenario characteristics to the experimental environment, identifying
and controlling the relevant configuration parameters of applications and system components, and defining the relevant
performance metrics.

Furthermore, this **methodology** **leverages** research quality aspects such as the **Repeatability**, **Replicability**, and
**Reproducibility** of experiments through a well-defined experimentation methodology and providing transparent access to
the experiment artifacts and experiment results. This is an important aspect that allows that the scientific claims are
verifiable by others in order to build upon them.

E2Clab sits on top of `EnOSlib <https://discovery.gitlabpages.inria.fr/enoslib/>`_, a library which brings reusable building blocks for configuring the infrastructure,
provisioning software on remote hosts as well as organizing the experimental workflow. Interaction with the testbeds is deferred
to EnOSlib's provider and various actions on remote hosts also rely on mechanisms offered by the library (e.g monitoring stack).


What E2Clab allows?
===================
E2Clab allows researchers to reproduce in a representative way the application behavior in a controlled environment for
extensive experiments and therefore to understand end-to-end performance of applications by correlating results to the
parameter settings. E2Clab provides a rigorous approach to answering questions like: *How to identify infrastructure
bottlenecks?* *Which system parameters and infrastructure configurations impact on performance and how?*

High-level features provided by E2Clab:

- **Leverage** experiment Repeatability, Replicability, and Reproducibility
- **Configure** the whole experimental environment (layers & services; network; and application workflow) in a **descriptive manner**
- **Map** between application parts and machines on the Edge, Fog and Cloud
- **Scale** and **variate** scenario deployments
- **Manage** **experiment** deployment and execution on large-scale testbed (e.g. `Grid'5000 <https://www.grid5000.fr/w/Grid5000:Home>`_)
- **Backup** metrics, log files, monitoring data, etc. generated during execution of experiments


E2Clab is, to the best of our knowledge, the first platform to support the complete analysis cycle of an application on
the Computing Continuum. It provides two simple abstractions for modeling such applications and infrastructures: *layers*
and *services*. While these abstractions are limited, we have found that they are powerful enough to express several
applications deployed on different environments, ranging from the Edge to the Cloud. Furthermore, we believe that the core
idea behind E2Clab, of a methodology to enable the design of relevant testbeds for 3R's experiments, may prove useful for
understanding the performance of large-scale applications.


Citation
========
If you publish work that uses E2Clab, please cite E2Clab as follows:

.. code-block:: bash

    @inproceedings{rosendo:hal-02916032,
      TITLE = {{E2Clab: Exploring the Computing Continuum through Repeatable, Replicable and Reproducible Edge-to-Cloud Experiments}},
      AUTHOR = {Rosendo, Daniel and Silva, Pedro and Simonin, Matthieu and Costan, Alexandru and Antoniu, Gabriel},
      URL = {https://hal.archives-ouvertes.fr/hal-02916032},
      BOOKTITLE = {{Cluster 2020 - IEEE International Conference on Cluster Computing}},
      ADDRESS = {Kobe, Japan},
      PAGES = {1-11},
      YEAR = {2020},
      MONTH = Sep,
      DOI = {10.1109/CLUSTER49012.2020.00028},
      KEYWORDS = {Reproducibility ; Methodology ; Computing Continuum ; Edge Intelligence},
      PDF = {https://hal.archives-ouvertes.fr/hal-02916032/file/Cluster_2020_E2Clab_HAL_v1.pdf},
      HAL_ID = {hal-02916032},
      HAL_VERSION = {v1},
    }

Please also consider adding your publication to the list of `E2Clab-based publications <https://e2clab.gitlabpages.inria.fr/e2clab/publications.html>`_ in the docs, just open a Pull Request.
