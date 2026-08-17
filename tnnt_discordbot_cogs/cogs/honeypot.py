"""
"Honeypot" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import io
import logging

# Third Party
from discord import Bot, File, Message, User
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
            # Preserve the full message content for reporting. Wrap in a code
            # block and escape any triple-backticks in the original message so
            # the report's fence isn't broken (which can result in content
            # appearing missing, e.g. the first line being lost).
            raw_user_message = (
                message.content
                if message.content
                else "No message content, probably just images or embeds…"
            )

            # Format the message creation timestamp as YYYY.MM.DD hh:mm:ss
            created_at_str = message.created_at.strftime("%Y.%m.%d %H:%M:%S")
            report_message = f"## {created_at_str} EVE Time - Honeypot triggered\n"

            await message.delete()

            if message.author.id in get_admins():
                await channel.send(
                    content=f"Test Complete <@{author.id}>, you nearly airlocked yourself :sweat_smile:",
                    delete_after=5,
                )

                # If a report channel is configured, send a report to it
                if (
                    Setting.get_setting(Setting.Field.HONEYPOT_REPORT_CHANNEL)
                    is not None
                ):
                    report_channel = self.bot.get_channel(
                        Setting.get_setting(
                            Setting.Field.HONEYPOT_REPORT_CHANNEL
                        ).channel
                    )
                    report_message += (
                        f"User <@{author.id}> `{display_name}` nearly airlocked "
                        "themselves in a honeypot channel on "
                        f"server _{message.guild.name}_, but was saved by their admin status.\n\n"
                        "### Message content"
                    )

                    # Attach the raw message content as a file to avoid any
                    # discord markdown/code-fence parsing issues.
                    try:
                        bio = io.BytesIO(raw_user_message.encode("utf-8"))
                        bio.seek(0)

                        await report_channel.send(
                            content=report_message,
                            file=File(bio, filename="honeypot_message.txt"),
                        )
                    except Exception:
                        logger.exception("Failed to send honeypot report")

                return

            try:
                # Ban the user and delete 10 minutes worth of messages, _on this server_
                # TODO: Consider writing a cross server cleanup task, but this is inbuilt to discord and works.
                await message.author.ban(
                    delete_message_seconds=600, reason="Triggered the honeypot!"
                )

                # If a report channel is configured, send a report to it
                if (
                    Setting.get_setting(Setting.Field.HONEYPOT_REPORT_CHANNEL)
                    is not None
                ):
                    report_channel = self.bot.get_channel(
                        Setting.get_setting(
                            Setting.Field.HONEYPOT_REPORT_CHANNEL
                        ).channel
                    )
                    report_message += (
                        f"User <@{author.id}> `{display_name}` has been banned from "
                        f"server _{message.guild.name}_ for posting in a honeypot channel.\n\n"
                        "### Message content"
                    )

                    # Attach the raw message content as a file to avoid any
                    # discord markdown/code-fence parsing issues.
                    try:
                        bio = io.BytesIO(raw_user_message.encode("utf-8"))
                        bio.seek(0)

                        await report_channel.send(
                            content=report_message,
                            file=File(bio, filename="honeypot_message.txt"),
                        )
                    except Exception:
                        logger.exception("Failed to send honeypot report")
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
