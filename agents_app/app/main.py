from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys

# weather_agentsモジュールからインポート
from weather_agents.base import get_weather_info_async

app = FastAPI(title="Weather Agent API")


class WeatherResponse(BaseModel):
    weather_info: str


@app.get("/")
async def root():
    return {"message": "Weather Agent API is running"}


@app.get("/weather", response_model=WeatherResponse)
async def weather():
    try:
        # 非同期関数を直接awaitで呼び出す
        weather_info = await get_weather_info_async()
        return WeatherResponse(weather_info=weather_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
