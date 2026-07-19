"""
"Honeypot" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import logging

# Third Party
from discord import Bot, Message, User
from discord.ext import commands

# Alliance Auth Discord Bot
from aadiscordbot.app_settings import get_admins

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.helper import unload_cog
from tnnt_discordbot_cogs.models.setting import Setting

logger = logging.getLogger(__name__)


class Honeypot(commands.Cog):
    """
    Monitor specific channels, ban any users that post here with the exception of configured admin users.
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def ban_user(self, message: Message) -> None:
        """
        Ban users who write in the monitored channels

        :param message: The message the user has sent
        :type message: Message
        :return: None
        :rtype: None
        """

        if message.author.bot is True:
            # Easy out, dont catch self or other bots
            return

        if type(message.author) is User:
            # Users are DMs or have left
            return

        if message.channel.id in Setting.get_setting(
            Setting.Field.HONEYPOT_CHANNELS
        ).values_list("channel", flat=True):
            author = message.author
            # Caching this here incase it gets lost after the kick
            display_name: str = message.author.display_name
            channel = self.bot.get_channel(message.channel.id)

            if message.author.id in get_admins():
                await message.delete()
                await channel.send(
                    content=f"Test Complete <@{author.id}>, you nearly airlocked yourself :sweat_smile:",
                    delete_after=5,
                )

                return

            try:
                # Ban the user and delete 10 minutes worth of messages, _on this server_
                # TODO: Consider writing a cross server cleanup task, but this is inbuilt to discord and works.
                await message.author.ban(
                    delete_message_seconds=600, reason="aadiscordbot.cogs.honeypot"
                )
            except Exception as e:
                logger.error(e)
                pass

            try:
                await channel.send(
                    content=f"Yeet <@{author.id}> `{display_name}`", delete_after=300
                )
            except Exception as e:
                logger.error(e)
                pass

            return
        else:
            return


def setup(bot: commands.Bot) -> None:
    """
    Setup function for the Honeypot cog.

    :param bot: The bot instance to which this cog is attached.
    :type bot: commands.Bot
    :return: None
    :rtype: None
    """

    # Unload any other Honeypot cog
    unload_cog(bot=bot, cog_name="Honeypot")

    # Add the Lookup cog to the bot
    bot.add_cog(Honeypot(bot))
