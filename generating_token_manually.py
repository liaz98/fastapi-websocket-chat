from jose import jwt
from datetime import datetime, timedelta
from app.main import SECRET_KEY, ALGORITHM

data = {
    "user_id": "123",
    "email": "user@example.com",
    "exp": datetime.utcnow() + timedelta(hours=1)
}
token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
print(token)