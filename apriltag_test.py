#import modules

import cv2 as cv
import numpy as np
import pupil_apriltags
import sys 

from pupil_apriltags import Detector 

tag_family = ["tag16h5", "tag36h11"]

image = cv.imread("specify image absolute path")
grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

#blur grayscale img
grayscale = cv.GaussianBlur(grayscale, (5, 5), 0)

#to detect specific tag, specify in constructor below
april_detector = Detector(tag_family[0])


detected = april_detector.detect(grayscale)

for result in detected:
    #coordinates of tl and br
    A, B, C, D = result.corners
    A = (int(A[0]), int(A[1]))
    B = (int(B[0]), int(B[1]))
    C = (int(C[0]), int(C[1]))
    D = (int(D[0]), int(D[1]))
    
    cv.line(image, A, B, (0, 255, 0), 2)
    cv.line(image, B, C, (0, 255, 0), 2)
    cv.line(image, C, D, (0, 255, 0), 2)
    cv.line(image, D, A, (0, 255, 0), 2)
    
    cv.putText(image, str(result.tag_family.decode()), (A[0], A[1] - 15), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
    
    
#print(type(detected[0]))

cv.imshow("Detected", image)

esc_key = cv.waitKey(1)

if esc_key == 27:
    cv.destroyAllWindows()
    sys.exit() 
