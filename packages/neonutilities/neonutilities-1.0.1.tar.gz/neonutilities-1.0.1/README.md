neonutilities
===============

[https://github.com/NEONScience/NEON-utilities-python](https://github.com/NEONScience/NEON-utilities-python)

The neonutilities Python package provides utilities for discovering, downloading, and working with data files published by the National Ecological Observatory Network (NEON). NEON data files can be downloaded from the NEON Data Portal (http://data.neonscience.org) or API (http://data.neonscience.org/data-api). NEON data files from instrumented and observation systems are delivered by NEON in tabular files organized by site and year-month. NEON data files from the airborne observation platform (AOP) are organized by site and year.

neonutilities is available on PyPi and most users will want to install it from there. If you want to use the current development version, you can install from GitHub, but be warned that the GitHub version may not be stable.

Brief examples below; see [NEON Data Tutorials](https://www.neonscience.org/resources/learning-hub/tutorials) for more information, particularly the [Download and Explore](https://www.neonscience.org/resources/learning-hub/tutorials/download-explore-neon-data) and [neonUtilities](https://www.neonscience.org/resources/learning-hub/tutorials/neondatastackr) tutorials.

```
$ pip install neonutilities
```

```
import neonutilities as nu

bird = nu.load_by_product(dpid="DP1.10003.001",
			site="RMNP",
			package="expanded",
			release="RELEASE-2024",
			token=os.environ.get("NEON_TOKEN"))
							   
nu.by_tile_aop(dpid="DP3.30015.001",
		site="WREF",
		year=2022,
		easting=[571000,578000],
		northing=[5079000,5080000],
		savepath="filepath on your machine",
		token=os.environ.get("NEON_TOKEN"))

```

To install the development version (not recommended):

```
$ pip install git+https://github.com/NEONScience/NEON-utilities-python.git@main
```

Credits & Acknowledgements
---

The National Ecological Observatory Network is a project solely funded by the National Science Foundation and managed under cooperative agreement by Battelle. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.


License
---

GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007

Disclaimer
---

Information and documents contained within this repository are available as-is. Codes or documents, or their use, may not be supported or maintained under any program or service and may not be compatible with data currently available from the NEON Data Portal.

