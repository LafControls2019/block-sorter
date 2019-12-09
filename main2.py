import cv2
import numpy as np
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

import detect
from matplotlib import pyplot as plt

# camera = PiCamera()
# camera.exposure_mode = "fixedfps"
# camera.iso = 100
# camera.resolution = (640, 480)
# camera.framerate = 32

font = cv2.FONT_HERSHEY_COMPLEX

def display_image(img):
	plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
	plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
	plt.show()

def sort(shape):
	vertices, center = shape

	print(len(vertices))

	if len(vertices) == 3:
		return "TRIANGLE"

	if len(vertices) == 6:
		return "HEXAGON"

	return "Unknown"

def crop_img(img, scale=1.0):
	center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
	width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
	left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
	top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
	img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
	return img_cropped

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.exposure_mode="fixedfps"
camera.iso = 100
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

print("beginning")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# image = crop_img(frame.array, scale=1)

	# shapes = detect.highlight_shapes(frame.array)
	shapes = detect.detect_shapes(frame.array, feedback=True)

	detect.draw_polygons(frame.array, shapes)
	detect.draw_labels(frame.array, shapes, ['label'])
	# blurred = cv2.GaussianBlur(image, (31,31), 0)

	# image_gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	# image_lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

	cv2.imshow("Image", frame.array)

	key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)
	rawCapture.seek(0)

# Main Code
#img = cv2.imread("../blocks.jpg")
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#shapes = detect.detect_shapes(img, feedback = True)

# print(len(shapes))


# rawCapture = PiRGBArray(camera)

# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
# 	img = frame.array
# 	cv2.imshow("Image", img)

# 	shapes = detect.detect_shapes(img)
# 	print(shapes)

# sorted_shapes = []

# for shape in shapes:

# 	sorted_shapes.append(sort(shape))

# print(sorted_shapes)
# rawCapture = PiRGBArray(camera)

# # grab an image from the camera

# while True:
# 	camera.capture(rawCapture, format="bgr", use_video_port=True)
# 	img = rawCapture.array

# 	shapes = detect.detect_shapes(img, feedback=True)

# 	display_image(img)
