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
        if count == 3:
            user_collection.update_one({"_id": ctx.user.id}, {"$set": {"warning": 0}})
            count += 1
        else:
            user_collection.update_one({"_id": ctx.user.id}, {"$inc": {"warning": 1}})
            count += 1

        if count < 3:
            warn_embed = self.client.create_embed(
                f"Warning for {user.name}",
                f"{user.mention} has been warned. {3 - count} more warnings till direct action will be taken.",
                0xFFFFFF
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


        else:
            warn_embed = self.client.create_embed(
                f"Warning for {user.name}",
                f"{user.mention} has been warned, they have reached the maximum warning limit. Action will be taken with the deserved punishment.",
                0xFFFFFF

            )
            warn_embed.add_field(
                name="Reason:",
                value=reason,
                inline=True
            )

            await channel.send(embed=warn_embed)

        await ctx.response.send_message("Warning has been sent.")
        log_channel = self.client.get_channel(1021391202756595712)

        log_embed = self.client.create_embed(
            f"Warning.",
            f"{user.mention} has been warned",
            0xFFFFFF

        )

        log_embed.add_field(name="Warning Count:", value=count, inline=True)
        log_embed.add_field(name="Reason: ", value=reason, inline=True)

        await log_channel.send(embed=log_embed)

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
