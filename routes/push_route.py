from fastapi import APIRouter, Request
import json
from pywebpush import webpush, WebPushException

from config import DevelopmentConfig
config = DevelopmentConfig()

push_router = APIRouter()

subscriptions = []  # เก็บไว้ชั่วคราว, ปกติจะเก็บใน DB

VAPID_PUBLIC_KEY = config.PUSH_PUB_KEY  # จากขั้นตอนสร้างคีย์
VAPID_PRIVATE_KEY = config.PUSH_PRI_KEY     # จากขั้นตอนสร้างคีย์

@push_router.post("/save-subscription")
async def save_subscription(request: Request):
    body = await request.json()
    subscriptions.append(body)
    return {"status": "saved"}

@push_router.post("/send-notification")
def send_notification():
    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps({
                    "title": "📢 แจ้งเตือน",
                    "body": "สวัสดีจาก FastAPI!"
                }),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": "mailto:you@example.com"
                }
            )
        except WebPushException as ex:
            print(f"❌ Push failed: {ex}")
    return {"status": "sent"}

@push_router.get("/public-key")
def get_public_key():
    return {"publicKey": VAPID_PUBLIC_KEY}
