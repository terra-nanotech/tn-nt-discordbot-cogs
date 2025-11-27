"""
Helper functions for the TNNT Discord bot.
"""

# Standard Library
from urllib.parse import urljoin

# Third Party
from discord.ext import commands

# Django
from django.conf import settings
from django.urls import reverse


def unload_cog(bot: commands.Bot, cog_name: str) -> None:
    """
    Unloads a cog from the bot.

    :param bot: The bot instance.
    :type bot: discord.ext.commands.Bot
    :param cog_name: The name of the cog to unload.
    :type cog_name: str
    """

    try:
        bot.remove_cog(name=cog_name)

        print(f"Unloaded {cog_name} successfully.")
    except Exception as e:
        print(f"Failed to unload {cog_name}: {e}")


def reverse_absolute(viewname: str, args: list | None = None) -> str:
    """
    Return absolute URL for a view name.

    Similar to Django's ``reverse()``, but returns an absolute URL.
    """

    return urljoin(base=settings.SITE_URL, url=reverse(viewname=viewname, args=args))
