import disnake, random, config, aiohttp
import qsearch
from cogs import general
from disnake.ext import commands
from disnake.ext.commands import slash_command, user_command, message_command
from disnake.ui import StringSelect, View
from importlib import reload
from datetime import datetime
import converter.cpdf as cpdf

partstobin = {}


class confirm(disnake.ui.View):
    author = ""
    arg = ""
    qty = ""
    def set_part(self, args):
        self.arg = args
    def set_author(self, author):
        self.author = author
    def set_qty(self, qty):
        self.qty = qty

    @disnake.ui.button(label="Yes", style=disnake.ButtonStyle.green)
    async def Yes(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if (interaction.user.id == self.author):
            reload(general)
            button.style = disnake.ButtonStyle.green
            for child in self.children: # loop through all the children of the view
                child.disabled = True # set the button to disabled
                print(child)
            button.label = str("Added to Cart!")

          # print(self.arg)

            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self)

            print(self.arg)
            print(general.idtt)
            print(general.idtn)
            print(interaction.user.id)
            #team_number = idtoteam[int(interaction.user.id)]
            name = general.idtn[int(interaction.user.id)]
            binnum = str(partstobin[self.arg])
            team = general.idtt[int(interaction.user.id)]
            print(name)
            #print(partstobin)
            if (self.arg).strip(' ') in partstobin: 
                wack = ("%".join(["?", name[:len(name)], binnum[1:(len(binnum)-1)], str(self.qty), self.arg, "?", "?"]))+"\n"
                print("!!!!!!:  "+wack)
            with open("teams\\"+str(team)+".txt", "a") as f:
                f.write(wack)

        else:
            print(interaction.user.id)
            print(self.author)
            await interaction.response.send_message(
              content="Please stop interacting with the components on this message." +
                      "A different user activated this command.", ephemeral=True)

    @disnake.ui.button(label="No", style=disnake.ButtonStyle.red)
    async def No(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if (interaction.user.id == self.author):
            button.style = disnake.ButtonStyle.red
            for child in self.children: # loop through all the children of the view
                child.disabled = True # set the button to disabled
            button.label = str("Order Cancelled")

            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self)
        else:
          await interaction.response.send_message(
            content="Please stop interacting with the components on this message." +
                    "A different user activated this command.", ephemeral=True)
