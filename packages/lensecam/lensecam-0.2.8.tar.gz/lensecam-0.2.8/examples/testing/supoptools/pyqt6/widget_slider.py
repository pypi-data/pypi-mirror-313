# -*- coding: utf-8 -*-
"""*widget_slider* file.

*widget_slider* file that contains :class::WidgetSlider 

.. module:: WidgetSlider
   :synopsis: class to display a slider in PyQt6.

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

#### TO REWRITE !!! PEP8 / PEP257

import sys

# Third pary imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, 
    QGridLayout, QVBoxLayout,
    QWidget, QLineEdit, QLabel, QPushButton, QSlider,
    QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt


def is_number(value, min_val=0, max_val=0):
    """Return if the value is a valid number.
    
    Return true if the value is a number between min and max.

    :param value: Float number to test.
    :type value: float
    :param min_val: Minimum of the interval to test.
    :type min_val: float
    :param max_val: Maximum of the interval to test.
    :type max_val: float
    :return: True if the value is between min and max.
    :rtype: bool    

    """
    min_ok = False
    max_ok = False
    value2 = str(value).replace('.', '', 1)
    value2 = value2.replace('e', '', 1)
    value2 = value2.replace('-', '', 1)
    if value2.isdigit():
        value = float(value)
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        if (min_val != '') and (int(value) >= min_val):
            min_ok = True
        if (max_val != '') and (int(value) <= max_val):
            max_ok = True
        if min_ok != max_ok:
            return False
        else:
            return True
    else:
        return False


class WidgetSlider(QWidget):    
    """Create a Widget with a slider.
    
    WidgetSlider class to create a widget with a slider and its value.
    Children of QWidget

    :param ratio_slider: Use to display non integer on the Slider.
        Defaults to 10.0.
    :type ratio_slider: float
    
    .. note::
        
        For example, with a ratio_slider at 10, the slider
        value of 500 corresponds to a real value of 50.0.


    max_real_value : float
        Maximum value of the slider.
    min_real_value : float
        Minimum value of the slider.
    real_value : float
        Value of the slider.

    """

    slider_changed_signal = pyqtSignal(str)

    def __init__(self, name="", percent=False, integer=False, signal_name=""):
        """
        
        :param name: Name of the slider, defaults to "".
        :type name: str, optional
        :param percent: Specify if the slider is in percent, defaults to False.
        :type percent: bool, optional
        :param integer: Specify if the slider is an integer, defaults to False.
        :type integer: bool, optional
        :param signal_name: Name of the signal, defaults to "".
        :type percent: str, optional
        :return: DESCRIPTION
        :rtype: TYPE

        """
        super().__init__(parent=None)

        # Global values
        self.percent = percent
        self.integer = integer
        self.min_real_value = 0
        self.max_real_value = 100
        self.ratio_slider = 10.0
        self.real_value = 1
        self.enabled = True
        self.name = name
        if signal_name == '':
            self.signal_name = self.name
        else:
            self.signal_name = signal_name
        ''' Layout Manager '''
        self.main_layout = QGridLayout()
        ''' Graphical Objects '''
        self.name_label = QLabel(name)
        self.user_value = QLineEdit()
        self.max_slider_label = QLabel(f'{self.max_real_value}')
        self.min_slider_label = QLabel(f'{self.min_real_value}')
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(int(self.min_real_value*self.ratio_slider))
        self.slider.setMaximum(int(self.max_real_value*self.ratio_slider))
        self.slider.setValue(int(self.real_value*self.ratio_slider))
        self.units = ''
        self.units_label = QLabel('')
        self.update_button = QPushButton('Update')
        self.update_button.setEnabled(True)
        
        # Adding graphical objects to the main layout
        self.main_layout.addWidget(self.name_label, 0, 0, 1, 3)
        self.main_layout.addWidget(self.user_value, 0, 3)
        self.main_layout.addWidget(self.units_label, 0, 4)
        self.main_layout.addWidget(self.min_slider_label, 1, 0)
        self.main_layout.addWidget(self.slider, 1, 1, 1, 3)
        self.main_layout.addWidget(self.max_slider_label, 1, 4)
        self.main_layout.addWidget(self.update_button, 2, 3, 1, 2)
        self.setLayout(self.main_layout)
        
        for i in range(self.main_layout.rowCount()):
            self.main_layout.setRowStretch(i, 1)
        for i in range(self.main_layout.columnCount()):
            self.main_layout.setColumnStretch(i, 1)

        ''' Events '''
        self.slider.valueChanged.connect(self.slider_changed)
        self.set_value(self.real_value)
        self.update_button.clicked.connect(self.value_changed)
        self.update_display()
        self.update_GUI()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.name_label.setText(name)

    def set_enabled(self, value):
        self.enabled = value
        self.update_GUI()

    def update_GUI(self):
        self.slider.setEnabled(self.enabled)
        self.user_value.setEnabled(self.enabled)

    def value_changed(self, event):
        value = self.user_value.text()
        value2 = value.replace('.', '', 1)
        value2 = value2.replace('e', '', 1)
        value2 = value2.replace('-', '', 1)
        if value2.isdigit():
            self.real_value = float(value)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(f"Not a number")
            msg.setWindowTitle("Not a Number Value")
            msg.exec()
            self.real_value = self.min_real_value
            self.user_value.setText(str(self.real_value))
        # Test if value is between min and max
        if not is_number(self.real_value, self.min_real_value, self.max_real_value):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText('This number is not in the good range')
            msg.setWindowTitle("Outside Range")
            msg.exec()
            self.real_value = self.min_real_value
            self.user_value.setText(str(self.real_value))
            self.real_value = self.min_real_value
        
        if self.integer:
            self.real_value = int(self.real_value)
        self.slider.setValue(int(self.real_value*self.ratio_slider))
        self.update_display()
        self.slider_changed_signal.emit('update:'+self.signal_name)

    def slider_changed(self, event):
        self.real_value = self.slider.value() / self.ratio_slider
        if self.integer:
            self.real_value = int(self.real_value)
        self.update_display()
        self.slider_changed_signal.emit('slider:'+self.signal_name)

    def set_min_max_slider(self, min_val: float, max_val: float) -> None:
        """
        Set the minimum and maximum values of the slider.

        Parameters
        ----------
        min_val : float
            Minimum value of the slider.
        max_val : float
            Maximum value of the slider.

        """
        self.min_real_value = min_val
        self.max_real_value = max_val
        self.slider.setMinimum(int(self.min_real_value*self.ratio_slider))
        self.min_slider_label.setText(f'{int(self.min_real_value)}')
        self.slider.setMaximum(int(self.max_real_value*self.ratio_slider))
        self.max_slider_label.setText(f'{int(self.max_real_value)}')
        self.slider.setValue(int(self.min_real_value*self.ratio_slider))
        self.update_display()

    def set_units(self, units):
        self.units = units
        self.update_display()

    def update_display(self):
        display_value = self.real_value
        display_units = self.units
        if self.integer is False:
            if self.real_value / 1000 >= 1:
                display_value = display_value / 1000
                display_units = 'k' + self.units
            if self.real_value / 1e6 >= 1:
                display_value = display_value / 1e6
                display_units = 'M' + self.units
        self.user_value.setText(f'{display_value}')
        self.units_label.setText(f'{display_units}')

    def get_real_value(self):
        if self.integer:
            return int(self.slider.value()/self.ratio_slider)
        else:
            return self.slider.value()/self.ratio_slider

    def set_value(self, value):
        self.real_value = value
        self.user_value.setText(str(value))
        self.slider.setValue(int(self.real_value*self.ratio_slider))

    def set_ratio(self, value):
        self.ratio_slider = value
        self.slider.setMinimum(int(self.min_real_value * self.ratio_slider))
        self.slider.setMaximum(int(self.max_real_value * self.ratio_slider))
        self.slider.setValue(int(self.min_real_value * self.ratio_slider))
        self.update_display()


# -----------------------------------------------------------------------------------------------
# Only for testing
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widget Slider test")
        self.setGeometry(300, 300, 200, 100)

        self.centralWid = QWidget()
        self.layout = QVBoxLayout()

        self.slider_widget = WidgetSlider()
        self.slider_widget.set_min_max_slider(20, 50)
        self.slider_widget.set_units('Hz')
        self.slider_widget.set_name('Slider to test')
        self.layout.addWidget(self.slider_widget)

        self.centralWid.setLayout(self.layout)
        self.setCentralWidget(self.centralWid)


# Launching as main for tests
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())
