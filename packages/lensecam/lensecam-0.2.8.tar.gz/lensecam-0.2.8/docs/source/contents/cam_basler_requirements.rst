Basler Requirements
###################

A Basler camera
***************

It goes without saying that you must own a **Basler** camera.

All the source codes of the wrapper were tested with a :program:`a2A 1920-160ucBAS` camera.


Pylon Viewer software and drivers
*********************************

Industrial camera sensors from the **Basler** family require the installation of the *Basler drivers*, including in their *pylon Viewer* software. More information on the  `Basler website <https://www.baslerweb.com/en/>`_.

.. figure:: ../_static/images/basler/basler_pylon_software_download.png
  :scale: 60%
  :align: center
  
  From Basler Website.

Pypylon wrapper
***************

An official python wrapper for the Basler pylon Camera Software Suite is called **pypylon**. You can get more information about pypylon on their GitHub repository : `Pypylon GitHub repository <https://github.com/basler/pypylon>`_.

.. figure:: ../_static/images/basler/pypylon_wrapper.png
  :scale: 60%
  :align: center
  
  From Pypylon Website.
  
You can install this extension in a shell by the command : :code:`pip install pypylon`

.. warning:: 
	
	A complete version of Python (higher than 3.9) must be already installed on your computer. To check the version number, you can use the next command in a shell : :code:`python --version`

Installation test
*****************

**Before any software development**, you need to test if the hardware is operational and if the driver of the USB camera is correctly installed.

.. warning::

	Be sure that your camera is connected to an USB port of your computer.

Pylon Software from Basler
==========================

First of all, you should try to obtain images **from the software** provided by *Basler*. 

#. Open the **pylon Viewer** software

	.. figure:: ../_static/images/basler/basler_pylon_software_icone.png
		:align: center

#. When the main window of the software is opened, you can see your device in the USB sub-section of the Devices area (in the upper left corner) : 

	.. figure:: ../_static/images/basler/basler_pylon_software_step1.png
		:align: center

#. Double-click on the device you want to test.
#. You have now control your device. Especially, in the lower left corner, you have access to different features of the camera :

	.. figure:: ../_static/images/basler/basler_pylon_software_step2.png
		:align: center
		
#. Start video by clicking on the Continuous Shot of the toolbar :

	.. figure:: ../_static/images/basler/basler_pylon_software_main_tools.png
		:align: center

Pypylon extension
=================

The :file:`pypylon_main_test.py` file from the :file:`progs/Basler/examples/` directory of the repository is an example to check that the **pypylon** extension is correctly installed and that the pylon driver is recognized by the Python API.

*You can also download this example* :download:`here 
<https://github.com/IOGS-LEnsE-ressources/camera-gui/blob/main/progs/Basler/examples/pypylon_main_test.py>`.

This file is provided by the development team of the **pypylon** wrapper.

You can execute this script by using this command in a shell : :code:`python pypylon_main_test.py`

This script starts the camera and process 10 images by giving their size and the value of the first pixel.

	.. figure:: ../_static/images/basler/pypylon_test.png
		:align: center

If the execution of this script proceeds without error, it means that everything is ready to use the *Basler* devices in a Python script or interface.
