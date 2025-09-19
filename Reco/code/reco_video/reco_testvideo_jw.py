import cv2
import os
import time
import numpy as np
from datetime import datetime
from collections import deque

# 입력/출력 폴더 경로 설정
input_folder = "./reco_testvideo"  # 처리할 비디오 파일이 저장된 폴더
output_folder = "./recorded_testvideos"  # 모션 감지된 영상을 저장할 폴더
os.makedirs(output_folder, exist_ok=True)  # 출력 폴더가 없으면 생성

# 기본 설정
frame_rate = 30  # 초당 프레임 수 (FPS)
buffer_seconds = 3  # 모션 발생 전 저장할 버퍼 시간 (초)
buffer_size = frame_rate * buffer_seconds  # 버퍼 프레임 수
contour_area_threshold = 800  # (사용되지 않음) 윤곽선 면적 임계값
threshold_value = 40  # 프레임 차이를 감지하기 위한 이진화 임계값
frame_width, frame_height = 1280, 720  # 프레임 해상도

# 녹화 상태 관련 전역 변수들
video_writer = None
is_recording = False
lock = None  # (사용되지 않음, 멀티스레드 환경에서 필요할 수 있음)
pre_event_frames = deque(maxlen=frame_rate * 10)  # 모션 전 최근 프레임을 저장하는 버퍼
motion_heatmap = None  # 누적된 움직임 정보를 저장하는 히트맵
decay_rate = 0.9  # 이전 움직임 정보를 서서히 감소시키는 계수
heatmap_threshold = 255 * 2000  # 누적 히트맵 합이 이 값을 넘으면 모션으로 판단
motion_start_time = None
post_recording_end_time = None
last_frame = None  # 이전 프레임(회색조) 저장용

# --- 움직임 감지 함수 ---
def detect_changes(frame):
    """
    현재 프레임과 이전 프레임 간의 차이를 이용하여 움직임을 감지.
    누적 히트맵을 사용하여 지속적인 움직임만 녹화 대상으로 판단.
    """
    global last_frame, motion_heatmap

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # 노이즈 제거용 블러

    if last_frame is None:
        # 첫 프레임 초기화
        last_frame = gray
        motion_heatmap = np.zeros_like(gray, dtype=np.float32)
        return False

    frame_diff = cv2.absdiff(last_frame, gray)  # 현재 프레임과 이전 프레임 차이 계산
    _, threshold_diff = cv2.threshold(frame_diff, threshold_value, 255, cv2.THRESH_BINARY)  # 움직임 영역 이진화

    # 히트맵 누적 (기존 값은 감쇠, 새로운 차이 정보 추가)
    motion_heatmap[:] = motion_heatmap * decay_rate + threshold_diff.astype(np.float32)

    last_frame = gray

    # 누적된 히트맵 값이 임계값을 넘으면 모션 발생으로 간주
    return np.sum(motion_heatmap) > heatmap_threshold

# --- 녹화 시작 함수 ---
def start_recording(filename_prefix):
    """
    비디오 파일 저장을 시작. 파일 이름은 prefix + 현재시간으로 구성.
    모션 감지 이전의 버퍼 프레임 일부를 함께 저장.
    """
    global video_writer, is_recording, motion_start_time

    filename = os.path.join(output_folder, f"{filename_prefix}_{time.strftime('%Y%m%d_%H%M%S')}.avi")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 코덱 설정

    height, width, _ = pre_event_frames[0][1].shape  # 프레임 해상도 추출
    video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (width, height))
    is_recording = True
    print(f"[녹화 시작] {filename}")

    # 녹화 시작 시점 기준 과거 몇 초(기본 3초)의 프레임을 미리 저장
    for _, frame in list(pre_event_frames)[-frame_rate * 3:]:
        video_writer.write(frame)

# --- 녹화 종료 함수 ---
def stop_recording():
    """
    비디오 녹화를 종료하고 파일 저장을 마무리함.
    """
    global video_writer, is_recording

    if video_writer:
        video_writer.release()  # 파일 저장 종료
        video_writer = None
    if is_recording:
        print("[녹화 종료]")
    is_recording = False

# --- 개별 비디오 파일 처리 함수 ---
def process_video(video_path):
    """
    입력 비디오 파일을 열고, 프레임을 순차적으로 읽으면서 모션을 감지하고 녹화함.
    """
    global is_recording, motion_start_time, post_recording_end_time, last_frame

    filename_prefix = os.path.splitext(os.path.basename(video_path))[0]
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 총 프레임 수

    frame_index = 0
    progress_checkpoint = 0  # 10% 단위 진행률 출력용
    last_frame = None  # 초기화
    post_recording_end_time = None
    motion_start_time = None

    print(f"\n[INFO] 처리 시작: {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 영상 끝

        # 진행률 출력
        current_progress = (frame_index / total_frames) * 100
        if total_frames > 0 and current_progress >= progress_checkpoint:
            print(f"  ▶ 진행률: ({current_progress:.2f}%)")
            progress_checkpoint += 10

        # 프레임 리사이즈 및 복사 저장
        frame = cv2.resize(frame, (frame_width, frame_height))
        now = time.time()
        pre_event_frames.append((now, frame.copy()))

        # 움직임 감지
        change_detected = detect_changes(frame)

        if is_recording:
            video_writer.write(frame)

        if change_detected:
            # 움직임이 계속되면 녹화 연장
            post_recording_end_time = None
            if not is_recording:
                motion_start_time = now
                start_recording(filename_prefix)
        else:
            # 움직임이 멈췄을 경우, 녹화를 2초 후에 종료
            if is_recording and post_recording_end_time is None:
                post_recording_end_time = now + 2
            if is_recording and post_recording_end_time and now >= post_recording_end_time:
                stop_recording()
                post_recording_end_time = None

        frame_index += 1

    # 모든 프레임 처리 후 종료 처리
    cap.release()
    stop_recording()

# --- 메인 루프 ---
if __name__ == '__main__':
    # 입력 폴더 내의 mp4 파일 목록 정렬
    video_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".mp4")])
    if not video_files:
        print("[WARN] 영상 파일이 없습니다.")
    for file in video_files:
        full_path = os.path.join(input_folder, file)
        process_video(full_path)

    print("\n모든 영상 처리 완료!")
