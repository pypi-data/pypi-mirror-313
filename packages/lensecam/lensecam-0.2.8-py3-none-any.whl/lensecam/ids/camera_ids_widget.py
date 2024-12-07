# -*- coding: utf-8 -*-
"""camera_ids file.

File containing :class::CameraIds
class to communicate with an IDS camera sensor.

.. module:: CameraIds
   :synopsis: class to communicate with an IDS camera sensor.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>


.. warning::

    **IDS peak** (2.8 or higher) and **IDS Sofware Suite** (4.95 or higher) softwares
    are required on your computer.

    For old IDS camera, IDS peak must be installed in Custom mode with the Transport Layer option.

    **IDS peak IPL** (Image Processing Library) and **Numpy** are required.

.. note::

    To use old IDS generation of cameras (type UI), you need to install **IDS peak** in **custom** mode
    and add the **uEye Transport Layer** option.

.. note::

    **IDS peak IPL** can be found in the *IDS peak* Python API.

    Installation file is in the directory :file:`INSTALLED_PATH_OF_IDS_PEAK\generic_sdk\ipl\binding\python\wheel\x86_[32|64]`.

    Then run this command in a shell (depending on your python version and computer architecture):

    .. code-block:: bash

        pip install ids_peak_1.2.4.1-cp<version>-cp<version>m-[win32|win_amd64].whl

    Generally *INSTALLED_PATH_OF_IDS_PEAK* is :file:`C:\Program Files\IDS\ids_peak`

@ see : https://www.1stvision.com/cameras/IDS/IDS-manuals/en/index.html
@ See API DOC : C:\Program Files\IDS\ids_peak\generic_sdk\api\doc\html

# >>> ids_peak.Library.Initialize()
# >>> device_manager = ids_peak.DeviceManager.Instance()
# >>> device_manager.Update()
# >>> device_descriptors = device_manager.Devices()
# >>> my_cam_dev = device_descriptors[0].OpenDevice(ids_peak.DeviceAccessType_Exclusive)
# >>> my_cam = CameraIds(my_cam_dev)

"""

import numpy as np
from ids_peak import ids_peak

if __name__ == "__main__":
    from camera_ids import CameraIds, get_bits_per_pixel
    from camera_list import CameraList
else:
    from lensecam.ids.camera_ids import CameraIds, get_bits_per_pixel
    from lensecam.ids.camera_list import CameraList

from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QGridLayout, QComboBox
from PyQt6.QtCore import pyqtSignal, Qt
from lensepy.images.conversion import array_to_qimage, resize_image_ratio


class CameraIdsWidget(QWidget):
    """CameraIdsWidget class, children of QWidget.

    Class to integrate an IDS camera into a PyQt6 graphical interface.

    :param cameras_list_widget: Widget containing a ComboBox with the list of available cameras.
    :type cameras_list_widget: CameraIdsListWidget
    :param layout: Main layout container of the widget.
    :type layout: QGridLayout
    :param camera: Device to control
    :type camera: CameraIds

    .. note::

        The camera is initialized with the following parameters :

        * Exposure time = 10 ms
        * FPS = 10
        * Black Level = 0
        * Color Mode = 'Mono12' (if possible)

    :param camera_display: Area to display the camera image
    :type camera_display: QLabel
    """
    connected = pyqtSignal(str)

    def __init__(self, camera: CameraIds = None, params_disp=False):
        """

        :param camera: The camera device to control.
        :param params_disp: If True, display parameters of the camera.
        """
        super().__init__(parent=None)
        self.layout = QGridLayout()
        # Camera
        self.display_params = params_disp
        self.camera = camera
        if camera is not None:
            self.camera_connected = True
        else:
            self.camera_connected = False
        # GUI
        self.camera_display = QLabel('Image')
        self.camera_display_params = SmallParamsDisplay(self)
        self.cameras_list_widget = QWidget()
        self.initUI()

    def initUI(self):
        self.setLayout(self.layout)
        if self.camera is None:
            self.cameras_list_widget = CameraIdsListWidget()
            self.layout.addWidget(self.cameras_list_widget, 0, 0)
            # Connect the signal emitted by the ComboList to its action
            self.cameras_list_widget.connected.connect(self.connect_camera)
        else:
            self.layout.addWidget(self.camera_display, 0, 0)
            self.set_camera(camera=self.camera)

    def set_camera(self, camera: CameraIds):
        """

        :param camera:
        :return:
        """
        self.camera = camera

        self.camera_connected = True
        self.camera_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.display_params:
            self.clear_layout(1, 0)
            self.layout.addWidget(self.camera_display_params, 1, 0)

    def connect_camera(self, event):
        try:
            cam_dev = self.cameras_list_widget.get_selected_camera_dev()
            self.camera = CameraIds(cam_dev)
            self.camera_connected = True

            self.clear_layout(0, 0)
            self.clear_layout(1, 0)
            self.camera_display = QLabel('Image')
            self.camera_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.camera_display, 0, 0)
            if self.display_params:
                self.clear_layout(1, 0)
                self.layout.addWidget(self.camera_display_params, 1, 0)
            self.connected.emit('cam')
        except Exception as e:
            print(f'Exception - connect_camera {e}')

    def update_params(self):
        if self.display_params:
            self.camera_display_params.update_params()

    def clear_layout(self, row: int, column: int) -> None:
        """Remove widgets from a specific position in the layout.

        :param row: Row index of the layout.
        :type row: int
        :param column: Column index of the layout.
        :type column: int

        """
        item = self.layout.itemAtPosition(row, column)
        if item is not None:
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.layout.removeItem(item)


