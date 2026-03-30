"""
"Locator" cog for discordbot - https://github.com/Solar-Helix-Independent-Transport/allianceauth-discordbot
"""

# Third Party
from discord import Colour, Embed, EmbedField, option
from discord.ext import commands
from eve_sde.models import ItemType, SolarSystem
from pendulum.datetime import DateTime

# Django
from django.core.exceptions import ObjectDoesNotExist

# Alliance Auth
from allianceauth.eveonline.evelinks import dotlan, evewho
from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger
from esi.models import Token

# Alliance Auth Discord Bot
from aadiscordbot.app_settings import get_all_servers
from aadiscordbot.cogs.utils.autocompletes import search_characters
from aadiscordbot.cogs.utils.decorators import message_in_channels, sender_has_perm

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs import __title__
from tnnt_discordbot_cogs.helper import unload_cog
from tnnt_discordbot_cogs.models.setting import Setting
from tnnt_discordbot_cogs.providers import AppLogger, ESIHandler

logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)


class Locator(commands.Cog):
    """
    A cog to locate characters and their alts in EVE Online.
    """

    def __init__(self, bot):
        """
        Initializes the Locator cog.

        :param bot: The bot instance to which this cog is added.
        :type bot: discord.ext.commands.Bot
        """

        self.bot = bot

    @staticmethod
    def _get_locate_channels() -> list:
        """
        Get the locate channels from the settings.

        :return: List of locate channels or an empty list if none are set.
        :rtype: dict
        """

        locate_channels = Setting.get_setting(Setting.Field.LOCATE_CHANNELS.value).all()

        return (
            [channel.channel for channel in locate_channels if channel is not None]
            if locate_channels
            else []
        )

    @staticmethod
    def _get_locate_embeds(char: EveCharacter) -> list[Embed]:
        """
        Generates embeds for the character's alts' locations.

        :param char: The character for which to generate the embeds.
        :type char: allianceauth.eveonline.models.EveCharacter
        :return: A list of Discord embeds containing the location information of the character's alts.
        :rtype: list[discord.Embed]
        """

        alts = char.character_ownership.user.character_ownerships.all().select_related(
            "character"
        )

        alt_online = []
        alt_offline = []
        alt_no_token = []

        for alt in alts:
            _alt = {
                "character_id": alt.character.character_id,
                "character_name": alt.character.character_name,
                "corporation_id": alt.character.corporation_id,
                "corporation_name": alt.character.corporation_name,
                "last_online": DateTime.min,
                "online": False,
                "ship": "",
                "system": None,
                "lookup": False,
            }
            scopes = [
                # Locations
                "esi-location.read_location.v1",
                "esi-location.read_online.v1",
                "esi-location.read_ship_type.v1",
            ]

            token = Token.get_token(
                character_id=alt.character.character_id, scopes=scopes
            )

            if token:
                online = ESIHandler.get_characters_character_id_online(
                    character_id=alt.character.character_id, token=token, use_etag=False
                )
                location_esi = ESIHandler.get_characters_character_id_location(
                    character_id=alt.character.character_id, token=token, use_etag=False
                )
                ship_esi = ESIHandler.get_characters_character_id_ship(
                    character_id=alt.character.character_id, token=token, use_etag=False
                )

                logger.debug(f"Online Status from ESI: {online}")
                logger.debug(f"Location from ESI: {location_esi}")
                logger.debug(f"Ship from ESI: {ship_esi}")

                try:
                    _alt["online_status"] = "Online" if online.online else "Offline"
                except Exception:
                    pass

                try:
                    _alt["last_login"] = online.last_login
                    _alt["last_logout"] = online.last_logout
                except Exception:
                    pass

                location_sde = SolarSystem.objects.get(id=location_esi.solar_system_id)
                ship_sde = ItemType.objects.get(id=ship_esi.ship_type_id)

                logger.debug(f"Location from SDE: {location_sde}")
                logger.debug(f"Ship from SDE: {ship_sde}")

                _alt["system"] = location_sde.name
                _alt["ship"] = ship_sde.name
                _alt["lookup"] = True

                if online.online:
                    alt_online.append(_alt)
                else:
                    alt_offline.append(_alt)
            else:
                alt_no_token.append(_alt)

        out_embeds = []

        def _process_character_list(
            embed_header: str,
            character_list: list[dict],
            embed_color: Colour = Colour.default(),
        ):
            """
            Process list of alt characters and generate the Discord embeds for them.

            :param embed_header: The header for the embed.
            :type embed_header: str
            :param character_list: The list of characters to process.
            :type character_list: list[dict]
            :param embed_color: The color for the embed.
            :type embed_color: discord.Colour
            :return: A list of Discord embeds containing the alt character information.
            :rtype: list[discord.Embed]
            """

            embeds = []

            for alt_character_group in [
                character_list[i : i + 10] for i in range(0, len(character_list), 10)
            ]:
                embed_fields = []

                for alt_character in alt_character_group:
                    logger.debug(f"Processing alt character {alt_character}")

                    evewho_character = evewho.character_url(
                        eve_id=alt_character["character_id"]
                    )
                    evewho_corporation = evewho.corporation_url(
                        eve_id=alt_character["corporation_id"]
                    )
                    character_line = (
                        f"[{alt_character['character_name']}]({evewho_character}) "
                        f"[[{alt_character['corporation_name']}]({evewho_corporation})]"
                    )

                    if alt_character["lookup"]:
                        dotlan_system = dotlan.solar_system_url(
                            name=alt_character["system"]
                        )
                        current_location_line = (
                            f"[{alt_character['system']}]({dotlan_system}) "
                            f"(**{alt_character['online_status']}**)"
                        )

                        login_time_line = (
                            f"**Offline Since:** {alt_character['last_logout'].strftime('%Y-%m-%d %H:%M')}"
                            if alt_character["online_status"] == "Offline"
                            else f"**Online Since:** {alt_character['last_login'].strftime('%Y-%m-%d %H:%M')}"
                        )

                        embed_fields.append(
                            EmbedField(
                                name=f"### {alt_character['character_name']} ###",
                                value=(
                                    f"**EVE Who:** {character_line}\n"
                                    f"**Current Location:** {current_location_line}\n"
                                    f"**Currently Flying:** {alt_character['ship']}\n"
                                    f"{login_time_line} EVE Time"
                                ),
                                inline=False,
                            )
                        )
                    else:
                        embed_fields.append(
                            EmbedField(
                                name=f"### {alt_character['character_name']} ###",
                                value=f"**EVEWho:** {character_line}",
                                inline=False,
                            )
                        )

                embed = Embed(
                    title=embed_header, fields=embed_fields, colour=embed_color
                )
                embeds.append(embed)

            return embeds

        for header, characters, color in [
            ("Online Characters", alt_online, Colour.green()),
            ("Offline Characters", alt_offline, Colour.orange()),
            ("No Tokens", alt_no_token, Colour.red()),
        ]:
            if characters:
                out_embeds += _process_character_list(
                    embed_header=header, character_list=characters, embed_color=color
                )

        return out_embeds

    @message_in_channels(channels=_get_locate_channels())
    @sender_has_perm("tnnt_discordbot_cogs.locate")
    @commands.slash_command(name="locate", guild_ids=get_all_servers())
    @option(
        name="character",
        description="Search for a Character!",
        autocomplete=search_characters,
    )
    async def locate(self, ctx, character: str):
        """
        Slash command to locate a character and their alts in EVE Online.

        :param ctx:
        :type ctx:
        :param character:
        :type character:
        :return:
        :rtype:
        """

        try:
            char = EveCharacter.objects.get(character_name=character)
        except EveCharacter.DoesNotExist:
            return await ctx.respond(
                f"Character **{character}** does not exist in our Auth system",
                ephemeral=True,
            )

        try:
            main = char.character_ownership.user.profile.main_character
        except ObjectDoesNotExist:
            return await ctx.respond(
                f"Character **{character}** Unlinked in auth", ephemeral=True
            )

        try:
            discord_string = f"<@{char.character_ownership.user.discord.uid}>"
        except Exception as e:
            logger.error(e)
            discord_string = "unknown"

        await ctx.respond(
            (
                f"Looking up the location of all known alts of {main} ({discord_string})\n"
                "Please Wait..."
            ),
            ephemeral=True,
        )

        embeds = self._get_locate_embeds(char)

        for e in embeds:
            await ctx.respond(embed=e, ephemeral=True)


def setup(bot):
    # Unload the Members cog from `aadiscordbot`
    unload_cog(bot=bot, cog_name="Locator")

    # Add the Lookup cog to the bot
    bot.add_cog(Locator(bot))
