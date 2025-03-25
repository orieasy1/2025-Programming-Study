from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from FastAPI.code.camera.mycamera import get_captured_picture

app = FastAPI()

@app.get("/capture")
def capture_picture():
    image = get_captured_picture()
    if image is None:
        return {"error": "웹캠을 열 수 없거나 캡처할 수 없습니다."}
    return StreamingResponse(image, media_type="image/jpeg")