import converter.cpdf as cpdf
import disnake, config
import os, asyncio
from keep_alive import keep_alive
from disnake.ext import commands, tasks

#requires installation og fpdf
TABLE_DATA = (
    ("Feb 14, 2023 ", "Gautham Venkateshwaran", "32A", "25", "Lock Nuts", "", "l"),
    ("Feb 19, 2023 ", "Gautham Venkateshwaran", "34B", "40", "1/2 in Screws", "", ""),
    ("June 24, 2023 ", "Dawson Sagal", "23C", "100", "Nylocks", "", ""),
)
cpdf = cpdf.pdfgenerator(TABLE_DATA)
cpdf.generate()
print("domne")
#imports and packages

#bot
asyncio.sleep(5.9) #to avoid discord rate limits
os.system('clear')

#setting up the bot
bot = commands.Bot(
  command_prefix=".",#prefix, not needed for slash commands
  intents=disnake.Intents.all(),
  help_command=None, #in case you want to add your own help command sync_commands_debug=True,
  test_guilds=[1048448989307093054], #put your guild ids here, that the bot is in
)

#checking when the bot is ready
@bot.event
async def on_ready():
  print(f"Im logged in as {bot.user}")
  print(f"In {len(bot.guilds)} guilds")
  print(f"Disnake Version: {disnake.__version__}")
  print(f"Starting Status Task: {config.status_task}")
  print("-----------------------------")
  status_task.start()
  keep_alive()

# Setup the game status task of the bot
# change the minutes to what ever you want, remove if you want, 5.9
@tasks.loop(minutes=0.1)
async def status_task():
    #change the 'ActivityType.playing' to listening, watching, streaming, playing, competing
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing, name=config.status_task))

#loading all extensions in the cogs folder
#only runs when ran as a script, not when imported as a module
if __name__ in '__main__':
  py_path = f"cogs"
  folder = f"cogs"
  for name in os.listdir(folder):
    if name.endswith(".py") and os.path.isfile(f"cogs/{name}"):#finding all python files (.py)
      bot.load_extension(f"{py_path}.{name[:-3]}") #loading extensions

def reload():
  py_path = f"cogs"
  folder = f"cogs"
  for name in os.listdir(folder):
    if name.endswith(".py") and os.path.isfile(f"cogs/{name}"):#finding all python files (.py)
      bot.load_extension(f"{py_path}.{name[:-3]}") #loading extensions

#running the bot with the token
bot.run(config.token)
