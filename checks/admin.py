from naff import Extension, InteractionContext, Extension
from naff.models.discord.enums import Permissions


class AdminCheck(Extension):
    def __init__(self, client: Extension):
        self.client = client
        self.add_extension_prerun(self.check)
        self.add_extension_postrun(self.sync_interactions)

    async def check(self, ctx: InteractionContext) -> bool:
        member = ctx.author
        return member.has_permission(Permissions.ADMINISTRATOR)

    async def sync_interactions(self, ctx: InteractionContext):
        await self.bot.synchronise_interactions()
