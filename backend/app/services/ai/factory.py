from app.core.config import settings
from .base import AIProvider
from .mock_provider import MockAIProvider


def get_ai_provider() -> AIProvider:
    # Providers are imported lazily so a missing optional SDK
    # (google-genai / openai) never breaks app startup.
    if settings.GEMINI_API_KEY:
        try:
            from .gemini_provider import GeminiProvider

            return GeminiProvider()
        except ImportError as e:
            print(f"Gemini SDK unavailable ({e}); falling back.")
    if settings.OPENAI_API_KEY:
        try:
            from .openai_provider import OpenAIProvider

            return OpenAIProvider()
        except ImportError as e:
            print(f"OpenAI SDK unavailable ({e}); falling back.")
    return MockAIProvider()
