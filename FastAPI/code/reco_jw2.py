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
lock = threading.Lock()

# 이벤트 감지용
pre_event_frames = deque(maxlen=frame_rate * 10)
post_event_frames = frame_rate * 3

# 히트맵 관련
motion_heatmap = None
heatmap_threshold = 255 * 1000
decay_rate = 0.9

# 모션 감지 상태 변수
motion_duration_counter = 0
motion_trigger_min_duration = frame_rate * 2
motion_start_time = None
record_ready = False
post_record_counter = 0

# 저장 디렉토리
SAVE_DIR = "recorded_videos"
os.makedirs(SAVE_DIR, exist_ok=True)


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

    motion_heatmap[:] = motion_heatmap * decay_rate + threshold_diff.astype(np.float32)
    heat_score = np.sum(motion_heatmap)

    return heat_score > heatmap_threshold


def start_recording():
    global video_writer, is_recording, motion_start_time
    filename = os.path.join(SAVE_DIR, f"event_{time.strftime('%Y%m%d_%H%M%S')}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    if pre_event_frames:
        height, width, _ = pre_event_frames[0][1].shape
    else:
        ret, frame = cap.read()
        if not ret:
            return
        height, width, _ = frame.shape

    with lock:
        video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height))
        is_recording = True
        print(f"[REC] 시작: {filename}")

        from_ts = motion_start_time - 3
        to_ts = motion_start_time + 2

        for ts, frame in pre_event_frames:
            if from_ts <= ts <= to_ts:
                video_writer.write(frame)


def stop_recording():
    global video_writer, is_recording
    with lock:
        if video_writer:
            video_writer.release()
            video_writer = None
            is_recording = False
            print("[REC] 종료")


# 🎥 모션 감지 및 녹화는 별도 스레드에서 실행
def motion_detection_thread():
    global is_recording, motion_duration_counter, record_ready, motion_start_time, post_record_counter

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        now = time.time()
        pre_event_frames.append((now, frame.copy()))

        change_detected = detect_changes(frame)

        if change_detected:
            if motion_duration_counter == 0:
                motion_start_time = now
            motion_duration_counter += 1
            post_record_counter = 0

            if not is_recording and motion_duration_counter >= motion_trigger_min_duration:
                record_ready = True

            if record_ready:
                start_recording()
                record_ready = False

            if is_recording:
                with lock:
                    video_writer.write(frame)

        else:
            if not is_recording:
                motion_duration_counter = 0
                record_ready = False

            if is_recording:
                if post_record_counter < post_event_frames:
                    with lock:
                        video_writer.write(frame)
                    post_record_counter += 1
                else:
                    stop_recording()
                    post_record_counter = 0

        time.sleep(1 / frame_rate)


# 📡 스트리밍 전용 (모션 감지는 안함)
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        heatmap_display = cv2.convertScaleAbs(motion_heatmap)
        colored_heatmap = cv2.applyColorMap(heatmap_display, cv2.COLORMAP_JET)
        combined = cv2.hconcat([frame, colored_heatmap])

        _, buffer = cv2.imencode('.jpg', combined)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


# 스트리밍 API
@app.get("/video")
async def video():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


# HTML 페이지 API
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


# 앱 시작 시 모션 감지 스레드 시작
@app.on_event("startup")
def start_motion_detection_thread():
    print("🔄 백그라운드 모션 감지 스레드 실행 중...")
    threading.Thread(target=motion_detection_thread, daemon=True).start()
