IDS Requirements
################


An IDS camera
*************

It goes without saying that you must own an **IDS** camera.

All the source codes of the wrapper were tested with a :program:`TO ADD` camera.


IDS Sofware Suite
*****************

Industrial camera sensors from the **IDS** family require the installation of the *IDS drivers*, including in their **IDS Software Suite**. More information on the `IDS Imaging website <https://en.ids-imaging.com/>`_.

.. warning::

    **IDS peak** (2.8 or higher) and **IDS Sofware Suite** (4.95 or higher) softwares are required on your computer.

    **IDS peak IPL** (Image Processing Library) and **Numpy** are required.


IDS-peak Software
*****************

IDS peak is a comprehensive software package from *IDS Imaging Development Systems GmbH* that can be used with IDS cameras. IDS peak provides all necessary tools to open cameras in an application with graphical user interface, to parametrize them, to capture images, etc. or to program your own application.


.. note::

    To use old IDS generation of cameras (type UI), you need to install **IDS peak** in **custom** mode
    and add the **uEye Transport Layer** option.
	
IDS-peak IPL package
********************

This package allows **image processing** from the raw data of an IDS camera. It is required to convert the raw data to an exploitable array.

**IDS peak IPL** can be found in the *IDS peak* Python API.

Installation file is in the directory :file:`INSTALLED_PATH_OF_IDS_PEAK\\generic_sdk\\ipl\\binding\\python\\wheel\\x86_[32|64]`.

Then run this command in a shell (depending on your python version and computer architecture):

.. code-block:: bash

    pip install ids_peak_1.2.4.1-cp<version>-cp<version>m-[win32|win_amd64].whl

Generally *INSTALLED_PATH_OF_IDS_PEAK* is :file:`C:\\Program Files\\IDS\\ids_peak`



Installation test
*****************

**Before any software development**, you need to test if the hardware is operational and if the driver of the USB camera is correctly installed.

.. warning::

	Be sure that your camera is connected to an USB port of your computer.

IDS peak Cockpit from IDS
=========================

First of all, you should try to obtain images **from the software** provided by *IDS*. 

#. Open the **IDS peak Cockpit** software

	.. figure:: ../_static/images/ids/ids_peak_cockpit_icon.png
		:align: center

#. When the main window of the software is opened, click on the camera list icon (top-left corner of the interface) : 

	.. figure:: ../_static/images/ids/ids_peak_cockpit_step1.png
		:align: center

#. Double-click on the device you want to test.

	.. figure:: ../_static/images/ids/ids_peak_cockpit_step2.png
		:align: center

#. You have now control your device. Especially, in the lower left corner, you have access to different features of the camera :

	.. figure:: ../_static/images/ids/ids_peak_cockpit_step3.png 
		:align: center

IDS-peak API
============

The :file:`ids_peak_main_test.py` file from the :file:`progs/IDS/examples/` directory of the repository is an example to check that the **IDS-peak** Python API is correctly installed.

*You can also download this example* :download:`here <https://github.com/IOGS-LEnsE-ressources/camera-gui/blob/main/progs/IDS/examples/ids_peak_main_test.py>`.


You can execute this script by using this command in a shell : :code:`python ids_peak_main_test.py`

This script starts the camera and process 10 images by giving their size and the value of the first pixel.

	.. figure:: ../_static/images/ids/ids_peak_test.png
		:align: center

If the execution of this script proceeds without error, it means that everything is ready to use the *IDS* devices in a Python script or interface.
