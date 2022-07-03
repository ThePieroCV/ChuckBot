import os

from naff import Client, Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SCOPE = os.getenv("ENV_SCOPE").split(" ")

## INSTANCIAR EL BOT
bot = Client(intents=Intents.DEFAULT, debug_scope=SCOPE[0], sync_interactions=True)

bot.load_extension("extensions.admin")
## CORREMOS EL BOT
bot.start(TOKEN)
