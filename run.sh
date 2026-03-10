#!/bin/bash
# Script cài đặt và chạy Face Recognition System

echo "================================"
echo "Face Recognition System Setup"
echo "================================"
echo ""

# Kiểm tra Python
echo "1️⃣  Kiểm tra Python..."
python --version || { echo "❌ Python chưa được cài đặt!"; exit 1; }
echo "✓ Python OK"
echo ""

# Cài đặt thư viện
echo "2️⃣  Cài đặt thư viện..."
pip install -r requirements.txt
echo "✓ Thư viện đã được cài đặt"
echo ""

# Menu chính
while true; do
  echo "================================"
  echo "MENU CHÍNH"
  echo "================================"
  echo "1. Thu thập dữ liệu khuôn mặt (collect_data.py)"
  echo "2. Huấn luyện mô hình (train.py)"
  echo "3. Nhận diện khuôn mặt (recognition.py)"
  echo "4. Xem hướng dẫn (README.md)"
  echo "5. Thoát"
  echo ""
  read -p "Chọn tùy chọn (1-5): " choice

  case $choice in
    1)
      echo "Chạy thu thập dữ liệu..."
      python collect_data.py
      ;;
    2)
      echo "Chạy huấn luyện mô hình..."
      python train.py
      ;;
    3)
      echo "Chạy nhận diện khuôn mặt..."
      python recognition.py
      ;;
    4)
      echo "Mở README.md..."
      cat README.md | less
      ;;
    5)
      echo "Tạm biệt!"
      exit 0
      ;;
    *)
      echo "❌ Tùy chọn không hợp lệ!"
      ;;
  esac

  echo ""
done
