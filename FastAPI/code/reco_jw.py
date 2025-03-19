from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2
import threading
import time
import os
import numpy as np
from collections import deque

app = FastAPI()

# 카메라 설정 (Raspberry Pi 최적화)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# 녹화 설정
video_writer = None
frame_rate = 30
is_recording = False
last_frame = None
no_change_counter = 0
no_change_limit = frame_rate * 3  # 3초 이상 변화 없으면 종료
lock = threading.Lock()

# 이벤트 감지 및 WebSocket 전송용
event_detected = False
pre_event_frames = deque(maxlen=frame_rate * 3)  # 이벤트 발생 전 3초치 프레임 저장
post_event_frames = frame_rate * 3  # 이벤트 종료 후 3초 추가 녹화

# 저장 디렉토리 설정
SAVE_DIR = "recorded_videos"
os.makedirs(SAVE_DIR, exist_ok=True)

# WebSocket 연결 관리
websocket_clients = set()

# 모션 감지 함수
def detect_changes(frame):
    global last_frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if last_frame is None:
        last_frame = gray_frame
        return False

    frame_diff = cv2.absdiff(last_frame, gray_frame)
    _, threshold_diff = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    last_frame = gray_frame

    for contour in contours:
        if cv2.contourArea(contour) > 1000:
            return True
    return False

# 녹화 시작 함수 (이전 프레임도 함께 저장)
def start_recording():
    global video_writer, is_recording
    filename = os.path.join(SAVE_DIR, f"event_{time.strftime('%Y%m%d_%H%M%S')}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # 첫 번째 프레임 해상도 가져오기
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

        # 이벤트 발생 전 프레임을 먼저 저장
        while pre_event_frames:
            video_writer.write(pre_event_frames.popleft())

# 녹화 종료 함수 (종료 후 3초 추가 녹화)
def stop_recording():
    global video_writer, is_recording
    with lock:
        if video_writer:
            # 🚀 이벤트 종료 후 3초 추가 녹화
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
    global is_recording, no_change_counter, event_detected

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 이전 3초 프레임 저장
        pre_event_frames.append(frame)

        if detect_changes(frame):
            no_change_counter = 0
            event_detected = True

            if not is_recording:
                start_recording()

            with lock:
                if video_writer:
                    video_writer.write(frame)

        else:
            if is_recording:
                no_change_counter += 1
                if no_change_counter > no_change_limit:
                    stop_recording()

        # 프레임 인코딩 후 전송
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# WebSocket으로 이벤트 알림 전송
async def event_notification():
    global event_detected
    while True:
        if event_detected:
            for client in websocket_clients:
                await client.send_text("이벤트 감지됨!")
            event_detected = False
        time.sleep(1)

# 스트리밍 라우트
@app.get("/video")
async def video():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# WebSocket 라우트 (이벤트 감지)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        pass
    finally:
        websocket_clients.remove(websocket)

# HTML 페이지 라우트
@app.get("/")
async def get():
    html_content = """
    <html>
        <head>
            <title>Live Stream</title>
            <script>
                let ws = new WebSocket("ws://" + window.location.host + "/ws");
                ws.onmessage = function(event) { alert(event.data); };
            </script>
        </head>
        <body>
            <h1>Live Stream</h1>
            <img src="/video" width="400">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# WebSocket 알림 스레드 시작
import asyncio
threading.Thread(target=lambda: asyncio.run(event_notification()), daemon=True).start()
