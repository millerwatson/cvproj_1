import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt


"""This program takes in a street sign from the user and returns what type of
   sign it is. It works by getting the amount of sides on the sign's contour
   and comparing those with a list of sign types. It also provides a color
   histogram for the user to analyze the color of the sign.
   Author: Miller Watson
   Date: 10/1/21"""


def determineSignType(contour, image):
    """Purpose: to determine the street sign type of a given contour and draw intermediate stages
    Parameters: contour: the contour to be analyzed, image: the image that the contour comes from
    Return: the type of street sign the contour could be"""

    # new image for modifying
    newImg = image.copy()

    # generates a bounding rectangle, to compare to the contour area
    (x, y, width, height) = cv2.boundingRect(contour)
    cv2.rectangle(newImg,(x,y),(x+width,y+height),(0,255,0),2)

    # smoothens the contour, then estimates the amount of sides
    epsilon = 0.02 * cv2.arcLength(contour, True)
    estimateCont = cv2.approxPolyDP(contour, epsilon, True)
    cv2.imshow("Estimated Contours", cv2.drawContours(image.copy(), [estimateCont], -1, (0,0,255), 5))
    sides = len(estimateCont)
    print("Simplified Contour Points: " + str(estimateCont))
    print("Amount of sides:" + str(sides))

    # draws the minimum area rectangle of the sign
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(newImg,[box],0,(0,0,255),2)

    # tests if the  shape is rotated, only for rectangles does this value get used
    if (cv2.contourArea(box) * 1.2) < (width * height):
        rotated = True
        print("It is a rotated shape")
    else:
        rotated = False
        print("It is not a rotated shape")

    # shows all contours
    cv2.imshow("Bounding box and best fit comparison", newImg)
    cv2.waitKey(0)

    # returns sign type based on number of sides
    if sides == 3:
        return "yield"
    elif sides == 4:
        return "Regulatory"
    elif sides == 5:
        return "Crossing"
    elif sides == 8:
        return "Stop"
    else:
        return "Unclear sign or irregular sign"


def main():


    # loads and displays image
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])
    cv2.imshow("Original", image)

    # prepares the image for edge detection
    blurImg = cv2.GaussianBlur(image, (7, 7), 0)
    grayBlur = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

    #displays prepared image
    cv2.imshow("Grayed and Blurred", grayBlur)
    cv2.waitKey(0)

    # applies the Canny algorithm for edge detection
    edges = cv2.Canny(grayBlur, 0, 155)
    (contours, nothing) = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draws all of the contours over the original image
    contourImg = image.copy()
    cv2.drawContours(contourImg, contours, -1, (0,0,255), 3)
    cv2.imshow("All contours", contourImg)
    cv2.waitKey(0)

    # iterates though to find the biggest contour
    maxArea = 0
    bestIndex = -1
    for i in range(len(contours)):
        if maxArea < cv2.contourArea(contours[i]):
            maxArea = cv2.contourArea(contours[i])
            bestIndex = i

    # Draws the biggest contour over the original image
    newImg = image.copy()
    cv2.drawContours(newImg, contours, bestIndex, (0,0,255), 3)
    cv2.imshow("Correct contour", newImg)
    cv2.waitKey(0)

    print("Sign type: " + determineSignType(contours[bestIndex], image.copy()))



main()
