import cv2
import numpy as np
import random

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠 열기 실패 ㅠ.ㅠ")
        return

    ret, frame = cap.read()
    if not ret:
        print("첫 프레임 읽기 실패 ㅠ.ㅠ")
        return
    # 펜이 그림을 따로 그리기 위해 사용하는 백업 이미지
    canvas = np.zeros_like(frame)

    # 이어지는 선을 그리려면 과거 위치와 현재 위치를 기억해야 함
    prev_center = None

    # 어두운 초록색 기준
    lower_dark_green = np.array([40, 70, 20])
    upper_dark_green = np.array([80, 255, 120])

    # 노이즈 제거할 때 사용할 커널
    kernel = np.ones((5, 5), np.uint8)

    print("키 입력 가이드 : 펜 지우기는 c, 펜 색상 바꾸기는 p, 종료는 q")

    # BGR 색상을 랜덤하게 정해서 초기 색상을 결정
    pen_color = [random.randint(0, 255) for i in range(3)]


    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 영상 반전
        frame = cv2.flip(frame, 1)

    
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # 초록색 부분만 강조된 영상 얻기
        mask = cv2.inRange(hsv, lower_dark_green, upper_dark_green)

        # 마스크는 이진화된 영상이므로 노이즈 제거를 위해 침식과 팽창을 사용함        
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

        # 강조된 부분의 경계선 얻기
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        center = None

        if contours:
            #컨투어 중에서 제일 큰 거 하나 고르기(면적을 기준으로)
            largest = max(contours, key=cv2.contourArea)
            # 실제 면적 계산
            area = cv2.contourArea(largest)

            # 면적도 어느정도 이상 될 때만 인정하기
            if area > 500:
                # 중심 좌표 계산
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) #가로축 중심 구하기 공식
                    cy = int(M["m01"] / M["m00"]) #세로축 중심 구하기 공식
                    center = (cx, cy)

                    # cv2.circle(frame, center, 7, (255, 0, 0), -1)

                    if prev_center is not None:
                        # 백업 이미지에 이전 중심과 현재 중심을 이어라
                        cv2.line(canvas, prev_center, center, pen_color, 5)

        prev_center = center

        # 캔버스에는 펜으로 그린 그림이 있고, 프레임에는 원본 영상이 있으니,
        # 둘을 합치면 완성이다!
        output = cv2.addWeighted(frame, 0.7, canvas, 0.8, 0)

        cv2.imshow("Output", output)
        # 키 입력 처리
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            canvas[:] = 0
            prev_center = None
        elif key == ord('p'):
            pen_color = [random.randint(0, 255) for i in range(3)] # 위에서 정의한 랜덤 색상으로 변경

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()