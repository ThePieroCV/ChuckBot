import re
import os
import urllib

from dis_snek import InteractionContext, OptionTypes, slash_command, Scale, slash_option
from dis_snek.api.voice.audio import YTDLAudio
import validators

from checks.music import MusicCheck

## COMANDOS GENERALES
class MusicScale(MusicCheck):  # Cambiar por MusicCheck
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
            # await ctx.send(f"Playing {audio.entry['track']} of {audio.entry['artist']}")
            await ctx.send(f"Playing {audio.entry['title']}")
            await ctx.voice_state.play(audio)
        else:
            if ctx.voice_state.paused:
                ctx.voice_state.resume()
                await ctx.send("Resuming the song!")
            elif ctx.voice_state.playing:
                await ctx.send("It is already playing the song!")
            else:
                await ctx.send("Introduce a song first!")

    @slash_command(name="stop", description="Stops the song and disconnect")
    async def music_stop(self, ctx: InteractionContext):
        if ctx.voice_state:
            await ctx.voice_state.disconnect()
            await ctx.send("Goodbye!")

    @slash_command(name="pause", description="Pauses the song")
    async def music_pause(self, ctx: InteractionContext):
        if ctx.voice_state.playing:
            ctx.voice_state.pause()
            await ctx.send("Paused!")
        else:
            await ctx.send("Not song is playing")


def setup(bot):
    MusicScale(bot)
