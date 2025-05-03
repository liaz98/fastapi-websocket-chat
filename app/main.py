from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from typing import List

app = FastAPI()

SECRET_KEY = "Hqywf53_9-kUlDbsEI0RBWiwqo-SM7yHZEX7DxYUabI"
ALGORITHM = "HS256"

connected_clients: List[WebSocket] = []


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, token: str = Query(None)):
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_data = verify_jwt_token(token)
    if user_data is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    connected_clients.append(websocket)
    user_id = user_data.get("user_id") or user_data.get("email")
    print(f"User connected: {user_id}")

    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                await client.send_text(f"[{user_id}]: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print(f"User disconnected: {user_id}")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
