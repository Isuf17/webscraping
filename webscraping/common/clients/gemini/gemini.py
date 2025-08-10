import httpx
from webscraping.common.clients.gemini.igemini import IGeminiClient


class GeminiClient(IGeminiClient):
    def __init__(self, api_key: str, client: httpx.AsyncClient):
        self.api_key = api_key
        self.client = client
        self.service_endpoint = "https://generativelanguage.googleapis.com"

    async def generate_text(self, prompt: str) -> str:
        url = f"{self.service_endpoint}/v1beta/models/gemini-2.5-pro:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        response = await self.client.post(url, headers=headers, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                "Gemini API request failed "
                f"[{e.response.status_code}]: "
                f"{e.response.text}"
            ) from e

        data = response.json()
        if "candidates" not in data:
            raise RuntimeError(f"Missing 'candidates' in response: {data}")

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"Unexpected format in Gemini response: {data}") from exc
