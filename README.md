# Hệ Thống Nhận Diện Khuôn Mặt Bằng Camera (Face Recognition System)

## 📋 Mô Tả Dự Án

Dự án này xây dựng một hệ thống nhận diện khuôn mặt thời gian thực sử dụng:
- **OpenCV**: Xử lý video và xác định khuôn mặt
- **LBPH Face Recognizer** (Local Binary Patterns Histograms): Thuật toán nhận diện khuôn mặt

## 🚀 Các Bước Thực Hiện

### 1️⃣ **Thu Thập Dữ Liệu** (`collect_data.py`)

Ghi rõ dữ liệu khuôn mặt cho mỗi người dùng.

```bash
python collect_data.py
```

**Hướng dẫn:**
- Nhập tên người dùng (không để trống)
- Khi cửa sổ camera mở, bấm **SPACE** để lưu ảnh
- Bạn cần thu thập tối thiểu **100 ảnh** mỗi người dùng
- Bấm **ESC** để dừng

**Lưu ý:**
- Thay đổi góc nhìn, ánh sáng để có dữ liệu đa dạng
- Lưu ảnh từng cái một bằng phím SPACE (không tự động)
- Dữ liệu sẽ được lưu vào thư mục `dataset/<user_name>/`

### 2️⃣ **Huấn Luyện Mô Hình** (`train.py`)

Huấn luyện mô hình nhận diện dựa trên dữ liệu đã thu thập.

```bash
python train.py
```

**Quá trình:**
- Đọc tất cả ảnh từ thư mục `dataset/`
- Huấn luyện mô hình LBPH
- Lưu mô hình vào `trainer/model.yml`
- Lưu mapping nhãn vào `trainer/labels.npy`

**Lưu ý:**
- Cần ít nhất 2 ảnh từ các người dùng khác nhau
- Quá trình này có thể mất vài giây

### 3️⃣ **Nhận Diện Khuôn Mặt** (`recognition.py`)

Chạy hệ thống nhận diện khuôn mặt thời gian thực.

```bash
python recognition.py
```

**Tính năng:**
- Hiển thị tên người dùng được nhận diện (xanh lá)
- Hiển thị "Unknown" cho khuôn mặt không được biết (đỏ)
- Hiển thị độ tin cậy (Confidence Score)
- Thống kê số lần nhận diện thành công / không thành công
- Bấm **ESC** để thoát

## 📁 Cấu Trúc Thư Mục

```
.
├── collect_data.py      # Thu thập dữ liệu khuôn mặt
├── train.py             # Huấn luyện mô hình
├── recognition.py       # Nhận diện khuôn mặt thời gian thực
├── dataset/             # Thư mục lưu trữ ảnh huấn luyện
│   ├── <user1>/         # Ảnh của người dùng 1
│   ├── <user2>/         # Ảnh của người dùng 2
│   └── ...
└── trainer/             # Thư mục lưu mô hình
    ├── model.yml        # Mô hình LBPH
    └── labels.npy       # Mapping ID -> Tên người dùng
```

## ⚙️ Yêu Cầu Hệ Thống

### Thư viện Python

```bash
pip install opencv-python numpy
```

### Phần cứng

- Camera (webcam hoặc camera tích hợp)
- CPU đủ để xử lý video real-time

## 📊 Thông Số Kỹ Thuật

| Thông Số | Giá Trị | Mô Tả |
|----------|--------|-------|
| **Images per user** | 100 | Số ảnh tối thiểu cho mỗi người dùng |
| **Confidence Threshold** | 80 | Ngưỡng tin cậy (< 80 = nhận diện) |
| **Face Cascade** | haarcascade_frontalface_default | Model xác định khuôn mặt |
| **Recognizer** | LBPHFaceRecognizer | Thuật toán nhận diện |

## ✅ Hướng Dẫn Sử Dụng

### Quy trình cơ bản:

1. **Thêm người dùng mới:**
   ```bash
   python collect_data.py  # Chạy và nhập tên
   ```

2. **Sau khi tất cả người dùng đã có 100 ảnh:**
   ```bash
   python train.py  # Huấn luyện mô hình
   ```

3. **Chạy nhận diện:**
   ```bash
   python recognition.py  # Nhận diện real-time
   ```

### Ví dụ tên người dùng:
- `A`, `B`, `C`, `D`, `E` (như trong flowchart)
- Hoặc tên đầy đủ: `Nguyen Van A`, `Tran Thi B`

## 🎯 Mẹo Cải Thiện Độ Chính Xác

1. **Thu thập dữ liệu:**
   - Thay đổi ánh sáng, góc nhìn
   - Mặc các loại kính, mũ khác nhau
   - Thay đổi biểu cảm khuôn mặt

2. **Huấn luyện:**
   - Sử dụng ít nhất 100 ảnh mỗi người
   - Tăng số lượng ảnh cho độ chính xác cao hơn

3. **Nhận diện:**
   - Đặt camera ở vị trí tốt, ánh sáng đủ
   - Khuôn mặt phải rõ ràng, không bị lệch quá

## ❌ Xử Lý Sự Cố

| Lỗi | Nguyên Nhân | Giải Pháp |
|-----|-----------|----------|
| `Camera không mở` | Camera không kết nối | Kiểm tra camera, restart máy |
| `Model.yml not found` | Chưa chạy train.py | Chạy `python train.py` |
| `Nhận diện không chính xác` | Dữ liệu huấn luyện kém | Thu thập lại 100+ ảnh |
| `AttributeError: cv2.face` | OpenCV không có module face | Cài lại: `pip install opencv-contrib-python` |

## 📝 Lưu Ý

- Chương trình sử dụng **LBPH Face Recognizer** - phương pháp đơn giản nhưng hiệu quả
- Để độ chính xác cao hơn, có thể sử dụng **Deep Learning** (nhưng cần GPU)
- Dữ liệu khuôn mặt của người dùng được lưu cục bộ, không tải lên cloud

## 🔒 Bảo Mật

- Tất cả dữ liệu được lưu cục bộ
- Không có kết nối internet trong quá trình nhận diện
- Có thể xóa thư mục `dataset/` hoặc `trainer/` để xóa dữ liệu

## 📞 Hỗ Trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. OpenCV đã được cài đặt đúng
2. Camera hoạt động bình thường
3. Đã thu thập đủ dữ liệu (ít nhất 100 ảnh/người)
4. Đã huấn luyện mô hình (`train.py`)

---

**Chúc bạn thực hiện thành công! 🎉**
