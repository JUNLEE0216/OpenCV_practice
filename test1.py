import cv2
import sys

fourcc = cv2.VideoWriter_fourcc(*'XVID') #코덱 설정
output = cv2.VideoWriter('output.avi', fourcc, 30.0 , (640,480))

#연속된 영상을 받을 수 있는 매개체가 인수로 전달됨
cap = cv2.VideoCapture(0) # 0번 카메라 (기본 웹캠)

if not cap.isOpened(): #카메라 연결 실패시
    print("Camera open failed!")
    sys.exit(-1)

while True:
    ret, frame = cap.read() # 한 프레임 읽기 ret: return value, frame: 영상 프레임
    if ret :
        output.write(frame) # 영상 저장
        cv2.imshow('frame', frame) # 영상 출력
        key = cv2.waitKey(1) 
        if key == ord("q"):
            break
cap.release() #캡쳐 객체 해제
output.release() #저장 객체 해제
cv2.destroyAllWindows() 