import cv2
import sys

cap = cv2.VideoCapture(0)
sticker = cv2.imread("face.png", cv2.IMREAD_UNCHANGED)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        
        left_eye = (int(x + w*0.3), int(y + h*0.35))
        right_eye = (int(x + w*0.7), int(y + h*0.35))
        nose = (int(x + w*0.5), int(y + h*0.6))

        sticker_resized = cv2.resize(sticker, (w, h))

        roi = frame[y:y+h, x:x+w]

        sticker_rgb = sticker_resized[:, :, :3]
        sticker_alpha = sticker_resized[:, :, 3] / 255.0

        for c in range(3):
            roi[:, :, c] = (roi[:, :, c] * (1 - sticker_alpha) +
                            sticker_rgb[:, :, c] * sticker_alpha)

        frame[y:y+h, x:x+w] = roi

        cv2.circle(frame, left_eye, 5, (255, 0, 0), -1)
        cv2.circle(frame, right_eye, 5, (255, 0, 0), -1)
        cv2.circle(frame, nose, 5, (0, 0, 255), -1)

    cv2.imshow("frame", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()