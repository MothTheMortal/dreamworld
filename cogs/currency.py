import discord
from discord.ext import commands
import config
import json
from time import time
from discord import app_commands


class Currency(commands.Cog):
    with open("data/command_details.json", "r") as json_file:
        command_details = json.load(json_file)
        balance_details = command_details["balance"]
        star_details = command_details["star"]
        lb_details = command_details["stars_top"]
        candy2_details = command_details["candy"]
        candy_details = command_details["candy_top"]
        shop_details = command_details["shop"]
        snow_details = command_details["snow_top"]
        snow2_details = command_details["snow"]


    def __init__(self, client):
        self.client = client
        

    @app_commands.command(name="add-currency")
    @app_commands.choices(currency=[app_commands.Choice(name="Star", value="star"), app_commands.Choice(name="Candy", value="candy"), app_commands.Choice(name="Snow", value="snow")])
    @app_commands.describe(
        members="Input the User IDs with space separating them."
    )
    async def add_currency(self, ctx: discord.Interaction, currency: app_commands.Choice[str], amount: int, members: str):
        user_collection = self.client.get_database_collection("users")
        emoji = config.emoji_field[currency.value]
        member_ids = list(map(int, members.split(" ")))
        user_collection.update_many({"_id": {"$in": member_ids}}, {"$inc": {currency.value: amount}})
        description = ""
        for i in member_ids:
            description += f"<@!{i}>: {amount} {emoji}\n"
        em = self.client.create_embed(f"Currency Added by {ctx.user.name}", description, config.embed_success_color)
        await ctx.response.send_message(embed=em)




    @app_commands.command(
        name="bal",
        description=balance_details["description"])
    @commands.cooldown(balance_details["cooldown_rate"], balance_details["cooldown_per"])
    async def bal(self, ctx: discord.Interaction, member: discord.Member = None):
        global users, user_info
        if member is None:
            member = ctx.user

        await self.client.database_user_preload(member)
        user_collection = self.client.get_database_collection("users")
        user_profile = user_collection.find_one({"_id": member.id})
        profile_embed = self.client.create_embed(
            f"{member.name}'s Pocket",
            f"",
            config.embed_purple
        )
        star = config.emoji_field['star']
        candy = config.emoji_field['candy']
        snow = config.emoji_field['snow']

        if ctx.guild.premium_subscription_count <= 14:
            star = config.emoji_field['dstar']
            candy = config.emoji_field['dcandy']
            snow = config.emoji_field['dsnow']


        profile_embed.add_field(
            name="Stars", value=f"{user_profile['star']} {star}",
            inline=True
        )
        profile_embed.add_field(
            name="Candy", value=f"{user_profile['candy']} {candy}",
            inline=True
        )
        profile_embed.add_field(
            name="Snow", value=f"{user_profile['snow']} {snow}",
            inline=True
        )
        return await ctx.response.send_message(embed=profile_embed)


    @app_commands.command(name="leaderboard", description="Shows the leaderboard for something!")
    @app_commands.choices(lb_type=[app_commands.Choice(name="Star", value="star"),
                                   app_commands.Choice(name="Candy", value="candy"),
                                   app_commands.Choice(name="Snow", value="snow"),
                                   app_commands.Choice(name="Weekly Messages", value="weekly"),
                                   app_commands.Choice(name="Monthly Messages", value="monthly"),
                                   app_commands.Choice(name="Yearly Messages", value="yearly")]
                          )
    async def lb(self, ctx: discord.Interaction, lb_type: app_commands.Choice[str], places: int = 10):

        if lb_type.value in ["weekly", "monthly", "yearly"]:
            if lb_type.value == "weekly":
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

            elif lb_type.value == "monthly":
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

            elif lb_type.value == "yearly":
                lb_type = "yearly_messages"


        else:
            emoji = config.emoji_field[lb_type.value]

            class LeaderBoardPosition:
                def __init__(self, id, coins, name):
                    self.id = id
                    self.coins = coins
                    self.name = name

            leaderboard = []

            user_collection = self.client.get_database_collection("users")

            for user in user_collection.find():
                leaderboard.append(LeaderBoardPosition(user["_id"], user[lb_type.value], user["name"]))

            top = sorted(leaderboard, key=lambda x: x.coins, reverse=True)

            leaderboard_embed = self.client.create_embed(
                "Dreamworld Leaderboard",
                f"The top {places} wealthiest people in all of Dreamworld!",
                config.embed_info_color
            )

            for i in range(1, places + 1, 1):
                try:
                    value_one = top[i - 1].id
                    value_two = top[i - 1].coins
                    value_three = top[i - 1].name
                    leaderboard_embed.add_field(
                        name=f"{i}. {value_two} {emoji}",
                        value=f"<@{value_one}> - {value_three}",
                        inline=False
                    )
                except IndexError:
                    leaderboard_embed.add_field(name=f"**<< {i} >>**", value="N/A | NaN", inline=False)

            return await ctx.response.send_message(embed=leaderboard_embed)

    @app_commands.command(
        name="shop",
        description=shop_details["description"])
    @app_commands.choices(
        category=[app_commands.Choice(name="MLBB",  value="mlbb"), app_commands.Choice(name="Genshin Impact", value="genshin"), app_commands.Choice(name="Roblox", value="roblox"), app_commands.Choice(name="Valorant", value="valorant"), app_commands.Choice(name="Discord", value="discord"), app_commands.Choice(name="Roles", value="roles")]
    )
    async def shop(self, ctx: discord.Interaction, category: app_commands.Choice[str]):

        star = config.emoji_field['star']
        candy = config.emoji_field['candy']
        snow = config.emoji_field['snow']

        user_collection = self.client.get_database_collection("users")



        await self.client.database_user_preload(ctx.user)

        category = category.value
        user_profile = user_collection.find_one({"_id": ctx.user.id})

        shop_embed = self.client.create_embed("Dreamworld Shop", "Loading Shop Items...", config.embed_info_color)
        await ctx.response.send_message(embed=shop_embed)
        shop_message = await ctx.original_response()

        await shop_message.add_reaction("⬅")
        await shop_message.add_reaction("⭐")
        await shop_message.add_reaction("➡")

        shop_items = config.category_items[category]
        item_index = 0

        index_bounds = (0, len(shop_items) - 1)
        while True:
            shop_item = shop_items[item_index]
            item_type = shop_item["type"]

            item_embed = self.client.create_embed("Dreamworld Shop", shop_item["description"], config.embed_info_color)
            if category in config.star_categories:
                item_embed.add_field(
                    name=shop_item["name"],
                    value=f"Price: {shop_item['price']} {star}",
                    inline=True
                )
            else:
                item_embed.add_field(
                    name=shop_item["name"],
                    value=f"Price: {shop_item['price']} {candy}",
                    inline=True
                )

            await shop_message.edit(embed=item_embed)
            shop_reply = await self.client.message_reaction(shop_message, ctx.user, 30)

            if shop_reply is None:
                return

            async def invalid_response():
                invalid_response_embed = self.client.create_embed(
                    "Invalid Response",
                    "The response that you provided to the question was not acceptable.",
                    config.embed_error_color
                )

                await shop_message.edit(embed=invalid_response_embed)

            if shop_reply not in ["⬅", "⭐", "➡"]:
                return await invalid_response()

            async def invalid_time(time_left):
                days = round(time_left / 86400, 1)
                invalid_response_embed = self.client.create_embed(
                    "Too Quick",
                    f"You have to wait one month after each purchase.\nTime left: {days} days",
                    config.embed_error_color
                )

                await shop_message.edit(embed=invalid_response_embed)

            await shop_message.remove_reaction(shop_reply, ctx.user)
            if shop_reply == "⬅":
                item_index -= 1

                if item_index < index_bounds[0]:
                    item_index = index_bounds[1]
            elif shop_reply == "➡":
                item_index += 1

                if item_index > index_bounds[1]:
                    item_index = index_bounds[0]
            else:  # Purchasing Item
                if category in config.star_categories:
                    with open("data/buy_period.json", "r") as file:
                        data_buy = json.load(file)
                    if str(ctx.user.id) in data_buy.keys():
                        timer = await self.client.buy_time(ctx.user.id)
                        if timer[0]:
                            return await invalid_time(timer[1])
                    if user_profile["star"] < shop_item["price"]:
                        price_embed = self.client.create_embed(
                            "Invalid Item Purchase",
                            "You are unable to purchase this item as you lack sufficient funds.",
                            config.embed_error_color
                        )
                        return await shop_message.edit(embed=price_embed)

                    user_collection.update_one({"_id": ctx.user.id}, {"$inc": {"star": -1 * shop_item["price"]}})


                    if item_type == "transaction":
                        transaction_embed = self.client.create_embed(
                            "Transaction Made",
                            shop_item["transaction"].format(member=ctx.user),
                            config.embed_info_color
                        )

                        transaction_embed.add_field(
                            name="Dreamworld Stars Spent",
                            value=f"{shop_item['price']} {star}",
                            inline=True
                        )

                        transaction_embed.add_field(
                            name="Staff Member Responsible",
                            value=f"<@!{shop_item['staff_id']}>",
                            inline=True
                        )

                        transaction_embed.set_footer(text="Delete This Once Completed!")

                        transaction_channel = self.client.get_channel(config.channel_ids["shop"])
                        await transaction_channel.send(embed=transaction_embed)

                        notification_message = await transaction_channel.send(f"<@!{shop_item['staff_id']}>")
                        await notification_message.delete()

                    purchased_embed = self.client.create_embed(
                        "Item Purchased",
                        "Your item has been successfully purchased, please allow us time to process your transaction.",
                        config.embed_success_color
                    )

                    purchased_embed.add_field(name="Item Purchased", value=shop_item["name"], inline=True)

                    purchased_embed.add_field(
                        name="Dreamworld Stars Spent",
                        value=f"{shop_item['price']} {star}",
                        inline=True
                    )
                    with open("data/buy_period.json", "r") as file:
                        data = json.load(file)
                        data[str(ctx.user.id)] = time()
                    with open("data/buy_period.json", "w") as file:
                        json.dump(data, file)
                    return await shop_message.edit(embed=purchased_embed)
                else:
                    with open("data/buy_period.json", "r") as file:
                        data_buy = json.load(file)
                    if str(ctx.user.id) in data_buy.keys():
                        timer = await self.client.buy_time(ctx.user.id)
                        if timer[0]:
                            return await invalid_time(timer[1])
                    if user_profile["candy"] < shop_item["price"]:
                        price_embed = self.client.create_embed(
                            "Invalid Item Purchase",
                            "You are unable to purchase this item as you lack sufficient funds.",
                            config.embed_error_color
                        )
                        return await shop_message.edit(embed=price_embed)

                    user_collection.update_one({"_id": ctx.user.id}, {"$inc": {"candy": -1 * shop_item["price"]}})


                    if item_type == "transaction":
                        transaction_embed = self.client.create_embed(
                            "Transaction Made",
                            shop_item["transaction"].format(member=ctx.user),
                            config.embed_info_color
                        )

                        transaction_embed.add_field(
                            name="Dreamworld Candy Spent",
                            value=f"{shop_item['price']} {candy}",
                            inline=True
                        )

                        transaction_embed.add_field(
                            name="Staff Member Responsible",
                            value=f"<@!{shop_item['staff_id']}>",
                            inline=True
                        )

                        transaction_embed.set_footer(text="Delete This Once Completed!")

                        transaction_channel = self.client.get_channel(config.channel_ids["shop"])
                        await transaction_channel.send(embed=transaction_embed)

                        notification_message = await transaction_channel.send(f"<@!{shop_item['staff_id']}>")
                        await notification_message.delete()

                    purchased_embed = self.client.create_embed(
                        "Item Purchased",
                        "Your item has been successfully purchased, Your role will be given shortly.",
                        config.embed_success_color
                    )

                    purchased_embed.add_field(name="Item Purchased", value=shop_item["name"], inline=True)
                    purchased_embed.add_field(
                        name="Dreamworld Candy Spent",
                        value=f"{shop_item['price']} {candy}",
                        inline=True
                    )
                    with open("data/buy_period.json", "r") as file:
                        data = json.load(file)
                        data[str(ctx.user.id)] = time()
                    with open("data/buy_period.json", "w") as file:
                        json.dump(data, file)
                    await self.client.role_period(ctx.user, shop_item["time_period"], shop_item["time"], shop_item["role_id"])
                    return await shop_message.edit(embed=purchased_embed)


async def setup(client):
    await client.add_cog(Currency(client))
