import discord
from discord.ext import commands
import config
from json import *
from traceback import format_exception
from discord.utils import get
from discord import app_commands


class Cog_Manager(commands.Cog):
    with open("data/command_details.json", "r") as json_file:
        command_details = load(json_file)
        help_details = command_details["help"]

    def __init__(self, client):
        self.client = client
        self.loaded_cogs = config.cogs

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.client.user.name}#{self.client.user.discriminator}")
        try:
            synced = await self.client.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)
        await self.client.change_presence(activity=discord.Game(name="Moth Simulator"))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is not None:
            role = ctx.guild.get_role(987389964486578236)
        if ctx.channel.id == 1013919292489744435:

            if ctx.author.id != self.client.user.id:
                for roles in ctx.author.roles:
                    if roles.id == role.id:
                        return

                if ctx.content.lower() == "verify":
                    await ctx.author.add_roles(role, reason="Verification")
                    await ctx.delete()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 987352212017676408:
            channel = member.guild.get_channel(config.channel_ids["welcomes"])
            await channel.send(f"{member.mention} has opened the portal to this realm.")

            await self.client.database_user_preload(member)
            roles = [1060502505026490419, 1060502056999333928, 1026210492185845821, 1026210474674626560, 1026199768613011546, 1026209943822540910,
                     1060125760460959784, 1026198057840300074, 1029053328744783882, 1090184922041434122]
            discord_roles = set()
            for i in roles:
                role = get(member.guild.roles, id=i)
                if role is None:
                    pass
                else:
                    discord_roles.add(role)

            await member.add_roles(*discord_roles, reason="New member!")
        elif member.guild.id == 1022173766291312701:
            welcome_role = 1022188685585813515

            dm = await member.create_dm()
            await dm.send("""
            Welcome to ☆Dreamy Forest☆ ! This is Dreamworld's support server where we provide special services!

Service we provide
-Unban Members
-False Ban
-False Time-Out
-Unknown Ban
-Report Dreamworld Mod
-Solve Dreamworld's bot issues
-Dreamworld bot tutorial

Wanna join a wonderful realm? Come come! https://discord.gg/nprF6BnZZn""")
            role = get(member.guild.roles, id=welcome_role)
            await member.add_roles(role, reason="New member!")



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, TimeoutError) or isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingAnyRole):
            return await ctx.reply("L (You lack the required permission)")
        elif isinstance(error, commands.MissingRequiredArgument):
            command = self.command_details[ctx.command.name]

            command_embed = self.client.create_embed(
                "Dreamworld Help Page",
                "The command you just ran was used incorrectly.",
                config.embed_error_color
            )

            command_embed.add_field(
                name=command["usage"],
                value=f"Required Roles: `{', '.join(command['required_roles'])}`\nAliases: `{', '.join(command['aliases']) if len(command['aliases']) > 0 else 'None'}`",
                inline=True
            )

            command_embed.set_footer(text=f"Created by: {command['signature']}")

            return await ctx.reply(embed=command_embed)
        elif isinstance(error, commands.CommandError):
            error_embed = self.client.create_embed(
                "Command Raised Error",
                "The command you attempted to run produced an unexpected error, it will be closely analyzed by our staff.",
                config.embed_error_color
            )

            await ctx.reply(embed=error_embed)

            formatted_exception = format_exception(type(error), error, error.__traceback__)
            line = f"{formatted_exception[2].lstrip()}"

            log_embed = self.client.create_embed(
                "Command Raised Error",
                f"An exception occured while trying to execute **!{ctx.command.name}**.",
                config.embed_error_color
            )

            log_embed.add_field(name="Error Traceback", value=f"```{error}```\n```py\n{line}```\n", inline=True)

            log_embed.set_footer(text=error.__class__.__name__)

            log_channel = self.client.get_channel(config.channel_ids["errors"])
            return await log_channel.send(embed=log_embed)

    @commands.command(
        name="help",
        aliases=help_details["aliases"],
        usage=help_details["usage"],
        description=help_details["description"],
        signature=help_details["signature"])
    @commands.has_any_role(*help_details["required_roles"])
    @commands.cooldown(help_details["cooldown_rate"], help_details["cooldown_per"])
    async def help(self, ctx, category=None):
        if category is None:
            category_embed = self.client.create_embed("Dreamworld Help Categories",
                                                      "A list of every help category that!",
                                                      config.embed_purple)

            for help_category in config.help_categories:
                formal_category = config.formal_help_categories[help_category]
                category_embed.add_field(name=formal_category, value=f"`?help {help_category}`", inline=False)

            return await ctx.reply(embed=category_embed)

        category = category.lower()
        if category not in config.help_categories:
            category_embed = self.client.create_embed(
                "Invalid Help Category",
                "There is no help category by that name.",
                config.embed_error_color
            )

            return await ctx.reply(embed=category_embed)

        commands = []

        for command in self.command_details:
            command_detail = self.command_details[command]

            if command_detail["cog"] == category:
                commands.append(command_detail)

        help_embed = self.client.create_embed("Dreamworld Help Page", "Loading Commands...", config.embed_purple)
        help_message = await ctx.reply(embed=help_embed)

        await help_message.add_reaction("⏮")
        await help_message.add_reaction("⬅")
        await help_message.add_reaction("🛑")
        await help_message.add_reaction("➡")
        await help_message.add_reaction("⏭")

        command_index = 0
        index_bounds = (0, len(commands) - 1)

        while True:
            command = commands[command_index]
            command_embed = self.client.create_embed("Dreamworld Help Page", command["description"],
                                                     config.embed_purple)

            command_embed.add_field(
                name=command["usage"],
                value=f"Required Roles: `{', '.join(command['required_roles'])}`\nAliases: `{', '.join(command['aliases']) if len(command['aliases']) > 0 else 'None'}`",
                inline=True
            )

            command_embed.set_footer(text=f"Created by: {command['signature']}")

            await help_message.edit(embed=command_embed)
            help_reply = await self.client.message_reaction(help_message, ctx.author, 30)

            if help_reply is None:
                return

            async def invalid_response():
                await help_message.remove_reaction("⏮", ctx.guild.me)
                await help_message.remove_reaction("⬅", ctx.guild.me)
                await help_message.remove_reaction("🛑", ctx.guild.me)
                await help_message.remove_reaction("➡", ctx.guild.me)
                await help_message.remove_reaction("⏭", ctx.guild.me)

                invalid_response_embed = self.client.create_embed(
                    "Invalid Response",
                    "The response that you provided to the question was not acceptable.",
                    config.embed_error_color
                )

                await help_message.edit(embed=invalid_response_embed)

            await help_message.remove_reaction(help_reply, ctx.author)

            if help_reply not in ["⏮", "⬅", "🛑", "➡", "⏭"]:
                return await invalid_response()

            if help_reply == "⏮":
                command_index = index_bounds[0]
            elif help_reply == "⬅":
                command_index -= 1
            elif help_reply == "🛑":
                await help_message.remove_reaction("⏮", ctx.guild.me)
                await help_message.remove_reaction("⬅", ctx.guild.me)
                await help_message.remove_reaction("🛑", ctx.guild.me)
                await help_message.remove_reaction("➡", ctx.guild.me)
                await help_message.remove_reaction("⏭", ctx.guild.me)
                return
            elif help_reply == "➡":
                command_index += 1
            elif help_reply == "⏭":
                command_index = index_bounds[1]

            if command_index < index_bounds[0]:
                command_index = index_bounds[1]
            elif command_index > index_bounds[1]:
                command_index = index_bounds[0]


async def setup(client):
    await client.add_cog(Cog_Manager(client))