class SmallParamsDisplay(QWidget):
    """Area to display main parameters of the camera.

    :param parent: Parent widget of this widget.
    :type parent: CameraIdsWidget
    :param camera: Device to control
    :type camera: pylon.TlFactory
    :param small_layout: Layout of the widget
    :type small_layout: QGridLayout
    :param camera_name_label: Label to display the name of the camera.
    :type camera_name_label: QLabel
    :param camera_colormode_label: Label to display the color mode of the camera.
    :type camera_colormode_label: QLabel
    :param camera_expotime_label: Label to display the exposure time of the camera.
    :type camera_expotime_label: QLabel
    :param camera_fps_label: Label to display the frame rate of the camera.
    :type camera_fps_label: QLabel
    """

    def __init__(self, parent) -> None:
        """
        Default constructor of the class.

        :param parent: Parent widget of this widget.
        :type parent: CameraIdsWidget
        """
        super().__init__(parent=None)
        self.parent = parent
        # Camera device
        self.camera = None
        # Layout Grid
        self.small_layout = QGridLayout()
        self.small_layout.setSpacing(20)
        # Internal Widgets
        self.camera_name_label = QLabel('Name')
        self.camera_colormode_label = QLabel('ColorMode')
        self.camera_expotime_label = QLabel('Exposure')
        self.camera_fps_label = QLabel('FPS')
        # Add widgets to the layout
        self.small_layout.addWidget(self.camera_name_label, 0, 0)
        self.small_layout.addWidget(self.camera_colormode_label, 0, 1)
        self.small_layout.addWidget(self.camera_expotime_label, 0, 2)
        self.small_layout.addWidget(self.camera_fps_label, 0, 3)
        # All the grid box have the same width
        for i in range(self.small_layout.columnCount()):
            self.small_layout.setColumnStretch(i, 1)
        self.setLayout(self.small_layout)

    def update_params(self) -> None:
        """
        Update the display of the parameters
        """
        camera = self.parent.camera
        _, name = camera.get_cam_info()
        name = 'Camera : ' + name
        self.camera_name_label.setText(name)
        colormode = camera.get_color_mode()
        self.camera_colormode_label.setText(colormode)
        expo = str(round(camera.get_exposure() / 1000, 2)) + ' ms'
        self.camera_expotime_label.setText(expo)
        fps = str(round(camera.get_frame_rate(), 2)) + ' fps'
        self.camera_fps_label.setText(fps)


