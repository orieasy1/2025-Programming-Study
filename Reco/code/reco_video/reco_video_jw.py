import cv2, os, threading, time, json
from collections import deque


# ---------- 영상 관련 초기화 ----------
video_path = "./reco_video/V1(Event).mp4"
cap = cv2.VideoCapture(video_path)
frame_rate = 30

video_writer = None
is_recording = False
last_frame = None
motion_heatmap = None
heatmap_threshold = 255 * 2000
decay_rate = 0.9

motion_start_time = None
post_recording_end_time = None
pre_event_frames = deque(maxlen=frame_rate * 10)

SAVE_DIR = "recorded_videos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------- 모션 감지 ----------
def detect_changes(frame):
    global last_frame, motion_heatmap
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if last_frame is None:
        last_frame = gray
        motion_heatmap = np.zeros_like(gray, dtype=np.float32)
        return False

    diff = cv2.absdiff(last_frame, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    last_frame = gray

    motion_heatmap[:] = motion_heatmap * decay_rate + thresh.astype(np.float32)
    heat_score = np.sum(motion_heatmap)

    return heat_score > heatmap_threshold

# ---------- 녹화 시작/종료 ----------
def start_recording():
    global video_writer, is_recording, motion_start_time
    filename = os.path.join(SAVE_DIR, f"event_{time.strftime('%Y%m%d_%H%M%S')}.avi")
    if pre_event_frames:
        h, w, _ = pre_event_frames[0][1].shape
    else:
        ret, f = cap.read()
        if not ret: return
        h, w, _ = f.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(filename, fourcc, frame_rate, (w, h))
    is_recording = True
    motion_start_time = time.time()
    print(f"녹화 시작: {filename}")
    for _, f in list(pre_event_frames)[-frame_rate * 3:]:
        video_writer.write(f)

def stop_recording():
    global video_writer, is_recording
    if video_writer:
        video_writer.release()
        video_writer = None
        is_recording = False
        print("녹화 종료")

# ---------- 메인 루프 ----------
def main():
    global is_recording, post_recording_end_time

    while True:
        ret, frame = cap.read()
        if not ret:
            print("영상 종료")
            stop_recording()
            break

        now = time.time()
        pre_event_frames.append((now, frame.copy()))

        change_detected = detect_changes(frame)

        if is_recording:
            video_writer.write(frame)

        heatmap_display = cv2.convertScaleAbs(motion_heatmap)
        heatmap_color = cv2.applyColorMap(heatmap_display, cv2.COLORMAP_JET)
        combined = cv2.hconcat([frame, heatmap_color])
        cv2.imshow("Motion Detection + Heatmap", combined)

        if change_detected:
            post_recording_end_time = None
            if not is_recording:
                start_recording()
        else:
            if is_recording and post_recording_end_time is None:
                post_recording_end_time = now + 2
            if is_recording and post_recording_end_time and now >= post_recording_end_time:
                stop_recording()
                post_recording_end_time = None

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("사용자 종료")
            stop_recording()
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
