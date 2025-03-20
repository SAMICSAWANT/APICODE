from enum import unique
import cv2
import pickle
from collections import defaultdict

width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread("C:/Users/dell/Documents/GitHub/PARKAPPSYSTEM/Pyt/carParkImg.png")
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width,
                      pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    if cv2.waitKey(10) & 0xFF == ord('d'):  # 0xFF is used to check if the key is pressed
        newlist = posList
        #print("The Value : " + str(newlist))
        temps = defaultdict(lambda: len(temps))

        UniqueID = [temps[ele] for ele in newlist]
        #print()
       # print("The ID : " + str(UniqueID))
        with open('UniqueID', 'wb') as f:
            pickle.dump(UniqueID, f)

        break
