import cv2
import pickle
import cvzone
import numpy as np
from collections import defaultdict
from database import CarInfo3
from ParkSpacePick3 import temps
import json

with open('CarParkPos3', 'rb') as f:
    posList3 = pickle.load(f)

with open('UniqueID3', 'rb') as f:
    UniqueID3 = pickle.load(f)

width, height = 150,80
counter = set()  # Creating a Set in Python , Now Counter is a Set
# counterprev = set()  # Creating a Set in Python , Now Counter is a Set
li=[]
xi=[]
for i in range(14):
    li.append(i)
for i in range(len(li)):
    xi.append(True)
dicto=dict(zip(li,xi))
colorBlack = (0, 0, 0)

# flag = false
####################################################################################################################


def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList3:
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
                                #    print(counter, ":Green")
                CarInfo3.drop()
                strCounter = []
                bools = []
                for i in range(14):
                    if(i in counter):
                        bools.append(True)
                        strCounter.append(str(i))
                    else:
                        bools.append(False)
                        strCounter.append(str(i))
                di = dict(zip(strCounter, bools))
                CarInfo3.insert_one(di)

        else:
            color = (0, 0, 255)  # RED
            thickness = 3

          # This is for Removing when Space is Vacant
            if temps[pos] in counter:   
                counter.remove(temps[pos])

                CarInfo3.drop()
                strCounter = []
                bools = []
                for i in range(14):
                    if(i in counter):
                        bools.append(True)
                        strCounter.append(str(i))
                    else:
                        bools.append(False)
                        strCounter.append(str(i))
                di = dict(zip(strCounter, bools))
                CarInfo3.insert_one(di)

        ID = str(temps[pos])
        cv2.rectangle(img, pos, (pos[0] + width,
                      pos[1] + height), color, thickness)
        # cvzone.putTextRect(img, str(count), (x, y + height - 200), scale=1,
        #                    thickness=1, offset=0, colorR=colorBlack)
        cvzone.putTextRect(img, ID, (x+1, y + height -3), scale=1,
                           thickness=2, offset=0, colorR=colorBlack)
        # if temps[pos] in counter:
            # cvzone.putTextRect(img, "Free", (x+width-40, y-310 ), scale=1,
                            #    thickness=1, offset=0, colorR=colorBlack)
        # else:
            # cvzone.putTextRect(img, "Parked", (x+width-60, y-310), scale=1,
                            #    thickness=1, offset=0, colorR=colorBlack)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList3)}', (460, 33), scale=1.6,
                       thickness=2, offset=20, colorR=(0, 200, 0))
####################################################################################################################


while True:

    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    img2 = cv2.imread('IMG3.jpg')
    # cv2.imshow("Im",img2)
    img = cv2.resize(img2, (700, 700))
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)

    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)
    # cv2.imshow("Image", imgGray)
    # cv2.imshow("ImageBlur", imgBlur)
    #cv2.imshow("ImageThresh", imgThreshold)
    #cv2.imshow("ImageMed", imgMedian)
    #cv2.imshow("imgDilate", imgDilate)
    if cv2.waitKey(15) & 0xFF == ord('d'):
        print("Empty are :", counter, "Total=", len(counter))
        break
        