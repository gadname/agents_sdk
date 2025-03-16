from agents import Agent, Runner, WebSearchTool
import asyncio  # asyncioモジュールをインポート

# WebSearchToolのインスタンスを作成
web_search_tool = WebSearchTool(
    user_location={
        "type": "approximate",  # "locality"から"approximate"に変更
        "city": "Tokyo",
        "country": "JP",
    },
    search_context_size="high",
)

# Agentの作成時にはツールのインスタンスを渡す
research_agent = Agent(
    name="Research Agent",
    instructions="""
    あなたは研究アシスタントです。ユーザーの質問に対して、最新の情報を含む詳細かつ正確な回答を提供してください。
    """,
    tools=[web_search_tool],  # 辞書ではなく、作成したツールのインスタンスを渡す
)


# 外部からインポートされる非同期関数を追加
async def get_web_search_info_async(query: str) -> str:
    """
    指定されたクエリに基づいてウェブ検索を実行し、結果を返す非同期関数

    Args:
        query: 検索クエリ文字列

    Returns:
        検索結果の文字列
    """
    result = await Runner.run(research_agent, query)
    return result.final_output


# 非同期関数を定義して実行
async def main():
    result = await Runner.run(
        research_agent, "最新のAIコーディングアシスタントについて教えてください"
    )
    print(result.final_output)


# 非同期関数を実行
if __name__ == "__main__":
    asyncio.run(main())
