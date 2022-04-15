import re
import os
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
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import validators
from youtubesearchpython.__future__ import VideosSearch

load_dotenv()
SPOTIFY_CLIENT = os.getenv("SPOTIFY_CLIENT")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT, client_secret=SPOTIFY_CLIENT_SECRET
    )
)


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
                await self.add_queries(ctx, song)
            else:
                if ctx.voice_state and ctx.voice_state.paused:
                    ctx.voice_state.resume()
                    await ctx.send("Resuming the song!")
                elif ctx.voice_state and ctx.voice_state.playing:
                    await ctx.send("It is already playing the song!")
                else:
                    if ctx.responded:
                        await ctx.channel.send("Introduce a song first!")
                    else:
                        await ctx.send("Introduce a song first!")

    @slash_command(
        name="force-play",
        description="Forces to play a song, clearing the current queue",
    )
    @slash_option(
        name="song",
        description="Song's name",
        required=True,
        opt_type=OptionTypes.STRING,
    )
    async def music_force_play(self, ctx: InteractionContext, song: str = ""):
        connected = await self.connect(ctx)
        if connected:
            self.queue = []
            if not ctx.voice_state.stopped:
                await ctx.voice_state.stop()
            if ctx.responded:
                await ctx.channel.send(f"Looking for {song}...")
            else:
                await ctx.send(f"Looking for {song}...")
            await self.add_queries(ctx, song)

    @slash_command(name="pause", description="Pauses the song")
    async def music_pause(self, ctx: InteractionContext):
        if self.queue and ctx.voice_state.playing:
            ctx.voice_state.pause()
            await ctx.send("Paused!")
        elif self.queue and ctx.voice_state.paused:
            await ctx.send("It is already paused!")
        else:
            await ctx.send("Not song is playing")

    @slash_command(name="skip", description="Skips the song")
    async def music_skip(self, ctx: InteractionContext):
        if self.queue:
            await ctx.voice_state.stop()
            await ctx.send("Skipping!")
        else:
            await ctx.send("Not music in queue!")

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
            type, audio = self.queue[0]
            if type == "query":
                videosSearch = VideosSearch(audio + " official audio", limit=1)
                videosResult = (await videosSearch.next())["result"][0]
                audio = videosResult["link"]
                type = "url"
            if type == "url":
                audio = await YTDLAudio.from_url(audio)
            await ctx.channel.send(f"Now playing {audio.entry['title']}")
            await ctx.voice_state.play(audio)
            _ = self.queue.pop(0) if self.queue else None

    async def add_queries(self, ctx: InteractionContext, query: str):
        is_playing = len(self.queue)
        if validators.url(query) and ("spotify" in query):
            items = []
            offset = 0
            spid = "spotify:playlist:" + query.split("/")[-1].split("?")[0]
            while True:
                response = sp.playlist_items(
                    spid,
                    offset=offset,
                    fields="items.track.name,items.track.artists.name",
                )

                if len(response["items"]) == 0:
                    break

                items.extend(
                    [
                        (
                            (
                                "query",
                                i["track"]["artists"][0]["name"]
                                + " "
                                + i["track"]["name"],
                            )
                        )
                        for i in response["items"]
                    ]
                )
                offset = offset + len(response["items"])
            self.queue.extend(items)
            await ctx.channel.send(f"Added playlist to queue")
        elif validators.url(query):
            audio = await YTDLAudio.from_url(query)
            self.queue.append(("audio", audio))
            if is_playing:
                await ctx.channel.send(f"Added {audio.entry['title']} to queue")
        else:
            videosSearch = VideosSearch(query, limit=1)
            videosResult = (await videosSearch.next())["result"][0]
            url = videosResult["link"]
            audio = await YTDLAudio.from_url(url)
            self.queue.append(("audio", audio))
            if is_playing:
                await ctx.channel.send(f"Added {audio.entry['title']} to queue")
        if not is_playing:
            await self.play_queue(ctx)


def setup(bot):
    MusicScale(bot)
