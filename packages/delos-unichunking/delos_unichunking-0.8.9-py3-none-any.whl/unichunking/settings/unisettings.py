"""Settings for universal chunking."""

from pydantic_settings import BaseSettings

from unichunking.settings.chunking import ChunkingSettings
from unichunking.settings.files import FilesSettings
from unichunking.settings.text import TextSettings


class UniSettings(BaseSettings):
    """Base settings for file processing."""

    chunking: ChunkingSettings = ChunkingSettings()
    files: FilesSettings = FilesSettings()
    text: TextSettings = TextSettings()


unisettings = UniSettings()
