from naff import InteractionContext, slash_command, listen
import os

from checks.admin import AdminCheck

## COMANDOS GENERALES
class AdminExtension(AdminCheck):  # Cambiar por AdminCheck
    @listen()
    async def on_ready(self):
        for extension in [
            sc[:-3]
            for sc in os.listdir("extensions")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.load_extension("extensions." + extension)
            await self.bot.synchronise_interactions()

    ## GROW EXTENSIONS
    @slash_command(
        name="_grow_extensions", description="Grows all extensions in the extensions folder"
    )
    async def grow_extensions(self, ctx: InteractionContext):
        for extension in [
            sc[:-3]
            for sc in os.listdir("extensions")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.load_extension("extensions." + extension)
            await self.bot.synchronise_interactions()
        await ctx.send("Grew", ephemeral=True)

    ## REGROW EXTENSIONS
    @slash_command(
        name="_regrow_extensions", description="Regrows all extensions in the extensions folder"
    )
    async def regrow_extensions(self, ctx: InteractionContext):
        for extension in [
            sc[:-3]
            for sc in os.listdir("extensions")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.reload_extension("extensions." + extension)
            await self.bot.synchronise_interactions()
        await ctx.send("Regrew", ephemeral=True)

    ## SHED EXTENSIONS
    @slash_command(
        name="_shed_extensions", description="Regrows all extensions in the extensions folder"
    )
    async def shed_extensions(self, ctx: InteractionContext):
        for extension in [
            sc[:-3]
            for sc in os.listdir("extensions")
            if sc.endswith(".py") and sc != "admin.py"
        ]:
            self.bot.shed_extension("extensions." + extension)
            await self.bot.synchronise_interactions()
        await ctx.send("Shed", ephemeral=True)


def setup(bot):
    AdminExtension(bot)
