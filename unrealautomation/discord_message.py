import requests
from . import config, secrets, ctx


def execute():
    url_title = config['DiscordMessageUrlTitle']
    content = config["DiscordMessagePrefix"] + f'[{url_title}]({ctx.public_url})'

    discord_webhook_url = secrets['DiscordWebhookUrl']
    try:
        response = requests.post(discord_webhook_url, data={"content": content})
    except requests.exceptions.ReadTimeout:
        print('Failed to reach discord API (timeout)')
        return False

    return response.ok
