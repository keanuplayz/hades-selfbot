# Library imports
import os
import json
import argparse
import discord
from discord.ext import commands

# Cog imports
from cogs.util.config import write_config_value, get_config_value


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(description="Discord Selfbot")
    parser.add_argument('--reset-config', action="store_true",
                        help="Reruns the setup")
    return parser


args = parse_cmd_arguments().parse_args()
_reset_cfg = args.reset_config


def wizard():
    config = {}
    print("Welcome to the Hades selfbot setup wizard.\nAll choices you make during this wizard can be changed by editing the settings/config.json file.")

    print("Enter your user token here.")
    print("-------------------------------------------------------------")
    config["token"] = input("| ").strip().strip(" ")

    config["cmd_prefix"] = False
    while not config["cmd_prefix"]:
        print("Please enter the prefix you would like to use for triggering commands.")
        print("-------------------------------------------------------------")
        config["cmd_prefix"] = input("| ").strip()
        if not config["cmd_prefix"]:
            print("Empty command prefixes are invalid.")

    input(
        "Your settings:\nPrefix: {prefix} | e.g. {prefix}ping\n\nPress enter to start.".format(prefix=config["cmd_prefix"]))
    with open("settings/config.json", encoding="utf8", mode="w") as f:
        json.dump(config, f, sort_keys=True, indent=4)


samples = os.listdir("settings")
for f in samples:
    if f.endswith("sample") and f.rsplit('.', 1)[0] not in samples:
        with open("settings/%s" % f, 'r', encoding="utf8") as template:
            with open("settings/%s" % f.rsplit('.', 1)[0], "w", encoding="utf8") as g:
                fields = json.load(template)
                json.dump(fields, g, sort_keys=True, indent=4)

bot = commands.Bot(command_prefix=get_config_value(
    'config', 'cmd_prefix'), description='''Hades Selfbot''', self_bot=True)


@bot.event
async def on_ready():
    print(f"huEHEHUHUUE\nlogged in as {bot.user.name}")


@bot.command()
async def ping(ctx):
    await ctx.send("PONG AHAHAHHA")

if _reset_cfg:
    wizard()

if __name__ == "__main__":
    for extension in os.listdir("cogs"):
        if extension.endswith(".py"):
            try:
                bot.load_extension("cogs." + extension[:-3])
            except:
                print("Failed to load extension {}\n{}: {}".format(
                    extension, type(e).__name__, e))

    while True:
        token = get_config_value("config", "token")
        try:
            bot.run(token, bot=False)
        except discord.errors.LoginFailure:
            print("Token is incorrect!")
            print("Enter your token below.")
            print("-------------------------------------------------------------")
            token = input("| ").strip('"')
            with open("settings/config.json", "r+", encoding="utf8") as fp:
                config = json.load(fp)
                config["token"] = token
                fp.seek(0)
                fp.truncate()
                json.dump(config, fp, indent=4)
            continue
        break
