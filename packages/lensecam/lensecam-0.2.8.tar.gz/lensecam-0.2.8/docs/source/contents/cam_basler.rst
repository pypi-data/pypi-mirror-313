Basler Camera Sensors
#####################

The LEnsE team developed *Python elements* for implementing industrial cameras from **Basler**.


To facilitate the integration of the pypylon API in the different projects, we developped : 

* a *list system* to list available cameras, based on the *pypylon* API,
* a *driver* to setup and to access a camera, based on the *pypylon* API,
* a set of *widgets* based on *PyQt6*, to control and to display images.

.. toctree::
	:maxdepth: 2

	Requirements and test<cam_basler_requirements>
	Basler Camera List<cam_basler_list>
	Basler Driver<cam_basler_driver>
	Basler Widgets<cam_basler_widgets>
	API reference<cam_basler_api>
