"""
Tests for the price_check cog.
"""

# Standard Library
from unittest import mock

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.cogs.price_check import PriceCheck, setup
from tnnt_discordbot_cogs.tests import BaseTestCase


class TestCogSetup(BaseTestCase):
    """
    Tests for the PriceCheck cog setup function.
    """

    def test_loads_price_check_cog_successfully(self):
        """
        Test that the PriceCheck cog loads successfully.

        :return:
        :rtype:
        """

        mock_bot = mock.Mock()
        with mock.patch(
            "tnnt_discordbot_cogs.cogs.price_check.unload_cog"
        ) as mock_unload_cog:
            setup(mock_bot)

            mock_unload_cog.assert_called_once_with(bot=mock_bot, cog_name="PriceCheck")
            mock_bot.add_cog.assert_called_once()

            self.assertIsInstance(mock_bot.add_cog.call_args[0][0], PriceCheck)

    def test_does_not_fail_when_unloading_nonexistent_cog(self):
        """
        Test that the PriceCheck cog setup handles unloading a non-existent cog gracefully.

        :return:
        :rtype:
        """

        mock_bot = mock.Mock()

        with mock.patch(
            "tnnt_discordbot_cogs.cogs.price_check.unload_cog",
            side_effect=Exception("Cog not found"),
        ) as mock_unload_cog:
            with self.assertRaises(Exception) as context:
                setup(mock_bot)

            self.assertEqual(str(context.exception), "Cog not found")
            mock_unload_cog.assert_called_once_with(bot=mock_bot, cog_name="PriceCheck")
