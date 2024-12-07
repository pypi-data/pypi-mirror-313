"""*images* file.

*images* file, from supop_images directory,
that contains functions to process images.

.. module:: supop_images.images
   :synopsis: To complete

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""

import cv2
import numpy as np
from PyQt6.QtGui import QImage, QPixmap


def resize_image(im_array: np.ndarray,
                 new_width: int,
                 new_height: int) -> np.ndarray:
    """Resize array containing image at a new size.

    :param im_array: Initial array to resize.
    :type im_array: numpy.ndarray
    :param new_width: Width of the new array.
    :type new_width: int
    :param new_height: Height of the new array.
    :type new_height: int
    :return: Resized array.
    :rtype: numpy.ndarray

    """
    resized_image = cv2.resize(im_array,
                               dsize=(new_width, new_height),
                               interpolation=cv2.INTER_CUBIC)
    return resized_image


def array_to_qimage(array: np.ndarray) -> QImage:
    """Transcode an array to a QImage.

    :param array: Array containing image data.
    :type array: numpy.ndarray
    :return: Image to display.
    :rtype: QImage

    """
    shape_size = len(array.shape)
    if shape_size == 2:
        height, width = array.shape
    else:
        height, width, _ = array.shape
    bytes_per_line = width  # only in 8 bits gray

    return QImage(array, width, height, bytes_per_line,
                  QImage.Format.Format_Grayscale8)
