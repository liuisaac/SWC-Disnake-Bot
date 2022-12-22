import disnake, config, traceback, pytz
from datetime import datetime
from disnake.ext import commands
from disnake.ext.commands import slash_command, user_command, message_command

def fancy_traceback(exc: Exception) -> str:
    """May not fit the message content limit"""
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    return f"```py\n{text[-4086:]}\n```"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    #command check
    # @commands.Cog.listener()
    # async def on_command(self, ctx: commands.Context):
    #   tz = pytz.timezone('America/Chicago')
    #   now = datetime.now(tz)
    #   current_time = now.strftime("%I:%M:%S %p")
    #   current_date = datetime.today().strftime('%m-%d-%Y')

    #   fullCommandName = ctx.data.name
    #   split = fullCommandName.split(" ")
    #   command_name = str(split[0])
    #   embed = disnake.Embed(
    #     title=f"Executed command '{command_name}'",
    #     color=config.success
    #   )
    #   embed.add_field(
    #     name=f"Executed by {ctx.author} (ID: {ctx.author.id})",
    #     value=f"in {ctx.guild.name} (ID: {ctx.guild.id})"
    #   )
    #   embed.set_footer(
    #     text=f"On {current_date} at {current_time}"
    #   )
    #   try:
    #     print(f"Executed command '{command_name}' in {ctx.guild.name} (ID: {ctx.guild.id})\nBy {ctx.author} (ID: {ctx.author.id})\nOn {current_date} at {current_time}")
    #     #logs channel
    #     channel = self.bot.get_channel(config.logs_channel)
    #     await channel.send(embed=embed) 
    #   except:
    #     print(f"Executed command '{command_name}' in {ctx.guild.name} (ID: {ctx.guild.id})\nBy {ctx.author} (ID: {ctx.author.id})\nOn {current_date} at {current_time}")

    # slash command check
    @commands.Cog.listener()
    async def on_slash_command(self, inter):
      tz = pytz.timezone('America/Chicago')
      now = datetime.now(tz)
      current_time = now.strftime("%I:%M:%S %p")
      current_date = datetime.today().strftime('%m-%d-%Y')

      command_name = inter.data.name
      split = command_name.split(" ")
      command_name = str(split[0])
      embed = disnake.Embed(
        title=f"Executed slash command '{command_name}'",
        color=config.success
      )
      embed.add_field(
        name=f"Executed by {inter.author} (ID: {inter.author.id})",
        value=f"in {inter.guild.name} (ID: {inter.guild.id})"
      )
      embed.set_footer(
        text=f"On {current_date} at {current_time}"
      )
      try:
        print(f"Executed slash command '{command_name}' in {inter.guild.name} (ID: {inter.guild.id})\nBy {inter.author} (ID: {inter.author.id})\nOn {current_date} at {current_time}")
        # logs channel
        channel = self.bot.get_channel(config.logs_channel)
        await channel.send(embed=embed)
      except:
        print(f"Executed slash command '{command_name}' in {inter.guild.name} (ID: {inter.guild.id})\nBy {inter.author} (ID: {inter.author.id})\nOn {current_date} at {current_time}")

    @commands.Cog.listener()
    async def on_user_command(self, inter):
      tz = pytz.timezone('America/Chicago')
      now = datetime.now(tz)
      current_time = now.strftime("%I:%M:%S %p")
      current_date = datetime.today().strftime('%m-%d-%Y')

      command_name = inter.data.name
      split = command_name.split(" ")
      command_name = str(split[0])
      embed = disnake.Embed(
        title=f"Executed user command '{command_name}'",
        color=config.success
      )
      embed.add_field(
        name=f"Executed by {inter.author} (ID: {inter.author.id})",
        value=f"in {inter.guild.name} (ID: {inter.guild.id})"
      )
      embed.set_footer(
        text=f"On {current_date} at {current_time}"
      )
      try:
        print(f"Executed user command '{command_name}' in {inter.guild.name} (ID: {inter.guild.id})\nBy {inter.author} (ID: {inter.author.id})\nOn {current_date} at {current_time}")
        # logs channel
        channel = self.bot.get_channel(config.logs_channel)
        await channel.send(embed=embed)
      except:
        print(f"Executed user command '{command_name}' in {inter.guild.name} (ID: {inter.guild.id})\nBy {inter.author} (ID: {inter.author.id})\nOn {current_date} at {current_time}")

    #on any command error
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
      embed = disnake.Embed(
        title=f"Command `{ctx.command}` raised an error: `{error}`",
        description=fancy_traceback(error),
        color=config.error
      )
      await ctx.send(embed=embed)

    # slash comamnd error
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
      embed = disnake.Embed(
        title=f"Slash command `{inter.data.name}` failed due to `{error}`",
        description=fancy_traceback(error),
        color=config.error,
      )

      send = inter.response.send_message
      await send(embed=embed)

    # context menu / user error
    @commands.Cog.listener()
    async def on_user_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
      embed = disnake.Embed(
        title=f"User command `{inter.data.name}` failed due to `{error}`",
        description=fancy_traceback(error),
        color=config.error,
      )
      if inter.response._responded:
        send = inter.channel.send
      else:
        send = inter.response.send_message
      await send(embed=embed)

    # Message command error
    @commands.Cog.listener()
    async def on_message_command_error(self, inter: disnake.AppCmdInter, error: commands.CommandError):
      embed = disnake.Embed(
        title=f"Message command `{inter.data.name}` failed due to `{error}`",
        description=fancy_traceback(error),
        color=config.error,
      )
      if inter.response._responded:
        send = inter.channel.send
      else:
        send = inter.response.send_message
      await send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
    print(f"> Extension {__name__} is ready")