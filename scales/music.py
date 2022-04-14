import re
import os
import urllib
from asyncio import Queue

from dis_snek import (
    InteractionContext,
    OptionTypes,
    slash_command,
    Scale,
    slash_option,
    Snake,
)
from dis_snek.api.voice.audio import YTDLAudio
import validators

from checks.music import MusicCheckConnect

## COMANDOS GENERALES
class MusicScaleConnect(MusicCheckConnect):
    def __init__(self, bot: Snake):
        super().__init__(bot)
        self.queue: Queue = Queue()

    @slash_command(name="play", description="Play and resume a song if its playing")
    @slash_option(
        name="song",
        description="Song's name",
        required=False,
        opt_type=OptionTypes.STRING,
    )
    async def music_play(self, ctx: InteractionContext, song: str = ""):
        if song:
            if not validators.url(song):
                search_keyword = song.replace(" ", "+")
                html = urllib.request.urlopen(
                    "https://www.youtube.com/results?search_query=" + search_keyword
                )
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                song = "https://www.youtube.com/watch?v=" + video_ids[0]
            audio = await YTDLAudio.from_url(song)
            if self.queue.empty() and (ctx.voice_state and not ctx.voice_state.playing):
                await self.queue.put(audio)
                await ctx.send(f"Playing {audio.entry['title']}")
                await self.play_queue(ctx)
            else:
                await self.queue.put(audio)
                await ctx.send(f"Added to queue {audio.entry['title']}")
        else:
            if ctx.voice_state and ctx.voice_state.paused:
                ctx.voice_state.resume()
                await ctx.send("Resuming the song!")
            elif ctx.voice_state and ctx.voice_state.playing:
                await ctx.send("It is already playing the song!")
            else:
                await ctx.send("Introduce a song first!")

    @slash_command(name="pause", description="Pauses the song")
    async def music_pause(self, ctx: InteractionContext):
        if ctx.voice_state and ctx.voice_state.playing:
            ctx.voice_state.pause()
            await ctx.send("Paused!")
        else:
            await ctx.send("Not song is playing")

    async def play_queue(self, ctx: InteractionContext):
        while True:
            audio = await self.queue.get()
            await ctx.send(f"Now playing {audio.entry['title']}")
            await ctx.voice_state.play(audio)
            if self.queue.empty():
                break
        await ctx.send("Music ended :)")


class MusicScale(Scale):
    @slash_command(name="stop", description="Stops the song and disconnect")
    async def music_stop(self, ctx: InteractionContext):
        if ctx.voice_state:
            await ctx.voice_state.disconnect()
            await ctx.send("Goodbye!")
        else:
            await ctx.send("Not connected yet!")


def setup(bot):
    MusicScaleConnect(bot)
    MusicScale(bot)
