import cv2
import imutils
import numpy as np
import random

def segment():
    # capture image
    path = 'C:/Users/96171/Desktop/dataset_training/jpg/75120201.jpg'
    image = cv2.imread(path)
    image = imutils.resize(image, width=500)
    resize_factor = 1


    blur = cv2.GaussianBlur(image, (9, 9), 0)
    cv2.imshow('Blurred', blur)
    cv2.waitKey()

    # this was the golden line that made it better
    # edged = cv2.Canny(blur, 0, 150)
    edged = cv2.Canny(blur, 0, 170)

    cv2.imshow('Edged', edged)
    cv2.waitKey()

    # edged = cv2.Canny(image, 0, 150)
    # cv2.imshow("Edged", edged)
    # cv2.waitKey()

    # dilated = cv2.dilate(edged, np.ones((15, 15)))
    dilated = cv2.dilate(edged, np.ones((3, 3)), iterations=1)
    cv2.imshow('Dilated', dilated)
    cv2.waitKey()


    def _contour_approx_bad(contour, *args, **kwargs):
        """
        Approximate contour and discard non rectangular contours
        :returns: True if rectangle else False
        """
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        return len(approx) == 4


    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        if not _contour_approx_bad(contour):
            rect = cv2.boundingRect(contour)
            x, y, w, h = [r*resize_factor for r in rect]
            b, g = random.sample(range(0, 255), 2)
            cv2.rectangle(image, (x,y), ((x+w), (y+h)), (b, g, 255), 3)
            # self.crop(name=str(i), **{'start': (x,y), 'end': ((x+w), (y+h))})

    cv2.imshow('Final Image', image)
    cv2.waitKey()
cv2.imwrite('tobecropped.png', image)