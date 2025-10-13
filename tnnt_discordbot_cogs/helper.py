"""
Helper functions for the TN-NT Discord bot.
"""

# Third Party
from discord.ext import commands

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter


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
    except Exception as e:  # pylint: disable=broad-except
        print(f"Failed to unload {cog_name}: {e}")


def get_discord_id(character: EveCharacter) -> int | None:
    """
    Get the Discord ID associated with an EveCharacter.

    :param character: The EveCharacter instance.
    :type character: allianceauth.eveonline.models.EveCharacter
    :return: The Discord ID if found, else None.
    :rtype: int | None
    """

    try:
        return character.character_ownership.user.discord.uid
    except AttributeError:
        return None
