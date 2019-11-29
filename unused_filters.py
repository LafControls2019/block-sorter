import cv2
import numpy as np

import time

"""
Filters that I no longer use but want to keep a copy of for reference

"""

def filter_1(img):

	# Convert image to hsv and isolate ths saturation channel
	hsv_shapes = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	saturation = hsv_shapes[:, :, 1]

	# Blur, Laplacian, Blur again
	saturation = cv2.blur(saturation, (6, 6), cv2.CV_8UC1)
	sat_gradient = cv2.Laplacian(saturation, cv2.CV_8UC1)
	sat_gradient = cv2.blur(sat_gradient, (6, 6), cv2.CV_8UC1)

	# Threshold
	_, sat_threshold = cv2.threshold(sat_gradient, 3, 100, cv2.THRESH_BINARY)

	return sat_threshold


def canny_edges(img):
	# Convert image to hsv and isolate ths saturation channel
	hsv_shapes = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	saturation = hsv_shapes[:, :, 1]

	saturation = cv2.blur(saturation, (3, 3), cv2.CV_8UC1)

	edges = cv2.Canny(saturation, 100, 200)

	return edges