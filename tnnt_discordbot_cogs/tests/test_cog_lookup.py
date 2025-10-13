"""
Tests for the lookup cog.
"""

# Standard Library
from unittest import mock

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.cogs.lookup import Lookup, setup
from tnnt_discordbot_cogs.tests import BaseTestCase


class TestCogSetup(BaseTestCase):
    """
    Tests for the Lookup cog setup function.
    """

    def test_loads_lookup_cog_successfully(self):
        mock_bot = mock.Mock()
        with mock.patch(
            "tnnt_discordbot_cogs.cogs.lookup.unload_cog"
        ) as mock_unload_cog:
            setup(mock_bot)

            self.assertEqual(mock_unload_cog.call_count, 2)
            mock_unload_cog.assert_any_call(bot=mock_bot, cog_name="Lookup")
            mock_unload_cog.assert_any_call(bot=mock_bot, cog_name="Members")
            mock_bot.add_cog.assert_called_once()
            self.assertIsInstance(mock_bot.add_cog.call_args[0][0], Lookup)

    def test_does_not_fail_when_unloading_nonexistent_cog(self):
        """
        Test that the Lookup cog setup handles unloading a non-existent cog gracefully.

        :return:
        :rtype:
        """

        mock_bot = mock.Mock()

        with mock.patch(
            "tnnt_discordbot_cogs.cogs.lookup.unload_cog",
            side_effect=Exception("Cog not found"),
        ) as mock_unload_cog:
            with self.assertRaises(Exception) as context:
                setup(mock_bot)

            self.assertEqual(str(context.exception), "Cog not found")
            mock_unload_cog.assert_called_once_with(bot=mock_bot, cog_name="Lookup")
