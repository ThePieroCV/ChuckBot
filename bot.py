import os

from dis_snek import Snake, Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SCOPE = os.getenv("ENV_SCOPE").split(" ")

## INSTANCIAR EL BOT
bot = Snake(intents=Intents.DEFAULT, default_prefix="!!", debug_scope=SCOPE[0])

bot.grow_scale("scales.admin")
## CORREMOS EL BOT
bot.start(TOKEN)
