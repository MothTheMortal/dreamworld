from discord.ext import commands
import asyncio
import config
import discord
from discord import app_commands, ui
import json
import datetime


class Clearance(ui.Modal, title="Clear Messages"):
    amount = ui.TextInput(label="Number of messages to delete", placeholder="10", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            samount = int(str(self.amount))
            await interaction.response.send_message(f"{self.amount} messages were wiped out from existence. _poof_",
                                                    ephemeral=True)
            await interaction.channel.purge(limit=samount)
        except Exception:
            await interaction.response.send_message(f"Invalid Input.",
                                                    ephemeral=True)


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @app_commands.command(name="remove-attendance", description="Removes a user from daily attendance.")
    async def remove_attendance(self, ctx: discord.Interaction, user: discord.Member):
        data_collection = self.client.get_database_collection("data")
        doc = data_collection.find_one({"_id": 0})

        if str(user.id) in doc["attendance"].keys():
            del doc["attendance"][str(user.id)]
            await ctx.response.send_message(f"{user.mention} has been removed from attendance.")
            data_collection.update_one({"_id": 0}, {"$set": {"attendance": doc["attendance"]}})
        else:
            await ctx.response.send_message(f"{user.mention} is not in attendance.", ephemeral=True)

    @app_commands.command(name="clear",
                          description="Clear messages in a channel.")
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, ctx: discord.Interaction):

        await ctx.response.send_modal(Clearance())

    @app_commands.command(name="warn",
                          description="Warns a user.")
    @app_commands.default_permissions(kick_members=True)
    async def warn(self, ctx: discord.Interaction, user: discord.Member, reason: str, channel: discord.TextChannel):

        user_collection = self.client.get_database_collection("users")
        user_profile = user_collection.find_one({"_id": ctx.user.id})
        count = user_profile["warning"]
        count += 1
        if count == 3:
            user_collection.update_one({"_id": ctx.user.id}, {"$set": {"warning": 0}})

        else:
            user_collection.update_one({"_id": ctx.user.id}, {"$inc": {"warning": 1}})

        if count < 3:
            try:
                dm_channel = await user.create_dm()
                warn2_embed = self.client.create_embed(
                    f"Warning for {user.name}",
                    f"You have been warned. {3 - count} more warnings till direct action will be taken.",
                    discord.Color.red()
                )
                warn2_embed.add_field(
                    name="Reason:",
                    value=reason,
                    inline=True
                )
                await dm_channel.send(embed=warn2_embed)
            except Exception as er:
                print(er)

            warn_embed = self.client.create_embed(
                f"Warning for {user.name}",
                f"{user.mention} has been warned. {3 - count} more warnings till direct action will be taken.",
                discord.Color.red()
            )
            warn_embed.add_field(
                name="Warning Count:",
                value=count,
                inline=True
            )
            warn_embed.add_field(
                name="Reason:",
                value=reason,
                inline=True
            )

            await channel.send(embed=warn_embed)
            log_channel = self.client.get_channel(1021391202756595712)

            log_embed = self.client.create_embed(
                f"Warning.",
                f"{user.mention} has been warned",
                discord.Color.red()

            )

            log_embed.add_field(name="Warning Count:", value=count, inline=True)
            log_embed.add_field(name="Reason: ", value=reason, inline=True)
            log_embed.add_field(name="Warned by:", value=ctx.user.mention, inline=True)

            await log_channel.send(embed=log_embed)

        else:

            try:
                dm_channel = await user.create_dm()
                warn2_embed = self.client.create_embed(
                    f"Warning for {user.name}",
                    f"You have reached the maximum warning.",
                    discord.Color.red()
                )
                warn2_embed.add_field(
                    name="Reason:",
                    value=reason,
                    inline=True
                )
                await dm_channel.send(embed=warn2_embed)
            except Exception as er:
                print(er)

            warn_embed = self.client.create_embed(
                f"Maximum Warning {user.name}",
                f"{user.mention} have reached the maximum warning limit. Staff will take action with the deserved punishment.",
                discord.Color.red()

            )
            warn_embed.add_field(
                name="Reason:",
                value=reason,
                inline=True
            )

            await channel.send(embed=warn_embed)
            log_channel = self.client.get_channel(1021391202756595712)

            log_embed = self.client.create_embed(
                f"Maximum Warning.",
                f"{user.mention} has been warned for the third time.\nStaff please take action.",
                discord.Color.red()

            )

            log_embed.add_field(name="Reason: ", value=reason, inline=True)
            log_embed.add_field(name="Warned by:", value=ctx.user.mention, inline=True)

            await log_channel.send(embed=log_embed)
        await ctx.response.send_message("Warning has been sent.", ephemeral=True)


    @commands.Cog.listener()
    async def on_message_edit(self, before, message):
        msg = message.content
        for i in config.filtered:
            if i in msg.lower():
                await message.channel.send(f"The use of negative words are not allowed {message.author.mention}.")
                await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 1035103134441287762:
            return

        msg = message.content
        for i in config.filtered:
            if i in msg.lower():
                await message.channel.send(f"The use of negative words are not allowed {message.author.mention}.")
                await message.delete()




async def setup(client):
    await client.add_cog(Moderation(client))
