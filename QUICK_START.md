# 🎯 HƯỚNG DẪN NHANH - Face Recognition System

## ⚡ Cài Đặt Nhanh

### Bước 1: Cài Đặt OpenCV
```bash
pip install -r requirements.txt
```

### Bước 2: Thu Thập Dữ Liệu
```bash
python collect_data.py
```

**Làm gì:**
- Nhập tên (ví dụ: A, B, C, D, E)
- Bấm **SPACE** 100 lần để lưu 100 ảnh khuôn mặt
- Bấm **ESC** để hoàn thành

**Mẹo:**
- Thay đổi góc nhìn (trái, phải, trên, dưới)
- Thay đổi ánh sáng (sáng, tối)
- Đổi biểu cảm (cười, không cười)

### Bước 3: Huấn Luyện Mô Hình
```bash
python train.py
```

**Kết quả:** Tạo 2 file:
- `trainer/model.yml` - Mô hình nhận diện
- `trainer/labels.npy` - Tên người dùng

### Bước 4: Chạy Nhận Diện
```bash
python recognition.py
```

**Kết quả:**
- ✅ **Xanh lá**: Nhận diện được
- ❌ **Đỏ**: Không nhận diện
- **Confidence**: Độ tin cậy

---

## 📝 Ví Dụ Cụ Thể

### Thu Thập 5 Người (A, B, C, D, E)

```
Lần 1:
$ python collect_data.py
→ Nhập: A
→ Bấm SPACE 100 lần
→ Bấm ESC

Lần 2:
$ python collect_data.py
→ Nhập: B
→ Bấm SPACE 100 lần
→ Bấm ESC

Lần 3-5: Lặp lại với C, D, E
```

### Huấn Luyện
```
$ python train.py

Kết quả:
📸 A: Tìm thấy 100 ảnh
📸 B: Tìm thấy 100 ảnh
📸 C: Tìm thấy 100 ảnh
📸 D: Tìm thấy 100 ảnh
📸 E: Tìm thấy 100 ảnh
✓ HOÀN THÀNH HUẤN LUYỆN MÔ HÌNH!
```

### Nhận Diện
```
$ python recognition.py

📋 Danh sách người dùng được đăng ký:
  • ID 0: A
  • ID 1: B
  • ID 2: C
  • ID 3: D
  • ID 4: E

📹 Đang khởi động camera...
→ Khuôn mặt xuất hiện → Nhận diện tên người
→ Bấm ESC để thoát
```

---

## ❌ Lỗi Phổ Biến và Cách Khắc Phục

| Lỗi | Giải Pháp |
|-----|----------|
| `Camera không mở` | Kiểm tra camera kết nối, restart máy |
| `Model.yml not found` | Chạy `python train.py` |
| `cv2.face not found` | Cài: `pip install opencv-contrib-python` |
| `Nhận diện sai lệch` | Thu thập lại 100+ ảnh/người người với ánh sáng khác nhau |

---

## 📊 Cấu Trúc Thư Mục Sau Khi Hoàn Thành

```
.
├── collect_data.py
├── train.py
├── recognition.py
├── dataset/
│   ├── A/          (100 ảnh người A)
│   ├── B/          (100 ảnh người B)
│   ├── C/          (100 ảnh người C)
│   ├── D/          (100 ảnh người D)
│   └── E/          (100 ảnh người E)
└── trainer/
    ├── model.yml   (Mô hình)
    └── labels.npy  (Nhãn)
```

---

## 🎬 Tips Để Cải Thiện Độ Chính Xác

✅ **Tốt:**
- Thu thập ảnh ở nhiều góc độ
- Ánh sáng tự nhiên hoặc đèn LED đều
- Camera ở cách xa 30-60cm
- Khuôn mặt chiếm 1/3 - 1/2 khu vực ảnh

❌ **Tránh:**
- Ánh sáng mạnh từ phía sau
- Khuôn mặt bị che phủ (khẩu trang, mắt kính)
- Quá gần hoặc quá xa camera
- Ảnh bị mờ hoặc che khuất

---

## 🚀 Chạy Nhanh Nhất (Chỉ 3 Bước)

```bash
# 1. Thu thập (lặp 5 lần với A, B, C, D, E)
python collect_data.py

# 2. Huấn luyện (chạy 1 lần)
python train.py

# 3. Nhận diện (chạy lặp lại)
python recognition.py
```

---

**Chúc bạn thành công! 🎉**
