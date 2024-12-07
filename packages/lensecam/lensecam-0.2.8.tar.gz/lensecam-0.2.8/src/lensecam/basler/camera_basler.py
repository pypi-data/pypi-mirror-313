# -*- coding: utf-8 -*-
"""camera_basler file.

File containing :class::CameraBasler
class to communicate with a Basler camera sensor.

.. module:: CameraBasler
   :synopsis: class to communicate with a Basler camera sensor.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

"""
from pypylon import pylon
import numpy


def get_converter_mode(color_mode: str) -> int:
    """Return the converter display mode.

    :param color_mode: color mode of the camera
        ('Mono8', 'Mono10', 'Mono12' or 'RGB8')
    :type color_mode: str
    :return: corresponding converter display mode
    :rtype: int

    @see : https://docs.baslerweb.com/pixel-format

    """
    return {
        "Mono8": pylon.PixelType_Mono8,
        "Mono10": pylon.PixelType_Mono16,
        "Mono12": pylon.PixelType_Mono16,
        "RGB8": pylon.PixelType_RGB8packed
    }[color_mode]


def get_bits_per_pixel(color_mode: str) -> int:
    """Return the number of bits per pixel.

    :param color_mode: color mode.
    :type color_mode: str
    :return: number of bits per pixel.
    :rtype: int

    """
    return {
        'Mono8': 8,
        'Mono10': 10,
        'Mono12': 12,
        'RGB8': 8
    }[color_mode]


