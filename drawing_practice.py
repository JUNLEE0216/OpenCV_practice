import cv2
import numpy as np

events = [i for i in dir(cv2) if 'EVENT' in i]
print(events)

click = False     
x1,y1 = -1,-1

def drawing(event, x ,y, flags, param):
    global x1,y1, click

    if event == cv2.EVENT_LBUTTONDOWN:
        click = True
        x1, y1 = x, y
        if click == True:
            cv2.circle(canvas,(x, y),30,(150,150,0),-1)
        
        print("시작 좌표:", x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if click == True:
            cv2.circle(canvas,(x, y),10,(0,0,0),-1)
            print("좌표", x, y)


    elif event == cv2.EVENT_LBUTTONUP:
        click = False
        cv2.circle(canvas,(x,y),30,(0,150,150),-1)
        print("종료 좌표", x, y)

canvas = np.full((512, 512, 3), 255, dtype=np.uint8)
cv2.namedWindow('canvas')
cv2.setMouseCallback('canvas', drawing)
while True:
    cv2.imshow('canvas', canvas) 
    key = cv2.waitKey(10) & 0xFF   
        
    if key == ord('c'):             
        canvas = np.full((512, 512, 3),255,dtype=np.uint8)
    elif key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()