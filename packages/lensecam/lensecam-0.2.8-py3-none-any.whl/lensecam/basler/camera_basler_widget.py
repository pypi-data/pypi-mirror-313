# -*- coding: utf-8 -*-
"""*camera_basler_widget* file.

*camera_basler_widget* file that contains :

    * :class::CameraBaslerWidget to integrate a Basler camera into a PyQt6 graphical interface.
    * :class::CameraBaslerListWidget to generate a Widget including the list of available camerasintegrate a Basler camera into a PyQt6 graphical interface.
    * :class::CameraBaslerParamsWidget to display the parameters of a camera.
    * :class::SmallParamsDisplay to ...

.. module:: CameraBaslerWidget
   :synopsis: class to integrate a Basler camera into a PyQt6 graphical interface.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import os
import sys
import time
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout,
    QLabel, QComboBox, QPushButton, QCheckBox,
    QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

from lensepy.images.conversion import *
from lensepy.pyqt6.widget_slider import WidgetSlider

from lensecam.basler.camera_list import CameraList
from lensecam.basler.camera_basler import CameraBasler, get_bits_per_pixel


class CameraBaslerListWidget(QWidget):
    """Generate available cameras list.

    Generate a Widget including the list of available cameras and two buttons :
        * connect : to connect a selected camera ;
        * refresh : to refresh the list of available cameras.

    :param cam_list: CameraList object that lists available cameras.
    :type cam_list: CameraList
    :param cameras_list: list of the available Basler Camera.
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
        """Default constructor of the class.
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

    def refresh_cameras_list(self):
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

    def refresh_cameras_list_combo(self):
        """Refresh the combobox list of available cameras.

        Update the cameras_list_combo parameter of this class.
        """
        self.refresh_cameras_list()
        self.cameras_list_combo.clear()
        for i, cam in enumerate(self.cameras_list):
            self.cameras_list_combo.addItem(f'BAS-{cam[1]}')

    def get_selected_camera_index(self):
        """Return the index of the selected device.
        :rtype: pylon.TlFactory
        """
        return self.cameras_list_combo.currentIndex()

    def get_selected_camera_dev(self):
        """Return the device object.

        Return the device object from pypylon wraper of the selected camera.

        :return: the index number of the selected camera.
        :rtype: pylon.TlFactory
        """
        cam_id = self.cameras_list_combo.currentIndex()
        dev = self.cam_list.get_cam_device(cam_id)
        return dev

    def send_signal_connected(self, event):
        """Send a signal when a camera is selected to be used.
        """
        cam_id = self.cameras_list_combo.currentIndex()
        self.connected.emit('cam:' + str(cam_id) + ':')


class CameraBaslerParamsWidget(QWidget):
    """CameraBaslerWidget class, children of QWidget.

    Class to display and to change the available parameters of a camera.

    :param parent: Parent widget of this widget.
    :type parent: SmallParamsDisplay
    :param camera: Device to control
    :type camera: pylon.TlFactory

    """
    params_dict = {'fps': 'FPS', 'expo': 'Exposure Time', 'black': 'Black Level'}

    def __init__(self, parent):
        """Default constructor of the class.

        :param parent: Parent widget of this widget.
        :type parent: SmallParamsDisplay
        """
        super().__init__(parent=None)
        self.parent = parent
        # Camera device
        self.camera = None
        # Main layout
        self.main_layout = QVBoxLayout()
        # Graphical objects
        self.name_label = QLabel('Parameters')
        self.auto_update_check = QCheckBox('Auto-Update')
        self.auto_update_validated = False

        top_layout = QGridLayout()
        top_layout.addWidget(self.name_label, 0, 0)
        top_layout.setRowStretch(0, 2)
        top_layout.addWidget(self.auto_update_check, 0, 1)
        top_layout.setRowStretch(1, 1)
        top_widget = QWidget()
        top_widget.setLayout(top_layout)

        self.main_layout.addWidget(top_widget)

        name = CameraBaslerParamsWidget.params_dict['fps']
        signal_name = 'fps'
        self.fps_slider = WidgetSlider(
            name=name, signal_name=signal_name)
        self.fps_slider.slider_changed_signal.connect(self.update_params)
        self.fps_slider.set_units('frames/s')
        self.fps_slider.set_min_max_slider(5, 50)
        fps_value = self.parent.camera.get_frame_rate()
        self.fps_slider.set_value(fps_value)
        self.main_layout.addWidget(self.fps_slider)

        name = CameraBaslerParamsWidget.params_dict['expo']
        signal_name = 'expo'
        self.expotime_slider = WidgetSlider(
            name=name, signal_name=signal_name, integer=True)
        self.expotime_slider.slider_changed_signal.connect(self.update_params)
        self.expotime_slider.set_units('ms')
        max_expo = 1000 / fps_value - 1  # in ms
        self.expotime_slider.set_min_max_slider(1, max_expo)
        expo_value = self.parent.camera.get_exposure()
        self.expotime_slider.set_value(expo_value / 1000)
        self.main_layout.addWidget(self.expotime_slider)

        name = CameraBaslerParamsWidget.params_dict['black']
        signal_name = 'black'
        self.blacklevel_slider = WidgetSlider(
            name=name, signal_name=signal_name, integer=True)
        self.blacklevel_slider.slider_changed_signal.connect(self.update_params)
        self.blacklevel_slider.set_units('LSB')
        cam_bits_nb = get_bits_per_pixel(self.parent.camera.get_color_mode())
        max_blacklevel = 2 ** cam_bits_nb - 1
        self.blacklevel_slider.set_min_max_slider(0, max_blacklevel)
        self.main_layout.addWidget(self.blacklevel_slider)

        self.setFixedSize(300, 400)
        self.setLayout(self.main_layout)

    def set_camera(self, camera) -> None:
        """Set the camera device to setup.

        :param camera: Device to control
        :type camera: pylon.TlFactory
        """
        self.camera = camera
        _, name = self.camera.get_cam_info
        self.name_label.setText(name + ' Parameters')

    def update_params(self, event) -> None:
        """Update parameters."""
        str_event = event.split(':')
        if str_event[0].lower() != 'update':
            if str_event[0].lower() == 'slider':
                if self.auto_update_check.isChecked() is False:
                    return

        if str_event[1].lower() == 'fps':
            value = self.fps_slider.get_real_value()
            # Verify if exposure time is lower than FPS limit
            expo = self.parent.camera.get_exposure() / 1000  # in ms
            fps_t = 1 / value * 1000  # in ms
            expo_val = int(fps_t - 1) * 1000
            print(f'Expo = {expo} - 1/FPS = {fps_t} --> EXP_V = {expo_val}')
            # Update exposure time limits
            self.expotime_slider.set_min_max_slider(1, expo_val / 1000)

            if expo > fps_t:
                print('UPD')
                self.parent.camera.set_exposure(expo_val)
                self.expotime_slider.set_value(expo_val)
            # Update frame rate of the camera
            self.parent.camera.set_frame_rate(value)
            # Update interval of the timer


        elif str_event[1].lower() == 'expo':
            value = self.expotime_slider.get_real_value() * 1000
            # time_ms = 1/value
            # self.parent.parent.main_timer.setInterval()
            self.parent.camera.set_exposure(value)
        elif str_event[1].lower() == 'black':
            value = self.blacklevel_slider.get_real_value()
            self.parent.camera.set_black_level(value)
        else:
            print('Error')

        # Update Small panel information
        self.parent.update_params()

    def closeEvent(self, event):
        """closeEvent redefinition.

        Use when the user clicks on the red cross
        to close the window.
        """
        reply = QMessageBox.question(self, 'Quit', 'Do you really want to close ?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()  # L'utilisateur a confirmé la fermeture
        else:
            event.ignore()  # L'utilisateur a annulé la fermeture


class SmallParamsDisplay(QWidget):
    """Area to display main parameters of the camera.

    :param parent: Parent widget of this widget.
    :type parent: CameraBaslerWidget
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
        :type parent: CameraBaslerWidget
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
        self.params_button = QPushButton('Parameters')
        self.params_button.clicked.connect(self.params_button_action)
        # Add widgets to the layout
        self.small_layout.addWidget(self.camera_name_label, 0, 0, 1, 2)
        self.small_layout.addWidget(self.params_button, 0, 2)
        self.small_layout.addWidget(self.camera_colormode_label, 1, 0)
        self.small_layout.addWidget(self.camera_expotime_label, 1, 1)
        self.small_layout.addWidget(self.camera_fps_label, 1, 2)
        # All the grid box have the same width
        for i in range(self.small_layout.columnCount()):
            self.small_layout.setColumnStretch(i, 1)

        self.setLayout(self.small_layout)

    def set_camera(self, camera) -> None:
        """
        Set the camera device to setup.

        :param camera: Device to control
        :type camera: pylon.TlFactory
        """
        self.camera = camera

    def update_params(self) -> None:
        """
        Update the display of the parameters
        """
        _, name = self.camera.get_cam_info()
        name = 'Camera : ' + name
        self.camera_name_label.setText(name)
        colormode = self.camera.get_color_mode()
        self.camera_colormode_label.setText(colormode)
        expo = str(self.camera.get_exposure() / 1000) + ' ms'
        self.camera_expotime_label.setText(expo)
        fps = str(self.camera.get_frame_rate()) + ' fps'
        self.camera_fps_label.setText(fps)

    def params_button_action(self):
        """
        Call when the parameters button is clicked.
        Open a new window to modify the camera parameters.
        """
        print('PARAMS')
        self.params_window = CameraBaslerParamsWidget(self)
        self.params_window.set_camera(self.camera)
        self.params_window.show()


