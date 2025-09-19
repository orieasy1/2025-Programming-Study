from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2
from collections import deque
import time

### 이벤트 발생 frame 3초 전 ~ 이벤트 종료 frame 3초 후후까지 녹화

app = FastAPI()

# 웹캠 연결
cap = cv2.VideoCapture(0)  # 기본 웹캠 (0번 포트 사용)

# 카메라 설정 (Raspberry Pi 최적화)
# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

video_writer = None # 녹화 객체
last_frame = None   # 이전 프레임 (변화 감지용)
frame_rate = 30     # 초당 프레임 수

is_recording = False # 녹화 중인지 판단
no_change_counter = 0
no_change_limit = frame_rate * 3 # 3초 (30프레임) 이상 변화 없으면 녹화 종료


# 이벤트 전 3초 버퍼
pre_event_buffer = deque(maxlen=frame_rate * 3)

# 변화 감지 함수
def detect_changes(frame):
    global last_frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 흑백으로 변환
    gray_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0) # 노이즈 제거 효과: 조명 효과 감지 방지

    if last_frame is None:
        last_frame = gray_frame
        return False

    frame_diff = cv2.absdiff(last_frame, gray_frame)  # 프레임 차이 계산
    _, threshold_diff = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)  # 차이 임계값 설정

    # 변화가 있을 경우
    if cv2.countNonZero(threshold_diff) > 1000:  # 변화가 일정 이상 클 경우
        last_frame = gray_frame  # 마지막 프레임 업데이트
        return True
    last_frame = gray_frame # 변화가 없어도 마지막 프레임 업데이트는 해야함
    return False

# 영상 녹화 시작 함수
def start_video_writer(frame):
    global video_writer
    
    if video_writer is None: # 실제 저장 객체 생성하기
        fourcc = cv2.VideoWriter_fourcc(*'XVID') # 비디오 코덱 설정
        height, width, _ = frame.shape # 해상도 설정
        filename = f"output_{time.strftime('%Y%m%d_%H%M%S')}.avi"
        video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height)) # 최종 저장 객체

# 영상 녹화 함수
def record_video(frame):
    global video_writer

    if video_writer is not None:
        video_writer.write(frame)


# 영상 스트리밍과 녹화 종료를 위한 함수
def process_frame():
    global video_writer, is_recording, no_change_counter

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # pre_event_buffer에 이전 3초 계속 갱신 (FIFO 방식)
        ## 버퍼가 다 차지 않았을 때 녹화가 시작되는 경우 에러 발생.. 작동에는 문제 없으나 최적화 필요
        pre_event_buffer.append(frame.copy())

        if detect_changes(frame):  # 변화 감지
            no_change_counter = 0  # 변화 있으니 카운터 초기화

            if not is_recording:  # 녹화 시작
                print("녹화 시작")
                is_recording = True
                start_video_writer(frame)  # 프레임 저장

                # pre-event 버퍼 내용 먼저 저장
                for buffered_frame in pre_event_buffer:
                    record_video(buffered_frame)

            record_video(frame) # 일단 녹화가 시작되었으면 계속 녹화 해야함

        else:  # 변화 없음
            if is_recording:
                no_change_counter += 1

                record_video(frame)

                # 변화 없던 시간이 너무 길면 종료 (일단 3초로 설정)
                if no_change_counter > no_change_limit:
                    print("녹화 종료")
                    video_writer.write(frame) # 마지막 프레임 누락 방지
                    video_writer.release()
                    video_writer = None
                    is_recording = False
                    no_change_counter = 0

        # 스트리밍용
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 영상 스트리밍 라우트
@app.get("/video")
async def video():
    return StreamingResponse(process_frame(), media_type="multipart/x-mixed-replace; boundary=frame")

# HTML 페이지 라우트
@app.get("/")
async def get():
    html_content = """
    <html>
        <head>
            <title>Streaming...</title>
        </head>
        <body>
            <h1>Streaming...</h1>
            <img src="/video" width="300" height="200">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
