import pytest
import httpx
from pytest_mock import MockerFixture
from webscraping.common.clients.gemini_client.gemini_client import GeminiClient


@pytest.mark.asyncio
async def test_generate_text_success(mocker: MockerFixture):
    # Arrange
    mock_client = mocker.AsyncMock(spec=httpx.AsyncClient)
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Hello from Gemini"}]}}]
    }
    mock_client.post.return_value = mock_response

    gemini = GeminiClient(api_key="test-key", client=mock_client)

    # Act
    result = await gemini.generate_text("Hi Gemini")

    # Assert
    assert result == "Hello from Gemini"
    mock_client.post.assert_awaited_once_with(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": "test-key",
        },
        json={"contents": [{"parts": [{"text": "Hi Gemini"}]}]},
    )
