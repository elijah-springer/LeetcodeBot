import configparser
from pathlib import Path
from typing import Any

import discord
from discord import Intents

CONFIG_PATH = Path('./bot.conf')
REQUIRED_CONFIG_SECTIONS = ['Token', 'ClientId']


class BotClient(discord.Client):
    def __init__(self, *, client_id, intents: Intents, **options: Any):
        self.client_id = client_id
        super().__init__(intents=intents, **options)

    async def on_ready(self):
        print(discord.utils.oauth_url(client_id=self.client_id, permissions=discord.Permissions.all()))
        print(f'logged on as {self.user}')

    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.TextChannel):
            if message.author.id == self.user.id:
                return
            await message.channel.send(f'hi, {message.author} hehe!')

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        print("there was a reaction")


def parse_config_file(file_path, required_sections):
    # Load config
    config = configparser.ConfigParser()
    if not CONFIG_PATH.exists() or not CONFIG_PATH.is_file():
        print("Could not find configuration file, generating new one...")
        config['DEFAULT'] = {}
        for section in required_sections:
            config['DEFAULT'][section] = ''
        with open(CONFIG_PATH, 'w') as configFile:
            config.write(configFile)

    config.read(CONFIG_PATH)

    for section in required_sections:
        # Make sure each section exists and is defined
        if section not in config['DEFAULT'] or not config['DEFAULT'][section]:
            print(f'Section {section} is missing from configuration file {CONFIG_PATH}, exiting!')
            exit(-1)
    return config['DEFAULT']  # Only one section, just return that for now


if __name__ == '__main__':
    config = parse_config_file(CONFIG_PATH, REQUIRED_CONFIG_SECTIONS)
    token = config['Token']
    client_id = config['ClientId']

    # Start the bot
    intents = discord.Intents.default()
    intents.message_content = True

    client = BotClient(client_id=client_id, intents=intents)
    client.run(token)