class selectpart(disnake.ui.View):
    author = ""
    arg = ""
    qty = ""
    def set_part(self, args):
        self.arg = args
    def set_author(self, author):
        self.author = author
    def set_qty(self, qty):
        self.qty = qty

    @disnake.ui.button(label="Continue", style=disnake.ButtonStyle.green)
    async def Yes(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if (interaction.user.id == self.author):
            reload(general)
            button.style = disnake.ButtonStyle.green
            for child in self.children: # loop through all the children of the view
                child.disabled = True # set the button to disabled
                #print(child)
            button.label = str("Added to Cart!")

            # print(self.arg)

            # Make sure to update the message with our updated selves
            
        else:
            #print(interaction.user.id)
            #print(self.author)
            await interaction.response.send_message(
              content="Please stop interacting with the components on this message." +
                      "A different user activated this command.", ephemeral=True)

    @disnake.ui.button(label="Proceed with Manual Type-in", style=disnake.ButtonStyle.red)
    async def No(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if (interaction.user.id == self.author):
            button.style = disnake.ButtonStyle.red
            for child in self.children: # loop through all the children of the view
                child.disabled = True # set the button to disabled
            button.label = str("Proceeding with Manual Type-in")

            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self)
        else:
          await interaction.response.send_message(
            content="Please stop interacting with the components on this message." +
                    "A different user activated this command.", ephemeral=True)


class ordering(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @slash_command(
       name="help_order",
       description="Instructions on how ordering works"
    )
    async def help_order(self, inter):
        embed = disnake.Embed(
          title="How ordering works.",
          description=f"Below is a list of commands that you can use and who can use them: \n\n" + 
          "**.quickorder** : Order directly by a parts name( NOTE: QUICKORDER IS NOT A SLASH COMMAND, USES THE '.' PREFIX)" + "\n**/searchorder** : Order from a menu-style GUI",
          color=disnake.Color.blue()
        )
        await inter.response.send_message(embed=embed)

    @slash_command(
      name="quickorder",
      description="Order a part by its name"
    )
    async def quickorder(self, inter, part, qty):
        # check if argument is a valid part

        if (str(inter.author.id) in general.users and (part).strip(' ') in partstobin):
            embed = disnake.Embed(
                title="Quickorder Menu",
                description = str("YOU ARE ORDERING <" + part + ">. CONTINUE?"),
                color=disnake.Color.purple()
            )
            newbuttons = confirm()
            newbuttons.set_part(part); newbuttons.set_author(inter.author.id); newbuttons.set_qty(qty)
            await inter.send(embed=embed, view = newbuttons)
            
        elif (str(inter.author.id) in general.users):
            embed = disnake.Embed(
                title="Quickorder Menu",
                description = str("NO PART WAS FOUND. DID YOU MEAN..."),
                color=disnake.Color.purple()
            )
            helpme = qsearch.search()
            option = []
            
            for element in helpme.generate_close_results(str(part)):
              print (element)
              option.append(disnake.SelectOption(label = element))

            select = disnake.ui.StringSelect(options = option)

            async def changePart(interaction: disnake.MessageInteraction):
                part2 = (select.values)[0] 
                await interaction.response.send_message(
            content="You have selected " + str(select.values[0]), ephemeral=False)
                embed = disnake.Embed(
                    title="Quickorder Menu",
                    description = str("YOU ARE ORDERING <" + part2 + ">. CONTINUE?"),
                    color=disnake.Color.purple()
                )
                newbuttons = confirm()
                newbuttons.set_part(part2); newbuttons.set_author(inter.author.id); newbuttons.set_qty(qty)
                await inter.send(embed=embed, view = newbuttons)

            select.callback = changePart
            views = View()
            views.add_item(select)
            await inter.send(embed=embed, view = views)

        else:
            embed = disnake.Embed(
                title="Quickorder Menu",
                description = str("YOU MUST BE REGISTERTED TO ACCESS THESE FUNCITONS.\nUSE THE /register FUNCTION TO REGISTER AND CONTINUE."),
                color=disnake.Color.red()
            )
            await inter.send(embed=embed)


    @slash_command(
      name="searchorder",
      description="Searchorder Menu"
    )
    async def searchorder(self, inter, emoji_1: disnake.Emoji, emoji_2: disnake.Emoji, emoji_3: disnake.Emoji, title):
        embed = disnake.Embed(
          title=title,
          description="A new poll has been created!",
          color=disnake.Color.green()
        )
    @slash_command(
      name="submitorder",
      description="Converts your Cart to a PDF"
    )
    async def submitorder(self, inter):
        embed = disnake.Embed(
          title="Order Submission",
          description="Your order has been outputted below",
          color=disnake.Color.green()
        )
        #convert txt into file
        team = general.idtt[int(inter.author.id)]

        data_list = []
        with open("teams\\"+str(team)+".txt") as f:
            sectioned = f.read().split("\n")
            sectioned.pop(len(sectioned)-1)
            for order in sectioned:
                norder = (order.replace("?", " ")).split("%")
                norder[0] = str(datetime.today().strftime('%m-%d-%y'))
                data_list.append(norder)

        print(data_list)

        npdf = cpdf.pdfgenerator(data_list)
        npdf.generate()

        await inter.send(embed=embed)
        await inter.send(file=disnake.File('converter\\out.pdf'))
        open('teams\\"+str(team)+".txt', 'w').close() #wiping the file


def setup(bot):
  splitter = '%'
  with open ("resources\\binnumbers.txt") as f:
    for element in f:
      try:
        partstobin[(element.split(splitter)[0]).strip(" ")] = (element.split(splitter)[1])
      except:
        print(element.split(splitter))

  bot.add_cog(ordering(bot))
  print(f"> Extension {__name__} is ready")