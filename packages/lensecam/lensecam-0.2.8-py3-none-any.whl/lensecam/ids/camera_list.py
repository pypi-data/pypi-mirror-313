"""CameraList class to obtain the list of IDS sensors connected to the computer.

.. module:: CameraList
   :synopsis: class to obtain the list of IDS sensors connected to the computer.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

"""
# IDS peak API
from ids_peak import ids_peak

class CameraList():
    """    
    Class to list IDS camera (all camera in a future evolution)
    
    :param available_cameras: List of the devices connected to the computer [id, device]
    :type available_cameras: list[tuple[int, pylon.TlFactory]]
    :param camera_list_str: List to print of the devices connected to the computer [id, serial number, device name]
    :type available_cameras: list[tuple[int, str, str]]
    :param nb_cam: Number of connected cameras
    :type nb_cam: int  
    
    Example
    
    In this example, you create a :class:`CameraList` object, then get the number of Basler cameras connected to your computer (in this case 1 camera is connected) and finally obtain the complete list of the available cameras (in this case a *a2A1920-160ucBAS* camera with the serial number *40282239*).

    >>> from camera_list import CameraList
    >>> cam_list = CameraList()
    >>> cam_list.get_nb_of_cam()
    '1'
    >>> cameras_list = cam_list.get_cam_list()
    >>> print(cameras_list)
    '[[0, 40282239, 'a2A1920-160ucBAS']]'
    
    """
    
    def __init__(self):
        """
        Default constructor of the class.
        """

        # Initialize library
        ids_peak.Library.Initialize()

        # Device manager
        self.device_manager = ids_peak.DeviceManager.Instance()
        self.device_manager.Update()
        self.device_descriptors = self.device_manager.Devices()

        self.available_cameras: list[tuple[int, ids_peak.Device]] = []
        self.camera_list_str: list[tuple[int, str, str]] = []
        self.nb_cam: int = 0
        self.__create_list()
        
    def __create_list(self) -> None:
        """
        Create the two lists of available cameras (devices and printable list).
        """
        self.device_manager.Update()
        self.device_descriptors = self.device_manager.Devices()

        self.available_cameras = []
        self.camera_list_str = []
        self.nb_cam = self.device_descriptors.size()

        # Display devices
        for id, device_desc in enumerate(self.device_descriptors):
            self.available_cameras.append([id, device_desc])
            self.camera_list_str.append([id, device_desc.SerialNumber(), device_desc.DisplayName()])

    def refresh_list(self) -> None:
        """
        Refresh the list of the connected devices.
        """
        self.__create_list()
    
    
    def get_nb_of_cam(self) -> int:
        """
        Return the number of connected cameras

        :return: Number of Basler connected cameras
        :rtype: int
        """
        return self.nb_cam

    def get_cam_list(self) -> list[tuple[int, str, str]]:
        """
        Return the list containing the ID, serial number and name of all cameras connected

        :return: list with ID, Serial Number and Name of each camera connected on the computer [[cam1_id, cam1_ser_no, cam1_name], ... ]
        :rtype: list
        """
        return self.camera_list_str
            
    def get_cam_device(self, idx: int) -> ids_peak.Device:
        """
        Return the list containing the ID and a device pypylon object

        :return: Device corresponding to the index in the list of available cameras
        :rtype: pylon.TlFactory.Device
        """
        for i, d in self.available_cameras:
            print('OK')
            if i == idx:
                my_camera = self. device_descriptors[i].OpenDevice(ids_peak.DeviceAccessType_Exclusive)
                return my_camera
            else:
                return None

if __name__ == "__main__":
    cam_list = CameraList()
    print(cam_list.get_nb_of_cam())
    cameras_list = cam_list.get_cam_list()
    print(cameras_list)