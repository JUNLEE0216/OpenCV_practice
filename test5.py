import numpy as np
import cv2

# HSV 색상 범위 설정 (형광 연두색)
l_lightgreen = np.array([25, 80, 150])   # 하한값 (Hue, Saturation, Value)
u_lightgreen = np.array([45, 255, 255])  # 상한값

# 웹캠 연결
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # 프레임 너비 설정
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 프레임 높이 설정

# 첫 프레임 읽기
ret, frame = cap.read()
height, width = frame.shape[:2]

# 그림을 그릴 캔버스(검은 배경) 생성
canvas = np.zeros((height, width, 3), dtype=np.uint8)

# 이전 좌표 저장 변수
prev_center = None
draw_color = (0, 255, 0)   # 선 색상 (초록)
thickness = 5              # 선 두께

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 좌우 반전 (거울 효과)
    frame = cv2.flip(frame, 1)

    # BGR → HSV 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 노이즈 제거를 위한 블러 처리
    hsv = cv2.GaussianBlur(hsv, (7,7), 0)

    # 지정한 색 범위에 해당하는 부분만 마스크 생성
    mask = cv2.inRange(hsv, l_lightgreen, u_lightgreen)

    # 마스크 노이즈 제거 (열림 → 닫힘 연산)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # 가장 큰 윤곽선 선택
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 1000:  # 작은 잡음 제거
            M = cv2.moments(c)
            if M["m00"] != 0:
                # 무게중심 좌표 계산
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center = (cX, cY)

                # 현재 위치 표시 (빨간 점)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # 이전 좌표와 연결하여 선 그리기
                if prev_center is not None:
                    cv2.line(canvas, prev_center, center, draw_color, thickness)

                # 현재 좌표를 이전 좌표로 저장
                prev_center = center
        else:
            prev_center = None
    else:
        prev_center = None

    # 원본 프레임 + 그림 캔버스 합성
    output = cv2.add(frame, canvas)

    # 결과 출력
    cv2.imshow("AirCanvas - Fluorescent Green", output)  # 그림 그린 화면
    cv2.imshow("Mask", mask)                             # 마스크 화면

    # 키 입력 처리
    key = cv2.waitKey(20)
    if key == 27:  # ESC 누르면 종료
        break
    elif key == ord('c'):  # 'c' 누르면 캔버스 초기화
        canvas = np.zeros((height, width, 3), dtype=np.uint8)

    elif key == ord('r'):
        draw_color = (0, 0, 255)  # 빨강
    elif key == ord('g'):
        draw_color = (0, 255, 0)  # 초록
    elif key == ord('b'):
        draw_color = (255, 0, 0)  # 파랑

# 자원 해제
cap.release()
cv2.destroyAllWindows()