class CameraBaslerWidget(QWidget):
    """CameraBaslerWidget class, children of QWidget.

    Class to integrate a Basler camera into a PyQt6 graphical interface.

    :param cameras_list_widget: Widget containing a ComboBox with the list of available cameras.
    :type cameras_list_widget: CameraBaslerListWidget
    :param main_layout: Main layout container of the widget.
    :type main_layout: QGridLayout
    :param camera: Device to control
    :type camera: pylon.TlFactory

    .. note::

        The camera is initialized with the following parameters :

        * Exposure time = 100 ms
        * FPS = 5
        * Black Level = 0
        * Color Mode = 'Mono12' (if possible)

    :param camera_display: Area to display the camera image
    :type camera_display: QLabel
    :param camera_infos: Area to display camera informations (FPS, expotime...)
    :type camera_display_params: SmallParamsDisplay
    :param main_timer: timer object to manage display refresh
    :type main_timer: QTimer

    """

    connected = pyqtSignal(str)

    def __init__(self, camera: CameraBasler = None, params_disp=False):
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
            self.cameras_list_widget = CameraBaslerListWidget()
            self.layout.addWidget(self.cameras_list_widget, 0, 0)
            # Connect the signal emitted by the ComboList to its action
            self.cameras_list_widget.connected.connect(self.connect_camera)
        else:
            self.layout.addWidget(self.camera_display, 0, 0)
            self.set_camera(camera=self.camera)

    def set_camera(self, camera: CameraBasler):
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
            self.camera_display_params.update_params()

    def connect_camera(self) -> None:
        """
        Trigger action when a connected signal from the combo list is emitted.
        """
        # Get the index of the selected camera
        cam_dev = self.cameras_list_widget.get_selected_camera_dev()
        # Create Camera object
        self.camera = CameraBasler(cam_dev)
        self.camera.init_camera(cam_dev)

        self.camera_connected = True

        self.clear_layout(0, 0)
        self.clear_layout(1, 0)
        self.camera_display = QLabel('Image')
        self.camera_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.camera_display, 0, 0)
        if self.display_params:
            self.clear_layout(1, 0)
            self.layout.addWidget(self.camera_display_params, 1, 0)
            self.camera_display_params.set_camera(self.camera)
            self.camera_display_params.update_params()
        self.connected.emit('cam')


    def is_connected(self) -> bool:
        """
        Test if a camera is connected.

        :return: True if a camera is connected.
        :rtype: bool
        """
        if self.camera is None:
            return False
        else:
            return True

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

    def refresh(self) -> None:
        """
        Refresh the image from camera.

        .. note::

            This function is called by a QTimer event
            according to the FPS rate.

        """

        if self.is_connected():
            # Get raw image
            image_array = self.camera.get_images()[0]
            # Get widget size
            frame_width = self.width() - 30
            frame_height = self.height() - 120

            # Depending on the color mode - display only in 8 bits mono
            nb_bits = get_bits_per_pixel(
                self.camera.get_color_mode())
            if nb_bits > 8:
                image_array = image_array.view(np.uint16)
                image_array_disp = (image_array / (2 ** (nb_bits - 8))).astype(np.uint8)
            else:
                image_array = image_array.view(np.uint8)
                image_array_disp = image_array.astype(np.uint8)

            # Resize to the display size
            image_array_disp2 = resize_image(
                image_array_disp,
                frame_width,
                frame_height)
            # Convert the frame into an image
            image = array_to_qimage(image_array_disp2)
            pmap = QPixmap(image)

            # display it in the cameraDisplay
            self.camera_display.setPixmap(pmap)
        else:
            self.camera_display.setText('No Camera Connected')

    def quit_application(self) -> None:
        """
        Quit properly the PyQt6 application window.
        """
        if self.main_timer.isActive():
            self.main_timer.stop()
            print('TIMER STOP')
        time.sleep(0.5)
        if self.camera is not None:
            self.camera.disconnect()
            print('DISCONNECTED')
        QApplication.instance().quit()


if __name__ == "__main__":

    class MyMainWindow(QMainWindow):
        """MyMainWindow class, children of QMainWindow.

        Class to test the previous widget.

        """

        def __init__(self) -> None:
            """
            Default constructor of the class.
            """
            super().__init__()
            self.setWindowTitle("CameraBaslerWidet Test Window")
            self.setGeometry(100, 100, 500, 400)
            # self.central_widget = CameraBaslerParamsWidget(self)
            self.central_widget = CameraBaslerWidget()
            self.setCentralWidget(self.central_widget)

        def closeEvent(self, event):
            """
            closeEvent redefinition. Use when the user clicks
            on the red cross to close the window
            """
            reply = QMessageBox.question(self, 'Quit', 'Do you really want to close ?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.central_widget.quit_application()
                event.accept()
            else:
                event.ignore()


    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())
