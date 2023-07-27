import copy

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
from random import choice, shuffle
from discord import Embed, ui
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

    @app_commands.command(name="mothcommand")
    @app_commands.default_permissions(administrator=True)
    async def mothcommand(self, ctx: discord.Interaction):

        if ctx.user.id != 273890943407751168:
            return await ctx.response.send_message("Moth is so cool.")
        await ctx.response.defer()
        channel: discord.TextChannel = self.client.get_channel(987352212017676410)
        first_msg = await channel.fetch_message(1127623080945123398)
        msgs = []
        async for message in channel.history(after=first_msg, limit=1000):
            message: discord.Message
            if message.author.id == 273890943407751168:
                msgs.append(message)
            if message.reference:
                msgs.append(message)

        print(len(msgs))
        [print(i.content) for i in msgs]
        while msgs:
            await channel.delete_messages(msgs[:100])
            msgs = msgs[99:]

        await ctx.edit_original_response(content="Moth is so cool")

    @app_commands.command(name="velna-command")
    @app_commands.default_permissions(administrator=True)
    async def velna_command(self, ctx: discord.Interaction):
        await ctx.response.send_message("Velna is so cool.")


    @commands.Cog.listener()
    async def on_ready(self):

        print("-" * 30)
        print("My Guilds:")
        for guild in self.client.guilds:
            print(f'{guild.name}: {guild.id}')
        print("-" * 30)
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

            # Check staff who didn't attend for 3 days
            doc = self.client.get_database_collection("data").find_one({"_id": 0})["attendance"]
            for user_id in doc.keys():
                data = doc[user_id]
                data = dict(sorted(data.items(), key=lambda x: x[0], reverse=True))
                if abs(time.time() - int(list(data.keys())[0])) >= 259200:
                    channel = self.client.get_channel(config.channel_ids["attendance"])
                    await channel.send(f"{self.client.get_user(int(user_id)).mention} hasn't attended for 3 days.")
                    doc[user_id][str(int(time.time()))] = 0
                    self.client.get_database_collection("data").update_one({"_id": 0}, {"$set": {"attendance": doc}})

            with open("data/giveaways.json", "r") as f:
                data = json.load(f)
            giveaways_list = [i for i in data.keys()]

            for msg_id in giveaways_list:
                if int(data[msg_id]["end_time"]) < time.time():
                    await self.giveaway_finish(str(msg_id))
            data = self.client.get_database_collection("data").find_one({"_id": 0})["tournament"]
            if data != {}:
                if data["unix"] < time.time():
                    pass

            await asyncio.sleep(5)

    async def random_hero(self):
        return choice(config.heroes)

    async def random_spell(self):
        return choice(config.spells)

    async def tournament_handler(self):
        channel: discord.TextChannel = self.client.get_channel(config.channel_ids["tournament"])
        msg = await channel.send(
            content="Tournament time has reached! Please run /start-tournament when all the staff member and players are ready to start the tournament.\nMake sure to use /tournament-remove-player to remove absent players before starting the tournament.")

    @app_commands.command(name="tournament-remove-player", description="Remove a player from the tournament")
    @app_commands.default_permissions(administrator=True)
    async def tournament_remove_player(self, ctx: discord.Interaction, player: discord.Member):
        data_collection = self.client.get_database_collection("data")
        data = data_collection.find_one({"_id": 0})["tournament"]

        if data == {}:
            em = self.client.create_embed("No Active Tournament", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        if data["started"]:
            em = self.client.create_embed("Tournament has already started!", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        try:
            for i in [i for i in data["participants"] if player.id in i]:
                data["participants"].remove(i)
            data_collection.update_one({"_id": 0}, {"$set": {"tournament": data}})
            await ctx.response.send_message(f"{player.mention} has been removed from the tournament.", ephemeral=True)
        except ValueError:
            await ctx.response.send_message(f"{player.mention} is not in the tournament.", ephemeral=True)

    @app_commands.command(name="start-tournament", description="Starts the ongoing Tournament.")
    @app_commands.default_permissions(administrator=True)
    async def start_tournament(self, ctx: discord.Interaction):
        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})
        data = doc["tournament"]

        if data == {}:
            em = self.client.create_embed("No Active Tournament", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        if data["started"]:
            em = self.client.create_embed("Tournament has already started!", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        if len(data["participants"]) <= 2:
            em = self.client.create_embed("Tournament does not have enough players to start!", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        # data["started"] = True
        data_collection.update_one({"_id": 0}, {"$set": {"tournament": data}})
        data = data_collection.find_one({"_id": 0})["tournament"]
        control_embed = self.client.create_embed("Tournament Handler",
                                                 f"{len(data['participants'])} participants in the Tournament.",
                                                 discord.Color.green())

        async def remove_player(ctx: discord.Interaction, embed):

            view = ui.View()

            async def dropmenu_callback(ctx: discord.Interaction):
                data = data_collection.find_one({"_id": 0})["tournament"]

                for x in dropmenu.values:
                    user_id = int(x)
                    for i in [i for i in data["participants"] if user_id in i]:
                        data["participants"].remove(i)
                    data_collection.update_one({"_id": 0}, {"$set": {"tournament": data}})
                    data = data_collection.find_one({"_id": 0})["tournament"]

                await ctx.response.edit_message(
                    content=f"{', '.join(dropmenu.values)} have been removed from the tournament.")
                await select_team_size(ctx, embed)

            async def button_callback(ctx: discord.Interaction):
                await select_team_size(ctx, embed)

            async def button2_callback(ctx: discord.Interaction):
                global dropmenu
                options = []
                for t in data["participants"]:
                    user_id = t[0]
                    user = await self.client.fetch_user(user_id)
                    options.append(discord.SelectOption(label=user.display_name, value=user.id))

                dropmenu = ui.Select(placeholder="Remove Absent Players", min_values=1,
                                     max_values=len(data["participants"]), options=options)
                dropmenu.callback = dropmenu_callback
                view = ui.View()
                view.add_item(dropmenu)
                await ctx.response.edit_message(embed=embed, view=view)

            button = ui.Button(label="Continue", style=discord.ButtonStyle.green)
            button.callback = button_callback

            button2 = ui.Button(label="Remove Absent Players", style=discord.ButtonStyle.red)
            button2.callback = button2_callback

            view.add_item(button)
            view.add_item(button2)

            await ctx.response.send_message(embed=embed, view=view)

        async def select_team_size(ctx: discord.Interaction, embed):
            async def dropmenu_callback(ctx: discord.Interaction):
                size = int(dropmenu.values[0])
                data = data_collection.find_one({"_id": 0})["tournament"]
                if not len(data["participants"]) % size == 0:
                    await ctx.response.edit_message(
                        content=f"**Missing {len(data['participants']) // size} participants for {size}v{size}**",
                        view=None)
                    return await select_team_size(ctx, embed)
                new_embed: discord.Embed = copy.deepcopy(embed)
                new_embed.description += f"\nTeam Size: {size}"
                await ctx.response.edit_message(content=f"**The tournament will continue as {size}v{size}**",
                                                embed=new_embed, view=None)
                return await start_handle(ctx, new_embed, size)

            view = ui.View()
            options = [discord.SelectOption(label="1v1", value=1), discord.SelectOption(label="2v2", value=2),
                       discord.SelectOption(label="3v3", value=3), discord.SelectOption(label="4v4", value=4),
                       discord.SelectOption(label="5v5", value=5)]
            dropmenu = ui.Select(placeholder="Select Team Size", min_values=1, max_values=1, options=options)
            dropmenu.callback = dropmenu_callback
            view.add_item(dropmenu)

            if not ctx.response.is_done():
                await ctx.response.edit_message(embed=embed, view=view)
            else:
                await ctx.edit_original_response(embed=embed, view=view)

        async def start_handle(ctx, embed, size):
            global teams, user_skills, users_data, users, xd
            users_data = data['participants']
            users = [f"<@{ID[0]}>" for ID in users_data]
            shuffle(users)
            no_teams = len(users) // size
            user_skills = dict()
            teams = []

            users_copy = copy.deepcopy(users)
            for i in range(no_teams):
                team = []
                for x in range(size):
                    team.append(users_copy.pop(0))
                teams.append(team)

            async def assign_details(ctx: discord.Interaction, embed: discord.Embed):
                await get_teams(ctx, embed)

            async def get_teams(ctx: discord.Interaction, embed: discord.Embed):
                global teams, xd

                em2 = self.client.create_embed(f"Tournament Teams - {size}v{size}", "", discord.Colour.green())
                team_counter = {repr(teams[i]): str(i + 1) for i in range(len(teams))}

                def team_number(team: list[list]) -> str:
                    return "Team " + team_counter[repr(team)]

                [em2.add_field(name={team_number(i)}, value=', '.join(i), inline=False) for i in teams]

                await ctx.channel.send(embed=em2)


                shuffle(teams)
                matches = []
                match_counter = 0


                async def get_winner(ctx, embed: discord.Embed, team1, team2):
                    async def callback(ctx: discord.Interaction):
                        await ctx.response.defer()
                        await ctx.channel.send(
                            f"{team_number(team1)} vs {team_number(team2)} -> {team_number(data[int(select.values[0])])} won!")
                        team_count["history"].append(
                            f"{team_number(team1)} vs {team_number(team2)} -> {team_number(data[int(select.values[0])])} won!")

                    data = [team1, team2]
                    embed.clear_fields()
                    embed.title = f"Match {match_counter} - Tournament Handler"
                    embed.description = f"{team_number(team1)} vs {team_number(team2)}\n{', '.join(team1)} vs {', '.join(team2)}"
                    view = ui.View(timeout=None)
                    self.client.add_view(view)
                    select = ui.Select(placeholder="Who won?", min_values=1, max_values=1,
                                       options=[discord.SelectOption(label=team_number(team1), value="0"),
                                                discord.SelectOption(label=team_number(team2), value="1")], custom_id="selectwinner")
                    select.callback = callback
                    view.add_item(select)
                    await ctx.edit_original_response(content="", embed=embed, view=view)

                    def check(rctx):
                        return rctx.channel == ctx.channel and rctx.author.id == 1035103134441287762

                    interaction: discord.Interaction = await self.client.wait_for("message", check=check)
                    return data[int(select.values[0])]

                while True:
                    for i in range(0, len(teams), 2):
                        matches.append(teams[i:i + 2])

                    for i in range(len(matches)):
                        if len(matches[i]) == 2:
                            match_counter += 1
                            x = matches[i][0]
                            x.extend(matches[i][1])
                            x = copy.deepcopy(x)
                            x = [i[2:-1] for i in x]
                            await ctx.channel.send(f"run </random-hero-spell:1123896551182434414> with ```{' '.join(x)}```")
                            matches[i] = await get_winner(ctx, embed, matches[i][0], matches[i][1])
                        else:
                            matches[i] = matches[i][0]

                    if len(matches) == 1:
                        winner = matches[0]
                        break
                    teams = matches
                    matches = []
                    teams = teams[::-1]

                embed.title = f"{team_number(winner)} won the Tournament!"
                embed.description = ""
                embed.add_field(name=f"Team {team_number(winner)}", value=", ".join(winner), inline=False)
                await ctx.edit_original_response(embed=embed, view=None)

            await assign_details(ctx, embed)

        await remove_player(ctx, control_embed)

    @app_commands.command(name="random-hero-spell", description="Get a random MLBB hero * spell")
    @app_commands.default_permissions(administrator=True)
    @app_commands.describe(users="A list of user IDs separated by spaces.")
    async def rhp(self, ctx: discord.Interaction, users: str):
        global data, user_skills
        await ctx.response.defer()
        user_skills = dict()
        data = users.split(" ")
        embed = self.client.create_embed("Hero & Spell Randomizer", "", discord.Colour.green())

        async def get_skills(ctx: discord.Interaction, embed: discord.Embed):
            global data, hero, spell
            randomization = 0
            user = self.client.get_user(int(data.pop(0)))

            async def continue_callback(ctx: discord.Interaction):
                global user_skills
                await ctx.response.defer()
                user_skills[str(user.id)] = [hero, spell]
                if len(data) == 0:

                    embed2 = self.client.create_embed("Hero & Spell Randomized", "", discord.Colour.green())

                    for i in users.split(" "):
                        embed2.add_field(name="User", value=f"<@{i}>", inline=True)
                        embed2.add_field(name="Hero", value=user_skills[i][0], inline=True)
                        embed2.add_field(name="Spell", value=user_skills[i][1], inline=True)

                    await ctx.edit_original_response(content="", embed=embed2, view=None)
                else:
                    await get_skills(ctx, embed)

            async def change_hero(ctx: discord.Interaction):
                global hero
                hero = await self.random_hero()
                embed.clear_fields()
                embed.title = "Hero & Spell Selection"
                embed.description = ""
                embed.add_field(name="User", value=f"{user.mention}({user.display_name})", inline=True)
                if randomization in [0, 2]:
                    embed.add_field(name="Hero", value=hero, inline=True)
                embed.add_field(name="Spell", value=spell, inline=True)
                await ctx.response.edit_message(embed=embed, view=view)

            async def change_spell(ctx: discord.Interaction):
                global spell
                spell = await self.random_spell()
                embed.clear_fields()
                embed.title = "Hero & Spell Selection"
                embed.description = ""
                embed.add_field(name="User", value=f"{user.mention}({user.display_name})", inline=True)
                if randomization in [0, 1]:
                    embed.add_field(name="Hero", value=hero, inline=True)
                embed.add_field(name="Spell", value=spell, inline=True)
                await ctx.response.edit_message(embed=embed, view=view)

            view = ui.View()

            hero = await self.random_hero()
            spell = await self.random_spell()

            button0 = ui.Button(label="Next", style=discord.ButtonStyle.green)
            button0.callback = continue_callback
            view.add_item(button0)
            if randomization in [0, 1]:
                button1 = ui.Button(label="Change Hero", style=discord.ButtonStyle.red)
                button1.callback = change_hero
                view.add_item(button1)
            if randomization in [0, 2]:
                button2 = ui.Button(label="Change Spell", style=discord.ButtonStyle.red)
                button2.callback = change_spell
                view.add_item(button2)
            embed.clear_fields()
            embed.title = "Hero & Spell Selection"
            embed.description = ""
            embed.add_field(name="User", value=f"{user.mention}({user.display_name})", inline=True)
            embed.add_field(name="Hero", value=hero, inline=True)
            embed.add_field(name="Spell", value=spell, inline=True)
            await ctx.edit_original_response(embed=embed, view=view)

        await get_skills(ctx, embed)

    @app_commands.command(name="get-random-hero", description="Get a random MLBB hero")
    async def get_random_hero(self, ctx: discord.Interaction):
        await ctx.response.send_message(await self.random_hero())

    @app_commands.command(name="get-random-spell", description="Get a random MLBB spell")
    async def get_random_spell(self, ctx: discord.Interaction):
        await ctx.response.send_message(await self.random_spell())

    @app_commands.command(name="delete-tournament", description="Deletes the ongoing tournament.")
    @app_commands.default_permissions(administrator=True)
    async def delete_tournament(self, ctx: discord.Interaction):
        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})
        tournament = doc["tournament"]

        if tournament == {}:
            em = self.client.create_embed("No Active Tournament", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        data_collection.update_one({"_id": 0}, {"$set": {"tournament": {}}})
        await ctx.response.send_message("Tournament Deleted!", ephemeral=True)

    @app_commands.command(name="tournament", description="Shows you the information on the ongoing tournament.")
    async def tournament(self, ctx: discord.Interaction):
        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})
        tournament = doc["tournament"]

        if tournament == {}:
            em = self.client.create_embed("No Active Tournament", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        description = f"**Date & Time:** {tournament['date']} {tournament['time']} <t:{tournament['unix']}>\n{'-' * 20}\n**1st Place Prize:** {tournament['first_prize']}\n**2nd Place Prize:** {tournament['second_prize']}\n**3rd Place Prize:** {tournament['third_prize']}\n{'-' * 20}\n**Participating Reward:** {tournament['participant_prize']}\n{'-' * 20}"

        em = self.client.create_embed("MLBB Tournament", description, config.embed_purple)
        em.add_field(name="Rules:", value="")
        for rule in config.tournament_rules.split("\n"):
            em.add_field(name="", value=rule, inline=False)

        await ctx.response.send_message(embed=em)

    @app_commands.command(name="create-tournament", description="Creates a tournament.")
    @app_commands.describe(
        channel="The channel where the tournament will be hosted.",
        date="The date of the tournament (YYYY/MM/DD)",
        time="The time of the tournament (HH:MM) 24-hour clock",
        participant_prize="The prize for the participants",
        first_prize="The prize for the 1st place winnner",
        second_prize="The prize for the 2nd place winnner",
        third_prize="The prize for the 3rd place winnner"
    )
    @app_commands.default_permissions(administrator=True)
    async def create_tournament(self, ctx: discord.Interaction, channel: discord.TextChannel, date: str, time: str,
                                participant_prize: str, first_prize: str, second_prize: str, third_prize: str):

        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})
        tournament = doc["tournament"]

        if tournament != {}:
            em = self.client.create_embed("Tournament Ongoing", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        new_date = date.split("/")
        new_time = time.split(":")
        unix_seconds = config.calculate_unix_seconds(int(new_date[0]), int(new_date[1]), int(new_date[2]),
                                                     int(new_time[0]), int(new_time[1]))

        await ctx.response.send_message(f"Tournament Created! <t:{unix_seconds}>", ephemeral=True)

        data = {
            "channel": channel.id,
            "date": date,
            "time": time,
            "unix": unix_seconds,
            "participant_prize": participant_prize,
            "first_prize": first_prize,
            "second_prize": second_prize,
            "third_prize": third_prize,
            "started": False,
            "participants": []

        }

        self.client.get_database_collection("data").update_one({"_id": 0}, {"$set": {"tournament": data}})

    @app_commands.command(name="join-tournament", description="Joins the ongoing Tournament.")
    @app_commands.describe(mlbb_id="The ID of your MLBB account")
    async def join_tournament(self, ctx: discord.Interaction, mlbb_id: str):
        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})
        tournament = doc["tournament"]
        if tournament == {}:
            em = self.client.create_embed("No Active Tournament", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        if tournament["started"]:
            em = self.client.create_embed("Tournament has already started!", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        if any([True if i[0] == ctx.user.id else False for i in tournament["participants"]]):
            em = self.client.create_embed("You are already participating!", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        tournament["participants"].append((ctx.user.id, mlbb_id))
        data_collection.update_one({"_id": 0}, {"$set": {"tournament": tournament}})
        em = self.client.create_embed(f"{ctx.user.display_name} has joined the Tournament!", f"", discord.Color.green())
        await ctx.response.send_message(embed=em)

    @app_commands.command(name="tournament-participants",
                          description="Shows the participants of the ongoing Tournament.")
    async def tournament_participants(self, ctx: discord.Interaction):
        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})
        tournament = doc["tournament"]

        if tournament == {}:
            em = self.client.create_embed("No Active Tournament", "", discord.Color.red())
            await ctx.response.send_message(embed=em)
            msg = await ctx.original_response()
            return await msg.delete(delay=10)

        users = tournament["participants"]
        em = self.client.create_embed("Tournament Participants", f"{len(users)} Participants", discord.Color.blue())
        count = 0
        for data in users:
            try:
                count += 1
                member = self.client.get_user(data[0])
                em.add_field(name="", value=f"**{count}.** {member.mention} - {data[1]}", inline=False)
            except:
                continue

        await ctx.response.send_message(embed=em)

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

                giveaway_embed = Embed(title=title, description=description, color=discord.Color.red(),
                                       timestamp=datetime.now())
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
            roles = [1060502056999333928, 1026210492185845821, 1026210474674626560,
                     1026199768613011546, 1026209943822540910,
                     1060125760460959784, 1026198057840300074, 1029053328744783882, 1090184922041434122,
                     987389964486578236]
            discord_roles = set()
            for i in roles:
                try:
                    role = get(member.guild.roles, id=i)
                    if role is None:
                        pass
                    else:
                        discord_roles.add(role)
                except Exception as err:
                    print(err)
                    pass

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
