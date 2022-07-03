import asyncio
from typing import Optional

from naff.api.voice.audio import AudioVolume
from yt_dlp import YoutubeDL

ytdl = YoutubeDL(
        {
            "format": "bestaudio/best",
            "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "default_search": "auto",
            "source_address": "0.0.0.0",
        }
    )

class YTDLAudio(AudioVolume):
    """An audio object to play sources supported by YTDLP"""

    def __init__(self, src) -> None:
        super().__init__( src )
        self.entry: Optional[dict] = None

    @classmethod
    async def from_url(cls, url, stream=True) -> "YTDLAudio":
        """Create this object from a YTDL support url."""
        data = await asyncio.to_thread(lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)

        new_cls = cls(filename)

        if stream:
            new_cls.ffmpeg_before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        new_cls.entry = data
        return new_cls