class CameraBasler:
    """Class to communicate with a Basler camera sensor.

    :param camera: Camera object that can be controlled.
    :type camera_device: pylon.TlFactory.InstantCamera

    TO COMPLETE

    .. note::

        In the context of this driver,
        the following color modes are available :

        * 'Mono8' : monochromatic mode in 8 bits raw data
        * 'Mono10' : monochromatic mode in 10 bits raw data
        * 'Mono12' : monochromatic mode in 12 bits raw data
        * 'RGB8' : RGB mode in 8 bits raw data

    """

    def __init__(self, cam_dev: pylon.TlFactory = None) -> None:
        """Initialize the object."""
        # Camera device
        self.camera_device = cam_dev
        if self.camera_device is None:
            self.camera_connected = False
        else:  # A camera device is connected
            self.camera_connected = True
        self.camera_acquiring = False  # The camera is acquiring
        self.camera_remote = None
        self.data_stream = None
        # Camera parameters
        self.color_mode = None
        self.nb_bits_per_pixels = 8
        self.converter = None

    def init_camera(self, cam_dev=None):
        """Initialize the camera."""
        if cam_dev is not None:
            self.camera_device = cam_dev
        self.converter = pylon.ImageFormatConverter()
        # Camera informations
        self.serial_no, self.camera_name = self.get_cam_info()
        self.width_max, self.height_max = self.get_sensor_size()
        self.nb_bits_per_pixels: int = 0
        self.color_mode = 'Mono8'  # default
        self.set_color_mode('Mono8')
        self.set_display_mode('Mono8')
        # AOI size
        self.aoi_x0: int = 0
        self.aoi_y0: int = 0
        self.aoi_width: int = self.width_max
        self.aoi_height: int = self.height_max
        # Test if camera is connected.
        self.is_camera_connected()
        self.set_aoi(self.aoi_x0, self.aoi_y0, self.aoi_width, self.aoi_height)

    def alloc_memory(self) -> bool:
        """Alloc the memory to get an image from the camera."""
        if self.camera_connected:
            return True
        else:
            return False

    def find_first_camera(self) -> bool:
        """Create an instance with the first IDS available camera.

        :return: True if an IDS camera is connected.
        :rtype: bool
        """
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        if len(devices) > 0:
            my_cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            if my_cam is not None:
                self.camera_device = my_cam
                self.camera_connected = True
                return True
        return False

    def is_camera_connected(self) -> bool:
        """Return the status of the device.

        :return: true if the device could be opened, and then close the device
        :rtype: bool (or error)

        """
        self.camera_device.Open()
        if self.camera_device.IsOpen():
            print('Device is well initialized.')
            self.camera_device.Close()
            return True
        else:
            self.camera_device.Close()
            return False

    def free_memory(self) -> None:
        """
        Free memory containing the data stream.
        """
        pass

    def start_acquisition(self) -> None:
        """Start acquisition"""
        if self.camera_acquiring is False:
            self.camera_acquiring = True

    def stop_acquisition(self):
        """Stop acquisition"""
        if self.camera_acquiring is True:
            self.camera_acquiring = False

    def disconnect(self):
        """Disconnect the camera."""
        if self.camera_device.IsOpen():
            self.camera_device.Close()

    def destroy_camera(self) -> None:
        self.camera_device = None

    def get_cam_info(self) -> tuple[str, str]:
        """Return the serial number and the name.

        :return: the serial number and the name of the camera
        :rtype: tuple[str, str]
        """
        serial_no, camera_name = None, None
        try:
            camera_name = self.camera_device.GetDeviceInfo().GetModelName()
            serial_no = self.camera_device.GetDeviceInfo().GetSerialNumber()
            return serial_no, camera_name
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_sensor_size(self) -> tuple[int, int]:
        """Return the width and the height of the sensor.

        :return: the width and the height of the sensor in pixels
        :rtype: tuple[int, int]
        """
        try:
            if self.camera_device.IsOpen():
                max_height = self.camera_device.Height.GetMax()
                max_width = self.camera_device.Width.GetMax()
                return max_width, max_height
            else:
                self.camera_device.Open()
                max_height = self.camera_device.Height.GetMax()
                max_width = self.camera_device.Width.GetMax()
                self.camera_device.Close()
                return max_width, max_height
        except Exception as e:
            print("Exception: " + str(e) + "")

    def set_display_mode(self, colormode: str = 'Mono8') -> None:
        """Change the color mode of the converter.

        :param colormode: Color mode to use for the device
        :type colormode: str, default 'Mono8'

        """
        mode_converter = get_converter_mode(colormode)
        try:
            self.converter.OutputPixelFormat = mode_converter
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_color_mode(self):
        """Get the color mode.

        :param colormode: Color mode to use for the device
        :type colormode: str, default 'Mono8'
        """
        try:
            # Test if the camera is opened
            if self.camera_device.IsOpen():
                pixelFormat = self.camera_device.PixelFormat.GetValue()
            else:
                self.camera_device.Open()
                pixelFormat = self.camera_device.PixelFormat.GetValue()
                self.camera_device.Close()
            self.color_mode = pixelFormat
            return pixelFormat
        except Exception as e:
            print("Exception: " + str(e) + "")

    def set_color_mode(self, colormode: str) -> None:
        """Change the color mode.

        :param colormode: Color mode to use for the device
        :type colormode: str, default 'Mono8'

        """
        try:
            # Test if the camera is opened
            if self.camera_device.IsOpen():
                self.camera_device.PixelFormat = colormode
            else:
                self.camera_device.Open()
                self.camera_device.PixelFormat = colormode
                self.camera_device.Close()
            self.color_mode = colormode
            self.nb_bits_per_pixels = get_bits_per_pixel(colormode)
            self.set_display_mode(colormode)
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_image(self) -> numpy.ndarray:
        """Get one image.

        :return: Array of the image.
        :rtype: array

        """
        image = self.get_images()
        return image[0]

    def get_images(self, nb_images: int = 1) -> list:
        """Get a series of images.

        :param nb_images: Number of images to collect
        :type nb_images: int, default 1
        :return: List of images
        :rtype: list

        """
        try:
            # Test if the camera is opened
            if not self.camera_device.IsOpen():
                self.camera_device.Open()
            # Test if the camera is grabbing images
            if not self.camera_device.IsGrabbing():
                self.camera_device.StopGrabbing()
            # Create a list of images
            images: list = []
            self.camera_device.StartGrabbingMax(nb_images)

            while self.camera_device.IsGrabbing():
                grabResult = self.camera_device.RetrieveResult(
                    1000,
                    pylon.TimeoutHandling_ThrowException)
                if grabResult.GrabSucceeded():
                    # Access the image data.
                    images.append(grabResult.Array)
                grabResult.Release()
            return images
        except Exception as e:
            print("Exception: " + str(e) + "")

    def __check_range(self, x: int, y: int) -> bool:
        """Check if the coordinates are in the sensor area.

        :param x: Coordinate to evaluate on X-axis.
        :type x: int
        :param y: Coordinate to evaluate on Y-axis.
        :type y: int

        :return: true if the coordinates are in the sensor area
        :rtype: bool

        """
        if 0 <= x <= self.width_max and 0 <= y <= self.height_max:
            return True
        else:
            return False

    def set_aoi(self, x0, y0, w, h) -> bool:
        """Set the area of interest (aoi).

        :param x0: coordinate on X-axis of the top-left corner of the aoi must be dividable without rest by Inc = 4.
        :type x0: int
        :param y0: coordinate on X-axis of the top-left corner of the aoi must be dividable without rest by Inc = 4.
        :type y0: int
        :param w: width of the aoi
        :type w: int
        :param h: height of the aoi
        :type h: int
        :return: True if the aoi is modified
        :rtype: bool

        """
        if self.__check_range(x0, y0) is False or self.__check_range(x0 + w, y0 + h) is False:
            return False
        if x0 % 4 != 0 or y0 % 4 != 0:
            return False
        self.aoi_x0 = x0
        self.aoi_y0 = y0
        self.aoi_width = w
        self.aoi_height = h
        try:
            if self.camera_device.IsOpen():
                self.camera_device.Width.SetValue(w)
                self.camera_device.Height.SetValue(h)
                self.camera_device.OffsetX.SetValue(x0)
                self.camera_device.OffsetY.SetValue(y0)
            else:
                self.camera_device.Open()
                self.camera_device.Width.SetValue(w)
                self.camera_device.Height.SetValue(h)
                self.camera_device.OffsetX.SetValue(x0)
                self.camera_device.OffsetY.SetValue(y0)
                self.camera_device.Close()
            return True
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_aoi(self) -> tuple[int, int, int, int]:
        """Return the area of interest (aoi).

        :return: [x0, y0, width, height] x0 and y0 are the
            coordinates of the top-left corner and width
            and height are the size of the aoi.
        :rtype: tuple[int, int, int, int]

        """
        return self.aoi_x0, self.aoi_y0, self.aoi_width, self.aoi_height

    def reset_aoi(self) -> bool:
        """Reset the area of interest (aoi).

        Reset to the limit of the camera.

        :return: True if the aoi is modified
        :rtype: bool
        """
        self.aoi_x0 = 0
        self.aoi_y0 = 0
        self.aoi_width = self.width_max
        self.aoi_height = self.height_max
        print(self.set_aoi(self.aoi_x0, self.aoi_y0,
                           self.width_max, self.height_max))

    def get_exposure(self) -> float:
        """Return the exposure time in microseconds.

        :return: the exposure time in microseconds.
        :rtype: float
        """
        try:
            if self.camera_device.IsOpen():
                exposure = self.camera_device.ExposureTime.GetValue()
            else:
                self.camera_device.Open()
                exposure = self.camera_device.ExposureTime.GetValue()
                self.camera_device.Close()
            return exposure
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_exposure_range(self) -> tuple[float, float]:
        """Return the range of the exposure time in microseconds.

        :return: the minimum and the maximum value
            of the exposure time in microseconds.
        :rtype: tuple[float, float]

        """
        try:
            if self.camera_device.IsOpen():
                exposureMin = self.camera_device.ExposureTime.GetMin()
                exposureMax = self.camera_device.ExposureTime.GetMax()
            else:
                self.camera_device.Open()
                exposureMin = self.camera_device.ExposureTime.GetMin()
                exposureMax = self.camera_device.ExposureTime.GetMax()
                self.camera_device.Close()
            return exposureMin, exposureMax
        except Exception as e:
            print("Exception: " + str(e) + "")

    def set_exposure(self, exposure: float) -> None:
        """Set the exposure time in microseconds.

        :param exposure: exposure time in microseconds.
        :type exposure: float

        """
        try:
            if self.camera_device.IsOpen():
                self.camera_device.ExposureTime.SetValue(exposure)
            else:
                self.camera_device.Open()
                self.camera_device.ExposureTime.SetValue(exposure)
                self.camera_device.Close()
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_frame_rate(self) -> float:
        """Return the frame rate.

        :return: the frame rate.
        :rtype: float

        """
        try:
            if self.camera_device.IsOpen():
                frameRate = self.camera_device.AcquisitionFrameRate.GetValue()
            else:
                self.camera_device.Open()
                frameRate = self.camera_device.AcquisitionFrameRate.GetValue()
                self.camera_device.Close()
            return frameRate
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_frame_rate_range(self):
        """Return the range of the frame rate in frames per second.

        :return: the minimum and the maximum value
            of the frame rate in frames per second.
        :rtype: tuple[float, float]

        """
        try:
            if self.camera_device.IsOpen():
                frameRateMin = self.camera_device.AcquisitionFrameRate.GetMin()
                frameRateMax = self.camera_device.AcquisitionFrameRate.GetMax()
            else:
                self.camera_device.Open()
                frameRateMin = self.camera_device.AcquisitionFrameRate.GetMin()
                frameRateMax = self.camera_device.AcquisitionFrameRate.GetMax()
                self.camera_device.Close()
            return frameRateMin, frameRateMax
        except Exception as e:
            print("Exception: " + str(e) + "")

    def set_frame_rate(self, fps):
        """Set the frame rate in frames per second.

        :param fps: frame rate in frames per second.
        :type fps:

        """
        try:
            if self.camera_device.IsOpen():
                self.camera_device.AcquisitionFrameRateEnable.SetValue(True)
                self.camera_device.AcquisitionFrameRate.SetValue(fps)
            else:
                self.camera_device.Open()
                self.camera_device.AcquisitionFrameRateEnable.SetValue(True)
                self.camera_device.AcquisitionFrameRate.SetValue(fps)
                self.camera_device.Close()
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_black_level(self):
        """Return the blacklevel.

        :return: the black level of the device in ADU.
        :rtype: int
        """
        try:
            if self.camera_device.IsOpen():
                BlackLevel = self.camera_device.BlackLevel.GetValue()
            else:
                self.camera_device.Open()
                BlackLevel = self.camera_device.BlackLevel.GetValue()
                self.camera_device.Close()
            return BlackLevel
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_black_level_range(self) -> tuple[int, int]:
        """Return the range of the black level.

        :return: the minimum and the maximum value
            of the frame rate in frames per second.
        :rtype: tuple[int, int]

        """
        try:
            if self.camera_device.IsOpen():
                BlackLevelMin = self.camera_device.BlackLevel.GetMin()
                BlackLevelMax = self.camera_device.BlackLevel.GetMax()
            elif not self.camera_device.IsOpen():
                self.camera_device.Open()
                BlackLevelMin = self.camera_device.BlackLevel.GetMin()
                BlackLevelMax = self.camera_device.BlackLevel.GetMax()
                self.camera_device.Close()
            return BlackLevelMin, BlackLevelMax
        except Exception as e:
            print("Exception: " + str(e) + "")

    def set_black_level(self, black_level) -> bool:
        """Set the blackLevel.

        :param black_level: blackLevel.
        :type black_level: int
        :return: True if the black level is lower than the maximum.
        :rtype: bool

        """
        if black_level > 2 ** self.nb_bits_per_pixels - 1:
            return False
        try:
            if self.camera_device.IsOpen():
                self.camera_device.BlackLevel.SetValue(black_level)
            else:
                self.camera_device.Open()
                self.camera_device.BlackLevel.SetValue(black_level)
                self.camera_device.Close()
            return True
        except Exception as e:
            print("Exception: " + str(e) + "")

    def get_clock_frequency(self) -> float:
        """Return the clock frequency of the device.

        :return: clock frequency of the device in Hz.
        :rtype: float

        """
        pass

    def get_clock_frequency_range(self) -> tuple[float, float]:
        """Return Return the range of the clock frequency of the device.

        :return: the minimum and the maximum value
            of the clock frequency of the device in Hz.
        :rtype: tuple[float, float]

        """
        pass

    def set_clock_frequency(self, clock_frequency: int) -> bool:
        """Set the clock frequency of the camera.

        :param clock_frequency: Clock Frequency in Hertz.
        :type clock_frequency: int

        :return: Return true if the Clock Frequency changed.
        :rtype: bool
        """
        pass


