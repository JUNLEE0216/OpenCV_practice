import numpy as np
import cv2


l_lightgreen = np.array([25, 80, 150])
u_lightgreen = np.array([45, 255, 255])

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ret, frame = cap.read()
height, width = frame.shape[:2]
canvas = np.zeros((height, width, 3), dtype=np.uint8)

prev_center = None
draw_color = (0, 255, 0)
thickness = 4

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (7,7), 0)

    mask = cv2.inRange(hsv, l_lightgreen, u_lightgreen)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 1000:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center = (cX, cY)

                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                if prev_center is not None:
                    cv2.line(canvas, prev_center, center, draw_color, thickness)

                prev_center = center
        else:
            prev_center = None
    else:
        prev_center = None

    output = cv2.add(frame, canvas)

    cv2.imshow("AirCanvas - Fluorescent Green", output)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(20)
    if key == 27:
        break
    elif key == ord('c'):
        canvas = np.zeros((height, width, 3), dtype=np.uint8)

cap.release()
cv2.destroyAllWindows()