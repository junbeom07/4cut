import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

# Tkinter 설정
root = tk.Tk()
root.withdraw()  # Tkinter 기본 창 숨기기

# 사용자로부터 폴더 이름 입력받기
folder_name = simpledialog.askstring("Input", "저장할 폴더 이름을 입력하세요:")

if not folder_name:
    print("폴더 이름이 입력되지 않았습니다. 프로그램을 종료합니다.")
    exit()

# 현재 날짜를 포함한 폴더 이름 생성
date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"InsaengNeCut_{folder_name}_{date_str}"

# 폴더가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 사진 저장용 리스트 및 파일 경로 설정
captured_images = [None] * 4
image_filenames = [os.path.join(output_dir, f"image_{i + 1}.jpg") for i in range(4)]

# 웹캠 실행
cap = cv2.VideoCapture(0)

print("사진을 찍으려면 1, 2, 3, 4 키를 누르세요.")
print("콜라주 생성을 위해 엔터 키를 누르세요.")

while True:
    ret, frame = cap.read()
    
    # 화면에 프레임 출력
    cv2.imshow('Webcam', frame)

    # 키 입력 대기
    key = cv2.waitKey(1) & 0xFF

    # '1', '2', '3', '4' 키를 눌렀을 때 해당하는 이미지를 캡처
    if key in [ord('1'), ord('2'), ord('3'), ord('4')]:
        index = key - ord('1')  # 0, 1, 2, 3에 해당하는 인덱스
        img_filename = image_filenames[index]
        # 새로운 이미지 저장
        cv2.imwrite(img_filename, frame)
        captured_images[index] = frame
        print(f"Captured image {index + 1}: {img_filename}")

    # 엔터 키를 눌렀을 때 콜라주 생성
    if key == 13:  # Enter 키
        break

# 웹캠 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()

# 캡처된 이미지로 콜라주 생성
# 이미지가 없어도 가능한 경우를 고려하여 `None` 체크
captured_images = [img for img in captured_images]

# 이미지 크기와 배경 설정
max_width = max((img.shape[1] for img in captured_images if img is not None), default=0)
max_height = max((img.shape[0] for img in captured_images if img is not None), default=0)

# 빈 이미지로 채우기 (배경은 흰색)
empty_img = np.full((max_height, max_width, 3), 255, dtype=np.uint8)

# 각 캡처된 이미지를 배경 위에 올리기
for i in range(4):
    if captured_images[i] is None:
        captured_images[i] = empty_img

padded_images = []
for img in captured_images:
    # 이미지 중앙에 맞게 패딩 추가
    height, width, _ = img.shape
    top_pad = (max_height - height) // 2
    bottom_pad = max_height - height - top_pad
    left_pad = (max_width - width) // 2
    right_pad = max_width - width - left_pad
    
    padded_img = cv2.copyMakeBorder(img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    padded_images.append(padded_img)

# 결과 이미지 출력 및 저장
fig, axes = plt.subplots(2, 2, figsize=(max_width/100, max_height/100))  # 2x2 배열의 서브플롯 생성, 크기는 동적으로 설정

# 서브플롯에 이미지 추가
for i, ax in enumerate(axes.flat):
    # BGR을 RGB로 변환 (Matplotlib는 RGB를 사용)
    img_rgb = cv2.cvtColor(padded_images[i], cv2.COLOR_BGR2RGB)
    ax.imshow(img_rgb)
    ax.axis('off')  # 축 제거

plt.tight_layout()  # 레이아웃 조정
collage_filename = os.path.join(output_dir, "인생네컷.jpg")
plt.savefig(collage_filename, dpi=300)  # 콜라주 이미지를 파일로 저장
plt.show()  # 콜라주 이미지를 화면에 표시

print(f"Collage saved as {collage_filename}")

