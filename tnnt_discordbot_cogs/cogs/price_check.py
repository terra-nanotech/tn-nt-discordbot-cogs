"""
Market Price Checks cog for discordbot - https://github.com/pvyParts/allianceauth-discordbot
"""

# Standard Library
import locale
import logging
from typing import Coroutine

# Third Party
import requests
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands

# Alliance Auth (External Libs)
from eveuniverse.models import EveEntity

logger = logging.getLogger(__name__)


class PriceCheck(commands.Cog):
    """
    Price checks on Jita, Amarr, Rens, Hek and Dodixie markets
    """

    imageserver_url = "https://images.evetech.net"

    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def _build_market_price_embed(
        cls, embed: Embed, market: dict, item_name: str, eve_type_id: str
    ) -> None:
        """
        Build the price embed for the selected market

        :param embed:
        :type embed:
        :param market:
        :type market:
        :param item_name:
        :type item_name:
        :param eve_type_id:
        :type eve_type_id:
        :return:
        :rtype:
        """

        market_system_name = market["name"]
        market_system_id = market["system_id"]
        url = "https://market.fuzzwork.co.uk/aggregates/"
        url_params = {"system": market_system_id, "types": eve_type_id}
        market_data = requests.get(url=url, params=url_params, timeout=2.50)

        embed.add_field(
            name=market_system_name,
            value=f"Prices for {item_name} on the {market_system_name} Market.",
            inline=False,
        )

        if market_data.status_code == 200:
            market_json = market_data.json()

            sell_min = market_json[eve_type_id]["sell"]["min"]
            sell_order_count = market_json[eve_type_id]["sell"]["orderCount"]
            buy_max = market_json[eve_type_id]["buy"]["max"]
            buy_order_count = market_json[eve_type_id]["buy"]["orderCount"]
            thumbnail_url = f"{cls.imageserver_url}/types/{eve_type_id}/icon?size=64"

            # Set the Embed thumbnail
            embed.set_thumbnail(url=thumbnail_url)

            locale.setlocale(category=locale.LC_ALL, locale="")

            # Sell order price
            market_min_sell_order_price = locale.format_string(
                f="%.2f", val=float(sell_min), grouping=True
            )

            if sell_order_count == 0:
                market_min_sell_order_price = "No sell orders found"

            embed.add_field(
                name=f"Sell Order Price ({sell_order_count} Orders)",
                value=f"{market_min_sell_order_price} ISK",
                inline=True,
            )

            # Buy order price
            market_max_buy_order_price = locale.format_string(
                f="%.2f", val=float(buy_max), grouping=True
            )

            if buy_order_count == 0:
                market_max_buy_order_price = "No buy orders found"

            embed.add_field(
                name=f"Buy Order Price ({buy_order_count} Orders)",
                value=f"{market_max_buy_order_price} ISK",
                inline=True,
            )
        else:
            embed.add_field(
                name="API Error",
                value=(
                    f"Could not not fetch the price for the {market_system_name} market."
                ),
                inline=False,
            )

    @commands.command(pass_context=True)
    async def price(self, ctx):
        """
        Check an item price on all major market hubs

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """

        markets = [
            {"name": "Jita", "system_id": 30000142},
            {"name": "Amarr", "system_id": 30002187},
            {"name": "Rens", "system_id": 60004588},
            {"name": "Hek", "system_id": 60005686},
            {"name": "Dodixie", "system_id": 30002659},
        ]

        await ctx.trigger_typing()

        item_name = ctx.message.content[7:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    @commands.command(pass_context=True)
    async def jita(self, ctx):
        """
        Check an item price on Jita market

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """

        markets = [{"name": "Jita", "system_id": 30000142}]

        await ctx.trigger_typing()

        item_name = ctx.message.content[6:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    @commands.command(pass_context=True)
    async def amarr(self, ctx):
        """
        Check an item price on Amarr market

        :param ctx:
        :type ctx:
        :return:
        :rtype:
        """

        markets = [{"name": "Amarr", "system_id": 60008494}]

        await ctx.trigger_typing()

        item_name = ctx.message.content[7:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    async def price_check(self, ctx, markets, item_name: str = None) -> Coroutine:
        """
        Do the price checks and post to Discord

        :param ctx:
        :type ctx:
        :param markets:
        :type markets:
        :param item_name:
        :type item_name:
        :return:
        :rtype:
        """

        await ctx.trigger_typing()

        if item_name != "":
            try:
                eve_type = (
                    EveEntity.objects.fetch_by_names_esi([item_name])
                    .filter(category=EveEntity.CATEGORY_INVENTORY_TYPE)
                    .values_list("id", flat=True)
                )

                eve_type_id = str(eve_type[0])
            except (EveEntity.DoesNotExist, IndexError):
                embed = Embed(
                    title=f"Price Lookup for {item_name}",
                    color=Color.orange(),
                )

                embed.add_field(
                    name="Error",
                    value=(
                        f"{item_name} could not be found. "
                        "Are you sure you spelled it correctly?"
                    ),
                    inline=False,
                )
            else:
                embed = Embed(
                    title=f"Price Lookup for {item_name}",
                    color=Color.green(),
                )

                for market in markets:
                    self._build_market_price_embed(
                        embed=embed,
                        market=market,
                        item_name=item_name,
                        eve_type_id=eve_type_id,
                    )
        else:
            embed = Embed(
                title="Price Lookup",
                color=Color.red(),
            )

            embed.add_field(
                name="Error",
                value=(
                    "You forget to enter an item you want to lookup the price for ..."
                ),
                inline=False,
            )

        return await ctx.send(embed=embed)


def setup(bot) -> None:
    """
    Set up the cog

    :param bot:
    :type bot:
    :return:
    :rtype:
    """

    bot.add_cog(PriceCheck(bot))
