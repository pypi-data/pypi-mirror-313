.. Camera GUI documentation master file, created by
   sphinx-quickstart on Fri Dec 15 11:17:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Camera GUI's documentation
##########################

.. warning::
   This application and its documentation website are still works in progress

**Camera GUI** is a library for industrial camera sensors to develop **graphical user interfaces** based on **PyQt6** in Python.

.. figure:: _static/images/biophotonique_labwork_interface.png
	:width: 60%
	:align: center
	
	Example of Basler camera integration in a PyQt6 application. `Biophotonic labwork - Structured illumination microscope <https://iogs-lense-platforms.github.io/>`_



Actual compatible cameras :

* Basler

Future updates :

* IDS

The GitHub repository of this project : `Camera GUI <https://github.com/IOGS-LEnsE-ressources/camera-gui>`_


GUI Tutorials
*************

.. toctree::
	
	How To use these ressources<contents/how_to_use>
	PyQt6 widget integration<contents/pyqt6_integration>

.. toctree::
	:maxdepth: 2
	:caption: Camera Sensors

	Basler Camera<contents/cam_basler>
	IDS Camera<contents/cam_ids>

.. toctree::
	:maxdepth: 2
	:caption: Applications
	
	Study of a CMOS sensor
	Interferometric controls



About the LEnsE
***************

This is a test.

.. raw:: html

	<span class="linkgit"><a href="https://lense.institutoptique.fr/mine/nucleo-bibliotheques-de-fonctions/"><i class="fa fa-github"></i> Bibliothèques MBED 6</a></span>


Help for Sphinx Documentation
*****************************

.. note:: 

	To delete
	https://blog.flozz.fr/2020/10/04/documenter-un-projet-python-avec-sphinx/
	
	https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
	
	https://numpy.org/doc/1.26/reference/arrays.ndarray.html
	
	https://github.com/numpy/numpy/blob/main/doc/source/reference/arrays.ndarray.rst
	
	https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html#headings
	
	https://sphinxawesome.xyz/demo/inline-code/