#import modules
import math 
import cv2 as cv
import numpy as np
import pupil_apriltags
import sys 

from pupil_apriltags import Detector 

#apriltag dimensions

width, length = 8, 11.5

#camera distance. Need to fill in values sometime 

measured_distance = None

source = 0

tag_family = {
    
    "tag16h5": (0, 255, 0)
              
}

camera = cv.VideoCapture(source)


#april_detector = Detector(tag_family[0])


def drawBoxes(frame, color: tuple) -> None:
    #necessary to convert to grayscale for pretrained model 
    detected = april_detector.detect(grayscale)
    
    for result in detected:
        #coordinates of tl and br
        A, B, C, D = result.corners
        A = (int(A[0]), int(A[1]))
        B = (int(B[0]), int(B[1]))
        C = (int(C[0]), int(C[1]))
        D = (int(D[0]), int(D[1]))
        
        #this function calculates cartesian distance between points and determines whether square 
        if isSquare(A, B, C, D):
            
            #draw straight lines between apriltag coordinate points 
            cv.line(frame, A, B, color, 2)
            cv.line(frame, B, C, color, 2)
            cv.line(frame, C, D, color, 2)
            cv.line(frame, D, A, color, 2)
            
            #draws a red hollow circle on the apriltag 
            drawCenter(frame, result)
            cv.putText(frame, str(result.tag_family.decode()), (A[0], A[1] - 13), cv.FONT_HERSHEY_COMPLEX, 1, color, 4)
            
            if result.tag_id == 1:
                cv.putText(frame, "SHOOT", (0, 130), cv.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
                
            elif result.tag_id == 0:
                cv.putText(frame, "CLIMB", (0, 130), cv.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
                
                
                
            
            
    
#print(type(detected[0]))
    
def drawCenter(frame, result) -> None:
    #approximates center of apriltag object using pre-existing functions 
    (X, Y) = (int(result.center[0]), int(result.center[1]))
    cv.circle(frame, (X, Y), 3, (0, 0, 255), 5)

def isSquare(coord_a: tuple, coord_b: tuple, coord_c: tuple, coord_d: tuple) -> bool:
    
    #calculates side length and approximates side length to check for square 
    side_a = math.dist([coord_a[0], coord_a[1]], [coord_b[0], coord_b[1]])
    side_b = math.dist([coord_b[0], coord_b[1]], [coord_c[0], coord_c[1]])
    side_c = math.dist([coord_c[0], coord_c[1]], [coord_d[0], coord_d[1]])
    side_d = math.dist([coord_d[0], coord_d[1]], [coord_a[0], coord_a[1]])
    
    #print(side_a, side_b, side_c, side_d)
    #print(side_a * side_b)
    
    #if side_a > 0 and side_b > 0 and side_c > 0 and side_d > 0:
     #   if 1.2 >= (side_a + side_b) / (side_c + side_d) >= .8:
            
        
    
    #returns true only if minimum area is greater than 500 coordinate points and all sides are rounded to the same value
    return (side_a * side_b) > 7000 and (round(side_a, -2) == round(side_b, -2) == round(side_c, -2) == round(side_d, -2))

def getDistance(focal_len, real_width, frame_width) -> float:
    distance = (real_width * focal_length)/ frame_width
    
    return distance 
    
if __name__ == "__main__":
    while True:
        ret, frame = camera.read()
        grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #blur grayscale image using a [5x5] matrix. Increase value of matrix to increase blurring effect. 
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
        
            
camera.release()
sys.exit()
