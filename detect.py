import cv2
import numpy as np

import time

def highlight_shapes(img):

	# Convert image to hsv and isolate ths saturation channel
	hsv_shapes = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	saturation = hsv_shapes[:, :, 1]

	saturation = cv2.blur(saturation, (3, 3), cv2.CV_8UC1)

	_, sat_threshold = cv2.threshold(saturation, 80, 255, cv2.THRESH_BINARY)

	return sat_threshold

def get_polygon(contour):

	perimeter = cv2.arcLength(contour,True)
	epsilon = 0.03*cv2.arcLength(contour,True)
	polygon = cv2.approxPolyDP(contour,epsilon,True)

	# print(perimeter)

	# find location
	M = cv2.moments(polygon)

	if(int(M["m00"] == 0)):
		center = (0, 0)
	else:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])

		center = (cX, cY)

	return (polygon, center)

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
			vertices, center = polygon
			cX, cY = center

			cv2.drawContours(img, [vertices], 0, (0, 255, 0), 3)
			cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
			cv2.putText(img, "center", (cX - 20, cY - 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	return output



