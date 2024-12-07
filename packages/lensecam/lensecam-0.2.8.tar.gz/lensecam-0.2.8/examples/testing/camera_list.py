"""CameraList class to obtain the list of Basler sensors connected to the computer.

.. module:: CameraList
   :synopsis: class to obtain the list of Basler sensors connected to the computer.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

"""
from pypylon import pylon

class CameraList():
    """    
    Class to list Basler camera (all camera in a future evoluation)
    
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
        self.available_cameras: list[tuple[int, pylon.TlFactory]] = []
        self.camera_list_str: list[tuple[int, str, str]] = []
        self.nb_cam: int = 0
        self.__create_list()
        
    def __create_list(self) -> None:
        """
        Create the two lists of available cameras (devices and printable list).
        """
        self.available_cameras = []
        self.camera_list_str = []
        self.nb_cam = 0
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        for id, d in enumerate(devices):
            dev = pylon.InstantCamera(tlFactory.CreateDevice(d))
            if dev.IsUsb():
                self.available_cameras.append([id, d])
                FriendlyName = d.GetFriendlyName().split(' ')
                FullModelName, SerNo = FriendlyName[1], int(FriendlyName[2].strip("()"))
                self.camera_list_str.append([id, SerNo, FullModelName])
                self.nb_cam += 1
                
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
            
    def get_cam_device(self, idx: int) -> pylon.TlFactory:
        """
        Return the list containing the ID and a device pypylon object

        :return: Device corresponding to the index in the list of available cameras
        :rtype: pylon.TlFactory.Device
        """
        for i, d in self.available_cameras:
            if i == idx:
                return pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(d))
            else:
                return None



if __name__ == "__main__":
    cam_list = CameraList()
    print(cam_list.get_nb_of_cam())
    cameras_list = cam_list.get_cam_list()
    print(cameras_list)