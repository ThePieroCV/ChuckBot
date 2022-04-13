from dis_snek import InteractionContext, slash_command, Scale, listen
import os

from checks.admin import AdminCheck

## COMANDOS GENERALES
class AdminScale(AdminCheck):  # Cambiar por AdminCheck
    @listen()
    async def on_ready(self):
        for scale in [
            sc[:-3]
            for sc in os.listdir("scales")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.grow_scale("scales." + scale)
            await self.bot.synchronise_interactions()

    ## GROW SCALES
    @slash_command(
        name="_grow_scales", description="Grows all scales in the scales folder"
    )
    async def grow_scales(self, ctx: InteractionContext):
        for scale in [
            sc[:-3]
            for sc in os.listdir("scales")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.grow_scale("scales." + scale)
            await self.bot.synchronise_interactions()
        await ctx.send("Grew", ephemeral=True)

    ## REGROW SCALES
    @slash_command(
        name="_regrow_scales", description="Regrows all scales in the scales folder"
    )
    async def regrow_scales(self, ctx: InteractionContext):
        for scale in [
            sc[:-3]
            for sc in os.listdir("scales")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.regrow_scale("scales." + scale)
            await self.bot.synchronise_interactions()
        await ctx.send("Regrew", ephemeral=True)

    ## SHED SCALES
    @slash_command(
        name="_shed_scales", description="Regrows all scales in the scales folder"
    )
    async def shed_scales(self, ctx: InteractionContext):
        for scale in [
            sc[:-3]
            for sc in os.listdir("scales")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.shed_scale("scales." + scale)
            await self.bot.synchronise_interactions()
        await ctx.send("Shed", ephemeral=True)


def setup(bot):
    AdminScale(bot)
