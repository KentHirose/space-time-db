from typing import Optional

from fastapi import FastAPI

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/map")
async def get_directions(origin="松戸駅", destination="渋谷駅", time="2024/8/1/10:00:00"):
    # 以下のダミーのデータを返す
    # 松戸駅から日暮里駅に手段=常磐線で行く(2024/8/1/10:00:00発、2024/8/1/10:30:00到着)
    # 日暮里駅常磐線ホームから山手線ホームに手段=乗り換え(2024/8/1/10:30:00発、2024/8/1/10:40:00到着)
    # 日暮里駅から渋谷駅まで手段=山手線で行く(2024/8/1/10:40:00発、2024/8/1/11:00:00到着)
    
    return [
        [
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
            }
        ]
    ]
