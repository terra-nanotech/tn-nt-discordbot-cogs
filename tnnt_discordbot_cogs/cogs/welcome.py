"""
"Welcome" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import asyncio
import logging

# Third Party
import discord
from aadiscordbot.app_settings import get_site_url
from aadiscordbot.models import WelcomeMessage
from aadiscordbot.utils.auth import is_user_authenticated
from discord.ext import commands

# Django
from django.conf import settings
from django.db.models import Q

logger = logging.getLogger(__name__)


class Welcome(commands.Cog):
    """
    Responds to on_member_join events from discord
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        """
        Responds to on_member_join events from discord

        :param member: discord.Member object representing the new member
        :type member: discord.Member
        :return: None
        :rtype: None
        """

        logger.info(msg=f"{member} joined {member.guild.name}")
        channel = member.guild.system_channel

        logger.debug(f"Channel: {channel}")

        if channel is not None:
            try:
                # Give AA a chance to save the UID for a joiner.
                await asyncio.sleep(3)

                authenticated = is_user_authenticated(user=member, guild=member.guild)
            except Exception:
                authenticated = False

            if authenticated:
                channel_id = getattr(
                    settings, "TNNT_DISCORDBOT_COGS_WELCOME_CHANNEL_AUTHENTICATED", None
                )

                if isinstance(channel_id, int):
                    channel = member.guild.get_channel(channel_id)

                try:
                    message = (
                        WelcomeMessage.objects.filter(
                            Q(Q(guild_id=member.guild.id) | Q(guild_id=None)),
                            authenticated=True,
                        )
                        .order_by("?")
                        .first()
                        .message
                    )
                    message_formatted = message.format(
                        user_mention=member.mention,
                        guild_name=member.guild.name,
                        auth_url=get_site_url(),
                    )

                    await channel.send(content=message_formatted)
                except IndexError:
                    logger.error(
                        msg="No Welcome Message configured for Discordbot Welcome cog"
                    )
                except Exception as e:
                    logger.error(msg=e)
            else:
                try:
                    message = (
                        WelcomeMessage.objects.filter(
                            Q(Q(guild_id=member.guild.id) | Q(guild_id=None)),
                            unauthenticated=True,
                        )
                        .order_by("?")
                        .first()
                        .message
                    )
                    message_formatted = message.format(
                        user_mention=member.mention,
                        guild_name=member.guild.name,
                        auth_url=get_site_url(),
                    )

                    await channel.send(message_formatted)
                except IndexError:
                    logger.error(
                        msg="No Welcome Message configured for Discordbot Welcome cog"
                    )
                except Exception as e:
                    logger.error(msg=e)


def setup(bot):
    """
    Set up the cog

    :param bot: discord bot
    """

    if bot.get_cog("Welcome") is None:
        bot.add_cog(Welcome(bot))
