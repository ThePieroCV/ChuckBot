import copy
import os
from shutil import which

from dis_snek import (
    InteractionContext,
    OptionTypes,
    slash_command,
    Scale,
    slash_option,
    Snake,
    SlashCommandChoice,
)
from dis_snek.ext.paginators import Paginator
from dis_snek.api.voice.audio import YTDLAudio
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import validators
from youtubesearchpython.__future__ import VideosSearch

from collect.queue import ChuckQueue

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
        self.queue: ChuckQueue = ChuckQueue([])
        self.repeat: int = 0
        self.shuffled: bool = False
        self.now_playing = ""
        self.paginator: Paginator = None

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
            self.queue = ChuckQueue([])
            self.shuffled = False
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
            self.queue = ChuckQueue([])
            self.shuffled = False
            self.now_playing = ""
            self.repeat = 0
            await ctx.voice_state.disconnect()
            await ctx.send("Goodbye!")
        else:
            await ctx.send("Not connected yet!")

    @slash_command(name="repeat", description="Repeats the song or queue")
    @slash_option(
        name="mode",
        description="Repeat's mode",
        required=True,
        opt_type=OptionTypes.INTEGER,
        choices=[
            SlashCommandChoice(name="No-Repeat", value=0),
            SlashCommandChoice(name="Repeat-Queue", value=1),
            SlashCommandChoice(name="Repeat-Current-Song", value=2),
        ],
    )
    async def music_repeat(self, ctx: InteractionContext, mode: int):
        if self.repeat == mode:
            await ctx.send("Repeat mode already set")
        else:
            self.repeat = mode
            match mode:
                case 0:
                    await ctx.send("Repeat mode disabled")
                case 1:
                    await ctx.send("Repeat mode activated on current queue")
                case 2:
                    await ctx.send("Repeat mode activated on current song")
            await self.reset_paginator()

    @slash_command(name="shuffle", description="Shuffle and reshuffle queue")
    async def music_shuffle(self, ctx: InteractionContext):
        if self.queue:
            self.shuffled = True
            self.queue.shuffle()
            await ctx.send("Shuffling queue")
        else:
            await ctx.send(f"A queue is not playing")

    @slash_command(name="unshuffle", description="Unshuffle queue")
    async def music_unshuffle(self, ctx: InteractionContext):
        if self.queue:
            if not self.shuffled:
                await ctx.send("Shuffling already disabled")
            else:
                self.shuffled = False
                self.queue.unshuffle()
                await ctx.send("Shuffling disabled")
                await self.reset_paginator()
        else:
            await ctx.send(f"A queue is not playing")

    @slash_command(
        name="now-playing", description="See info of what's playing right now"
    )
    async def music_np(self, ctx: InteractionContext):
        if self.queue:
            if ctx.voice_state.paused:
                await ctx.send(f"It is paused {self.now_playing} right now!")
            else:
                await ctx.send(f"It is playing {self.now_playing} right now!")
        else:
            await ctx.send(f"No song is playing")

    @slash_command(
        name="queue-show", description="Show the current queue and state of it"
    )
    async def music_qs(self, ctx: InteractionContext):
        if self.queue:
            match self.repeat:
                case 0:
                    string_repeat = "No Repeat"
                case 1:
                    string_repeat = "Repeating Queue"
                case 2:
                    string_repeat = "Repeating Song"
            string_playing = "Paused" if ctx.voice_state.paused else "Playing"
            string_shuffled = "ON" if self.shuffled else "OFF"
            string_init = f"🔸**Repeat:** ***{string_repeat}*** 🔸**Shuffled:** ***{string_shuffled}*** 🔸**State:** ***{string_playing}***\n"
            string_current = f"**Current song: {self.now_playing}\n**"
            string = (
                "🔹" + "\n🔹 ".join(tuple(zip(*self.queue))[2][1:])
                if len(self.queue) > 1
                else ""
            )
            self.paginator = Paginator.create_from_string(
                self.bot, string_init + string_current + string, page_size=600
            )
            await self.paginator.send(ctx)
        else:
            await ctx.send(f"A queue is not playing")

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
            type, audio, title = self.queue[0]
            if type == "query":
                videosSearch = VideosSearch(audio, limit=1)
                videosResult = (await videosSearch.next())["result"][0]
                audio = videosResult["link"]
                type = "url"
            if type == "url":
                audio = await YTDLAudio.from_url(audio)
            self.now_playing = title
            await ctx.channel.send(f"Now playing {self.now_playing}")
            await ctx.voice_state.play(audio)
            match self.repeat:
                case 0:
                    _ = self.queue.next() if self.queue else None
                case 1:
                    _ = self.queue.rotate()
            await self.reset_paginator()
        self.queue = ChuckQueue([])
        self.shuffled = False
        self.now_playing = ""
        self.repeat = 0

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
                                + i["track"]["name"]
                                + " audio",
                                i["track"]["name"]
                                + " "
                                + "**"
                                + i["track"]["artists"][0]["name"]
                                + "**",
                            )
                        )
                        for i in response["items"]
                    ]
                )
                offset = offset + len(response["items"])
            self.queue.extend(items)
            await ctx.channel.send(f"Added playlist to queue")
            await self.reset_paginator()
        else:
            videosSearch = VideosSearch(query, limit=1)
            vr_root = await videosSearch.next()
            if vr_root:
                videosResult = ["result"][0]
                url = videosResult["link"]
                self.queue.append(("url", url, videosResult["title"]))
                if is_playing:
                    await ctx.channel.send(f"Added {videosResult['title']} to queue")
                await self.reset_paginator()
            else:
                ctx.channel.send(f"The song {query} was not found")
        if not is_playing:
            await self.play_queue(ctx)

    async def reset_paginator(self):
        if self.paginator:
            await self.paginator.stop()
            await self.paginator.message.edit("***Queue Changed***")
            self.paginator = None


def setup(bot):
    MusicScale(bot)
