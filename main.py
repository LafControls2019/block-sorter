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

# Main Code
img = cv2.imread("../blocks.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(img)
shapes = detect.detect_shapes(img, feedback = False)



print(shapes)
display_image(img)

# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()