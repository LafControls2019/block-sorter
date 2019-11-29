import cv2
import numpy as np

import time

def highlight_shapes(img):

	# Convert from BGR to RGB
	# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	# Convert image to hsv and isolate ths saturation channel
	hsv_shapes = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	saturation = hsv_shapes[:, :, 1]

	saturation = cv2.blur(saturation, (3, 3), cv2.CV_8UC1)

	_, sat_threshold = cv2.threshold(saturation, 80, 255, cv2.THRESH_BINARY)

	return sat_threshold

def get_polygon(contour):

	perimeter = cv2.arcLength(contour,True)
	epsilon = 0.03*cv2.arcLength(contour,True)
	approx = cv2.approxPolyDP(contour,epsilon,True)

	return approx

def detect_shapes(img, feedback = False):
	output = []

	# Filter Image
	img_highlighted = highlight_shapes(img)

	# Find Contours
	_, contours, _ = cv2.findContours(img_highlighted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:
		polygon = get_polygon(contour)
		output.append(polygon)

		if(feedback):
			cv2.drawContours(img, [polygon], 0, (0, 255, 0), 3)

	return output