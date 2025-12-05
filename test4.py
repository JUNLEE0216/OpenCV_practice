import cv2
import sys

cap = cv2.VideoCapture(0)
sticker = cv2.imread("tigermask.png", cv2.IMREAD_UNCHANGED)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def overlay_transparent(background, overlay, x, y):

    ol_h, ol_w, _ = overlay.shape
    alpha = overlay[:, :, 3] / 255.0 
    overlay_img = overlay[:, :, :3]

    for c in range(3): # B, G, R
        background[y:y+ol_h, x:x+ol_w, c] = \
            (overlay_img[:, :, c] * alpha + 
             background[y:y+ol_h, x:x+ol_w, c] * (1.0 - alpha))
             
    return background

if cap.isOpened() :
    while True :
        ret, frame = cap.read()

        if not ret : break

        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:

            # 스티커 리사이즈 (얼굴 너비에 맞춤... 이미지에 맞게 적절하게)
            sticker_resized = cv2.resize(sticker, (int(2.2*w), int(2.2*h))) 
            
            # x, y 좌표는 이미지에 맞게 적절한 조정 필요 
            frame = overlay_transparent(frame, sticker_resized, x-60, y-40)

        cv2.imshow("frame", frame)
        key = cv2.waitKey(20)
        if key == 27 : break
else :
    sys.exit()

cap.release()
cv2.destroyAllWindows()