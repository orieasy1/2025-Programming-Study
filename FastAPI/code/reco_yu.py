import cv2
import numpy as np
import time
import threading
import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from datetime import datetime
from collections import deque

app = FastAPI()

# **웹캠 설정 (HD 해상도 & 최적 FPS)**
video_source = 0
cap = cv2.VideoCapture(video_source)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 기존 1920 → 1280 (녹화 해상도와 통일)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 기존 1080 → 720
fps = 5  # FPS 유지

# **영상 저장 설정**
save_folder = "recorded_videos"
if not os.path.exists(save_folder):
    os.makedirs(save_folder, exist_ok=True)  # 저장 폴더 자동 생성

video_writer = None
recording = False
last_motion_time = None
previous_frame = None

# **움직임 감지 전후 3초 프레임 저장**
buffer_seconds = 3
frame_buffer = deque(maxlen=buffer_seconds * fps)

def detect_motion():
    global previous_frame, recording, video_writer, last_motion_time

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue  # 빈 프레임 발생 시 건너뜀

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if previous_frame is None:
            previous_frame = gray
            continue

        frame_delta = cv2.absdiff(previous_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        if np.sum(thresh) > 300000:  # 감지 민감도 조정
            last_motion_time = time.time()

            if not recording:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                video_filename = f"{save_folder}/{timestamp}.avi"  # 확장자 avi로 변경
                fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 'avc1' → 'XVID'
                video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (1280, 720))

                # **3초 전 영상 저장**
                for buffered_frame in frame_buffer:
                    video_writer.write(buffered_frame)

                print(f"[INFO] 녹화 시작: {video_filename}")
                recording = True

        else:
            if recording and (time.time() - last_motion_time > 3):
                print("[INFO] 녹화 중지")
                recording = False
                video_writer.release()
                video_writer = None

        if recording and video_writer is not None:
            video_writer.write(frame)

        frame_buffer.append(frame)
        previous_frame = gray
        time.sleep(1 / fps)

# **실시간 스트리밍 함수**
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue  # 빈 프레임 발생 시 건너뜀

        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])  # 화질 최적화
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/")
def index():
    return HTMLResponse("""
    <html>
        <head><title>Live Stream</title></head>
        <body>
            <h1>실시간 스트리밍</h1>
            <img src="/video_feed" width="640">
        </body>
    </html>
    """)

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/recorded_videos")
def list_videos():
    files = os.listdir(save_folder)
    return {"videos": files}

@app.get("/download_video/{filename}")
def download_video(filename: str):
    file_path = os.path.join(save_folder, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/avi", filename=filename)
    return {"error": "파일을 찾을 수 없습니다."}

motion_thread = threading.Thread(target=detect_motion, daemon=True)
motion_thread.start()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='192.168.137.84', port=8080)
