import asyncio
from webscraping.common.container import Container


async def main():
    container = Container()
    container.httpx_client()
    await container.init_resources()

    gemini_client = await container.gemini_client()

    prompt = "What is 2 * 2"
    try:
        result = await gemini_client.generate_text(prompt)
        print("Generated text:", result)
    except Exception as e:
        print("Error calling Gemini:", e)
    finally:
        container.shutdown_resources()


if __name__ == "__main__":
    asyncio.run(main())
