from dis_snek import Scale, InteractionContext, Snake


class MusicCheckConnect(Scale):
    def __init__(self, client: Snake):
        self.client = client
        self.add_scale_check(self.check)

    async def check(self, ctx: InteractionContext) -> bool:
        await ctx.defer()
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
