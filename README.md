# cvproj_1
My first OpenCV project, which takes an image of a street sign and returns the type of sign it is.

This code works by taking an image and using the Canny algorithm to detect the edges. Then, it finds the biggest shape contained by some of those edges and counts the sides of it. 
It then test if the shape is rotated or not by comparing the bounding box (un-rotated rectangle that encloses the shape with the smallest area possible) and the minimum-area box 
(a box that encloss the shape with the actual minimum area, rotated or not). This part only is put into use for rectangles. Finally, it returns the type of sign and a histogram 
containing the sign's color.

This project is complete.
