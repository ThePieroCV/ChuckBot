from dis_snek import Scale, InteractionContext, Snake
from dis_snek.models.discord.enums import Permissions


class AdminCheck(Scale):
    def __init__(self, client: Snake):
        self.client = client
        self.add_scale_check(self.check)
        self.add_scale_postrun(self.sync_interactions)

    async def check(self, ctx: InteractionContext) -> bool:
        member = ctx.author
        return member.has_permission(Permissions.ADMINISTRATOR)

    async def sync_interactions(self, ctx: InteractionContext):
        await self.bot.synchronise_interactions()
