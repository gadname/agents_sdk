import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI
import agents

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEYが設定されていません。.envファイルを確認してください。"
    )

os.environ["OPENAI_API_KEY"] = api_key
client = OpenAI(api_key=api_key)

# エージェントの作成
weather_agent = agents.Agent(
    name="weather_agent",
    instructions="あなたは天気情報を提供するエージェントです。ユーザーの質問に対して、丁寧に天気情報を回答してください。",
    model="gpt-4o",
)


# 非同期関数として定義
async def get_weather_info_async():
    # Runnerクラスのインスタンスを作成（引数なし）
    runner = agents.Runner()
    # runメソッドにagentを渡す
    result = await runner.run(weather_agent, "今日の東京の天気を教えてください。")
    return result.final_output


# 同期関数のラッパー
def get_weather_info():
    # 非同期関数を同期的に実行するためのヘルパー関数
    return asyncio.run(get_weather_info_async())


# このファイルが直接実行された場合のみ実行
if __name__ == "__main__":
    weather_info = get_weather_info()
    print("天気情報:")
    print(weather_info)
