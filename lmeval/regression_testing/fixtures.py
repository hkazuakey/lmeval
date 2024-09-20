"""Fixture for regression tests."""

import pytest
import os
from dotenv import load_dotenv
from lmeval.models.gemini import GeminiModel


@pytest.fixture
def gemini() -> GeminiModel:
    "Gemini model fixture"
    load_dotenv()  # take environment variables from .env.
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    model = GeminiModel(api_key=GEMINI_API_KEY)
    return model

@pytest.fixture
def gemini_pro15() -> GeminiModel:
    "Gemini model fixture"
    load_dotenv()  # take environment variables from .env.
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    model = GeminiModel(api_key=GEMINI_API_KEY, model_version="gemini-1.5-pro-001")
    return model