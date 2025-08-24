from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "coupon_guard"
COLLECTION_NAME = "coupons"

app = FastAPI()
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class Feedback(BaseModel):
    code: str
    success: bool

@app.get("/coupons")
async def get_coupons(site: str):
    coupons = await collection.find({"site": site, "success_rate": {"$gt": 0.5}}).sort("success_rate", -1).to_list(10)
    if not coupons:
        raise HTTPException(status_code=404, detail="No coupons found")
    return [{**c, "_id": str(c["_id"])} for c in coupons]  # Convert ObjectId to str

@app.post("/feedback")
async def submit_feedback(feedback: Feedback):
    coupon = await collection.find_one({"code": feedback.code})
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    new_tests = coupon.get("tests", 0) + 1
    new_successes = coupon.get("successes", 0) + (1 if feedback.success else 0)
    success_rate = new_successes / new_tests if new_tests > 0 else 0
    
    await collection.update_one(
        {"code": feedback.code},
        {"$set": {"tests": new_tests, "successes": new_successes, "success_rate": success_rate}}
    )
    return {"message": "Feedback updated"}

# Run with: uvicorn main:app --reload