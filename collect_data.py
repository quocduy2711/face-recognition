import cv2
import os
import time

# Cấu hình
TOTAL_IMAGES = 100
DATASET_PATH = "dataset"

# Yêu cầu tên người dùng
user_name = input("Nhập tên người dùng: ").strip()
if not user_name:
    print("Lỗi: Tên người dùng không được để trống!")
    exit()

save_path = f"{DATASET_PATH}/{user_name}"

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)
    
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print(f"✓ Tạo thư mục: {save_path}")
else:
    print(f"📂 Thư mục đã tồn tại: {save_path}")

# Model nhận diện khuôn mặt của OpenCV
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

if face_cascade.empty():
    print("Lỗi: Không thể tải face cascade classifier!")
    exit()

# Mở camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Lỗi: Không thể mở camera!")
    exit()

print(f"\n📹 Đang thu thập ảnh cho người dùng: {user_name}")
print(f"Nhấn 'SPACE' để lưu ảnh hoặc 'ESC' để thoát")
print(f"Cần thu thập: {TOTAL_IMAGES} ảnh\n")

count = 0  # Đếm số ảnh đã lấy
frame_skip = 2  # Lấy 1 ảnh mỗi 2 frame
frame_count = 0

try:
    while count < TOTAL_IMAGES:
        ret, frame = cap.read()
        if not ret:
            print("Lỗi: Không thể đọc frame từ camera!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Vẽ hình chữ nhật quanh khuôn mặt
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Hiển thị thông tin trên frame
        text = f"Collected: {count}/{TOTAL_IMAGES}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
        cv2.putText(frame, "Press SPACE to capture, ESC to exit", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow("Thu thap Khuon mat", frame)

        key = cv2.waitKey(1) & 0xFF
        
        # SPACE key - lưu ảnh
        if key == 32 and len(faces) > 0:
            face_roi = gray[faces[0][1]:faces[0][1]+faces[0][3], 
                           faces[0][0]:faces[0][0]+faces[0][2]]
            count += 1
            filename = f"{save_path}/{count}.jpg"
            cv2.imwrite(filename, face_roi)
            print(f"✓ Đã lưu ảnh {count}/{TOTAL_IMAGES}: {filename}")
            time.sleep(0.3)  # Delay để tránh lưu nhiều ảnh cùng lúc
            
        # ESC key - thoát
        elif key == 27:
            print(f"\n⚠️  Đã dừng. Thu thập được {count}/{TOTAL_IMAGES} ảnh")
            break

    if count >= TOTAL_IMAGES:
        print(f"\n✓ Hoàn thành! Đã thu thập {TOTAL_IMAGES} ảnh cho {user_name}")
        
except KeyboardInterrupt:
    print(f"\n⚠️  Bị gián đoạn. Thu thập được {count}/{TOTAL_IMAGES} ảnh")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("✓ Đã đóng camera")