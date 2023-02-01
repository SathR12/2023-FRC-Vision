import cv2 as cv
import sys
import apriltag
import math
import numpy as np
import ntcore

camera = cv.VideoCapture(0)
 
inst = ntcore.NetworkTableInstance.getDefault()
sd_table = inst.getTable("Smartdashboard")

def getCartesianDistance(coord_1, coord_2):
    squared = ((coord_1[1] - coord_1[0]) **2) + ((coord_2[1] - coord_2[0]) **2)
    dist = math.sqrt(squared)

    return dist

def isLarge(coord_a, coord_b, coord_c):
    global side_a, side_b

    side_a = getCartesianDistance(coord_a, coord_b)
    side_b = getCartesianDistance(coord_b, coord_c)
    return (side_a * side_b) > 1500

def getDistance(focal_length, real_width, frame_width):
    distance = (real_width * focal_length) / frame_width

    return distance

def getDistanceFromCenter(result, frame):
    (h,w) = tuple(frame.shape[:2])
    cv.circle(frame, (w//2, h//2), 3, (255,0,0), -1)
    cv.line(frame, tuple(map(int, result.center)), (w//2,h//2), (255,0,0), 2)
    return getCartesianDistance(tuple(map(int, result.center)), (w//2,h//2))

def getDistance(realDist):
    try:
        return int(14446 * math.pow(realDist, -1.07))
    except:
        return 0

K = [338.563277422543, 0.0, 336.45495347495824, 0.0, 338.939280638548, 230.486982216255, 0.0, 0.0, 1.0]
cameraMatrix = np.array(K).reshape((3,3))
camera_params = (cameraMatrix[0,0], cameraMatrix[1, 1], cameraMatrix[0, 2], cameraMatrix[1,2])

headless = True

while True:

    ret, frame = camera.read()
    grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions("tag16h5")
    detector = apriltag.Detector(options)
    results = detector.detect(grayscale)

    detected = False
    dist = -1
    xOffset = -999999
    yOffset = -999999
    tag_id = -1

    for result in results:
        A, B, C, D = result.corners
        A = (int(A[0]), int(A[1]))
        B = (int(B[0]), int(B[1]))
        C = (int(C[0]), int(C[1]))
        D = (int(D[0]), int(D[1]))

        if result.hamming == 0 and isLarge(A, B, C):
            detected = True
            if not headless:
                cv.line(frame, A, B, (0, 255, 0), 2)
                cv.line(frame, B, C, (0, 255, 0), 2)
                cv.line(frame, C, D, (0, 255, 0), 2)
                cv.line(frame, D, A, (0, 255, 0), 2)

            dist = getDistance(B[0] - A[0])
            xOffset = int(result.center[0]) - (frame.shape[0] // 2)
            yOffset = (frame.shape[1] // 2) - int(result.center[1])
            tag_id = result.tag_id

        getDistanceFromCenter(result, frame)

        if not headless:	    
            cv.putText(frame, str(int(dist)) + "cm" , (A[0], A[1] - 13), cv.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
            cv.imshow("feed", frame)

    key = cv.waitKey(1)
    if key == 27:
        break

    print(tag_id)

camera.release()
cv.destroyAllWindows()
sys.exit() 
