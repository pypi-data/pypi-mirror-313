.. warning::

	This page is still under construction.
	
	*Device object* section to modify.
	
	*Camera general informations* section to modify.
	
	*Complete example* section to modify.


IDS / Driver
############

The **driver** is based on the **IDS-peak** software.. 

The source is in the :file:`camera_ids.py` :download:`< <https://github.com/IOGS-LEnsE-ressources/camera-gui/blob/main/progs/IDS/src/camera_ids.py>` file including :

* :class:`CameraIds` class, 
* :samp:`get_converter_mode(color_mode: str)`
* :samp:`get_bits_per_pixel(color_mode: str)`


.. warning::

	The :file:`camera_ids.py` must be in the same directory as the Python file containing your script.
	
Import the CameraBasler class
*****************************

To access :class:`CameraIds` class and its functions, import the class in your Python code like this:

.. code-block:: python
	
	from camera_ids import CameraIds


Initialize a camera
*******************

Device object
=============

First of all, you need to create a device ... :

.. code-block:: python

	...
	
This script gets the first Ids camera connected device. If no device is connected, it returns an error.

You can also use the :class:`CameraList` class, as shown in the previous section. The :samp:`get_cam_device()` method returns a :class:`ids_peak.Device` object that is the same type as the :samp:`ids_peak` module.

Camera object
=============

An instance of the :class:`CameraIds` class creates an object able to communicate with the device.

To use our driver, you have to create an instance of the :class:`CameraIds` class like this:

.. code-block:: python

	my_cam = CameraBasler(my_cam_dev)