class CameraIdsListWidget(QWidget):
    """Generate available cameras list.

    Generate a Widget including the list of available cameras and two buttons :
        * connect : to connect a selected camera ;
        * refresh : to refresh the list of available cameras.

    :param cam_list: CameraList object that lists available cameras.
    :type cam_list: CameraList
    :param cameras_list: list of the available IDS Camera.
    :type cameras_list: list[tuple[int, str, str]]
    :param cameras_nb: Number of available cameras.
    :type cameras_nb: int
    :param cameras_list_combo: A QComboBox containing the list of the available cameras
    :type cameras_list_combo: QComboBox
    :param main_layout: Main layout container of the widget.
    :type main_layout: QVBoxLayout
    :param title_label: title displayed in the top of the widget.
    :type title_label: QLabel
    :param bt_connect: Graphical button to connect the selected camera
    :type bt_connect: QPushButton
    :param bt_refresh: Graphical button to refresh the list of available cameras.
    :type bt_refresh: QPushButton
    """

    connected = pyqtSignal(str)

    def __init__(self) -> None:
        """
        Default constructor of the class.
        """
        super().__init__(parent=None)
        # Objects linked to the CameraList object
        self.cam_list = CameraList()
        self.cameras_list = self.cam_list.get_cam_list()
        self.cameras_nb = self.cam_list.get_nb_of_cam()

        # Graphical list as QComboBox
        self.cameras_list_combo = QComboBox()

        # Graphical elements of the interface
        self.main_layout = QVBoxLayout()

        self.title_label = QLabel('Available cameras')

        self.bt_connect = QPushButton('Connect')
        self.bt_connect.clicked.connect(self.send_signal_connected)
        self.bt_refresh = QPushButton('Refresh')
        self.bt_refresh.clicked.connect(self.refresh_cameras_list_combo)

        if self.cameras_nb == 0:
            self.bt_connect.setEnabled(False)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.cameras_list_combo)
        self.main_layout.addWidget(self.bt_connect)
        self.main_layout.addWidget(self.bt_refresh)

        self.setLayout(self.main_layout)
        self.refresh_cameras_list_combo()

    def refresh_cameras_list(self) -> None:
        """Refresh the list of available cameras.

        Update the cameras_list parameter of this class.
        """
        self.cam_list.refresh_list()
        self.cameras_list = self.cam_list.get_cam_list()
        self.cameras_nb = self.cam_list.get_nb_of_cam()
        if self.cameras_nb == 0:
            self.bt_connect.setEnabled(False)
        else:
            self.bt_connect.setEnabled(True)

    def refresh_cameras_list_combo(self) -> None:
        """Refresh the combobox list of available cameras.

        Update the cameras_list_combo parameter of this class.
        """
        self.refresh_cameras_list()
        self.cameras_list_combo.clear()
        for i, cam in enumerate(self.cameras_list):
            self.cameras_list_combo.addItem(f'IDS-{cam[1]}')

    def get_selected_camera_index(self):
        """Return the index of the selected device.
        :rtype: pylon.TlFactory
        """
        return self.cameras_list_combo.currentIndex()

    def get_selected_camera_dev(self) -> ids_peak.Device:
        """Return the device object.

        Return the device object from ids_peak API of the selected camera.

        :return: the index number of the selected camera.
        :rtype: ids_peak.Device
        """
        cam_id = self.cameras_list_combo.currentIndex()
        dev = self.cam_list.get_cam_device(cam_id)
        return dev

    def send_signal_connected(self, event) -> None:
        """Send a signal when a camera is selected to be used.
        """
        cam_id = self.cameras_list_combo.currentIndex()
        self.connected.emit('cam:' + str(cam_id) + ':')


