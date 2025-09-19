from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2, os, threading, time, json, atexit, psutil
import numpy as np
from collections import deque

app = FastAPI()

# ---------------- CPU 모니터링 ----------------
cpu_samples = []
start_time = time.time()

def monitor_cpu():
    while True:
        usage = psutil.cpu_percent(interval=1.0)
        elapsed = time.time() - start_time
        cpu_samples.append({"time": elapsed, "cpu": usage})

threading.Thread(target=monitor_cpu, daemon=True).start()

@atexit.register
def save_cpu_log():
    elapsed_time = time.time() - start_time
    if cpu_samples:
        total_cpu_usage = sum(sample["cpu"] for sample in cpu_samples)
        average_cpu_usage = total_cpu_usage / elapsed_time
        max_cpu_usage = max(sample["cpu"] for sample in cpu_samples)
        min_cpu_usage = min(sample["cpu"] for sample in cpu_samples)
    else:
        average_cpu_usage = max_cpu_usage = min_cpu_usage = total_cpu_usage = 0

    result_data = {
        "elapsed_time_seconds": elapsed_time,
        "average_cpu_usage": average_cpu_usage,
        "max_cpu_usage": max_cpu_usage,
        "min_cpu_usage": min_cpu_usage,
        "total_cpu_usage": total_cpu_usage
    }

    with open("cpu_usage_log.json", "w") as f:
        json.dump(result_data, f, indent=4)

# ---------------- 카메라 설정 ----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cap.set(cv2.CAP_PROP_FPS, 5)

# ---------------- 변수 초기화 ----------------
video_writer = None
frame_rate = 5
is_recording = False
last_frame = None
lock = threading.Lock()

pre_event_frames = deque(maxlen=frame_rate * 10)
post_event_frames = frame_rate * 3

motion_heatmap = None
heatmap_threshold = 255 * 1000
decay_rate = 0.9

motion_duration_counter = 0
motion_trigger_min_duration = frame_rate * 2
motion_start_time = None
record_ready = False
post_record_counter = 0

SAVE_DIR = "recorded_videos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------- 모션 감지 함수 ----------------
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

# ---------------- 녹화 제어 함수 ----------------
def start_recording():
    global video_writer, is_recording, motion_start_time
    filename = os.path.join(SAVE_DIR, f"event_{time.strftime('%Y%m%d_%H%M%S')}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

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
        print(f"[녹화 시작] {filename}")

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
            print("[녹화 종료]")

# ---------------- 감지 + 녹화 루프 ----------------
def detect_and_record():
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

# ---------------- 스트리밍 루프 ----------------
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        if motion_heatmap is None:
            continue

        heatmap_display = cv2.convertScaleAbs(motion_heatmap)
        colored_heatmap = cv2.applyColorMap(heatmap_display, cv2.COLORMAP_JET)
        combined = cv2.hconcat([frame, colored_heatmap])

        _, buffer = cv2.imencode('.jpg', combined)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        time.sleep(1 / frame_rate)

# ---------------- API 엔드포인트 ----------------
@app.get("/video")
async def video():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def root():
    html_content = """
    <html>
        <head><title>Live Stream + Heatmap</title></head>
        <body>
            <h2>📹 Live Stream with Motion Heatmap</h2>
            <img src="/video" width="800">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ---------------- 감지 스레드 시작 ----------------
threading.Thread(target=detect_and_record, daemon=True).start()
