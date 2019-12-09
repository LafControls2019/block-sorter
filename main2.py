import cv2
import numpy as np
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

import detect
from matplotlib import pyplot as plt

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

GPIO.output(6, 1)
GPIO.output(24, 1)
GPIO.output(19, 1)

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


def crop_img(img, scale=1.0):
	center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
	width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
	left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
	top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
	img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
	return img_cropped

def sort(color):
	if 0 <= color <= 12: 
		return "white"

	elif 12 <= color <= 50:
		return "blue"

	elif 50 <= color <= 80:
		return "green"

	elif 80 <= color <= 96:
		return "yellow"

	elif 96 <= color <= 115:
		return "orange"

	elif 115 <= color <= 150:
		return "red"


def sort_all(shapes, image):
	output = []

	for shape in shapes:
		vertices, center = shape
		print(vertices)

		mask = np.zeros((480, 640), np.uint8)
		cv2.fillPoly(mask, pts=[vertices], color=1)

		color = cv2.bitwise_and(frame.array, frame.array, mask = mask) 
		color_mean, _, _, _ = cv2.mean(hue, mask=mask)

		output.append( (sort(color_mean), center))

	return output

		

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.exposure_mode="fixedfps"
camera.iso = 100
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

def set_ramp_bits(bits):
	GPIO.output(6,	bits[0])
	GPIO.output(24,	bits[1])
	GPIO.output(19,	bits[2])

def set_ramp(color):
	if color == "white":
		set_ramp_bits([0, 0, 1])
	elif color == "blue":
		set_ramp_bits([0, 1, 0])
	elif color == "green":
		set_ramp_bits([0, 1, 1])
	elif color == "yellow":
		set_ramp_bits([1, 0, 0])
	elif color == "orange":
		set_ramp_bits([1, 0, 1])
	elif color == "red":
		set_ramp_bits([1, 1, 0])
	else:
		set_ramp_bits([0, 0, 0])



print("beginning")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# image = crop_img(frame.array, scale=1)

	# shapes = detect.highlight_shapes(frame.array)

	hsv_img = cv2.cvtColor(frame.array, cv2.COLOR_RGB2HSV)
	hue = hsv_img[:,:,0]

	shapes = detect.detect_shapes(frame.array, feedback=True)

	detect.draw_polygons(frame.array, shapes)

	sorted_shapes = sort_all(shapes, frame.array)

	names = []
	for name, center in sorted_shapes:
		names.append(name)

	detect.draw_labels(frame.array, shapes, names)


	### Determine which position to switch to
	if len(sorted_shapes) == 0:
		# set_ramp("")
		pass
	elif len(sorted_shapes) == 1:
		set_ramp(names[0])
	else:
		set_ramp("")
	# elif:
	# 	pass

	# for shape in shapes:
	# 	vertices, _ = shape
	# 	print(vertices)

	# 	mask = np.zeros((480, 640), np.uint8)
	# 	cv2.fillPoly(mask, pts=[vertices], color=1)

	# 	color = cv2.bitwise_and(frame.array, frame.array, mask = mask) 
	# 	color_mean, _, _, _ = cv2.mean(hue, mask=mask)

	# 	detect.draw_labels(frame.array, [shape], [sort(color_mean)])

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