if __name__ == '__main__':
    class Remote(QWidget):
        """"""
        transmitted = pyqtSignal(str)

        def __init__(self, camera: CameraIds = None):
            super().__init__(parent=None)
            self.initUI()
            self.camera = camera

        def set_camera(self, camera: CameraIds):
            self.camera = camera
            self.camera.init_camera()
            self.camera.alloc_memory()

        def initUI(self):
            self.get_image_button = QPushButton('Get Image')
            self.get_image_button.clicked.connect(self.action_button)
            self.stop_acq_button = QPushButton('Stop Acq')
            self.stop_acq_button.clicked.connect(self.action_button)
            self.start_acq_button = QPushButton('Start Acq')
            self.start_acq_button.clicked.connect(self.action_button)
            self.expo_button = QPushButton('Expo')
            self.expo_button.clicked.connect(self.action_button)

            self.layout = QVBoxLayout()
            self.layout.addWidget(self.get_image_button)
            self.layout.addWidget(self.start_acq_button)
            self.layout.addWidget(self.stop_acq_button)
            self.layout.addWidget(self.expo_button)

            self.setLayout(self.layout)

        def action_button(self, event):
            button = self.sender()
            if button == self.get_image_button:
                self.transmitted.emit('get')
            if button == self.start_acq_button:
                self.transmitted.emit('start')
            if button == self.stop_acq_button:
                self.transmitted.emit('stop')
            if button == self.expo_button:
                self.transmitted.emit('expo')


    from PyQt6.QtWidgets import QMainWindow
    from PyQt6.QtGui import QPixmap
    from lensecam.camera_thread import CameraThread


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.initUI()

            self.camera_thread = CameraThread()
            self.camera_thread.image_acquired.connect(self.update_image)

        def initUI(self):
            self.setWindowTitle("IDS Camera Display")
            self.setGeometry(100, 100, 800, 600)

            self.layout = QGridLayout()
            self.camera_widget = None
            self.remote = Remote()
            self.remote.transmitted.connect(self.action_remote)
            self.layout.addWidget(self.remote, 2, 0)

            self.central_widget = QWidget()
            self.central_widget.setLayout(self.layout)
            self.setCentralWidget(self.central_widget)

        def action_remote(self, event):
            if event == 'get':
                try:
                    self.camera_widget.update_params()
                    self.camera_widget.camera.alloc_memory()
                    self.camera_widget.camera.start_acquisition()
                    raw_array = self.camera_widget.camera.get_image()
                    # Depending on the color mode - display only in 8 bits mono
                    nb_bits = 8  # get_bits_per_pixel(self.camera.get_color_mode())
                    if nb_bits > 8:
                        image_array = raw_array.view(np.uint16)
                        image_array_disp = (image_array / (2 ** (nb_bits - 8))).astype(np.uint8)
                    else:
                        image_array_disp = raw_array
                    frame_width = self.camera_widget.width()
                    frame_height = self.camera_widget.height()
                    # Resize to the display size
                    image_array_disp2 = resize_image_ratio(
                        image_array_disp,
                        frame_width,
                        frame_height)
                    # Convert the frame into an image
                    image = array_to_qimage(image_array_disp2)
                    pmap = QPixmap(image)
                    # display it in the cameraDisplay
                    self.camera_widget.camera_display.setPixmap(pmap)
                    self.camera_widget.camera.stop_acquisition()
                    self.camera_widget.camera.free_memory()
                except Exception as e:
                    print("Exception - action_get_image: " + str(e) + "")
            elif event == 'start':
                self.camera_thread.start()
            elif event == 'stop':
                self.camera_widget.camera.set_exposure(1000)
                self.camera_thread.stop()
            elif event == 'expo':
                self.camera_widget.camera.set_exposure(20000)

        def set_camera(self, camera: CameraIds, mode_max: bool = False):
            """

            """
            self.camera_thread.set_camera(camera)
            self.camera_widget = CameraIdsWidget(camera, params_disp=True)
            self.camera_widget.camera.init_camera(mode_max=mode_max)
            self.layout.addWidget(self.camera_widget, 1, 0)

        def update_image(self, image_array):
            try:
                frame_width = self.camera_widget.width()
                frame_height = self.camera_widget.height()
                # Resize to the display size
                image_array_disp2 = resize_image_ratio(
                    image_array,
                    frame_width,
                    frame_height)
                # Convert the frame into an image
                image = array_to_qimage(image_array_disp2)
                pmap = QPixmap(image)
                # display it in the cameraDisplay
                self.camera_widget.camera_display.setPixmap(pmap)
            except Exception as e:
                print(f'Exception - update_image {e}')

        def closeEvent(self, event):
            self.camera_thread.stop()
            event.accept()


    import sys
    from PyQt6.QtWidgets import QApplication

    camera_ids = CameraIds()
    if camera_ids.find_first_camera():
        device = camera_ids.camera_device

    # Test with a Thread
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.set_camera(camera_ids)  # , mode_max=True)
    main_window.show()
    sys.exit(app.exec())

    ''' # Test image by image
    try:
        print(camera_ids.get_cam_info())
        camera_ids.init_camera()
        camera_ids.alloc_memory()

        numberOfImagesToGrab = 2
        camera_ids.start_acquisition()

        for k in range(numberOfImagesToGrab):
            raw_image = camera_ids.get_image()
            color_image = raw_image.ConvertTo(ids_ipl.PixelFormatName_Mono8)
            picture = color_image.get_numpy_3D()
            picture_shape = picture.shape
            # Access the image data.
            print("SizeX: ", picture_shape[1])
            print("SizeY: ", picture_shape[0])
            print("Gray value of first pixel: ", picture[0, 0])

            cv2.imshow('image', picture)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        camera_ids.stop_acquisition()
        camera_ids.free_memory()

    except Exception as e:
        print("EXCEPTION: " + str(e))

    finally:
        ids_peak.Library.Close()

    '''