"""
"WhereIs" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import logging

# Third Party
from corptools.models import CharacterAsset, EveItemType, MapSystem
from discord import AutocompleteContext, option
from discord.embeds import Embed
from discord.ext import commands

# Django
from django.db.models import Q
from django.db.models.functions import Length

# Alliance Auth
from allianceauth.services.modules.discord.models import DiscordUser

# Alliance Auth Discord Bot
from aadiscordbot.app_settings import get_all_servers
from aadiscordbot.cogs.utils.decorators import has_any_perm
from aadiscordbot.utils.auth import get_auth_user

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.helper import unload_cog

logger = logging.getLogger(__name__)


class WhereIs(commands.Cog):
    """
    Help me find my stuff without logging in every single character!
    """

    def __init__(self, bot):
        """
        Initialize the cog

        :param bot:
        :type bot:
        """

        self.bot = bot

    @staticmethod
    def pluralize(name: str) -> str:
        """
        Very small pluralizer for simple English words.

        :param name:
        :type name:
        :return:
        :rtype:
        """

        if not name:
            return name

        lower = name.lower()

        # common endings that take 'es'
        if lower.endswith(("s", "x", "z")) or lower.endswith(("ch", "sh")):
            return name + "es"

        # words ending in consonant + y -> replace y with ies
        if lower.endswith("y") and len(name) >= 2 and name[-2].lower() not in "aeiou":
            return name[:-1] + "ies"

        # default: add 's'
        return name + "s"

    @staticmethod
    async def search_items(ctx: AutocompleteContext):
        """
        Returns a list of items that begin with the characters entered so far

        :return:
        :rtype:
        """

        return [
            a
            async for a in EveItemType.objects.filter(name__icontains=ctx.value)
            .order_by(Length("name").asc())
            .values_list("name", flat=True)
            .distinct()[:10]
        ]

    @staticmethod
    async def search_systems(ctx: AutocompleteContext):
        """
        Returns a list of systems that begin with the characters entered so far.

        :return:
        :rtype:
        """

        return [
            a
            async for a in MapSystem.objects.filter(name__icontains=ctx.value)
            .values_list("name", flat=True)
            .distinct()[:10]
        ]

    @commands.slash_command(name="where_is", guild_ids=get_all_servers())
    @option("system", description="Search in this System!", autocomplete=search_systems)
    @option("item", description="Search for this Item!", autocomplete=search_items)
    async def slash_where_is(self, ctx, item: str, system: str = None):
        """
        Find where you missplaced your stuff

        :param ctx:
        :type ctx:
        :param item:
        :type item:
        :param system:
        :type system:
        :return:
        :rtype:
        """
        await ctx.defer(ephemeral=True)

        try:
            has_any_perm(ctx.author.id, ["corptools.view_characteraudit"], ctx.guild)

            try:
                du = get_auth_user(ctx.author, guild=ctx.guild)
                chars = du.character_ownerships.all().values_list(
                    "character__character_id", flat=True
                )

                try:
                    items = CharacterAsset.objects.filter(
                        character__character__character_id__in=chars,
                        type_name__name=item,
                        location_name__isnull=False,
                    )

                    if system:
                        items = items.filter(
                            Q(location_name__location_name=system)
                            | Q(location_name__system__name=system)
                        )

                    if not await items.aexists():
                        return await ctx.respond(
                            "Found no items. Do you actually have some?", ephemeral=True
                        )

                    output = {}
                    total_count = 0

                    async for i in items:
                        total_count += 1
                        cn = i.character.character.character_name

                        if cn not in output:
                            output[cn] = set()

                        output[cn].add(f"{i.location_name.location_name}")

                    e = Embed(title=f"{item} Search")

                    # Build a header that is singular/plural aware
                    if total_count == 1:
                        header = f"Found 1 {item}"
                    else:
                        # if the user already provided a plural-looking word, use it as-is
                        if item.lower().endswith("s"):
                            item_label = item
                        else:
                            item_label = self.pluralize(item)

                        header = f"Found {total_count} {item_label}"

                    if system:
                        header += f" in {system}"

                    msg = header + "\n"

                    for c, locs in output.items():
                        m = f"\n**{c}**"

                        for cl in locs:
                            m += f"\n- {cl}"

                        msg += m

                    msg += "\n"
                    e.description = msg

                    await ctx.respond(embed=e, ephemeral=True)
                except Exception as e:
                    return await ctx.respond(f"An error occured {e}", ephemeral=True)
            except DiscordUser.DoesNotExist:
                return await ctx.respond(
                    "Who are you? Have you linked your discord on auth?", ephemeral=True
                )
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)


def setup(bot):
    """
    Set up the WhereIs cog

    :param bot: discord bot
    """

    # Unload the WhereStuff/WhereIs cog from `aadiscordbot`, so we can load our own.
    unload_cog(bot=bot, cog_name="WhereStuff")
    unload_cog(bot=bot, cog_name="WhereIs")

    # Add the Welcome cog to the bot
    bot.add_cog(WhereIs(bot))
