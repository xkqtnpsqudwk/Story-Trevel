"""데모 실행 스크립트 (다른 PC에서도 접속 가능하게).

host="0.0.0.0" : 내 PC뿐 아니라 같은 네트워크의 다른 기기에서도 접속 허용.
port=8000      : 접속 포트. 다른 PC는 http://<내 PC IP>:8000 으로 들어온다.
"""
import uvicorn

if __name__ == "__main__":
    # 0.0.0.0 = 모든 네트워크 인터페이스에서 수신 (다른 PC 접속 허용)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
