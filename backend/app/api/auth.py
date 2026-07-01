from fastapi import APIRouter, HTTPException, Depends, Header
from bson import ObjectId
from datetime import datetime
from app.models.user import UserCreate, UserLogin, UserOut
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.database import get_database

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(user: UserCreate):
    db = get_database()
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    doc = {
        "email": user.email,
        "name": user.name,
        "hashed_password": hashed,
        "created_at": datetime.utcnow(),
    }
    result = db.users.insert_one(doc)
    token = create_access_token({"sub": str(result.inserted_id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(credentials: UserLogin):
    db = get_database()
    user = db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    db = get_database()
    user = db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.get("/me", response_model=UserOut)
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "email": current_user["email"],
        "name": current_user.get("name"),
        "created_at": current_user["created_at"],
    }