from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2, os, threading, time, json, threading, atexit, psutil
import numpy as np
from collections import deque

#-------CPU 모니터링---------
cpu_samples = []  # {"time": ..., "cpu": ...} 형태를 저장할 리스트
start_time = time.time()

def monitor_cpu():
    while True:
        # 1초 간격으로 CPU 사용률을 측정
        usage = psutil.cpu_percent(interval=1.0)
        elapsed = time.time() - start_time
        cpu_samples.append({"time": elapsed, "cpu": usage})

threading.Thread(target=monitor_cpu, daemon=True).start()

@atexit.register
def save_cpu_log():
    elapsed_time = time.time() - start_time  # 총 실행 시간(초)
   
    if len(cpu_samples) > 0:
        # 모든 cpu 값 합계
        total_cpu_usage = sum(sample["cpu"] for sample in cpu_samples)
        # "cpu 값 모두 더한 것 ÷ 실행 시간(초)" --> 사용자 요청대로 구간 평균
        average_cpu_usage = total_cpu_usage / elapsed_time

        # 가장 높았던/낮았던 CPU 사용률
        max_cpu_usage = max(sample["cpu"] for sample in cpu_samples)
        min_cpu_usage = min(sample["cpu"] for sample in cpu_samples)
    else:
        # 샘플이 한 개도 없을 경우(프로그램이 매우 빨리 종료될 때) 대비
        average_cpu_usage = 0
        max_cpu_usage = 0
        min_cpu_usage = 0
        total_cpu_usage = 0

    # 최종으로 JSON에 저장할 데이터 구조 (샘플 목록은 제외)
    result_data = {
        "elapsed_time_seconds": elapsed_time,
        "average_cpu_usage": average_cpu_usage,  # 전체 구간 평균
        "max_cpu_usage": max_cpu_usage,          # 최고 CPU
        "min_cpu_usage": min_cpu_usage,           # 최저 CPU
        "total_cpu_usage" : total_cpu_usage
    }

    # cpu_usage_log.json 파일로 저장
    with open("cpu_usage_log.json", "w") as f:
        json.dump(result_data, f, indent=4)

# --------------------------------------------------------------

app = FastAPI()

# 웹캠 연결
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
cap.set(cv2.CAP_PROP_FPS, 5)

# 녹화 설정
video_writer = None
frame_rate = 5
is_recording = False
last_frame = None
lock = threading.Lock()

# 이벤트 감지용
pre_event_frames = deque(maxlen=frame_rate * 10) # 이벤트 전 10초 프레임 저장
post_event_frames = frame_rate * 3 # 이벤트 이후 프레임 저장장

# 히트맵 누적 관련 변수
motion_heatmap = None # 변화가 누적되는 이미지
heatmap_threshold = 255 * 1000 # 이벤트 발생 기준값, 더 커야 이벤트로 감지됨됨
decay_rate = 0.9 # 히트맵 감쇠율

# 모션 지속 체크용 변수수 
motion_duration_counter = 0 # 변화가 지속된 프레임 수
motion_trigger_min_duration = frame_rate * 2 # 2초 이상 지속 시 이벤트 감지
motion_start_time = None
record_ready = False # 녹회 시작 조건(2초 이상 모션 지속) 충족 여부
post_record_counter = 0 # 후처리 프레임 카운터터

# 저장 디렉토리 설정
SAVE_DIR = "recorded_videos"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR, exist_ok=True)

# 모션 감지 함수
def detect_changes(frame):
    global last_frame, motion_heatmap

    # 현재 프레임의 노이즈 제거거
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # 첫 프레임이라면 초기화
    if last_frame is None:
        last_frame = gray_frame
        motion_heatmap = np.zeros_like(gray_frame, dtype=np.float32)
        return False

    # 이전 프레임과 차이 계산
    frame_diff = cv2.absdiff(last_frame, gray_frame)
    _, threshold_diff = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # 현재 프레임을 다음 비교용으로 저장
    last_frame = gray_frame

    # 히트맵 누적(감쇠 적용 + 현재 변화 누적적)
    motion_heatmap = motion_heatmap * decay_rate + threshold_diff.astype(np.float32)
    # 전체 변화량 계산
    heat_score = np.sum(motion_heatmap)

    # 기준 초과 시 모션 감지로 간주주
    return heat_score > heatmap_threshold

# 녹화 시작 함수
def start_recording():
    # 파일 이름은 현재 시간 기반으로 설정정
    global video_writer, is_recording, motion_start_time
    filename = os.path.join(SAVE_DIR, f"event_{time.strftime('%Y%m%d_%H%M%S')}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 또는 'MJPG'

    
    # 프레임 사이즈 결정 (사전 프레임이 있다면 그것을 기준준)
    if pre_event_frames:
        height, width, _ = pre_event_frames[0][1].shape
    else:
        ret, frame = cap.read()
        if not ret:
            return
        height, width, _ = frame.shape

    # 녹화 시작
    with lock:
        video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height))
        is_recording = True
        print(f"녹화 시작: {filename}")

        # 이벤트 시간 기준으로 과거 3초 ~ 미래 2초 프레임 저장장
        from_ts = motion_start_time - 3
        to_ts = motion_start_time + 2

        for ts, frame in pre_event_frames:
            if from_ts <= ts <= to_ts:
                video_writer.write(frame)

# 녹화 종료 함수
def stop_recording():
    global video_writer, is_recording
    with lock:
        if video_writer:
            video_writer.release()
            video_writer = None
            is_recording = False
            print("녹화 종료")

# 영상 프레임 생성 및 처리 (스트리밍 + 이벤트 감지지)
def generate_frames():
    global is_recording, motion_duration_counter, record_ready, motion_start_time, post_record_counter

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time() # 현재 시간
        pre_event_frames.append((now, frame.copy())) # 사전 버퍼에 저장

        change_detected = detect_changes(frame) # 모션 감지

        # 히트맵 시각화용 이미지 생성성
        heatmap_display = cv2.convertScaleAbs(motion_heatmap)
        colored_heatmap = cv2.applyColorMap(heatmap_display, cv2.COLORMAP_JET)
        
        # 원본 영상과 히트맵을 좌우로 붙여 스트리밍
        combined = cv2.hconcat([frame, colored_heatmap])


        # 변화가 감지된 경우우
        if change_detected:
            if motion_duration_counter == 0:
                motion_start_time = now
            motion_duration_counter += 1
            post_record_counter = 0

            # 지속 시간이 설정 이상이면(2초 이상 모션 감지) 녹화 준비
            if not is_recording and motion_duration_counter >= motion_trigger_min_duration:
                record_ready = True
            
            # 녹화 조건 충족 시 녹화 시작작
            if record_ready:
                start_recording()
                record_ready = False

            # 녹화 중이면 현재 프레임 저장장
            if is_recording:
                with lock:
                    video_writer.write(frame)

        else:
            # 변화가 사라졌다면 초기화화
            if not is_recording:
                motion_duration_counter = 0
                record_ready = False

            # 녹화 중이면 후처리 프레임 저장장
            if is_recording:
                if post_record_counter < post_event_frames:
                    with lock:
                        video_writer.write(frame)
                    post_record_counter += 1
                else:
                    stop_recording()
                    post_record_counter = 0

        # 스트리밍을 위한 프레임 인코딩 및 전송송
        _, buffer = cv2.imencode('.jpg', combined)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

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
