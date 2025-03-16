from openai import OpenAI
import os
import asyncio
import json
import base64
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "OPENAI_API_KEYが設定されていません。.envファイルを確認してください。"
    )

os.environ["OPENAI_API_KEY"] = api_key
client = OpenAI(api_key=api_key)


async def run_computer_use_async(
    instruction: str,
    environment: str = "browser",
    display_width: int = 1024,
    display_height: int = 768,
    screenshot_base64: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Computer Use APIを非同期で実行する関数

    Args:
        instruction: ユーザーからの指示
        environment: 実行環境 ("browser", "mac", "windows", "ubuntu")
        display_width: 画面の幅
        display_height: 画面の高さ
        screenshot_base64: スクリーンショットのBase64エンコード

    Returns:
        APIからのレスポンス（辞書型）
    """
    # 基本的な入力メッセージを作成
    messages = [{"role": "user", "content": instruction}]

    # スクリーンショットが提供されている場合の処理
    if screenshot_base64:
        try:
            # Base64文字列が有効かチェック
            base64.b64decode(screenshot_base64)

            # 既にdata:image/png;base64,プレフィックスが含まれているか確認
            if not screenshot_base64.startswith("data:image/"):
                # プレフィックスがない場合は追加
                image_url = f"data:image/png;base64,{screenshot_base64}"
            else:
                # 既にプレフィックスがある場合はそのまま使用
                image_url = screenshot_base64

            # 画像付きのメッセージを作成
            messages = [
                {
                    "role": "user",
                    "content": [  # type: ignore
                        {"type": "text", "text": instruction},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ]
        except Exception as e:
            # Base64デコードに失敗した場合はログに記録し、画像なしで続行
            print(f"スクリーンショットのBase64エンコードに問題があります: {str(e)}")
            # 画像なしで続行

    # APIリクエスト
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # computer-use-previewの代わりにgpt-4oを使用
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "computer_use",
                        "description": "Control a virtual computer to perform tasks",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "configuration": {
                                    "type": "object",
                                    "properties": {
                                        "display_width": {
                                            "type": "integer",
                                            "default": display_width,
                                        },
                                        "display_height": {
                                            "type": "integer",
                                            "default": display_height,
                                        },
                                        "environment": {
                                            "type": "string",
                                            "enum": [
                                                "browser",
                                                "mac",
                                                "windows",
                                                "ubuntu",
                                            ],
                                            "default": environment,
                                        },
                                    },
                                }
                            },
                        },
                    },
                }
            ],
            messages=messages,
        )

        # レスポンスの処理
        assistant_message = response.choices[0].message
        result = {"content": assistant_message.content, "tool_calls": []}

        # ツール呼び出しがある場合の処理
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "computer_use":
                    tool_call_data = {
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments),
                    }
                    result["tool_calls"].append(tool_call_data)

        return result

    except Exception as e:
        # エラーが発生した場合はエラーメッセージを含む結果を返す
        return {
            "content": f"エラーが発生しました: {str(e)}",
            "tool_calls": [],
            "error": str(e),
        }


# 同期バージョンの関数（必要に応じて）
def run_computer_use(
    instruction: str,
    environment: str = "browser",
    display_width: int = 1024,
    display_height: int = 768,
    screenshot_base64: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Computer Useモデルを使用してコンピュータ操作を実行する同期関数
    """
    return asyncio.run(
        run_computer_use_async(
            instruction, environment, display_width, display_height, screenshot_base64
        )
    )


# テスト用のメイン関数
async def main():
    result = await run_computer_use_async("Check the latest OpenAI news on bing.com.")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
