#import modules

import math 
import cv2 as cv
import numpy as np
import pupil_apriltags
import sys 

from pupil_apriltags import Detector 

source = 0

tag_family = {
    
    "tag16h5": (0, 255, 0),
    "tag36h11": (255, 255, 0)
              
}

camera = cv.VideoCapture(source)


#april_detector = Detector(tag_family[0])


def drawBoxes(frame, color: tuple) -> None:
    detected = april_detector.detect(grayscale)
    
    for result in detected:
        #coordinates of tl and br
        A, B, C, D = result.corners
        A = (int(A[0]), int(A[1]))
        B = (int(B[0]), int(B[1]))
        C = (int(C[0]), int(C[1]))
        D = (int(D[0]), int(D[1]))
        
        if isSquare(A, B, C, D):
            cv.line(frame, A, B, color, 2)
            cv.line(frame, B, C, color, 2)
            cv.line(frame, C, D, color, 2)
            cv.line(frame, D, A, color, 2)
            
            drawCenter(frame, result)
            
            cv.putText(frame, str(result.tag_family.decode()), (A[0], A[1] - 13), cv.FONT_HERSHEY_COMPLEX, 0.5, color, 2)
    
    
#print(type(detected[0]))
    
def drawCenter(frame, result) -> None:
    (X, Y) = (int(result.center[0]), int(result.center[1]))
    cv.circle(frame, (X, Y), 3, (0, 0, 255), -1)

def isSquare(coord_a: list, coord_b: list, coord_c: list, coord_d: list) -> bool:
    side_a = math.dist([coord_a[0], coord_a[1]], [coord_b[0], coord_b[1]])
    side_b = math.dist([coord_b[0], coord_b[1]], [coord_c[0], coord_c[1]])
    side_c = math.dist([coord_c[0], coord_c[1]], [coord_d[0], coord_d[1]])
    side_d = math.dist([coord_d[0], coord_d[1]], [coord_a[0], coord_a[1]])
    
    #print(side_a, side_b, side_c, side_d)
    #print(side_a * side_b)
    
    return (side_a * side_b) > 500 and (round(side_a, -1) == round(side_b, -1) == round(side_c, -1) == round(side_d, -1))

if __name__ == "__main__":
    while True:
        ret, frame = camera.read()
        grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #blur grayscale img
        grayscale = cv.GaussianBlur(grayscale, (5, 5), 0)
        
    
        for tag_id in tag_family:
            april_detector = Detector(
                tag_id
                                                                
    )
            
            drawBoxes(frame, tag_family[tag_id]) 

        
        cv.imshow("Detected", frame)
        esc_key = cv.waitKey(1)
    
        if esc_key == 27:
            cv.destroyAllWindows()
            sys.exit() 

