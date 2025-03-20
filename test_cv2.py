import cv2
import numpy as np

# Create a simple test image
img = np.zeros((300, 300, 3), dtype=np.uint8)
cv2.rectangle(img, (100, 100), (200, 200), (0, 255, 0), 2)
cv2.putText(img, 'OpenCV Test', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Show the image
cv2.imshow('OpenCV Test', img)
cv2.waitKey(0)
cv2.destroyAllWindows() 