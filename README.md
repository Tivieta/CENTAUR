# CENTAUR

CENTAUR is a python-based hybrid power system simulation program with a functional and lighweight GUI. It can be used for the design and simulation of hybrid solar PV-battery-diesel microgrids and is intended for both research and practical/commercial purposes. In particular, CENTAUR was originally designed as an open source platform to trial and experiment with novel control operating modes / strategies in a solar PV-battery-genset system. 

The program is fundamentally a chronological simulation whereby energy balances within a hybrid power system are calculated for every hour of a standard year (i.e. 8760 hours). It is functionally similar to the simulation components in packages such as HOMER and Hybrid2. Hourly solar PV outputs are [generated synthetically](https://github.com/susantoj/synthetic-solar) (using the TAG model by Aguiar and Collares-Pereira) and battery energy flows are estimated using Manwell and McGowan's [kinetic battery model (KiBaM)](https://github.com/susantoj/kinetic-battery).

Key benefits of CENTAUR include:
* Open source and extensible for research or commercial purposes
* Functional and lightweight GUI
* Explicitly defined system control operating modes for solar PV-battery-genset systems, describing the exact function of the genset and battery, e.g. backup, ramp control, load following, schedule operation, etc. This facilitates the simulation of user-defined control strategies. 

![screenshot of solar PV tab](/media/solar_pv_tab.png?raw=true) <!-- .element height="60%" width="60%" -->

![screenshot of simulation tab](/media/simulation_tab.png?raw=true) <!-- .element height="60%" width="60%" -->

![screenshot of simulation output](/media/battery_soc_snapshot.png?raw=true) <!-- .element height="60%" width="60%" -->

Requirements
------------

CENTAUR has the following dependencies:

* [Python](https://www.python.org) 3 or later.
* [SciPy Stack](https://scipy.org) 0.9 or later.
* [PyQT4](https://www.riverbankcomputing.com/software/pyqt/download)

Documentation
-------------

Refer to the [CENTAUR Wiki](https://github.com/susantoj/CENTAUR/wiki).

License & Copyright
-------------------

Copyright (C) 2017-2018 Julius Susanto. All rights reserved.

The code is distributed under the 3-clause BSD license found in the LICENSE file.
