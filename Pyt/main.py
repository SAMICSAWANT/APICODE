import cv2
import pickle
import cvzone
import numpy as np
from collections import defaultdict
# from database import CarInfo
from ParkingSpacePicker import temps
import json
import os
# Video feed
print("main")

# Use absolute path to the video file
video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'carPark.mp4')

# Set to False to use the uploaded video file instead of camera
use_camera = False  # Changed to False to use the uploaded video project
if use_camera:
    cap = cv2.VideoCapture(0)  # Use default camera (change index if needed)
    print("Using live camera feed")
else:
    cap = cv2.VideoCapture(video_path)
    print(f"Video path: {video_path}")
    print(f"Video opened successfully: {cap.isOpened()}")

# cap = cv2.VideoCapture('carPark_Reverse.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

with open('UniqueID', 'rb') as f:
    UniqueID = pickle.load(f)

width, height = 107, 48

counter = set()  # Creating a Set in Python , Now Counter is a Set
# counterprev = set()  # Creating a Set in Python , Now Counter is a Set
li=[]
xi=[]
for i in range(69):
    li.append(i)
for i in range(len(li)):
    xi.append(True)
dicto=dict(zip(li,xi))
colorBlack = (0, 0, 0)

# flag = false
####################################################################################################################


def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        flag = False
        if count < 900:
            color = (0, 255, 0)  # GREEN
            thickness = 3
            spaceCounter += 1
            # This is for Adding when Space is not Vacant
            if temps[pos] not in counter:
                counter.add(temps[pos])
                
                # Commenting out database operations
                # CarInfo.drop()
                # strCounter = []
                # bools = []
                # for i in range(69):
                #     if(i in counter):
                #         bools.append(True)
                #         strCounter.append(str(i))
                #     else:
                #         bools.append(False)
                #         strCounter.append(str(i))
                # di = dict(zip(strCounter, bools))
                # CarInfo.insert_one(di)

        else:
            color = (0, 0, 255)  # RED
            thickness = 3

          # This is for Removing when Space is Vacant
            if temps[pos] in counter:   
                counter.remove(temps[pos])

                # Commenting out database operations
                # CarInfo.drop()
                # strCounter = []
                # bools = []
                # for i in range(69):
                #     if(i in counter):
                #         bools.append(True)
                #         strCounter.append(str(i))
                #     else:
                #         bools.append(False)
                #         strCounter.append(str(i))
                # di = dict(zip(strCounter, bools))
                # CarInfo.insert_one(di)

        ID = str(temps[pos])
        cv2.rectangle(img, pos, (pos[0] + width,
                      pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=1, offset=0, colorR=colorBlack)
        cvzone.putTextRect(img, ID, (x+1, y + height - 34), scale=1,
                           thickness=2, offset=0, colorR=colorBlack)
        if temps[pos] in counter:
            cvzone.putTextRect(img, "Free", (x+width-40, y + height), scale=1,
                               thickness=1, offset=0, colorR=colorBlack)
        else:
            cvzone.putTextRect(img, "Parked", (x+width-60, y + height-3), scale=1,
                               thickness=1, offset=0, colorR=colorBlack)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))
####################################################################################################################


while True:
    print("inside while")
    if not use_camera:  # Only reset frame position for video files
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    if not success:
        print("Failed to read frame")
        break
        
    # Create copies for different displays
    original_img = img.copy()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)

    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    # Display multiple views
    cv2.imshow("Original", original_img)
    cv2.imshow("Grayscale", imgGray)
    cv2.imshow("Threshold", imgThreshold)
    
    # Resize the main processed image for better visibility
    img_resized = cv2.resize(img, (800, 600))
    cv2.imshow("Processed Image", img_resized)
    
    key = cv2.waitKey(15)
    if key & 0xFF == ord('d'):
        print("Empty are :", counter, "Total=", len(counter))
        break
    elif key & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
        