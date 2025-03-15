from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys

# weather_agentsモジュールからインポート
from sdk_agents.base import get_weather_info_async
from sdk_agents.web_search import get_web_search_info_async

app = FastAPI(title="Weather Agent API")


class WeatherResponse(BaseModel):
    weather_info: str


class WebSearchResponse(BaseModel):
    web_search_info: str


@app.get("/")
async def root():
    return {"message": "Weather Agent API is running"}


@app.get("/weather", response_model=WeatherResponse)
async def weather():
    try:
        weather_info = await get_weather_info_async()
        return WeatherResponse(weather_info=weather_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/web_search", response_model=WebSearchResponse)
async def web_search():
    try:
        # デフォルトのクエリを指定して関数を呼び出す
        web_search_info = await get_web_search_info_async(
            "最新のテクノロジートレンドについて教えてください"
        )
        return WebSearchResponse(web_search_info=web_search_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
