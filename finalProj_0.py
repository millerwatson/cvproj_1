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

    # smoothens the contour, then estimates the amount of sides
    epsilon = 0.02 * cv2.arcLength(contour, True)
    estimateCont = cv2.approxPolyDP(contour, epsilon, True)
    cv2.imshow("Estimated Contours", cv2.drawContours(image.copy(), [estimateCont], -1, (0,0,255), 5))
    sides = len(estimateCont)
    print("Simplified Contour Points: " + str(estimateCont))
    print("Amount of sides:" + str(sides))

    return "Testing statement"


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
