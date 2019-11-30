import cv2
import numpy as np
import time

import detect

from matplotlib import pyplot as plt

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

# Main Code
img = cv2.imread("../blocks.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

shapes = detect.detect_shapes(img, feedback = True)

# print(len(shapes))

sorted_shapes = []

for shape in shapes:

	sorted_shapes.append(sort(shape))

print(sorted_shapes)

display_image(img)