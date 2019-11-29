import cv2
import numpy as np

import time

from matplotlib import pyplot as plt

font = cv2.FONT_HERSHEY_COMPLEX

def display_image(img):
	plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
	plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
	plt.show()

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

def highlight_shapes(img):
	# Convert image to hsv and isolate ths saturation channel
	hsv_shapes = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	saturation = hsv_shapes[:, :, 1]

	saturation = cv2.blur(saturation, (3, 3), cv2.CV_8UC1)

	_, sat_threshold = cv2.threshold(saturation, 80, 255, cv2.THRESH_BINARY)
	# shapes = cv2.adaptiveThreshold(saturation, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

	return sat_threshold

def evaluate_shape(cnt):

	perimeter = cv2.arcLength(cnt,True)
	epsilon = 0.03*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt,epsilon,True)

	print(approx)

	return approx

	# return contours

# Main Code
img = cv2.imread("../blocks.jpg")
shapes = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

filtered = highlight_shapes(shapes)
_, contours, _ = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
	poly = evaluate_shape(contour)

	print(poly)
	cv2.drawContours(img, [poly], 0, (0, 255, 0), 3)



# cnt = cnts[4]
# cv2.drawContours(img, [cnt], 0, (0,255,0), 3)

display_image(filtered)

# sat_threshold = cv2.adaptiveThreshold(sat_gradient, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

# im2, contours, hierarchy = cv2.findContours(filtered, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# cnt = contours[0]
# max_area = cv2.contourArea(cnt)

# for cont in contours:
#     if cv2.contourArea(cont) > max_area:
#         cnt = cont
#         max_area = cv2.contourArea(cont)

# canvas = np.zeros(img.shape, np.uint8)
# cv2.drawContours(canvas, contours, -1, (0, 255, 0), 3)