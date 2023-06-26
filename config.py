import datetime
import pytz

# Cogs Configuration
cogs = ["cog_manager", "currency", "moderation", "miscellaneous"]

# Moderation Configuration
filtered = ["dick"]

# Bot Configuration
name = "Dreamworld"

shop_emoji = None
shop_categories = ["mlbb", "genshin", "roblox", "valorant", "discord", "roles"]
formal_shop_categories = {"mlbb": "Mobile Legend", "genshin": "Genshin Impact", "roblox": "Roblox",
                          "valorant": "Valorant", "discord": "Discord", "roles": "Roles"}

star_categories = ["mlbb", "genshin", "roblox", "valorant", "discord"]
candy_categories = ["roles"]

help_categories = ["currency"]
formal_help_categories = {"cog_manager": "Cog Manager", "moderation": "Moderation", "miscellaneous": "Miscellaneous",
                          "currency": "Currency"}

category_items = {'roles': [
    {'type': 'transaction', 'name': '1 Day Sleepy Dreamer Role', 'description': 'Discord Roles', 'price': 25100,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Day Sleepy Dreamer Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 1065976137739669574, 'time': 'day'},
    {'type': 'transaction', 'name': '1 Week Sleepy Dreamer Role', 'description': 'Discord Roles', 'price': 25500,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Week Sleepy Dreamer Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 1065976137739669574, 'time': 'week'},
    {'type': 'transaction', 'name': '1 Month Sleepy Dreamer Role', 'description': 'Discord Roles', 'price': 28500,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Month Sleepy Dreamer Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 1065976137739669574, 'time': 'month'},
    {'type': 'transaction', 'name': '1 Year Sleepy Dreamer Role', 'description': 'Discord Roles', 'price': 34500,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Year Sleepy Dreamer Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 1065976137739669574, 'time': 'year'},
    {'type': 'transaction', 'name': '1 Month Duke/Duchess Role', 'description': 'Discord Roles', 'price': 30000,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Month Duke/Duchess Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 1027052753895301151, 'time': 'month'},
    {'type': 'transaction', 'name': '1 Year Duke/Duchess Role', 'description': 'Discord Roles', 'price': 40000,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Year Duke/Duchess Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 1027052753895301151, 'time': 'year'},
    {'type': 'transaction', 'name': '1 Month Nobles Role', 'description': 'Discord Roles', 'price': 35000,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Month Nobles Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 996191436406018098, 'time': 'month'},
    {'type': 'transaction', 'name': '1 Year Nobles Role', 'description': 'Discord Roles', 'price': 125000,
     'transaction': '{member.name} ({member.mention}) has purchased 1 Year Nobles Role.',
     'staff_id': 940570942332092486, 'time_period': True, 'role_id': 996191436406018098, 'time': 'year'},
    {'type': 'transaction', 'name': 'Candy Monster Role (Permanent)', 'description': 'Discord Roles', 'price': 125000,
     'transaction': '{member.name} ({member.mention}) has purchased the Candy Monster Role.',
     'staff_id': 940570942332092486, 'time_period': False, 'role_id': 1065986585847406613, 'time': None}], 'mlbb': [
    {'type': 'transaction', 'name': '1x Livestream Flower', 'description': 'Mobile Legends Streaming Gift',
     'price': 8000, 'transaction': '{member.name} ({member.mention}) has purchased a 1x Livestream Flower.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Any 20 Diamonds Charisma Gift', 'description': 'Mobile Legends Charisma Gift',
     'price': 18000, 'transaction': '{member.name} ({member.mention}) has purchased a 20 Diamonds Charisma Gift.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Any 79 Diamonds Emote', 'description': 'Mobile Legends Emote', 'price': 30000,
     'transaction': '{member.name} ({member.mention}) has purchased a 79 Diamonds Charisma Gift.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Painted Skin', 'description': 'Mobile Legends Skin', 'price': 55000,
     'transaction': '{member.name} ({member.mention}) has purchased a MLBB Painted Skin.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Normal Skin', 'description': 'Mobile Legends Skin', 'price': 97000,
     'transaction': '{member.name} ({member.mention}) has purchased a MLBB Normal Skin.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Elite Skin', 'description': 'Mobile Legends Skin', 'price': 137000,
     'transaction': '{member.name} ({member.mention}) has purchased a MLBB Elite Skin.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Special Skin', 'description': 'Mobile Legends Skin', 'price': 185000,
     'transaction': '{member.name} ({member.mention}) has purchased a MLBB Special Skin.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Epic Skin', 'description': 'Mobile Legends Skin', 'price': 225000,
     'transaction': '{member.name} ({member.mention}) has purchased a MLBB Epic Skin.', 'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': 'Starlight Membership', 'description': 'Mobile Legends Starlight Membership',
     'price': 105000, 'transaction': '{member.name} ({member.mention}) has purchased a Starlight Membership.',
     'staff_id': 940570942332092486}], 'genshin': [
    {'type': 'transaction', 'name': '60 Genesis Crystal', 'description': 'Genshin Impact Genesis Crystal',
     'price': 44000, 'transaction': '{member.name} ({member.mention}) has purchased 60 Genesis Crystal.',
     'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': '330 Genesis Crystal', 'description': 'Genshin Impact Genesis Crystal',
     'price': 125000, 'transaction': '{member.name} ({member.mention}) has purchased 330 Genesis Crystal.',
     'staff_id': 940570942332092486}], 'roblox': [
    {'type': 'transaction', 'name': '80 Robux', 'description': 'Roblox Robux', 'price': 62000,
     'transaction': '{member.name} ({member.mention}) has purchased 80 Robux.', 'staff_id': 940570942332092486},
    {'type': 'transaction', 'name': '110 Robux', 'description': 'Roblox Robux', 'price': 85000,
     'transaction': '{member.name} ({member.mention}) has purchased 110 Robux.', 'staff_id': 940570942332092486}],
    'valorant': [{'type': 'transaction', 'name': '300 Valorant Points', 'description': 'Valorant Points',
                  'price': 57000,
                  'transaction': '{member.name} ({member.mention}) has purchased 300 Valorant Points.',
                  'staff_id': 940570942332092486}], 'discord': [
        {'type': 'transaction', 'name': 'Nitro Basic', 'description': 'Nitro Basic Membership', 'price': 70000,
         'transaction': '{member.name} ({member.mention}) has purchased Nitro Basic.', 'staff_id': 940570942332092486},
        {'type': 'transaction', 'name': 'Nitro', 'description': 'Nitro Membership', 'price': 110000,
         'transaction': '{member.name} ({member.mention}) has purchased Nitro.', 'staff_id': 940570942332092486}]}

