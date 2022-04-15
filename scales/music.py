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

## COMANDOS GENERALES
class MusicScale(Scale):
    def __init__(self, bot: Snake):
        super().__init__()
        self.queue: list = []

    @slash_command(name="play", description="Play and resume a song if its playing")
    @slash_option(
        name="song",
        description="Song's name",
        required=False,
        opt_type=OptionTypes.STRING,
    )
    async def music_play(self, ctx: InteractionContext, song: str = ""):
        connected = await self.connect(ctx)
        if connected:
            if song:
                if ctx.responded:
                    await ctx.channel.send(f"Looking for {song}...")
                else:
                    await ctx.send(f"Looking for {song}...")
                if not validators.url(song):
                    search_keyword = song.replace(" ", "+")
                    html = urllib.request.urlopen(
                        "https://www.youtube.com/results?search_query=" + search_keyword
                    )
                    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                    song = "https://www.youtube.com/watch?v=" + video_ids[0]
                audio = await YTDLAudio.from_url(song)
                self.queue.append(audio)
                if len(self.queue) == 1:
                    await self.play_queue(ctx)
                else:
                    await ctx.channel.send(f"Added to queue {audio.entry['title']}")
            else:
                if ctx.voice_state and ctx.voice_state.paused:
                    ctx.voice_state.resume()
                    await ctx.send("Resuming the song!")
                elif ctx.voice_state and ctx.voice_state.playing:
                    await ctx.send("It is already playing the song!")
                else:
                    if ctx.voice_state:
                        await ctx.channel.send("Introduce a song first!")
                    else:
                        await ctx.send("Introduce a song first!")

    @slash_command(name="pause", description="Pauses the song")
    async def music_pause(self, ctx: InteractionContext):
        if self.queue and ctx.voice_state.playing:
            ctx.voice_state.pause()
            await ctx.send("Paused!")
        elif self.queue and ctx.voice_state.paused:
            await ctx.send("It is already paused!")
        else:
            await ctx.send("Not song is playing")

    @slash_command(name="stop", description="Stops the song and disconnect")
    async def music_stop(self, ctx: InteractionContext):
        if ctx.voice_state:
            await ctx.voice_state.disconnect()
            await ctx.send("Goodbye!")
        else:
            await ctx.send("Not connected yet!")

    async def connect(self, ctx: InteractionContext):
        if ctx.author.voice:
            if (
                ctx.voice_state is None
                or ctx.voice_state.channel != ctx.author.voice.channel
            ):
                await ctx.author.voice.channel.connect(deafened=True)
                await ctx.send(f"Join channel <#{ctx.author.voice.channel.id}>")
            return True
        else:
            await ctx.send("User not connected to a channel")
            return False

    async def play_queue(self, ctx: InteractionContext):
        while self.queue:
            audio = self.queue[0]
            await ctx.channel.send(f"Now playing {audio.entry['title']}")
            await ctx.voice_state.play(audio)
            _ = self.queue.pop(0)


def setup(bot):
    MusicScale(bot)
