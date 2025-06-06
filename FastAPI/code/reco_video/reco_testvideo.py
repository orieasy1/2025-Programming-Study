import cv2
import os
import time
import numpy as np
from datetime import datetime
from collections import deque

# --------- 설정 ---------
input_folder = "./reco_testvideo"
output_folder = "./recorded_testvideos"
os.makedirs(output_folder, exist_ok=True)

frame_rate = 30
buffer_seconds = 3
buffer_size = frame_rate * buffer_seconds
contour_area_threshold = 800
threshold_value = 40
frame_width, frame_height = 1280, 720

# --------- 전역 변수 ---------
video_writer = None
is_recording = False
pre_event_frames = deque(maxlen=frame_rate * 10)
motion_heatmap = None
decay_rate = 0.9
heatmap_threshold = 255 * 2000
motion_start_time = None
post_recording_end_time = None
last_frame = None

# --------- 모션 감지 함수 ---------
def detect_changes(frame):
    global last_frame, motion_heatmap
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if last_frame is None:
        last_frame = gray
        motion_heatmap = np.zeros_like(gray, dtype=np.float32)
        return False

    frame_diff = cv2.absdiff(last_frame, gray)
    _, threshold_diff = cv2.threshold(frame_diff, threshold_value, 255, cv2.THRESH_BINARY)
    motion_heatmap[:] = motion_heatmap * decay_rate + threshold_diff.astype(np.float32)
    last_frame = gray

    return np.sum(motion_heatmap) > heatmap_threshold

# --------- 녹화 시작 함수 ---------
def start_recording(filename_prefix):
    global video_writer, is_recording, motion_start_time
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_folder, f"{filename_prefix}_{timestamp}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    height, width, _ = pre_event_frames[0][1].shape
    video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height))
    is_recording = True
    print(f"[녹화 시작] {filename}")

    for _, frame in list(pre_event_frames)[-frame_rate * 3:]:
        video_writer.write(frame)

# --------- 녹화 종료 함수 ---------
def stop_recording():
    global video_writer, is_recording
    if video_writer:
        video_writer.release()
        video_writer = None
    if is_recording:
        print("[녹화 종료]")
    is_recording = False

# --------- 비디오 파일 처리 함수 ---------
def process_video(video_path):
    global is_recording, motion_start_time, post_recording_end_time, last_frame
    filename_prefix = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_index = 0
    progress_checkpoint = 0
    last_frame = None
    post_recording_end_time = None
    motion_start_time = None

    print(f"\n[INFO] 처리 시작: {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_progress = (frame_index / total_frames) * 100
        if total_frames > 0 and current_progress >= progress_checkpoint:
            print(f"  ▶ 진행률: ({current_progress:.2f}%)")
            progress_checkpoint += 10

        frame = cv2.resize(frame, (frame_width, frame_height))
        now = time.time()
        pre_event_frames.append((now, frame.copy()))
        change_detected = detect_changes(frame)

        if is_recording:
            video_writer.write(frame)

        if change_detected:
            post_recording_end_time = None
            if not is_recording:
                motion_start_time = now
                start_recording(filename_prefix)
        else:
            if is_recording and post_recording_end_time is None:
                post_recording_end_time = now + 2
            if is_recording and post_recording_end_time and now >= post_recording_end_time:
                stop_recording()
                post_recording_end_time = None

        frame_index += 1

    cap.release()
    stop_recording()

# --------- 메인 실행 ---------
if __name__ == '__main__':
    video_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".mp4")])
    if not video_files:
        print("[WARN] 영상 파일이 없습니다.")
    for file in video_files:
        full_path = os.path.join(input_folder, file)
        process_video(full_path)

    print("\n✅ 모든 영상 처리 완료!")
