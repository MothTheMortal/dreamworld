import discord
from discord.ext import commands
import config
from json import *
from traceback import format_exception
from discord.utils import get
from discord import app_commands
import asyncio
import json
import time
from random import choice
from discord import Embed
from datetime import datetime, timedelta


class Cog_Manager(commands.Cog):
    with open("data/command_details.json", "r") as json_file:
        command_details = load(json_file)
        help_details = command_details["help"]

    def __init__(self, client):
        self.client = client
        self.loaded_cogs = config.cogs

    @app_commands.command(name="runconsole")
    @app_commands.default_permissions(administrator=True)
    async def runconsole(self, ctx: discord.Interaction, command: str):
        await ctx.response.send_message(f"Running command: {command}")
        try:
            exec(command)
            x = await ctx.original_response()
            await x.reply("Command executed successfully")
        except Exception as e:
            x = await ctx.original_response()
            await x.reply(f"Error: {e}")
        x = self.client.get_channel(994217959260172308)
        msg = await x.fetch_message(1114625120288374824)
        for i in msg.embeds:
            print(i.description)


    @commands.Cog.listener()
    async def on_ready(self):
        print("My Guilds:")
        for i in self.client.guilds:
            print(i.name)
        print(f"Logged in as {self.client.user.name}#{self.client.user.discriminator}")
        try:
            synced = await self.client.tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)
        await self.client.change_presence(activity=discord.Game(name="Moth Simulator"))
        await self.giveaway_handler()

    async def giveaway_handler(self):
        while True:
            with open("data/giveaways.json", "r") as f:
                data = json.load(f)
            giveaways_list = [i for i in data.keys()]
            for msg_id in giveaways_list:
                if int(data[msg_id]["end_time"]) < time.time():
                    await self.giveaway_finish(str(msg_id))
            await asyncio.sleep(5)

    async def giveaway_finish(self, message_id: str):
        with open("data/giveaways.json", "r") as f:
            giveaway_data = json.load(f)[message_id]
            print("Giving ending: ")
            print(giveaway_data)

        try:
            winners = giveaway_data["winners"]
            guild: discord.Guild = self.client.get_guild(int(giveaway_data["guild_id"]))
            format_time = giveaway_data["format_time"]
            prize = giveaway_data["prize"]
            title = giveaway_data["title"]
            host = guild.get_member(int(giveaway_data["host_id"]))
            thumbnail_url = giveaway_data["thumbnail_url"]
            channel = guild.get_channel(int(giveaway_data["channel_id"]))

            giveaway_msg = await channel.fetch_message(int(message_id))

            reactions = giveaway_msg.reactions[0]

            users = []

            nobles = guild.get_role(996191436406018098)
            traveler = guild.get_role(1023914137895587970)
            treason = guild.get_role(1090184365566333009)
            safe = guild.get_role(1090185036688531466)

            async for user in reactions.users():
                try:
                    if user.bot or user.id == host.id or treason in user.roles or safe not in user.roles:
                        pass
                    else:
                        if nobles in user.roles:
                            [users.append(user.id) for _ in range(3)]
                        elif traveler in user.roles:
                            [users.append(user.id) for _ in range(2)]
                        else:
                            [users.append(user.id) for _ in range(1)]
                except Exception:
                    pass

            if len(users) >= winners:

                winners_list = []
                while len(winners_list) < winners:
                    winner = choice(users)
                    if winner not in winners_list:
                        winners_list.append(winner)

                win = []

                for i in winners_list:
                    if guild.get_member(i) is not None:
                        win.append(f"<@{i}>")

                description = f"""
                                        Winner(s): {", ".join(win)}\nEnded at: {format_time}
                                        """

                await channel.send(
                    f"🎉 **GIVEAWAY** 🎉 -> {giveaway_msg.jump_url}\n**Prize**: {prize}\n**Winner(s)**: {', '.join(win)}")


                giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
                giveaway_embed.set_footer(text="Giveaway Ended.")
                giveaway_embed.set_author(name=host.name, icon_url=host.avatar)
                if thumbnail_url != "":
                    try:
                        giveaway_embed.set_thumbnail(url=thumbnail_url)
                    except Exception:
                        pass

                await giveaway_msg.edit(embed=giveaway_embed)
            else:
                await channel.send(f"🎉 **GIVEAWAY** 🎉\n**Prize**: {prize}\n**Winner(s)**: No one")

                description = f"""
                                                    Winner(s): None\nEnded at: {format_time}
                                                    """

                giveaway_embed = Embed(title=title, description=description, color=discord.Color.red(), timestamp=datetime.now())
                giveaway_embed.set_footer(text="Giveaway Ended.")
                giveaway_embed.set_author(name=host.name, icon_url=host.avatar)
                if thumbnail_url != "":
                    try:
                        giveaway_embed.set_thumbnail(url=thumbnail_url)
                    except Exception:
                        pass
                await giveaway_msg.edit(embed=giveaway_embed)

        except Exception as ex:
            print(ex)

        with open("data/giveaways.json", "r") as f:
            data = json.load(f)
            del data[message_id]
        with open("data/giveaways.json", "w") as f:
            json.dump(data, f, indent=4)

    @app_commands.command(
        name="start_giveaway",
        description="Starts a giveaway."
    )
    @app_commands.describe(
        host="User who's hosting the giveaway",
        channel="Channel where the giveaway will be hosted.",
        winners="Number of winners.",
    )
    @app_commands.default_permissions(manage_messages=True)
    async def giveaway(self, ctx: discord.Interaction, host: discord.Member, channel: discord.TextChannel, winners: int,
                       days: float, hours: float, minutes: float, prize: str, thumbnail_url: str = ""):

        duration_secs = days * 86400 + hours * 3600 + minutes * 60
        delta_time = timedelta(days=days, hours=hours, minutes=minutes)
        unix_end_datetime = int((datetime.now() + delta_time).timestamp())

        format_time = f"<t:{unix_end_datetime}>"

        title = "🎉 " + prize + " 🎉"

        description = f"""
                    Number of Winners: {winners}
                    Ends: {format_time}
                    """

        giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
        giveaway_embed.set_footer(text="React to join giveaway.")
        giveaway_embed.set_author(name=host.name, icon_url=host.avatar)

        if thumbnail_url != "":
            try:
                giveaway_embed.set_thumbnail(url=thumbnail_url)
            except Exception:
                pass

        await ctx.response.send_message(f"Giveaway started for {prize}!", ephemeral=True)

        msg = await channel.send(embed=giveaway_embed)

        await msg.add_reaction("🎉")
        with open("data/giveaways.json", "r") as f:
            data = json.load(f)
        with open("data/giveaways.json", "w") as f:
            data[str(msg.id)] = {
                "guild_id": str(ctx.guild.id),
                "host_id": str(host.id),
                "winners": winners,
                "format_time": format_time,
                "prize": prize,
                "end_time": str(unix_end_datetime),
                "title": title,
                "thumbnail_url": thumbnail_url,
                "channel_id": str(channel.id),
                "message_id": str(msg.id)
            }
            json.dump(data, f, indent=4)

    @app_commands.command(
        name="reroll_giveaway",
        description="Re-rolls a giveaway."
    )
    @app_commands.describe(
        giveaway_msg="ID of the giveaway message which will be re-rolled.",
        host="User who's hosting the giveaway",
        channel="Channel where the giveaway will be hosted.",
        winners="Number of winners."
    )
    @app_commands.default_permissions(manage_messages=True)
    async def reroll_giveaway(self, ctx: discord.Interaction, giveaway_msg: str, host: discord.Member,
                              winners: int, channel: discord.TextChannel, prize: str):
        giveaway_msg = await channel.fetch_message(int(giveaway_msg))
        title = "🎉 " + prize + " 🎉"
        reactions = giveaway_msg.reactions[0]

        users = []
        nobles = ctx.guild.get_role(996191436406018098)
        traveler = ctx.guild.get_role(1023914137895587970)
        treason = ctx.guild.get_role(1090184365566333009)
        safe = ctx.guild.get_role(1090185036688531466)

        async for user in reactions.users():
            try:
                if user.bot or user.id == host.id or treason in user.roles or not safe in user.roles:
                    pass
                else:
                    if nobles in user.roles:
                        [users.append(user.id) for _ in range(3)]
                    elif traveler in user.roles:
                        [users.append(user.id) for _ in range(2)]
                    else:
                        [users.append(user.id) for _ in range(1)]
            except Exception:
                pass

        winners_list = []
        while len(winners_list) < winners:
            winner = choice(users)
            if winner not in winners_list:
                winners_list.append(winner)
        win = []

        for i in winners_list:
            if ctx.guild.get_member(i) is not None:
                win.append(f"<@{i}>")

        description = f"""
                                    Re-Rolled Winner(s): {", ".join(win)}
                                    """
        await channel.send(
            f"🎉 **GIVEAWAY** 🎉 -> {giveaway_msg.jump_url}\n**Prize**: {prize}\n**Re-Rolled Winner(s)**: {', '.join(win)}")

        giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
        giveaway_embed.set_footer(text="Giveaway Ended.")
        giveaway_embed.set_author(name=host.name, icon_url=host.avatar)
        await giveaway_msg.edit(embed=giveaway_embed)
        await ctx.response.send_message("Re-rolled!", ephemeral=True)



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
