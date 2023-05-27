import discord
from discord.ext import commands
from time import monotonic
import config
from requests import get
import json
import asyncio
import time
from discord import app_commands, Embed
from discord.ext import tasks
from datetime import datetime, timedelta, timezone
from discord.ui import Button, View
from random import choice, sample
from pytube import YouTube
from os import remove
class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="ping",
                          description="Checks your ping.")
    async def ping(self, ctx: discord.Interaction):
        before = monotonic()
        ping_embed = self.client.create_embed("🏓 Ping!", "Processing Response...", config.embed_error_color)
        await ctx.response.send_message(embed=ping_embed)
        pong_message = await ctx.original_response()

        ping = round((monotonic() - before) * 1000)
        pong_embed = self.client.create_embed("🏓 Pong!", "Response Processed!", config.embed_info_color)
        pong_embed.add_field(name="Response Time", value=f"Response took {ping} ms")
        await pong_message.edit(embed=pong_embed)
        
    @app_commands.command(name="downloadaudio")
    async def downloadaudio(self, ctx: discord.Interaction, link: str):
        await ctx.response.send_message("Downloading Audio.")
        yt = YouTube(link)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path="./pics/", filename=f"{yt.title}.mp3")
        channel: discord.TextChannel = ctx.channel
        file = discord.File(f"pics/{yt.title}.mp3")
        await channel.send(file=file, reference=ctx.message)
        remove(f"pics/{yt.title}.mp3")

    @app_commands.command(name="kill",
                          description="Kill a user!")
    async def kill(self, ctx: discord.Interaction, user: discord.Member):
        if user.id == ctx.user.id:
            await ctx.response.send_message(f"{ctx.user.mention} has suicidal tendencies and requires mental support.")
        elif user.id == 940570942332092486:
            await ctx.response.send_message(
                f"{ctx.user.mention} has tried to kill the Owner of the Universe itself, and has been blown into smithereens by Hidaki's Rocket Launcher.")
        elif user.id == 1035103134441287762:
            await ctx.response.send_message(f"{ctx.user.mention} has tried to kill God, but ended up dying himself.")
        elif user.id == 478552612657037315:
            await ctx.response.send_message(
                f"Before {ctx.user.mention} even thought of killing Hidaki, his whole being poofed from existence; akin to being Thanos snapped.")
        elif user.id == 273890943407751168:
            await ctx.response.send_message(
                f"{ctx.user.mention} has tried to kill the Creator of God himself, and now lost all their stars.")
        elif user.id == 987228839212089365:
            await ctx.response.send_message(
                f"{ctx.user.mention} has tried to kill {user.mention} but was stabbed by Atriz before he could even come close.")
        elif user.id == 835436949065957416:
            await ctx.response.send_message(
                f"{ctx.user.mention} has tried to kill {user.mention} but was lit on fire by Aria.")
        elif user.id == 369817231498018816:
            await ctx.response.send_message(
                f"{ctx.user.mention} has tried to kill {user.mention} but had their ass gorilla glued by Ivy.")

        else:
            await ctx.response.send_message(f"{ctx.user.mention} has killed {user.mention}")

    @app_commands.command(name="confess",
                          description="Confess something anonymously.")
    async def confess(self, ctx: discord.Interaction, text: str):
        collection = self.client.get_database_collection("data")
        collection.update_one({'_id': 0}, {"$inc": {"confession_count": 1}})
        profile = collection.find_one({"_id": 0})
        count = profile["confession_count"]

        await ctx.response.send_message(
            f":ballot_box_with_check: Confession has been sent to <#{config.channel_ids['confession']}> ",
            ephemeral=True)
        confess_channel = self.client.get_channel(config.channel_ids["confession"])

        confess_embed = self.client.create_embed(
            f"Anonymous Confession (#{count})",
            f'"{text}"',
            config.embed_info_color
        )

        await confess_channel.send(embed=confess_embed)

        log_channel = self.client.get_channel(config.channel_ids["logs2"])
        log_embed = self.client.create_embed(
            f"Confession Log (#{count})",
            f'"{text}"',
            config.embed_info_color
        )
        log_embed.add_field(
            name="Submitted by:",
            value=f"{ctx.user.mention}",
            inline=True
        )
        await log_channel.send(embed=log_embed)

    @app_commands.command(name="quote",
                          description="Tells a random Zen Quote.")
    async def quote(self, ctx: discord.Interaction):
        response = get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.response.send_message(quote)

    @app_commands.command(name="riddle",
                          description="Asks a random riddle.")
    async def riddle(self, ctx: discord.Interaction):
        response = get("https://riddles-api.vercel.app/random")
        json_data = json.loads(response.text)
        riddle = json_data['riddle']
        ans = json_data['answer']
        riddle_embed = self.client.create_embed(
            f"Riddle:",
            f"{riddle}\nAnswer will be given automatically in 30 seconds.",
            config.embed_info_color
        )
        await ctx.response.send_message(embed=riddle_embed)
        og = await ctx.original_response()
        await asyncio.sleep(5)
        await og.reply(f"Answer: {ans}")

    @app_commands.command(name="snowball",
                          description="Throws a snowball at a user.")
    @app_commands.checks.cooldown(1, 86400)
    async def snowball(self, ctx: discord.Interaction, user: discord.Member):
        if ctx.channel_id not in [1036274705805607013, 1023478164682440805, 1045760539109883908, 987352212017676410]:
            fail_embed = self.client.create_embed(
                "Invalid response",
                "Command can only be used in <#1036274705805607013> or <#1045760539109883908>.",
                config.embed_error_color
            )
            return await ctx.response.send_message(embed=fail_embed)
        if ctx.user == user:
            fail_embed = self.client.create_embed(
                "Invalid response",
                "You cannot attack yourself with a snowball.",
                config.embed_red
            )
            return await ctx.response.send_message(embed=fail_embed)

        user_collection = self.client.get_database_collection("users")
        user_profile = user_collection.find_one({"_id": user.id})
        ctx_profile = user_collection.find_one({"_id": ctx.id})
        user_bal = user_profile["star"]
        ctx_bal = ctx_profile["star"]

        if not user_bal >= 50:
            fail_embed = self.client.create_embed(
                "Invalid response",
                f"{user.name} does not have enough stars.",
                config.embed_red
            )
            return await ctx.response.send_message(embed=fail_embed)
        if not ctx_bal >= 50:
            fail_embed = self.client.create_embed(
                "Invalid response",
                f"You don't have enough stars.",
                config.embed_red
            )
            return await ctx.response.send_message(embed=fail_embed)

        attack_embed = self.client.create_embed(
            f"{ctx.user.name} has thrown a snowball towards {user.name}",
            f"{user.mention} has 5 minutes to dodge.\nIf {user.name} dodges; 50 stars is stolen from you, otherwise you steal 50 stars from {user.name}",
            config.embed_purple
        )
        attack_embed.set_footer(text="Dodge by reacting to the message.")

        await ctx.response.send_message(embed=attack_embed)

        msg = await ctx.original_response()

        await msg.add_reaction("<:Y4_greenverification:1022441184934768701>")

        await user.send(
            f"Someone has thrown a snowball to you in <#{msg.channel.id}>. Dodge to avoid losing any stars.")
        shop_reply = await self.client.message_reaction(msg, user, 300)

        async def stolen():
            stolen_embed = self.client.create_embed(
                f"{ctx.user.name} has succesfully hit {user.name} with a snowball",
                f"{ctx.user.name} has stolen 50 coins from {user.name}.",
                config.embed_red
            )

            await msg.edit(embed=stolen_embed)
            await msg.remove_reaction(shop_reply, ctx.user)

        if shop_reply is None:
            user_collection.update_one({"_id": user.id}, {"$inc": {"star": -50}})
            user_collection.update_one({"_id": ctx.id}, {"$inc": {"star": 50}})

            await ctx.user.send(f"You have successfully stolen 50 coins from {user.name}.")
            await user.send(f"{ctx.user.name} has stolen 50 coins from you!")
            return await stolen()

        async def dodged():
            dodged_embed = self.client.create_embed(
                f"{user.name} has successfully dodged {ctx.user.name}'s snowball",
                f"{user.name} has stolen 50 coins from {ctx.user.name}",
                config.embed_red
            )

            await msg.edit(embed=dodged_embed)
            await msg.remove_reaction(shop_reply, ctx.user)

        if shop_reply in ["<a:Y4_greenverification:1022441184934768701>"]:
            user_collection.update_one({"_id": ctx.id}, {"$inc": {"star": -50}})
            user_collection.update_one({"_id": user.id}, {"$inc": {"star": 50}})
            return await dodged()
        print(shop_reply)

    @app_commands.command(
        name="msg_monthly"
    )
    async def monthlylb(self, ctx: discord.Interaction, places: int = 10):
        class LeaderBoardPosition:
            def __init__(self, id, coins):
                self.id = id
                self.coins = coins

        leaderboard = []
        collection = self.client.get_database_collection("data")
        profile = collection.find_one({"_id": 0})
        name_monthly = profile["monthly_time"]

        with open("data/msg_monthly.json", "r") as file:
            data = json.load(file)
        user_ids = list(data["users"].keys())
        user_msgs = []
        for i in user_ids:
            user_msgs.append(data["users"][i]["messages"])

        user_collection = {user_ids[i]: user_msgs[i] for i in range(len(user_ids))}

        for key, ele in user_collection.items():
            leaderboard.append(LeaderBoardPosition(key, ele))

        top = sorted(leaderboard, key=lambda x: x.coins, reverse=True)

        leaderboard_embed = self.client.create_embed(
            "Dreamworld Leaderboard",
            f"The top {places} chattiest people this {name_monthly} in Dreamworld!",
            config.embed_info_color
        )

        for i in range(1, places + 1, 1):
            try:
                value_one = top[i - 1].id
                value_two = top[i - 1].coins
                leaderboard_embed.add_field(
                    name=f"{i}. :thought_balloon:  {value_two}",
                    value=f"<@{value_one}>",
                    inline=False
                )
            except IndexError:
                leaderboard_embed.add_field(name=f"**<< {i} >>**", value="N/A | NaN", inline=False)

        return await ctx.response.send_message(embed=leaderboard_embed)

    @app_commands.command(
        name="msg_weekly"
    )
    async def weeklylb(self, ctx, places: int = 10):
        class LeaderBoardPosition:
            def __init__(self, id, coins):
                self.id = id
                self.coins = coins

        leaderboard = []

        with open("data/msg_weekly.json", "r") as file:
            data = json.load(file)
        collection = self.client.get_database_collection("data")
        profile = collection.find_one({"_id": 0})

        weekly = profile["weekly_time"]
        dt_object = datetime.fromtimestamp(weekly + 604800)
        date_str = dt_object.strftime("%Y/%m/%d - %H:%M")

        user_ids = list(data["users"].keys())
        user_msgs = []
        for i in user_ids:
            user_msgs.append(data["users"][i]["messages"])

        user_collection = {user_ids[i]: user_msgs[i] for i in range(len(user_ids))}

        for key, ele in user_collection.items():
            leaderboard.append(LeaderBoardPosition(key, ele))

        top = sorted(leaderboard, key=lambda x: x.coins, reverse=True)

        leaderboard_embed = self.client.create_embed(
            "Dreamworld Leaderboard",
            f"The top {places} chattiest people this week in Dreamworld!\nResets - {date_str}",
            config.embed_info_color
        )

        for i in range(1, places + 1, 1):
            try:
                value_one = top[i - 1].id
                value_two = top[i - 1].coins
                leaderboard_embed.add_field(
                    name=f"{i}. :thought_balloon:  {value_two}",
                    value=f"<@{value_one}>",
                    inline=False
                )
            except IndexError:
                leaderboard_embed.add_field(name=f"**<< {i} >>**", value="N/A | NaN", inline=False)

        return await ctx.response.send_message(embed=leaderboard_embed)

    @snowball.error
    async def on_error(self, ctx: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            cd = (str(error)).split()
            cd = round(float(str(cd[len(cd) - 1])[:len(cd)]) / 3600, 1)
            error_embed = self.client.create_embed(
                "Command Cooldown Error",
                f"You are on cooldown. Try again in {cd} hour/s",
                config.embed_error_color
            )
            await ctx.response.send_message(embed=error_embed, ephemeral=True)

    @app_commands.command(name="joke",
                          description="Tells a random joke.")
    async def joke(self, ctx: discord.Interaction):
        response = get("https://official-joke-api.appspot.com/random_joke")
        json_data = json.loads(response.text)
        await ctx.response.send_message(json_data['setup'])
        msg = await ctx.original_response()
        await asyncio.sleep(3)
        await msg.channel.send(json_data['punchline'])

    @tasks.loop(hours=1)
    async def check_inactive_channel(self):
        await self.client.wait_until_ready()
        inactive_time = timedelta(hours=1)
        general_channel = self.client.get_channel(987352212017676410)
        staff_channel = self.client.get_channel(1040242387563323503)
        while not self.client.is_closed():
            last_message_time = general_channel.last_message.created_at if general_channel.last_message else datetime.now(
                timezone.utc)
            if datetime.now(timezone.utc) - last_message_time > inactive_time:
                await staff_channel.send(
                    f"<#987352212017676410> has been inactive for 1 hour, <@&987388843684679730> <@&987388572195778560> <@&1075444317734314065> <@&1075441065835896832> Please try to revive the chat.")
            await asyncio.sleep(1800)  # Check every minute

    @app_commands.command(
        name="sendmsg",
        description="Sends a message in a specified channel.")
    @app_commands.default_permissions(manage_messages=True)
    async def sendmsg(self, ctx: discord.Interaction, channel: discord.TextChannel, text: str):
        await ctx.response.send_message(f"Message has been successfully sent to <#{channel.id}>.")
        await channel.send(text)

    @app_commands.command(
        name="sendembed",
        description="Sends an embed in a specified channel."
    )
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        channel="Select a channel. Example #general",
        content="Content of the message outside of the embed.",
        title="Title of the embed (Located at the inner-top of the embed).",
        description="Description of the embed (Located directly under the Title).",
        image="Put an image in the embed. Located at the inner-bottom of the index. (Use discord attachment link)",
        footer="Text at the bottom of the embed in much smaller size.",
        footer_icon="An icon at the start of the footer. (Use discord attachment link)",
        title_hyperlink="Make the title an Hyperlink. (Input a url)",
        author="Adds a sma  ll name above the title. Usually to put the name of the Message Writer."
    )
    async def sendembed(self,
                        ctx: discord.Interaction,
                        channel: discord.TextChannel,
                        title: str,
                        description: str,
                        content: str = None,
                        image: str = None,
                        footer: str = None,
                        footer_icon: str = None,
                        title_hyperlink: str = None,
                        author: str = None
                        ):
        msg_embed = Embed(title=title, description=description, color=0xa22aaf, url=title_hyperlink)

        if footer is not None:
            msg_embed.set_footer(text=footer, icon_url=footer_icon)
        if image is not None:
            msg_embed.set_image(url=image)
        if author is not None:
            msg_embed.set_author(name=author)
        try:
            await channel.send(content, embed=msg_embed)
        except:
            return await ctx.response.send_message(f"Incorrect URL has been used. Try again.")
        await ctx.response.send_message(f"Message has been successfully sent to {channel.mention}.")

    @app_commands.command(
        name="giverole"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def giverole(self, ctx: discord.Interaction, role: discord.Role):
        treason = ctx.guild.get_role(1090184365566333009)
        for user in ctx.guild.members:
            if not treason in user.roles:
                await user.add_roles(role, reason="Automatic Safe Role Given")
        print("Done.")

    @app_commands.command(
        name="start_giveaway",
        description="Starts a giveaway."
    )
    @app_commands.describe(
        host="User who's hosting the giveaway",
        channel="Channel where the giveaway will be hosted.",
        winners="Number of winners.",
        duration="How long the giveaway will last. Format: HH:MM:SS",
        roleinfluence="Let the participant's role decide their chances of winning"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def giveaway(self, ctx: discord.Interaction, host: discord.Member, channel: discord.TextChannel, winners: int,
                       duration: str, prize: str, roleinfluence: bool = True):

        duration_list = [int(i) for i in duration.split(":")]
        duration_secs = duration_list[0] * 3600 + duration_list[1] * 60 + duration_list[2]
        delta_time = timedelta(hours=duration_list[0], minutes=duration_list[1], seconds=duration_list[2])
        unix_end_datetime = int((datetime.now() + delta_time).timestamp())

        format_time = f"<t:{unix_end_datetime}>"

        title = "🎉 " + prize + " 🎉"

        description = f"""
        Hosted by: {host.mention}
        Number of Winners: {winners}
        Ends: {format_time}
        """
        giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())

        await ctx.response.send_message("Giveaway started!")

        msg = await channel.send(embed=giveaway_embed)

        await msg.add_reaction("🎁")

        await asyncio.sleep(duration_secs)

        giveaway_msg = await channel.fetch_message(msg.id)

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

                    if roleinfluence is True:
                        if nobles in user.roles:
                            [users.append(user.id) for _ in range(3)]
                        elif traveler in user.roles:
                            [users.append(user.id) for _ in range(2)]
                        else:
                            [users.append(user.id) for _ in range(1)]
                    else:
                        users.append(user.id)

            except Exception:
                pass

        if len(set(users)) >= winners:

            winners_list = []
            while len(winners_list) < winners:
                winner = choice(users)
                if winner not in winners_list:
                    winners_list.append(winner)

            winners_list = [ctx.guild.get_member(i).mention for i in winners_list]
            description = f"""
                    Hosted by: {host.mention}
                    Winner(s): {", ".join(winners_list)}
                    Ended at: {format_time}
                    """

            await channel.send(f"GIVEAWAY: 🎉🎉🎉{', '.join(winners_list)} WON {prize}🎉🎉🎉!!!")

            giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
            await giveaway_msg.edit(embed=giveaway_embed)
            print(users, winners_list)

        else:

            description = f"""
                               Hosted by: {host.mention}
                               Winner(s): None
                               Ended at: {format_time}
                               """

            await channel.send(f"GIVEAWAY: NO ONE WON {prize} ;(")

            giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
            await giveaway_msg.edit(embed=giveaway_embed)

    @app_commands.command(
        name="reroll_giveaway",
        description="Re-rolls a giveaway."
    )
    @app_commands.describe(
        giveaway_msg="ID of the giveaway message which will be re-rolled.",
        host="User who's hosting the giveaway",
        channel="Channel where the giveaway will be hosted.",
        winners="Number of winners.",
        roleinfluence="Let the participant's role decide their chances of winning"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def reroll_giveaway(self, ctx: discord.Interaction, giveaway_msg: str, host: discord.Member,
                              winners: int, channel: discord.TextChannel, prize: str, roleinfluence: bool = True, ):
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

                    if roleinfluence is True:
                        if nobles in user.roles:
                            [users.append(user.id) for _ in range(3)]
                        elif traveler in user.roles:
                            [users.append(user.id) for _ in range(2)]
                        else:
                            [users.append(user.id) for _ in range(1)]
                    else:
                        users.append(user.id)

            except Exception:
                pass

        if len(set(users)) >= winners:

            winners_list = []
            while len(winners_list) < winners:
                winner = choice(users)
                if winner not in winners_list:
                    winners_list.append(winner)

            winners_list = [ctx.guild.get_member(i).mention for i in winners_list]
            description = f"""
                            Hosted by: {host.mention}
                            Winner(s): {", ".join(winners_list)}
                            """

            await channel.send(f"REROLL - 🎉🎉🎉{', '.join(winners_list)} WON {prize}🎉🎉🎉!!!")

            giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
            await giveaway_msg.edit(embed=giveaway_embed)
            print(users, winners_list)

        else:
            description = f"""
                                       Hosted by: {host.mention}
                                       Winner(s): None
                                       """

            await channel.send(f"REROLL - NO ONE WON {prize} ;(")

            giveaway_embed = Embed(title=title, description=description, color=0xa22aaf, timestamp=datetime.now())
            await giveaway_msg.edit(embed=giveaway_embed)

        await ctx.response.send_message("Re-rolled!", ephemeral=True)

    async def verifymsg(self, ctx):
        await ctx.purge()

        button = Button(label="Verify!", style=discord.ButtonStyle.green, emoji="✅")

        async def button_callback(interaction):
            if interaction.guild is not None:
                role = interaction.guild.get_role(987389964486578236)
                for roles in interaction.user.roles:
                    if roles.id == role.id:
                        await interaction.response.send_message(f"You are already verified.", ephemeral=True)
                        return
                await interaction.user.add_roles(role, reason="Verification")
                await interaction.response.send_message(f"You have been verified.", ephemeral=True)

        embed = discord.Embed()
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/987411993088655421/1051827621740158976/Verify_2.png")
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send(embed=embed, view=view)

    async def verifymsg2(self, ctx):
        await ctx.purge()

        button = Button(label="Verify!", style=discord.ButtonStyle.green, emoji="✅")

        async def button_callback(interaction):
            if interaction.guild is not None:
                role = interaction.guild.get_role(1042478120093110333)
                for roles in interaction.user.roles:
                    if roles.id == role.id:
                        print(interaction.user.id)
                        try:
                            await interaction.response.send_message(f"You are already verified.", ephemeral=True)
                        except Exception as err:
                            print(err)
                        return
                await interaction.user.add_roles(role, reason="Verification")
                await interaction.response.send_message(f"You have been verified.", ephemeral=True)

        embed = discord.Embed()
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/987411993088655421/1051827621740158976/Verify_2.png")
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send(embed=embed, view=view)

    @tasks.loop(hours=1)
    async def msg_task(self):

        # collection = self.client.get_database_collection("users")
        # result = collection.find({}, {"_id": 1})
        # now = datetime.now(timezone.utc)
        # one_week_ago = now - timedelta(days=7)
        #
        # user = await self.client.fetch_member(940570942332092486)
        # async for message in user.history(limit=10, before=now):
        #     print(message.created_at)
        # for i in result:
        #     id = i["_id"]
        #     try:
        #         user = await self.client.fetch_member(id)
        #
        #         if not user.history(limit=1):
        #             print(user.name, "has never sent a single mf message")
        #         async for message in user.history(limit=1):
        #             created_at_utc = message.created_at.replace(tzinfo=timezone.utc)
        #             if created_at_utc > one_week_ago:
        #                 print("USER last message more thanb a week agfo tstsk", user.name)
        #     except Exception as err:
        #         print(err)
        collection = self.client.get_database_collection("data")
        profile = collection.find_one({"_id": 0})
        name_monthly = profile["monthly_time"]
        time_weekly = profile["weekly_time"]

        current_time = int(time.time())

        dt_object = datetime.fromtimestamp(time.time())
        month_name = dt_object.strftime("%B")

        if name_monthly != month_name:
            places = 3

            class LeaderBoardPosition:
                def __init__(self, id, coins):
                    self.id = id
                    self.coins = coins

            leaderboard = []
            collection = self.client.get_database_collection("data")
            profile = collection.find_one({"_id": 0})
            name_monthly = profile["monthly_time"]

            with open("data/msg_monthly.json", "r") as file:
                data = json.load(file)
            user_ids = list(data["users"].keys())
            user_msgs = []
            for i in user_ids:
                user_msgs.append(data["users"][i]["messages"])

            user_collection = {user_ids[i]: user_msgs[i] for i in range(len(user_ids))}

            for key, ele in user_collection.items():
                leaderboard.append(LeaderBoardPosition(key, ele))

            top = sorted(leaderboard, key=lambda x: x.coins, reverse=True)

            leaderboard_embed = self.client.create_embed(
                "Dreamworld Monthly Activity Leaderboard",
                f"The top {places} most active people in {name_monthly} on Dreamworld!",
                config.embed_info_color
            )

            for i in range(1, places + 1, 1):
                try:
                    value_one = top[i - 1].id
                    value_two = top[i - 1].coins

                    leaderboard_embed.add_field(
                        name=f"{i}. :thought_balloon:  {value_two}",
                        value=f"<@!{value_one}>",
                        inline=False
                    )
                except IndexError:
                    leaderboard_embed.add_field(name=f"**<< {i} >>**", value="N/A | NaN", inline=False)

            record = await self.client.fetch_channel(1021391202756595712)

            await record.send(embed=leaderboard_embed)

            collection.update_one({"_id": 0}, {"$set": {"monthly_time": month_name}})

        if (time_weekly + 604800) < current_time:
            places = 3

            class LeaderBoardPosition:
                def __init__(self, id, coins):
                    self.id = id
                    self.coins = coins

            leaderboard = []

            with open("data/msg_weekly.json", "r") as file:
                data = json.load(file)
            collection = self.client.get_database_collection("data")
            profile = collection.find_one({"_id": 0})

            weekly = profile["weekly_time"]
            dt_object = datetime.fromtimestamp(weekly + 604800)
            date_str = dt_object.strftime("%Y/%m/%d - %H:%M")

            user_ids = list(data["users"].keys())
            user_msgs = []
            for i in user_ids:
                user_msgs.append(data["users"][i]["messages"])

            user_collection = {user_ids[i]: user_msgs[i] for i in range(len(user_ids))}

            for key, ele in user_collection.items():
                leaderboard.append(LeaderBoardPosition(key, ele))

            top = sorted(leaderboard, key=lambda x: x.coins, reverse=True)

            leaderboard_embed = self.client.create_embed(
                "Dreamworld Weekly Activity Leaderboard",
                f"The top {places} most active people this week in Dreamworld!\n{datetime.fromtimestamp(time_weekly).strftime('%Y/%m/%d - %H:%M')} -> {datetime.fromtimestamp(time_weekly + 604800).strftime('%Y/%m/%d - %H:%M')}",
                config.embed_info_color
            )

            for i in range(1, places + 1, 1):
                try:
                    value_one = top[i - 1].id
                    value_two = top[i - 1].coins

                    leaderboard_embed.add_field(
                        name=f"{i}. :thought_balloon:  {value_two}",
                        value=f"<@!{value_one}>",
                        inline=False
                    )
                except IndexError:
                    leaderboard_embed.add_field(name=f"**<< {i} >>**", value="N/A | NaN", inline=False)

            record = await self.client.fetch_channel(1021391202756595712)
            await record.send(embed=leaderboard_embed)
            collection.update_one({"_id": 0}, {"$set": {"weekly_time": time.time()}})

        with open("data/role_period.json", "r") as file:
            current_time = time.time()
            data = json.load(file)
            purchase_list = data["users"]
            indexes = []
            for i in range(len(purchase_list)):
                member = await self.client.fetch_member(purchase_list[i][0])
                role = member.guild.get_role(purchase_list[i][2])
                remove_time = purchase_list[i][1]
                if current_time >= remove_time:
                    await member.remove_roles(role)
                    indexes.append(i)
            for i in indexes:
                del data["users"][i]
        with open("data/role_period.json", "w") as file:
            json.dump(data, file, indent=4)

        #  check
        with open("msg_monthly.json", "r") as file:
            data = json.load(file)
        x = data

        for users in data["users"].keys():
            try:
                user = self.client.fetch_member(int(users))
            except Exception:
                del x["users"][users]

        with open("msg_monthly.json", "w") as file:
            json.dump(x, file)

        #  check 2
        with open("msg_weekly.json", "r") as file:
            data = json.load(file)
        x = data

        for users in data["users"].keys():
            try:
                user = self.client.fetch_member(int(users))
            except Exception:
                del x["users"][users]

        with open("msg_weekly.json", "w") as file:
            json.dump(x, file)

    @commands.Cog.listener()
    async def on_message(self, message) -> None:

        userid = str(message.author.id)

        if message.author.bot:
            return

        with open("data/msg_monthly.json", "r") as file:
            data = json.load(file)

        if userid in data["users"].keys():
            data["users"][userid]["messages"] += 1
            with open("data/msg_monthly.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            data["users"][userid] = dict()
            data["users"][userid]["messages"] = 1
            with open("data/msg_monthly.json", "w") as file:
                json.dump(data, file, indent=4)

        with open("data/msg_weekly.json", "r") as file:
            data = json.load(file)

        if userid in data["users"].keys():
            data["users"][userid]["messages"] += 1
            with open("data/msg_weekly.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            data["users"][userid] = dict()
            data["users"][userid]["messages"] = 1
            with open("data/msg_weekly.json", "w") as file:
                json.dump(data, file, indent=4)

        if message.channel != await self.client.fetch_channel(987352212017676410):
            return

        with open("data/treasonduration.json", "r") as file:
            data = json.load(file)

        data["users"][userid] = time.time()

        with open("data/treasonduration.json", "w") as file:
            json.dump(data, file, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):

        self.check_inactive_channel.start()
        self.msg_task.start()
        Channel = self.client.get_channel(1022186110828429432)
        await Channel.purge()

        emb = Embed(title=None,
                    description=":loudspeaker: --> <@&1022525447910731877>\n:video_game: --> <@&1022520639111827466>",
                    color=config.embed_info_color)
        message = await Channel.send(embed=emb)
        await message.add_reaction("📢")
        await message.add_reaction("🎮")

        channel = self.client.get_channel(1042450717174149294)
        if channel.guild.premium_subscription_count >= 14:
            self.client.boost = True

        channel_2 = self.client.get_channel(1042450717174149294)
        channel_1 = self.client.get_channel(1013919292489744435)

        while True:
            await self.verifymsg2(channel_2)
            await self.verifymsg(channel_1)

            current = time.time()

            treason = message.guild.get_role(1090184365566333009)
            safe = message.guild.get_role(1090185036688531466)

            with open("data/treasonduration.json", "r") as file:
                data = json.load(file)
            removed = []
            for user_id in data["users"].keys():

                try:
                    user = await self.client.fetch_member(user_id)
                    if current - data["users"][user_id] > 604800:
                        if safe in user.roles:
                            await user.remove_roles(safe)
                        if not treason in user.roles:
                            await user.add_roles(treason)
                    else:
                        if treason in user.roles:
                            await user.remove_roles(treason)
                        if not safe in user.roles:
                            await user.add_roles(safe)

                except Exception:
                    removed.append(user_id)

            for i in removed:
                del data["users"][i]

            with open("data/treasonduration.json", "w") as file:
                json.dump(data, file, indent=4)

            await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        Channel = self.client.get_channel(1022186110828429432)

        if user.id == 1035103134441287762:
            return
        if reaction.message.channel.id != Channel.id:
            print("Wrong channel")
            return
        if reaction.emoji == "📢":
            print("Loudspeaker given")
            Role = discord.utils.get(user.guild.roles, name="║Event Access║")
            await user.add_roles(Role)
        if reaction.emoji == "🎮":
            print("Gamer given")
            Role = discord.utils.get(user.guild.roles, name="║Game Access║")
            await user.add_roles(Role)
        await reaction.message.remove_reaction(reaction.emoji, user)

    @commands.command(name="test1")
    async def test1(self, ctx):
        pass

    # @tasks.loop(hours=1)
    # async def temp_task(self):
    #     channel = self.client.get_channel(1042450717174149294)

    #     while True:
    #         await Miscellaneous.verifymsg2(self, channel)
    #         await Miscellaneous.verifymsg(self, channel)
    #         await asyncio.sleep(60)


async def setup(client):
    await client.add_cog(Miscellaneous(client))