When you use this constructor, a well-initialized message is written in the console (if the camera is correctly connected and recognized by the system.

>>> my_cam = CameraIds(my_cam_dev)
Device is well initialized.

Connected camera
================

The :code:`is_camera_connected()` method returns the status of the camera, in other words it says if the camera could be opened or not.
	
To check if the camera is well connected, you can use this command:

>>> my_cam.is_camera_connected()
Device is well initialized.
True

If the camera is well initialized, you will obtain a success message in the console, following by :samp:`True`. 

Get information from the camera
*******************************

Different kind of informations are available on Basler camera. You can get the name, the serial number, the frame rate, the exposure time... of the camera.

Camera general informations
===========================

Serial Number and name
----------------------

The :code:`get_cam_info()` method returns a tuple with the serial number (str) and the name of the camera (str).

>>> my_cam.get_cam_info
('40282239', 'a2A1920-160ucBAS')

>>> my_cam.get_cam_info
('40282239', 'a2A1920-160ucBAS')

>>> my_cam.get_cam_info()
('40282239', 'a2A1920-160ucBAS')


Sensor size
-----------

The :code:`get_sensor_size()` method returns a tuple with the width (int) and the height (int) of the sensor.

>>> my_cam.get_sensor_size()
(1936, 1216)

Camera parameters
=================

Color mode
----------

The color mode corresponds to the format of the image data transmitted by the camera. There are different pixel formats depending on the model of your camera and whether it is a color or a mono camera.

Four color modes are implemented in this driver :

* 'Mono8' : monochromatic mode in 8 bits raw data
* 'Mono10' : monochromatic mode in 10 bits raw data
* 'Mono12' : monochromatic mode in 12 bits raw data
* 'RGB8' : RGB mode in 8 bits raw data

The :code:`get_color_mode()` method returns the color mode of the camera (str).

>>> my_cam.get_color_mode()
'Mono8'

For more informations about the color mode of Basler camera, you can check on the `Basler Website <https://docs.baslerweb.com/pixel-format#python>`_.

Exposure Time
-------------

The exposure time of a camera specifies how long the image sensor is exposed to light during image acquisition.

The :code:`get_exposure()` method returns the exposure time of the camera (float) in microseconds.

>>> my_cam.get_exposure()
5000.0

Frame Rate
----------

The frame rate specifies the maximum value of images per second collected by the camera. This factor depends on the exposure time (and other parameters).

The :code:`get_frame_rate()` method returns the frame rate of the camera (float) in frames per second.

>>> my_cam.get_frame_rate()
100.0

Area of interest (AOI)
----------------------

The AOI camera feature lets the user specify a portion of the camera's sensor array to use. Only the pixels contained in this area are transmitted.

The :code:`get_aoi()` method returns the position and the size of the area of interest (AOI). It gives a tuple of 4 integers : x, y, width, height. All these values are in pixels. x and y are the coordinates of the upper-left corner.

>>> my_cam.get_aoi()
(0, 0, 1936, 1216)

Black Level
-----------

The Black Level camera feature allows you to change the overall brightness of an image. Adjusting the camera's black level will result in an offset to the pixel's gray values output by the camera.

The :code:`get_black_level()` method returns the black level of the camera (int) in ADU (analog-to-digital units).

>>> my_cam.get_black_level()
0.0

Setup a camera
**************

Color mode
==========

The color mode corresponds to the format of the image data transmitted by the camera. There are different pixel formats depending on the model of your camera and whether it is a color or a mono camera.

Four color modes are implemented in this driver :

* 'Mono8' : monochromatic mode in 8 bits raw data
* 'Mono10' : monochromatic mode in 10 bits raw data
* 'Mono12' : monochromatic mode in 12 bits raw data
* 'RGB8' : RGB mode in 8 bits raw data

The :code:`set_color_mode(value)` method changes the color mode of the camera (str). The parameter is a str value corresponding to one of the four available modes.

>>> my_cam.set_color_mode('Mono12')

Exposure Time
=============

The exposure time of a camera specifies how long the image sensor is exposed to light during image acquisition.

The :code:`set_exposure(value)` method changes the exposure time of the camera. The parameter is a floatting number corresponding to the value of the exposure time in microseconds.

>>> my_cam.set_exposure(20000)

Frame Rate
==========

The frame rate specifies the maximum value of images per second collected by the camera. This factor depends on the exposure time (and other parameters).

The :code:`set_frame_rate(value)` method changes the frame rate of the camera. The parameter is a floatting number corresponding to the value of the frame rate in frames per second.

>>> my_cam.set_frame_rate(20)

Area of interest (AOI)
======================

The AOI camera feature lets the user specify a portion of the camera's sensor array to use. Only the pixels contained in this area are transmitted.


Set a new AOI
-------------

The :code:`set_aoi(x, y, w, h)` method changes the position and the size of the area of interest (AOI). It requires four parameters (integers) : x, y, width, height. All these values are in pixels. x and y are the coordinates of the upper-left corner.

>>> my_cam.set_aoi(16, 32, 500, 600)
True

.. caution::
	
	x and y coordinates must be dividable without rest by 4.

If the coordinates or the sizes are out of the range of the sensor size, the function returns False and no changes are applied.

>>> my_cam.set_aoi(10, 12, 522, 600)
False

>>> my_cam.set_aoi(-2, -3, 522, 600)
False

Reset AOI
---------


The :code:`reset_aoi()` method forces the position to 0,0 and the size of the area of interest (AOI) to the width and the height of the sensor. 

>>> my_cam.reset_aoi()
True

Black Level
===========

The Black Level camera feature allows you to change the overall brightness of an image. Adjusting the camera's black level will result in an offset to the pixel's gray values output by the camera.

The :code:`set_black_level(value)` method changes the black level of the camera. The parameter is an integer number corresponding to the value of the black level in ADU (analog-to-digital units).

>>> my_cam.set_black_level(50)
True

Get and display images
**********************

The main purpose of a camera is to capture images and transmit the data to the computer.


Images format and display
=========================

Each image is stored in a :code:`numpy.ndarray`. Depending on the color mode, this array is a two-dimensional ('MonoXX') or three-dimensional array ('RGB8' - two-dimensional array per color). 

Each pixel is encoded in 8 bits ('Mono8' or 'RGB8') or in 16 bits ('Mono10' or 'Mono12').

The next table gives an overview of the images format depending on the color mode.

.. list-table:: Images format
   :widths: 25 25 25 25
   :header-rows: 1

   * - Color Mode
     - Numpy.ndarray shape
     - Pixel type
     - Pixel Range Value
   * - Mono8
     - (H, W)
     - numpy.uint8
     - 0 to 255
   * - Mono10
     - (H, W)
     - numpy.uint16
     - 0 to 1023
   * - Mono12
     - (H, W)
     - numpy.uint16
     - 0 to 4095
   * - RGB8
     - (H, W, 3)
     - numpy.uint8
     - 0 to 255

The simplest way to display images in Python is to use **Matplotlib** library, as it shows in the next exemple.

.. code-block:: python

	from matplotlib import pyplot as plt
	
	plt.imshow(image, interpolation='nearest')
	plt.show()

Get one image
=============

The :code:`get_image()` method configures the camera to capture one image and to store it in a :code:`numpy.ndarray`. 

The array has the same shape as the AOI.

>>> image = my_cam.get_image()

Get a set of images
===================

The :code:`get_images(value)` method configures the camera to capture a set of images and to store them in a list of arrays. Each array corresponds to an image. The parameter is an integer number corresponding to the number of images to capture.

Without any parameter, this method return only one image.

>>> images = my_cam.get_images(10)

You can then access to one of the image like this:

>>> image1 = images[0]


Complete example
================

.. code-block:: python

    from matplotlib import pyplot as plt
	
	my_cam_dev = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
	
    my_cam = CameraBasler(my_cam_dev)

    # Check the colormode
    print(my_cam.get_color_mode())

    # Change colormode to Mono12
    my_cam.set_color_mode('Mono12')
    my_cam.set_display_mode('Mono12')
    print(my_cam.get_color_mode())
    
    # Test to catch one image
    images = my_cam.get_images()    
    print(images[0].shape)
    
    # display image
    plt.imshow(images[0], interpolation='nearest')
    plt.show()



Start a continuous shot
***********************

Coming soon...