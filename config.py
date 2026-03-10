# Configuration file - Face Recognition + Active Liveness v3

# =============================================
# Data Collection & Training
# =============================================
TOTAL_IMAGES   = 100
DATASET_PATH   = "dataset"
FRAME_SKIP     = 2
TRAINER_PATH   = "trainer"
MODEL_FILENAME = "model.yml"
LABELS_FILENAME= "labels.npy"

# =============================================
# Recognition
# =============================================
CONFIDENCE_THRESHOLD = 80    # < 80 = recognized, >= 80 = unknown
CAMERA_INDEX         = 0

# =============================================
# Face Detection
# =============================================
SCALE_FACTOR  = 1.3
MIN_NEIGHBORS = 5

# =============================================
# Colors (BGR)
# =============================================
COLOR_RECOGNIZED = (0, 255, 0)    # Xanh la
COLOR_UNKNOWN    = (0, 0, 255)    # Do
COLOR_WAITING    = (0, 200, 255)  # Vang cam (chua chop mat)
COLOR_TEXT       = (255, 255, 255)

# =============================================
# Active Liveness (Blink Detection)
# =============================================

# Bat / Tat yeu cau chop mat
# True  = Bat: Phai chop mat moi nhan dien duoc
# False = Tat: Nhan dien truc tiep khong can chop mat
LIVENESS_ENABLED = True

# -------------------------------------------
# EAR (Eye Aspect Ratio) Settings
# -------------------------------------------
# Nguong EAR: duoi nguong nay = mat dang nhac
# 0.22 = thong thuong | 0.20 = chat hon | 0.25 = de hon
EAR_THRESHOLD = 0.22

# So frame mat phai nhac LIEN TUC de tinh la chop mat hop le
# 1 frame = ok tu nhien | 2 = an toan hon khoi false positive
BLINK_MIN_FRAMES = 1

# So frame mat nhac TOI DA (han che viec nhan mat co tinh)
# 10 frame ~ 0.33 giay (o 30fps)
BLINK_MAX_FRAMES = 10

# So frame khong thay mat -> reset trang thai (yeu cau chop mat lai)
NO_FACE_RESET_FRAMES = 20

# =============================================
# UI
# =============================================
SHOW_FPS = True
LOG_LEVEL = 1

# =============================================
# Keys
# =============================================
KEY_CAPTURE = 32   # SPACE
KEY_EXIT    = 27   # ESC

"""
Huong dan chinh calibration:

1. Neu khong chop mat duoc (EAR khong xuong du thap):
   - Giam EAR_THRESHOLD xuong 0.18 hoac 0.15
   - Kiem tra lai duoi EAR: show trong HUD

2. Neu chop mat gia qua de (tay run / phong thieu sang):
   - Tang BLINK_MIN_FRAMES len 2 hoac 3
   - Tang EAR_THRESHOLD len 0.25

3. Reset yeu cau chop mat: Nhan phim R
"""
