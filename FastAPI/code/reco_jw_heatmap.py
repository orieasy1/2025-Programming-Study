from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2
import threading
import time
import os
import numpy as np
from collections import deque

app = FastAPI()

# 웹캠 연결
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 녹화 설정
video_writer = None
frame_rate = 30
is_recording = False
last_frame = None
no_change_counter = 0
no_change_limit = frame_rate * 3
lock = threading.Lock()

# 이벤트 감지용
pre_event_frames = deque(maxlen=frame_rate * 6)  # 3초 전 + 2초 지속 + 1초 여유
post_event_frames = frame_rate * 3

# 히트맵 설정
motion_heatmap = None
heatmap_threshold = 255 * 1000
decay_rate = 0.9

# 지속적 변화 감지용
motion_duration_counter = 0
motion_trigger_min_duration = frame_rate * 2  # 2초 연속 변화 필요
record_ready = False

# 저장 디렉토리 설정
SAVE_DIR = "recorded_videos"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR, exist_ok=True)

# 모션 감지 함수 (히트맵 누적 방식)
def detect_changes(frame):
    global last_frame, motion_heatmap

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if last_frame is None:
        last_frame = gray_frame
        motion_heatmap = np.zeros_like(gray_frame, dtype=np.float32)
        return False

    frame_diff = cv2.absdiff(last_frame, gray_frame)
    _, threshold_diff = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    last_frame = gray_frame

    motion_heatmap = motion_heatmap * decay_rate + threshold_diff.astype(np.float32)
    heat_score = np.sum(motion_heatmap)

    return heat_score > heatmap_threshold

def start_recording():
    global video_writer, is_recording
    filename = os.path.join(SAVE_DIR, f"event_{time.strftime('%Y%m%d_%H%M%S')}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    if pre_event_frames:
        height, width, _ = pre_event_frames[0].shape
    else:
        ret, frame = cap.read()
        if not ret:
            return
        height, width, _ = frame.shape

    with lock:
        video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height))
        is_recording = True
        print(f"녹화 시작: {filename}")

        if len(pre_event_frames) >= frame_rate * 5:
            buffer_list = list(pre_event_frames)[-frame_rate * 5:]  # 마지막 5초
        else:
            buffer_list = list(pre_event_frames)

        for frame in buffer_list:
            video_writer.write(frame)


# 녹화 종료 함수
def stop_recording():
    global video_writer, is_recording
    with lock:
        if video_writer:
            for _ in range(post_event_frames):
                ret, frame = cap.read()
                if not ret:
                    break
                video_writer.write(frame)
                time.sleep(1 / frame_rate)

            video_writer.release()
            video_writer = None
            is_recording = False
            print("녹화 종료")

# 영상 스트리밍 및 녹화 처리
def generate_frames():
    global is_recording, no_change_counter, motion_duration_counter, record_ready

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        pre_event_frames.append(frame.copy())

        change_detected = detect_changes(frame)

        # 히트맵 시각화
        heatmap_display = cv2.convertScaleAbs(motion_heatmap)
        colored_heatmap = cv2.applyColorMap(heatmap_display, cv2.COLORMAP_JET)
        combined = cv2.hconcat([frame, colored_heatmap])

        if change_detected:
            motion_duration_counter += 1

            if not is_recording and motion_duration_counter >= motion_trigger_min_duration:
                record_ready = True

            if record_ready:
                start_recording()
                record_ready = False

            if is_recording:
                with lock:
                    video_writer.write(frame)

            no_change_counter = 0
        else:
            if not is_recording:
                motion_duration_counter = 0
                record_ready = False
            if is_recording:
                no_change_counter += 1
                with lock:
                    video_writer.write(frame)
                if no_change_counter > no_change_limit:
                    stop_recording()

        _, buffer = cv2.imencode('.jpg', combined)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 스트리밍 라우트
@app.get("/video")
async def video():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# HTML 페이지 라우트
@app.get("/")
async def get():
    html_content = """
    <html>
        <head>
            <title>Live Stream with Heatmap</title>
        </head>
        <body>
            <h1>Live Stream + Heatmap</h1>
            <img src="/video" width="800">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
