import cv2
import os
import numpy as np

# Cấu hình
DATASET_PATH = "dataset"
TRAINER_PATH = "trainer"

print("=" * 50)
print("HUẤN LUYỆN MÔ HÌNH NHẬN DIỆN KHUÔN MẶT")
print("=" * 50)

# Tạo thư mục lưu mô hình
if not os.path.exists(TRAINER_PATH):
    os.makedirs(TRAINER_PATH)
    print(f"✓ Tạo thư mục: {TRAINER_PATH}")

# Kiểm tra dataset tồn tại
if not os.path.exists(DATASET_PATH):
    print(f"❌ Lỗi: Thư mục '{DATASET_PATH}' không tồn tại!")
    print("Vui lòng chạy collect_data.py trước")
    exit()

# Khởi tạo recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_dict = {}
current_label = 0

print(f"\n📂 Đang đọc dữ liệu từ: {DATASET_PATH}")

# Đọc ảnh từ dataset
for user in sorted(os.listdir(DATASET_PATH)):
    user_path = os.path.join(DATASET_PATH, user)
    if not os.path.isdir(user_path):
        continue

    image_count = len([f for f in os.listdir(user_path) if f.endswith('.jpg')])
    
    if image_count == 0:
        print(f"⚠️  {user}: Không có ảnh nào!")
        continue
    
    print(f"📸 {user}: Tìm thấy {image_count} ảnh")
    
    label_dict[current_label] = user

    for image_name in os.listdir(user_path):
        if not image_name.endswith('.jpg'):
            continue
            
        img_path = os.path.join(user_path, image_name)
        try:
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"  ⚠️  Không thể đọc: {image_name}")
                continue
            faces.append(img)
            labels.append(current_label)
        except Exception as e:
            print(f"  ❌ Lỗi khi xử lý {image_name}: {str(e)}")

    current_label += 1

# Kiểm tra có đủ dữ liệu để huấn luyện và
if len(faces) < 2:
    print("\n❌ Lỗi: Cần ít nhất 2 ảnh từ các người dùng khác nhau để huấn luyện!")
    exit()

print(f"\n✓ Tổng cộng: {len(faces)} ảnh từ {len(label_dict)} người dùng")

# Huấn luyện mô hình
print("\n🔄 Đang huấn luyện mô hình...")
try:
    recognizer.train(faces, np.array(labels))
    recognizer.save(f"{TRAINER_PATH}/model.yml")
    print(f"✓ Mô hình đã được lưu: {TRAINER_PATH}/model.yml")
    
    # Lưu label dictionary
    np.save(f"{TRAINER_PATH}/labels.npy", label_dict)
    print(f"✓ Labels đã được lưu: {TRAINER_PATH}/labels.npy")
    
    print("\n" + "=" * 50)
    print("✓ HOÀN THÀNH HUẤN LUYỆN MÔ HÌNH!")
    print("=" * 50)
    print(f"\nBảng ánh xạ ID:")
    for id_, name in label_dict.items():
        print(f"  ID {id_}: {name}")
    
except Exception as e:
    print(f"\n❌ Lỗi khi huấn luyện: {str(e)}")
    exit()