# Embed Configuration
embed_success_color = 0x2ecc71
embed_info_color = 0xff8d00
embed_error_color = 0xf44336
embed_purple = 0xCBC3E3
embed_red = 0xFF0000
profile_picture = "https://cdn.discordapp.com/attachments/1022541233383559209/1035879359266947142/Screenshot_1147.png"
thumbnail = "https://cdn.discordapp.com/attachments/1022541233383559209/1035879359266947142/Screenshot_1147.png"

heroes = ["Novaria", "Arlott", "Joy", 'Aamon', 'Akai', 'Aldous', 'Alice', 'Alpha', 'Alucard', 'Angela', 'Argus',
          'Atlas', 'Aurora', 'Aulus', 'Badang', 'Balmond', 'Bane', 'Barats', 'Baxia', 'Beatrix', 'Belerick',
          'Benedetta', 'Brody', 'Bruno', 'Carmilla', 'Cecilion', "Chang'e", 'Chou', 'Claude', 'Clint', 'Cyclops',
          'Diggie', 'Dyrroth', 'Esmeralda', 'Edith', 'Estes', 'Eudora', 'Fanny', 'Faramis', 'Floryn', 'Franco',
          'Fredrinn', 'Freya', 'Gatotkaca', 'Gloo', 'Gord', 'Granger', 'Grock', 'Guinevere', 'Gusion', 'Hanabi',
          'Hanzo', 'Harith', 'Harley', 'Hayabusa', 'Helcurt', 'Hilda', 'Hylos', 'Irithel', 'Jawhead', 'Johnson',
          'Julian', 'Kadita', 'Kagura', 'Kaja', 'Karina', 'Karrie', 'Khaleed', 'Khufra', 'Kimmy', 'Lancelot',
          'Lapu-lapu', 'Layla', 'Leomord', 'Lesley', 'Ling', 'Lolita', 'Lunox', 'Luo yi', 'Lylia', 'Mathilda', 'Martis',
          'Masha', 'Melissa', 'Minotaur', 'Minsitthar', 'Miya', 'Moskov', 'Nana', 'Natan', 'Natalia', 'Odette',
          'Pharsa', 'Phoveus', 'Popol and Kupa', 'Paquito', 'Rafaela', 'Roger', 'Ruby', 'Saber', 'Selena', 'Silvanna',
          'Sun', 'Terizla', 'Thamuz', 'Tigreal', 'Uranus', 'Vale', 'Valentina', 'Valir', 'Vexana', 'Wanwan', 'Xavier',
          'X.borg', 'Yin', 'Yi Sun-Shin', 'Yuzhong', 'Yve', 'Zhask', 'Zilong']
spells = ["Execute", "Retribution", "Inspire", "Sprint", "Revitalize", "Aegis", "Petrify", "Purify", "Flameshot",
          "Flicker", "Arrival", "Vengeance"]

tournament_rules = """
1. No trash talking
2. No cheats/hack
3. No bribe
4. Must follow game rules
5. No rage quit
"""


def calculate_unix_seconds(year, month, day, hour, minute):
    tz = pytz.timezone("UTC")
    dt = datetime.datetime(year, month, day, hour, minute, tzinfo=tz)
    unix_timestamp = int(dt.timestamp())
    return unix_timestamp - 8 * 60 * 60


# ID Configuration
channel_ids = {
    "welcomes": 987358087327387708,
    "errors": 1036546879741243393,
    "logs": 987396702073921626,
    "shop": 1036907324532588584,
    "confession": 1044927789284982814,
    "logs2": 1021391202756595712
}

emoji_field = {
    'star': "<:A1_Dream_Star:1081265844119679006>",
    'candy': "<:A1_Estrella_Candy:1081274689416081518>",
    'snow': "<:A1_Snow_Shards:1081247899544989796>",
    'dstar': "<:A1_Dream_Star:1081265844119679006>",
    'dcandy': "<:A1_Estrella_Candy:1081274689416081518>",
    'dsnow': "<:A1_Snow_Shards:1081247899544989796>"
}

emoji_ids = {
    'dreamstar': 1038311533291253801,
    'candy': 1046331415811338320,
    'snow': 1046331395544449105
}
