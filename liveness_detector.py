"""
Liveness Detector v3 - Active Liveness: Blink Detection (Pure OpenCV)
======================================================================
Phương pháp: Phát hiện chớp mắt bằng OpenCV Haar Cascade (KHÔNG cần mediapipe).

Nguyên lý:
  - Dùng haarcascade_eye_tree_eyeglasses.xml (hoạt động với cả kính mắt).
  - Theo dõi vùng mắt trên khuôn mặt.
  - Khi mắt biến mất rồi xuất hiện lại → Đã chớp mắt → Xác thực REAL.
  - Ảnh tĩnh mắt mở: cascade luôn thấy mắt → không bao giờ chớp → BLOCKED.
  - Ảnh tĩnh mắt nhắm: không bao giờ mở ra → không bao giờ pass.

Trạng thái:
  WAITING  → Yêu cầu chớp mắt (box vàng)
  VERIFIED → Đã xác thực, nhận diện bình thường (box xanh)
"""

import cv2
import numpy as np
from collections import deque


class LivenessDetector:
    """
    Blink Detector chỉ dùng OpenCV (không phụ thuộc mediapipe).
    """

    STATE_WAITING  = "WAITING"
    STATE_VERIFIED = "VERIFIED"

    def __init__(
        self,
        ear_threshold: float = 0.22,    # Không dùng, giữ để tương thích config
        blink_min_frames: int = 1,      # Frame mắt "biến mất" tối thiểu
        blink_max_frames: int = 12,     # Frame mắt "biến mất" tối đa (quá nhiều → không tính)
        no_face_reset: int = 20,        # Frame không thấy mặt → reset
    ):
        self.blink_min_frames = blink_min_frames
        self.blink_max_frames = blink_max_frames
        self.no_face_reset    = no_face_reset

        # Eye cascade - hoạt động tốt với kính mắt
        self._eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"
        )
        if self._eye_cascade.empty():
            # Fallback sang cascade cơ bản
            self._eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_eye.xml"
            )

        # State machine
        self._state           = self.STATE_WAITING
        self._eye_gone_frames = 0     # Số frame mắt đang "biến mất" liên tiếp
        self._no_face_frames  = 0

        # Smoothing: buffer 3 frame để lọc false negative
        self._eye_visible_buf: deque = deque([True, True, True], maxlen=3)

    # ──────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────

    def process(
        self,
        frame_bgr: np.ndarray,
        face_box: tuple[int, int, int, int] | None = None,
    ) -> tuple[bool, str, float, str]:
        """
        Phân tích frame, phát hiện chớp mắt.

        Args:
            frame_bgr : Frame đầy đủ BGR từ camera.
            face_box  : (x, y, w, h) vùng mặt từ Haar Cascade. Nếu None = không thấy mặt.

        Returns:
            is_real  (bool)  : True = đã xác thực
            state    (str)   : "WAITING" / "VERIFIED"
            debug    (float) : Số mắt phát hiện được (dùng debug)
            message  (str)   : Thông báo cho UI
        """
        # ── Không có mặt ──────────────────────────────────────────────
        if face_box is None:
            self._no_face_frames += 1
            if self._no_face_frames >= self.no_face_reset:
                self.reset()
            return False, self._state, -1.0, "Khong thay khuon mat"

        self._no_face_frames = 0

        # ── Đã xác thực rồi ───────────────────────────────────────────
        if self._state == self.STATE_VERIFIED:
            return True, self._state, 1.0, "Da xac thuc!"

        # ── Cắt vùng mặt, lấy phần trên (vùng mắt) ───────────────────
        x, y, w, h = face_box
        # Đảm bảo không vượt biên frame
        fh, fw = frame_bgr.shape[:2]
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(fw, x + w), min(fh, y + h)

        face_bgr  = frame_bgr[y1:y2, x1:x2]
        face_gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(face_gray, face_gray)

        fh2, fw2 = face_gray.shape
        # Chỉ lấy phần trên 55% của khuôn mặt (vùng mắt)
        eye_roi = face_gray[max(0, fh2 // 7) : int(fh2 * 0.55), :]

        # ── Phát hiện mắt ─────────────────────────────────────────────
        eyes = self._eye_cascade.detectMultiScale(
            eye_roi,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(int(fw2 * 0.10), int(fw2 * 0.06)),
        )
        eyes_visible = len(eyes) > 0

        # Smoothing: mắt coi là "có" nếu ít nhất 1/3 frame gần nhất thấy được
        self._eye_visible_buf.append(eyes_visible)
        smoothed_visible = sum(self._eye_visible_buf) >= 1

        # ── State machine chớp mắt ────────────────────────────────────
        if not smoothed_visible:
            self._eye_gone_frames += 1
        else:
            if self.blink_min_frames <= self._eye_gone_frames <= self.blink_max_frames:
                # Mắt biến mất đủ lâu rồi xuất hiện lại → BLINK ✅
                self._state          = self.STATE_VERIFIED
                self._eye_gone_frames = 0
                return True, self._state, float(len(eyes)), "Da xac thuc!"
            # Chuyển về 0 kể cả khi không hợp lệ
            self._eye_gone_frames = 0

        debug_val = float(len(eyes))
        msg = f"Vui long CHOP MAT (mat:{int(debug_val)})"
        return False, self._state, debug_val, msg

    def reset(self):
        """Reset trạng thái về WAITING."""
        self._state           = self.STATE_WAITING
        self._eye_gone_frames = 0
        self._no_face_frames  = 0
        self._eye_visible_buf = deque([True, True, True], maxlen=3)

    @property
    def is_verified(self) -> bool:
        return self._state == self.STATE_VERIFIED


# ──────────────────────────────────────────────────────────────────────
# Helper: Vẽ lên frame
# ──────────────────────────────────────────────────────────────────────

def draw_liveness_result(
    frame: np.ndarray,
    x: int, y: int, w: int, h: int,
    name: str,
    confidence: float,
    is_real: bool,
    state: str,
    avg_ear: float,
    message: str,
) -> np.ndarray:
    """
    Màu box:
      Xanh lá  → VERIFIED + nhận diện được
      Đỏ       → VERIFIED + Unknown
      Vàng cam → WAITING (chưa chớp mắt) → ảnh giả hoặc chưa xác thực
    """
    if not is_real:
        color = (0, 200, 255)    # Vàng cam
        label = "CHOP MAT!"
    elif confidence < 80:
        color = (0, 255, 0)      # Xanh lá
        label = name
    else:
        color = (0, 0, 255)      # Đỏ
        label = "Unknown"

    thickness = 3 if not is_real else 2
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

    # Label phía trên
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2)
    cv2.rectangle(frame, (x, y - th - 10), (x + tw + 6, y), color, -1)
    cv2.putText(frame, label, (x + 3, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

    # Sub-text
    if not is_real:
        cv2.putText(frame, message, (x, y + h + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, color, 1)
        if avg_ear >= 0:
            cv2.putText(frame, f"eyes:{int(avg_ear)}", (x, y + h + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (130, 130, 255), 1)
    else:
        cv2.putText(frame, f"Conf:{confidence:.1f}", (x, y + h + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, color, 1)

    return frame
