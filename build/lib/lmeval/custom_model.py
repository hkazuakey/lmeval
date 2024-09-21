from pydantic import BaseModel
from pydantic import ConfigDict

class CustomModel(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True  # ensure we can json serialize
        )
