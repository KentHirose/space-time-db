from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware

import os
import asyncio
from supabase import create_client, Client
from dotenv import load_dotenv
from outscraper import ApiClient

load_dotenv()

api_client = ApiClient(api_key=os.environ.get("OUTSCRAPER_API_KEY"))

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_API_KEY")
password: str = os.environ.get("SUPABASE_PASSWORD")
supabase: Client = create_client(url, key)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/map")
async def get_directions(
    origin="松戸駅", destination="渋谷駅", time="2024/8/1/11:00:00"
):
    return [
        {
            "origin": "松戸駅",
            "destination": "日暮里駅",
            "transportation": "常磐線",
            "departure": "2024/8/1/10:00:00",
            "arrival": "2024/8/1/10:30:00",
        },
        {
            "origin": "日暮里駅常磐線ホーム",
            "destination": "日暮里駅山手線ホーム",
            "transportation": "乗り換え",
            "departure": "2024/8/1/10:30:00",
            "arrival": "2024/8/1/10:40:00",
        },
        {
            "origin": "日暮里駅",
            "destination": "渋谷駅",
            "transportation": "山手線",
            "departure": "2024/8/1/10:40:00",
            "arrival": "2024/8/1/11:00:00",
        },
    ]


@app.get("/route")
async def get_route(origin: str, destination: str, name: str):
    supabase.table("route").insert(
        {
            "origin": origin,
            "destination": destination,
            "name": name,
        }
    ).execute()
    return "ok"


@app.get("/route_search")
# nameの最新だけを取得する
async def get_route_search(name: str):
    res = (
        supabase.table("route")
        .select("*")
        .eq("name", name)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0]
