"""
Hệ Thống Nhận Diện Khuôn Mặt v3 + Active Liveness (OpenCV Blink Detection)
============================================================================
Chống giả mạo: Yêu cầu CHỚP MẮT 1 lần để xác thực là người thật.
Ảnh tĩnh / điện thoại cầm ảnh: không bao giờ chớp mắt được → bị chặn.

Phím tắt:
  ESC : Thoát
  L   : Bật/Tắt liveness
  R   : Reset (yêu cầu chớp mắt lại)
"""

import cv2
import numpy as np
import os
import time

from config import (
    TRAINER_PATH, CONFIDENCE_THRESHOLD,
    SCALE_FACTOR, MIN_NEIGHBORS, CAMERA_INDEX,
    LIVENESS_ENABLED,
    EAR_THRESHOLD, BLINK_MIN_FRAMES, BLINK_MAX_FRAMES,
    NO_FACE_RESET_FRAMES,
)
from liveness_detector import LivenessDetector, draw_liveness_result


# ─────────────────────────────────────────────
# Helper: HUD
# ─────────────────────────────────────────────

def draw_hud(frame, fps, liveness_on, state, stats):
    h_frame = frame.shape[0]

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (320, 120), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)

    cv2.putText(frame, "Face Recognition + Blink Liveness", (8, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
    cv2.putText(frame, f"FPS: {fps:.1f}", (8, 44),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (180, 255, 180), 1)

    as_color = (0, 255, 120) if liveness_on else (80, 80, 80)
    cv2.putText(frame, f"Liveness: {'ON' if liveness_on else 'OFF'}", (8, 66),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, as_color, 1)

    st_color = (0, 255, 0) if state == "VERIFIED" else (0, 200, 255)
    cv2.putText(frame, f"State: {state}", (8, 88),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, st_color, 1)

    cv2.putText(frame,
                f"OK:{stats['recognized']}  ?:{stats['unknown']}  BLOCKED:{stats['blocked']}",
                (8, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (200, 200, 200), 1)

    cv2.putText(frame, "ESC=exit  L=toggle  R=reset",
                (8, h_frame - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (130, 130, 130), 1)


# ─────────────────────────────────────────────
# Khởi động
# ─────────────────────────────────────────────

print("=" * 55)
print("  HE THONG NHAN DIEN KHUON MAT - BLINK LIVENESS v3")
print("=" * 55)

if not os.path.exists(f"{TRAINER_PATH}/model.yml"):
    print(f"[LOI] Khong thay model: {TRAINER_PATH}/model.yml")
    exit()
if not os.path.exists(f"{TRAINER_PATH}/labels.npy"):
    print(f"[LOI] Khong thay labels.")
    exit()

# LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(f"{TRAINER_PATH}/model.yml")
label_dict = np.load(f"{TRAINER_PATH}/labels.npy", allow_pickle=True).item()

print(f"[OK] Model: {TRAINER_PATH}/model.yml")
print(f"[OK] Labels: {len(label_dict)} nguoi")
for id_, name in label_dict.items():
    print(f"     * ID {id_}: {name}")

# Haar Cascade (mặt)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
if face_cascade.empty():
    print("[LOI] Khong the tai haarcascade!")
    exit()

# Liveness detector (pure OpenCV blink)
liveness_on = LIVENESS_ENABLED
detector = LivenessDetector(
    ear_threshold=EAR_THRESHOLD,
    blink_min_frames=BLINK_MIN_FRAMES,
    blink_max_frames=BLINK_MAX_FRAMES,
    no_face_reset=NO_FACE_RESET_FRAMES,
)
print(f"\n[Liveness] {'BAT' if liveness_on else 'TAT'} — Blink Detection (Pure OpenCV)")

cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("[LOI] Khong mo duoc camera!")
    exit()

print("\n[Camera] Dang khoi dong...")
print("  ESC=thoat | L=bat/tat liveness | R=yeu cau chop mat lai\n")

# ─────────────────────────────────────────────
# Thống kê & FPS
# ─────────────────────────────────────────────
stats     = {"recognized": 0, "unknown": 0, "blocked": 0}
fps_timer = time.time()
fps       = 0.0
frame_cnt = 0

current_state = "WAITING"

# ─────────────────────────────────────────────
# Vòng lặp chính
# ─────────────────────────────────────────────
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[LOI] Khong doc duoc frame!")
            break

        # FPS
        frame_cnt += 1
        now = time.time()
        if now - fps_timer >= 1.0:
            fps       = frame_cnt / (now - fps_timer)
            frame_cnt = 0
            fps_timer = now

        # Phát hiện khuôn mặt (Haar Cascade)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NEIGHBORS
        )

        # ── Xử lý từng khuôn mặt ──────────────────────────────────────
        if len(faces) == 0:
            # Không thấy mặt → báo detector
            if liveness_on:
                is_real, current_state, debug_val, message = detector.process(frame, None)
        else:
            for (x, y, w, h) in faces:
                face_box = (x, y, w, h)

                # Liveness check (truyền face_box để crop vùng mắt)
                if liveness_on:
                    is_real, current_state, debug_val, message = detector.process(frame, face_box)
                else:
                    is_real, current_state, debug_val, message = True, "VERIFIED", 1.0, ""

                # Nhận diện danh tính (chỉ khi VERIFIED)
                face_gray  = gray[y : y + h, x : x + w]
                id_, confidence = recognizer.predict(face_gray)

                if not is_real:
                    stats["blocked"] += 1
                    frame = draw_liveness_result(
                        frame, x, y, w, h,
                        name="", confidence=confidence,
                        is_real=False, state=current_state,
                        avg_ear=debug_val, message=message,
                    )
                else:
                    if confidence < CONFIDENCE_THRESHOLD:
                        name = label_dict.get(id_, "Unknown")
                        stats["recognized"] += 1
                    else:
                        name = "Unknown"
                        stats["unknown"] += 1

                    frame = draw_liveness_result(
                        frame, x, y, w, h,
                        name=name, confidence=confidence,
                        is_real=True, state=current_state,
                        avg_ear=debug_val, message=message,
                    )

        # HUD
        draw_hud(frame, fps, liveness_on, current_state, stats)
        cv2.imshow("Nhan Dien Khuon Mat - Chop mat de xac thuc", frame)

        # Phím tắt
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            print("\n[Thoat] Dang dong...")
            break
        elif key in (ord("l"), ord("L")):
            liveness_on = not liveness_on
            detector.reset()
            current_state = "WAITING"
            print(f"[Liveness] {'BAT' if liveness_on else 'TAT'}")
        elif key in (ord("r"), ord("R")):
            detector.reset()
            current_state = "WAITING"
            print("[Reset] Yeu cau chop mat lai")

except KeyboardInterrupt:
    print("\n[Ngat] Nguoi dung dung chuong trinh")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("\n" + "=" * 55)
    print("THONG KE:")
    print(f"  * Nhan dien thanh cong : {stats['recognized']}")
    print(f"  * Unknown              : {stats['unknown']}")
    print(f"  * Bi chan (chop mat)   : {stats['blocked']}")
    print("=" * 55)
    print("[OK] Da dong camera")