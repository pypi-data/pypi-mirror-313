"""Test of the different library for Basler integration in a PyQt6 graphical user interface

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>

"""
from camera_list import *
from camera_basler import *
from matplotlib import pyplot as plt
import time
import numpy as np

if __name__ == "__main__":
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
    my_cam = CameraBasler(my_cam_dev)
    # Check the colormode
    print(my_cam.get_color_mode())

    # Change colormode to Mono12
    my_cam.set_color_mode('Mono12')
    my_cam.set_display_mode('Mono12')
    print(my_cam.get_color_mode())
    
    # Test to catch images
    st = time.time()
    images = my_cam.get_images()
    et = time.time()
    
    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    
    print(images[0].shape)
    
    '''
    # display image
    plt.imshow(images[0], interpolation='nearest')
    plt.show()
    '''
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
 