if __name__ == "__main__":
    '''
    from camera_list import CameraList

    # Create a CameraList object
    cam_list = CameraList()
    # Print the number of camera connected
    print(f"Test - get_nb_of_cam : {cam_list.get_nb_of_cam()}")
    # Collect and print the list of the connected cameras
    cameras_list = cam_list.get_cam_list()
    print(f"Test - get_cam_list : {cameras_list}")

    cam_id = 'a'
    while cam_id.isdigit() is False:
        cam_id = input('Enter the ID of the camera to connect :')
    cam_id = int(cam_id)
    print(f"Selected camera : {cam_id}")

    # Create a camera object
    my_cam_dev = cam_list.get_cam_device(cam_id)
    '''
    my_cam_dev = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    my_cam = CameraBasler(my_cam_dev)
    my_cam.init_camera()

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
    from matplotlib import pyplot as plt

    plt.imshow(images[0], interpolation='nearest', cmap='gray')
    plt.show()

    '''
    if my_cam.set_aoi(200, 300, 500, 400):
        print('AOI OK')
        # Test to catch images
        st = time.time()
        images = my_cam.get_images()
        et = time.time()

        # get the execution time
        elapsed_time = et - st
        print('\tExecution time:', elapsed_time, 'seconds')  
        print(images[0].shape)      
    '''
    '''
    # Different exposure time
    my_cam.reset_aoi()

    t_expo = np.linspace(t_min, t_max/10000.0, 11)
    for i, t in enumerate(t_expo):
        print(f'\tExpo Time = {t}us')
        my_cam.set_exposure(t)
        images = my_cam.get_images()
        plt.imshow(images[0], interpolation='nearest')
        plt.show()        
    '''
    '''
    # Frame Rate
    ft_act = my_cam.get_frame_rate()
    print(f'Actual Frame Time = {ft_act} fps')
    my_cam.set_frame_rate(20)
    ft_act = my_cam.get_frame_rate()
    print(f'New Frame Time = {ft_act} fps')

    # BlackLevel
    bl_act = my_cam.get_black_level()
    print(f'Actual Black Level = {bl_act}')
    my_cam.set_black_level(200)
    bl_act = my_cam.get_black_level()
    print(f'New Black Level = {bl_act}')
    '''
