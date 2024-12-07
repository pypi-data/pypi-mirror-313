"""Example of pypylon library usage

    Tested with Basler a2A 1920-160ucBAS camera


@see https://github.com/basler/pypylon
"""
import numpy as np
import cv2
from ids_peak import ids_peak
import ids_peak_ipl.ids_peak_ipl as ids_ipl
 
if __name__ == '__main__':
	# Initialize library
	ids_peak.Library.Initialize()

	# Create a DeviceManager object
	device_manager = ids_peak.DeviceManager.Instance()
 
	try:
		# Update the DeviceManager
		device_manager.Update()

		# Exit program if no device was found
		if device_manager.Devices().empty():
		   print("No device found. Exiting Program.")

		# Open the first device
		device = device_manager.Devices()[0].OpenDevice(ids_peak.DeviceAccessType_Control)
		remote = device.RemoteDevice().NodeMaps()[0]
		
		numberOfImagesToGrab = 2
		# Preparing image acquisition - buffers
		data_streams = device.DataStreams()
		if data_streams.empty():
			print("No datastream available.")
 
		data_stream = data_streams[0].OpenDataStream()
		nodemapDataStream = data_stream.NodeMaps()[0]
		
		# Flush queue and prepare all buffers for revoking
		data_stream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)
 
		# Clear all old buffers
		for buffer in data_stream.AnnouncedBuffers():
			data_stream.RevokeBuffer(buffer)
 
		payload_size = remote.FindNode("PayloadSize").Value()
 
		# Get number of minimum required buffers
		num_buffers_min_required = data_stream.NumBuffersAnnouncedMinRequired()
 
		# Alloc buffers
		for count in range(num_buffers_min_required):
			buffer = data_stream.AllocAndAnnounceBuffer(payload_size)
			data_stream.QueueBuffer(buffer)
		
		# Software trigger
		remote.FindNode("TriggerSelector").SetCurrentEntry("ExposureStart")
		remote.FindNode("TriggerSource").SetCurrentEntry("Software")
		remote.FindNode("TriggerMode").SetCurrentEntry("On")
		
		# Start Acquisition
		data_stream.StartAcquisition(ids_peak.AcquisitionStartMode_Default)
		remote.FindNode("TLParamsLocked").SetValue(1)
		remote.FindNode("AcquisitionStart").Execute()
		remote.FindNode("AcquisitionStart").WaitUntilDone()
		
		for k in range(numberOfImagesToGrab):
			# trigger image
			remote.FindNode("TriggerSoftware").Execute()
			buffer = data_stream.WaitForFinishedBuffer(1000)
			# convert to RGB
			raw_image = ids_ipl.Image.CreateFromSizeAndBuffer( buffer.PixelFormat(), buffer.BasePtr(), buffer.Size(), buffer.Width(), buffer.Height())
			color_image = raw_image.ConvertTo(ids_ipl.PixelFormatName_Mono8)
			data_stream.QueueBuffer(buffer)
			picture = color_image.get_numpy_3D()
			
			picture_shape = picture.shape
		    # Access the image data.
			print("SizeX: ", picture_shape[1])
			print("SizeY: ", picture_shape[0])
			print("Gray value of first pixel: ", picture[0, 0])

			cv2.imshow('image', picture)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		# Stop Acquisition
		remote.FindNode("AcquisitionStop").Execute()
		remote.FindNode("AcquisitionStop").WaitUntilDone()
		remote.FindNode("TLParamsLocked").SetValue(0)
		data_stream.StopAcquisition()

	except Exception as e:
		print("EXCEPTION: " + str(e))

	finally:
		ids_peak.Library.Close()
 
