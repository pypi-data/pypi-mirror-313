"""Example of pypylon library usage

    Tested with Basler a2A 1920-160ucBAS camera


@see https://github.com/basler/pypylon
"""
import numpy as np
from ids_peak import ids_peak
import ids_peak_ipl.ids_peak_ipl as ids_ipl
import cv2

def init_lib():
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
		return device
	except Exception as e:
		print("EXCEPTION - init_cam: " + str(e))

def alloc_memory(dev_cam):
	try:
		# Preparing image acquisition - buffers
		data_streams = dev_cam.DataStreams()
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
		return data_stream

	except Exception as e:
		print("EXCEPTION - alloc_memory: " + str(e))

def trigger(remote):
	# Software trigger
	remote.FindNode("TriggerSelector").SetCurrentEntry("ExposureStart")
	remote.FindNode("TriggerSource").SetCurrentEntry("Software")
	remote.FindNode("TriggerMode").SetCurrentEntry("On")

def start_acquisition(data_stream, remote):
	# Start Acquisition
	data_stream.StartAcquisition(ids_peak.AcquisitionStartMode_Default)
	remote.FindNode("TLParamsLocked").SetValue(1)
	remote.FindNode("AcquisitionStart").Execute()
	remote.FindNode("AcquisitionStart").WaitUntilDone()

def stop_acquisition(data_stream, remote):
	# Stop Acquisition
	remote.FindNode("AcquisitionStop").Execute()
	remote.FindNode("AcquisitionStop").WaitUntilDone()
	remote.FindNode("TLParamsLocked").SetValue(0)
	data_stream.StopAcquisition()

def get_image(data_stream, remote):
	try:
		# trigger image
		remote.FindNode("TriggerSoftware").Execute()
		buffer = data_stream.WaitForFinishedBuffer(1000)
		raw_image = ids_ipl.Image.CreateFromSizeAndBuffer(buffer.PixelFormat(), buffer.BasePtr(), buffer.Size(),
															  buffer.Width(), buffer.Height())

		data_stream.QueueBuffer(buffer)
		return raw_image

	except Exception as e:
		print("EXCEPTION - get_image: " + str(e))

if __name__ == '__main__':
		try:
			my_cam = init_lib()
			remote = my_cam.RemoteDevice().NodeMaps()[0]
			numberOfImagesToGrab = 2

			remote.FindNode("PixelFormat").SetCurrentEntry('Mono10')
			data_stream = None
			data_stream = alloc_memory(my_cam)
			trigger(remote)
			start_acquisition(data_stream, remote)

			for k in range(numberOfImagesToGrab):
				raw_image = get_image(data_stream, remote)

				width = raw_image.Width()
				height = raw_image.Height()
				pixel_format = raw_image.PixelFormat()
				timestamp = raw_image.Timestamp()

				print(f"Width: {width}")
				print(f"Height: {height}")
				print(f"Pixel Format: {pixel_format}")

				img_data = raw_image.get_numpy_3D()
				if pixel_format == ids_ipl.PixelFormatName_RGB8:
					img_np = np.frombuffer(img_data, dtype=np.uint8).reshape(height, width, 3)
				elif pixel_format in [ids_ipl.PixelFormatName_Mono8,
									  ids_ipl.PixelFormatName_Mono10,
									  ids_ipl.PixelFormatName_Mono12]:
					# Conversion de 16 bits en 8 bits pour Mono10 et Mono12
					img_np = np.frombuffer(img_data, dtype=np.uint16).reshape(height, width)
					img_np = (img_np / 4).astype(np.uint8)  # Convertir de 16 bits à 8 bits
				else:
					raise RuntimeError("Format de pixel non supporté")

				picture = img_np # raw_image.get_numpy_3D()
				# Access the image data.
				print("Shape: ", picture.shape)
				print("Type: ", picture.dtype)
				cv2.imshow('image', picture)
				cv2.waitKey(0)
				cv2.destroyAllWindows()
			stop_acquisition(data_stream, remote)

			remote.FindNode("PixelFormat").SetCurrentEntry('Mono8')
			data_stream = None
			data_stream = alloc_memory(my_cam)
			start_acquisition(data_stream, remote)
			raw_image = get_image(data_stream, remote)
			picture = raw_image.get_numpy_3D()
			picture_shape = picture.shape
			print("Shape: ", picture.shape)
			print("Type: ", picture.dtype)
			cv2.imshow('image', picture)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			data_stream = None
			my_cam = None
		except Exception as e:
			print("EXCEPTION: " + str(e))

		finally:
			ids_peak.Library.Close()
 
