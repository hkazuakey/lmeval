import os
from dotenv import load_dotenv
from ..media import Modality
from .litellm_model import LiteLLMModel


# try:
#     import ollama
# except ImportError:
#     raise ImportError("To use ollama please install dependencies with: pip install llmeval[ollama]")



## subclasses per provider

class OllamaModel(LiteLLMModel):
    """
        Model names: https://ollama.com/library
        https://github.com/ollama/ollama

    Args:
        LiteLLMModel: _description_
    """

    def __init__(self,
                 model_version: str = "gemma2",
                 publisher: str = "Google",
                 endpoint: str = ""):



        modalities = [Modality.text, Modality.code]
        litellm_model = f'ollama_chat/{model_version}' # https://docs.litellm.ai/docs/providers/ollama#using-ollama-apichat
        publisher = model_version.split('-')[0].capitalize()
        super().__init__(model_version=model_version,
                         modalities=modalities,
                         publisher=publisher,
                         litellm_model=litellm_model)
