import disnake, random, config, aiohttp
from disnake.ext import commands
from disnake.ext.commands import slash_command, user_command, message_command

users = []
idtn = {}
idtt = {}

splitter = '%'
with open ("resources\\user.txt") as f:
  for userdata in f:
    users.append(str((userdata.split(splitter))[2]).strip('\n'))
# maps for the  ordering fill out
with open ("resources\\user.txt") as f:
  for userdata in f:
    idtn[int(userdata.split(splitter)[2])] = (str(userdata.split(splitter)[0]))
    idtt[int(userdata.split(splitter)[2])] = (str(userdata.split(splitter)[1]))
  print(idtn)


class General(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @slash_command(
       name="ping",
       description="Check if the bot is alive"
    )
    async def ping(self, inter):
        embed = disnake.Embed(
          title=":ping_pong: Pong!",
          description=f"{round(self.bot.latency * 1000)}ms.",
          color=disnake.Color.green()
        )
        print("pong")
        await inter.response.send_message(embed=embed)
    # register
    @slash_command(
       name="register",
       description="Check if the bot is alive"
    )
    async def register(self, inter, arg:disnake.Member, first_name, last_name, team_number):
        for user in users:
          print(user)
          print(str(inter.author.id))
        if (str(inter.author.id) not in users):
            embed = disnake.Embed(
                title="Registration",
                description=f"You have successfully registered!",
                color=disnake.Color.green()
            )
            await inter.response.send_message(embed=embed)

            appended = str(first_name) + " " + str(last_name) + '%' + str(team_number) + "%" + str(inter.author.id)
            users.append(str(inter.author.id))

            # adding registered role
            try:
                await arg.add_roles(disnake.utils.get(inter.guild.roles, name="Registered"))
            except:
                embed = disnake.Embed(
                    title="Error",
                    description=f"Failed to add role,ask a moderator to manually add the role",
                    color=disnake.Color.red()
                )
                await inter.response.send_message(embed=embed)

            with open ("resources\\user.txt", "a") as f:
                f.write(appended+"\n")

        else:
            embed = disnake.Embed(
                title="Registration",
                description=f"You have already registered! Contact the Mentor team if you are having issues.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed)

    @slash_command(
       name="help",
       description="How to use this bot"
    )
    async def help(self, inter):
        embed = disnake.Embed(
          title="How this discord bot can be used.",
          description=f"Below is a list of commands that you can use and who can use them: \n\n" + 
          "**/help** : This window right now :) \n" +
          "**/mutematthew** : mutes Matthew from team 3388H in VC and chats. Accessible by anyone in the server.\n" +
          "**/findjacobs** : finds mr.jacobs. If he is within a 5 mile radius, ***RUN***\n" +
          "**/quickorder** : order parts by exact name, very quick but requires memorization of parts list.\n" +
          "**/searchorder** : search for parts through an interactive menu. Once your part is found, you can order, fetch a Inventor model, get specifications, or exit",
          color=disnake.Color.blue()
        )
        print("pong")
        await inter.response.send_message(embed=embed)

    @slash_command(
      name="botinfo",
      description="Get some information about the bot"
    )
    async def botinfo(self, inter):
        embed = disnake.Embed(
          title=f"Name: {self.bot.user}",
          description=f"ID: {self.bot.user.id}",
          color=disnake.Color.green()
        )
        embed.add_field(
          name="Owner information",
          value="Ravost99#3361"
        )
        embed.add_field(
          name="Used [Ravost99's](https://github.com/Ravost99/Disnake.py-Bot-Template) Template",
          value="Share the repo!"
        )
        embed.add_field(
          name="Disnake Version",
          value=f"{disnake.__version__}"
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await inter.send(embed=embed)


    @slash_command(
      name="serverinfo",
      description="Get some info on the current server"
    )
    async def serverinfo(self, inter):
        server = inter.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = disnake.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x42F56C
        )
        try:
          embed.set_thumbnail(
              url=server.icon_url
          )
        except:
          print(f"No server icon found for {server.name}")
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
          name="Boosts",
          value=f"{str(inter.guild.premium_subscription_count)}"
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await inter.send(embed=embed)


def setup(bot):
    splitter = '%'
    with open ("resources\\user.txt") as f:
      for userdata in f:
        users.append(str((userdata.split(splitter))[2]).strip('\n'))
    # maps for the  ordering fill out
    with open ("resources\\user.txt") as f:
      for userdata in f:
        idtn[int(userdata.split(splitter)[2])] = (str(userdata.split(splitter)[0]))
        idtt[int(userdata.split(splitter)[2])] = (str(userdata.split(splitter)[1]))
      print(idtn)
    bot.add_cog(General(bot))
    print(f"> Extension {__name__} is ready")