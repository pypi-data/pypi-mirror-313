IDS Camera Sensors
##################

The LEnsE team developed *Python elements* for implementing industrial cameras from **IDS**.

.. warning::

    **IDS peak** (2.8 or higher) and **IDS Sofware Suite** (4.95 or higher) softwares
    are required on your computer.

    **IDS peak IPL** (Image Processing Library) and **Numpy** are required.

.. note::

    To use old IDS generation of cameras (type UI), you need to install **IDS peak** in **custom** mode
    and add the **uEye Transport Layer** option.

.. note::

    **IDS peak IPL** can be found in the *IDS peak* Python API.

    Installation file is in the directory :file:`INSTALLED_PATH_OF_IDS_PEAK/generic_sdk/ipl/binding/python/wheel/x86_[32|64]`.

    Then run this command in a shell (depending on your python version and computer architecture):

    .. code-block:: bash

        pip install ids_peak_1.2.4.1-cp<version>-cp<version>m-[win32|win_amd64].whl

    Generally *INSTALLED_PATH_OF_IDS_PEAK* is :file:`C:/Program Files/IDS/ids_peak`

To facilitate the integration of the **IDS peak** API in the different projects, we developped :

* a *list system* to list available cameras, based on the *IDS peak* API,
* a *driver* to setup and to access a camera, based on the *IDS peak* API,
* a set of *widgets* based on *PyQt6*, to control and to display images.

.. toctree::
	:maxdepth: 2

	Requirements and test<cam_ids_requirements>
	IDS Camera List<cam_ids_list>
	IDS Driver<cam_ids_driver>
	IDS Widgets<cam_ids_widgets>
	API reference<cam_ids_api>
