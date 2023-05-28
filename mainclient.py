import discord_module as discord
from discord.ext import commands
import json
import discord
import config
import asyncio
import time
import pymongo


class DreamBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.database_client = pymongo.MongoClient(kwargs["mongodb_uri"])
        self.discord_database = self.database_client["discord"]
        self.boost = False

    def insert_database_user(self, user: discord.Member):
        database_collection = self.get_database_collection("users")
        database_collection.insert_one({
            "_id": user.id,
            "star": 0,
            "candy": 0,
            "snow": 0,
            "name": user.name,
            "warning": 0
        })

    async def database_user_preload(self, user: discord.Member):
        database_count = self.get_database_collection("users").count_documents({"_id": user.id})

        if database_count > 1:
            emergency_embed = self.create_embed(
                "Database Emergency",
                "There are duplicate entries in the database that could lead to future data corruption.",
                config.embed_error_color
            )

            emergency_embed.add_field(name="User ID", value=user.id)

            staff_channel = self.get_channel(config.channel_ids["errors"])
            await staff_channel.send(embed=emergency_embed)
            return await staff_channel.send("<@273890943407751168>")

        if database_count == 0:
            self.insert_database_user(user)

    def get_database_collection(self, collection):
        return self.discord_database[collection]

    class VerifyView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Verify!", style=discord.ButtonStyle.green, emoji="✅", custom_id="verify")
        async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.guild is not None:
                role = interaction.guild.get_role(987389964486578236)
                for roles in interaction.user.roles:
                    if roles.id == role.id:
                        await interaction.response.send_message(f"You are already verified.", ephemeral=True)
                        return
                await interaction.user.add_roles(role, reason="Verification")
                await interaction.response.send_message(f"You have been verified.", ephemeral=True)

    async def setup_hook(self):
        for cog in config.cogs:
            await self.load_extension(f"cogs.{cog}")
        await self.add_view(self.VerifyView())

    async def fetch_member(self, user_id):
        guild = await self.fetch_guild(987352212017676408)
        member = await guild.fetch_member(user_id)
        return member

    async def buy_time(self, user_id):
        with open("data/buy_period.json", "r") as file:
            user = str(user_id)
            data = json.load(file)
            time_bought = data[user]
            since = time.time() - time_bought
            if since < 2628288:
                since = 2628288 - since
                return [True, since]
            else:
                del data[user]
                with open("data/buy_period.json", "w") as file:
                    json.dump(data, file, indent=4)
                return [False]

    async def role_period(self, member: discord.Member, time_state: bool, length: str, role_bet: int):
        role = member.guild.get_role(role_bet)
        await member.add_roles(role, reason="Shop Purchase")

        with open("data/role_period.json", "r") as file:
            upload_data = json.load(file)
        unix_add = 0

        if not time_state:
            return

        if length == "day":
            unix_add = 86400
        elif length == "week":
            unix_add = 604800
        elif length == "month":
            unix_add = 2.628e+6
        elif length == "year":
            unix_add = 3.154e+7
        end_unix = time.time() + unix_add
        data_list = [member.id, end_unix, role.id]
        upload_data["users"].append(data_list)
        with open("data/role_period.json", "w") as file:
            json.dump(upload_data, file, indent=4)

    async def message_reaction(self, message, member, timeout):
        def check_reaction(reaction, user):
            if reaction.message != message:
                return False
            if user != member:
                return False

            return True

        try:
            return str((await self.wait_for("reaction_add", check=check_reaction, timeout=timeout))[0].emoji)
        except asyncio.TimeoutError:
            return None

    async def message_response(self, message, member, timeout):
        def check_message(to_check):
            if to_check.channel != message.channel:
                return False
            if to_check.author != member:
                return False

            return True

    @staticmethod
    def create_embed(title, description, color):
        return DreamBot_Embed(title, description, color)


class DreamBot_Embed(discord.Embed):
    def __init__(self, title, description, color):
        super().__init__(title=title, description=description, color=color)
        self.set_author(name=config.name,
                        icon_url=config.profile_picture)
        self.set_thumbnail(
            url=config.thumbnail)
