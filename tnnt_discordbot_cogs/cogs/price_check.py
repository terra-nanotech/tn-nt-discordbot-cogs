"""
Market Price Checks
"""
# Standard Library
import locale
import logging

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
    Price checks on Jita, Amarr, Rens, Hek, Dodixie and Perimeter markets
    """

    imageserver_url = "https://images.evetech.net"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def price(self, ctx):
        """
        Check an item price on all major market hubs
        :param ctx:
        :return:
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
        :return:
        """

        markets = [
            {"name": "Jita", "system_id": 30000142},
        ]

        await ctx.trigger_typing()

        item_name = ctx.message.content[6:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    @commands.command(pass_context=True)
    async def amarr(self, ctx):
        """
        Check an item price on Amarr market
        :param ctx:
        :return:
        """

        markets = [
            {"name": "Amarr", "system_id": 60008494},
        ]

        await ctx.trigger_typing()

        item_name = ctx.message.content[7:]

        await self.price_check(ctx=ctx, markets=markets, item_name=item_name)

    async def price_check(self, ctx, markets, item_name: str = None):
        """
        Do the price checks and post to Discord
        :param ctx:
        :param markets:
        :param item_name:
        :return:
        """

        has_thumbnail = False
        eve_type_id = None

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
                    embed.add_field(
                        name=market["name"],
                        value=f'Prices for {item_name} on the {market["name"]} Market.',
                        inline=False,
                    )

                    system_id = market["system_id"]
                    url = "https://market.fuzzwork.co.uk/aggregates/"
                    url_params = {"system": system_id, "types": eve_type_id}
                    market_data = requests.get(url=url, params=url_params, timeout=2.50)

                    if market_data.status_code == 200:
                        market_json = market_data.json()

                        sell_min = market_json[eve_type_id]["sell"]["min"]
                        sell_order_count = market_json[eve_type_id]["sell"][
                            "orderCount"
                        ]
                        buy_max = market_json[eve_type_id]["buy"]["max"]
                        buy_order_count = market_json[eve_type_id]["buy"]["orderCount"]
                        thumbnail_url = (
                            f"{self.imageserver_url}/types/{eve_type_id}/icon?size=64"
                        )

                        if has_thumbnail is False:
                            embed.set_thumbnail(url=thumbnail_url)
                            has_thumbnail = True

                        # locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
                        locale.setlocale(locale.LC_ALL, "")

                        # Sell order price
                        market_min_sell_order_price = locale.format_string(
                            "%.2f", float(sell_min), grouping=True
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
                            "%.2f", float(buy_max), grouping=True
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
                                f"Could not not fetch the price "
                                f'for the {market["name"]} market.'
                            ),
                            inline=False,
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


def setup(bot):
    """
    Add the cogg
    :param bot:
    :return:
    """

    bot.add_cog(PriceCheck(bot))
