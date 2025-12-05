# TechVidvan - Air Canvas

# 필요한 패키지 임포트
import cv2
import numpy as np

# 다양한 색상 정의
colors = [(255, 0, 0), (255, 0, 255), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

# 기본 색상 선택
color = colors[0]

# 컨투어의 최소 허용 면적
min_area = 1000

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))

# 빈 캔버스 생성
canvas = np.zeros((height, width, 3), np.uint8)

# 녹색을 검출하기 위한 색상 범위
lower_bound = np.array([50,100,100])
upper_bound = np.array([90,255,255])

# 10x10 커널 정의
kernel = np.ones((10,10), np.uint8)

previous_center_point = 0


while True:
    # 웹캠에서 각 프레임 읽기
    success, frame = cap.read()

    # 프레임 좌우 반전
    frame = cv2.flip(frame, 1)

    # 프레임을 BGR에서 HSV 색공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 녹색의 이진 마스크 생성
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # 분할 영역을 넓히기 위해 팽창(dilation) 추가
    mask = cv2.dilate(mask, kernel, iterations=1)

    # 분할된 마스크의 모든 컨투어 찾기
    contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 컨투어가 감지되면 다음 문장 실행
    if len(contours) > 0:
        
        # 감지된 컨투어 중 가장 큰 컨투어 가져오기
        cmax = max(contours, key = cv2.contourArea)

        # 컨투어의 면적 계산
        area = cv2.contourArea(cmax)
        # print(area)

        # 컨투어 면적이 임계값보다 큰지 확인
        if area > min_area:

            # 컨투어의 중심점 찾기
            M = cv2.moments(cmax)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # 컨투어 중심점에 원 그리기
            cv2.circle(frame, (cX, cY), 10, (0, 0, 255), 2)
            
            # 캔버스에 그릴 색상 선택
            if previous_center_point == 0:
                if cY < 65:
                    # 전체 지우기
                    if cX > 20 and cX < 120:
                        canvas = np.zeros((height, width, 3), np.uint8)
                    
                    elif cX > 140 and cX < 220:
                        color = colors[0]

                    elif cX > 240 and cX < 320:
                        color = colors[1]
                    
                    elif cX > 340 and cX < 420:
                        color = colors[2]
                    
                    elif cX > 440 and cX < 520:
                        color = colors[3]
                    
                    elif cX > 540 and cX < 620:
                        color = colors[4]

            # 그리기가 시작되면 각 프레임의 중심점 사이에 선 그리기
            if previous_center_point != 0:
                cv2.line(canvas, previous_center_point, (cX, cY), color, 2)

            # 중심점 업데이트
            previous_center_point = (cX, cY)

        else:
            previous_center_point = 0

    # 캔버스 마스크를 원본 프레임에 추가
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, canvas_binary = cv2.threshold(canvas_gray, 20, 255, cv2.THRESH_BINARY_INV)

    canvas_binary = cv2.cvtColor(canvas_binary, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, canvas_binary)
    frame = cv2.bitwise_or(frame, canvas)

    # 색상 버튼을 라이브 프레임에 추가하여 색상 선택 가능하게 하기
    cv2.rectangle(frame, (20,1), (120,65), (122,122,122), -1)
    cv2.rectangle(frame, (140,1), (220,65), colors[0], -1)
    cv2.rectangle(frame, (240,1), (320,65), colors[1], -1)
    cv2.rectangle(frame, (340,1), (420,65), colors[2], -1)
    cv2.rectangle(frame, (440,1), (520,65), colors[3], -1)
    cv2.rectangle(frame, (540,1), (620,65), colors[4], -1)
    cv2.putText(frame, "CLEAR ALL", (30, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (155, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "VIOLET", (255, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (355, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (465, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (555, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

    # 프레임을 새로운 OpenCV 창에 표시
    cv2.imshow("Frame", frame)
    # cv2.imshow("mask", mask)
    cv2.imshow('Canvas', canvas)

    # 'q' 키가 눌릴 때까지 OpenCV 창 열기
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()