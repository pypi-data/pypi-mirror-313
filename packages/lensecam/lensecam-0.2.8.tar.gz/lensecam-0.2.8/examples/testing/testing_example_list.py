# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from camera_list import CameraList

cam_list = CameraList()
cameras_list = cam_list.get_cam_list()

for cam in cameras_list:
        print(f'ID:{cam[0]} - Name: {cam[2]} - Serial: {cam[1]}')

cam_id = 'a'
while cam_id.isdigit() is False:
        cam_id = input('Enter the ID of the camera to connect :')
cam_id = int(cam_id)

my_cam_dev = cam_list.get_cam_device(cam_id)