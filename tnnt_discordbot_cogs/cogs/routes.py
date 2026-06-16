"""
"Routes" cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import logging

# Third Party
from corptools.models import MapJumpBridge, MapSystem
from corptools.providers import routes
from discord import AutocompleteContext, option
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands

# Alliance Auth Discord Bot
from aadiscordbot.app_settings import get_all_servers

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.helper import unload_cog

logger = logging.getLogger(__name__)


class Routes(commands.Cog):
    """
    Find your way through New Eden
    """

    def __init__(self, bot):
        """
        Initialize the cog

        :param bot:
        :type bot:
        """

        self.bot = bot

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

    @commands.slash_command(name="route", guild_ids=get_all_servers())
    @option("start", description="Your start system…", autocomplete=search_systems)
    @option(
        "destination",
        description="Your destination system…",
        autocomplete=search_systems,
    )
    async def route(self, ctx, start: str, destination: str):
        """
        Find a route in EVE (with Jumpbridges)
        """

        await ctx.defer(ephemeral=True)

        start = MapSystem.objects.get(name=start)
        end = MapSystem.objects.get(name=destination)

        message = routes.route(start.system_id, end.system_id)

        dotlan_url = "https://evemaps.dotlan.net/route/{}".format(message.get("dotlan"))
        embed = Embed(title=f"{start.name} to {end.name}")
        embed.colour = Color.blue()
        embed.description = "Shortest Route is: {} Jumps\n\n{}".format(
            message.get("length"), message.get("path_message")
        )
        embed.add_field(name="Dotlan", value=f"[Route Link]({dotlan_url})")

        return await ctx.respond(embed=embed, ephemeral=True)

    @commands.slash_command(name="jumpbridges", guild_ids=get_all_servers())
    async def jumpbridges(self, ctx):
        """
        List all known Jumpbridges
        """

        await ctx.defer(ephemeral=True)

        embed = Embed(title="Known Jumpbridges")
        embed.colour = Color.blue()
        embed.description = (
            "These do not auto populate. Please advise admins of ommissions/errors!\n\n"
        )

        jbs = MapJumpBridge.objects.all().select_related(
            "from_solar_system", "to_solar_system", "owner"
        )

        for jb in jbs:
            embed.description += f"`{jb.from_solar_system.name}` > `{jb.to_solar_system}` [{jb.owner.name}]\n"

        return await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    """
    Set up the Routes cog

    :param bot: discord bot
    """

    # Unload the Routes cog from `aadiscordbot`, so we can load our own.
    unload_cog(bot=bot, cog_name="Routes")

    # Add the Welcome cog to the bot
    bot.add_cog(Routes(bot))
