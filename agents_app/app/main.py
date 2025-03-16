from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys
from typing import Optional, Dict, Any, List

# weather_agentsモジュールからインポート
from sdk_agents.base import get_weather_info_async
from sdk_agents.web_search import get_web_search_info_async
from sdk_agents.computer_use import run_computer_use_async

app = FastAPI(title="Weather Agent API")


class WeatherResponse(BaseModel):
    weather_info: str


class WebSearchResponse(BaseModel):
    web_search_info: str


class ComputerUseRequest(BaseModel):
    instruction: str
    environment: str = "browser"
    display_width: int = 1024
    display_height: int = 768
    screenshot_base64: Optional[str] = None


class ComputerUseResponse(BaseModel):
    result: Dict[str, Any]


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


@app.post("/computer_use", response_model=ComputerUseResponse)
async def computer_use(request: ComputerUseRequest):
    try:
        result = await run_computer_use_async(
            instruction=request.instruction,
            environment=request.environment,
            display_width=request.display_width,
            display_height=request.display_height,
            screenshot_base64=request.screenshot_base64,
        )
        return ComputerUseResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
