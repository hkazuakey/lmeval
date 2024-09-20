from lmeval.custom_model import CustomModel
from lmeval.enums import Modality, FileType
from pydantic import Field


class Media(CustomModel):
    "media represent a unified format for files to be stored in benchmark and used in questions"
    modality: Modality
    filetype: FileType
    filename: str = Field(default="")
    size: int  = Field(default=0)
    # used to track if the file is stored in the benchmark archive
    is_stored: bool = Field(default=False)

    # used to move files during saving or single generation
    # its empty when loaded from a benchmark archive
    original_path: str = Field(default="")

    # used to pass the content during evaluation from benchmark archive
    content: bytes = Field(default_factory=bytes)

    def __str__(self) -> str:
        return str(self.filetype.value)
