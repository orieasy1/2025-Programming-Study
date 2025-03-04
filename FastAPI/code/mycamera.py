import cv2
import io

def get_captured_picture():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("웹캠을 열 수 없습니다.")
        return
    
    success, frame = cam.read()
    cam.release()

    
    if not success:
        print("이미지를 캡처할 수 없습니다.")
        return None

    _, buffer = cv2.imencode('.jpg', frame)
    return io.BytesIO(buffer)