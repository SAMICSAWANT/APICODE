from enum import unique
import cv2
import pickle
from collections import defaultdict

width, height = 150,80

try:
    with open('CarParkPos3', 'rb') as f:
        posList3 = pickle.load(f)
except:
    posList3 = []


def mouseClick(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:
        posList3.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList3):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList3.pop(i)

    with open('CarParkPos3', 'wb') as f:
        pickle.dump(posList3, f)


while True:
    img2 = cv2.imread('IMG3.jpg')
    img = cv2.resize(img2, (700, 700))
    for pos in posList3:
        cv2.rectangle(img, pos, (pos[0] + width,
                      pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    if cv2.waitKey(10) & 0xFF == ord('d'):  # 0xFF is used to check if the key is pressed
        newlist = posList3
        #print("The Value : " + str(newlist))
        temps = defaultdict(lambda: len(temps))

        UniqueID3 = [temps[ele] for ele in newlist]
        #print()
       # print("The ID : " + str(UniqueID3))
        with open('UniqueID3', 'wb') as f:
            pickle.dump(UniqueID3, f)

        break
