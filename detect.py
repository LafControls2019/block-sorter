import cv2
import numpy as np

import time

def highlight_shapes(img, threshold = 220, blur_radius = 3):

	# Convert image to hsv and isolate ths saturation channel
	hsv_shapes = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	# saturation = hsv_shapes[:, :, 1]
	value = hsv_shapes[:, :, 2]

	# saturation = cv2.blur(saturation, (blur_radius, blur_radius), cv2.CV_8UC1)
	value = cv2.blur(value, (blur_radius, blur_radius), cv2.CV_8UC1)

	# _, sat_threshold = cv2.threshold(saturation, threshold, 255, cv2.THRESH_BINARY)
	_, val_threshold = cv2.threshold(value, threshold, 255, cv2.THRESH_BINARY)

	return val_threshold

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

def detect_shapes(img, minimum_area=8000, feedback = False):
	output = []

	# Filter Image
	img_highlighted = highlight_shapes(img)

	# Find Contours
	_, contours, _ = cv2.findContours(img_highlighted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:

		area = cv2.contourArea(contour)

		if(area > minimum_area):
			polygon = get_polygon(contour)
			output.append(polygon)

	return output

def draw_polygons(img, polygons):
	
	for polygon in polygons:
		vertices, center = polygon
		cX, cY = center

		cv2.drawContours(img, [vertices], 0, (0, 255, 0), 3)

def draw_labels(img, polygons, labels):

	for polygon, label in zip(polygons, labels):
		_, center = polygon
		x, y = center

		cv2.circle(img, (x, y), 7, (255, 255, 255), -1)
		cv2.putText(img, label, (x - 20, y- 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


