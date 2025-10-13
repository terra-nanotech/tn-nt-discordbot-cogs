"""
Tests for helper functions in tnnt_discordbot_cogs.
"""

# Standard Library
from unittest import mock

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.helper import get_discord_id, unload_cog
from tnnt_discordbot_cogs.tests import BaseTestCase


class TestHelperGetDiscordId(BaseTestCase):
    """
    Tests for the get_discord_id function.
    """

    def test_returns_discord_id_when_character_has_valid_user(self):
        """
        Test that get_discord_id returns the correct Discord ID when the character has a valid user.

        :return:
        :rtype:
        """

        mock_character = mock.Mock()
        mock_character.character_ownership.user.discord.uid = 123456789

        result = get_discord_id(mock_character)

        self.assertEqual(result, 123456789)

    def test_returns_none_when_character_has_no_discord_user(self):
        """
        Test that get_discord_id returns None when the character's user has no Discord ID.

        :return:
        :rtype:
        """

        mock_character = mock.Mock()
        mock_character.character_ownership.user = None

        result = get_discord_id(mock_character)

        self.assertIsNone(result)

    def test_returns_none_when_character_has_no_character_ownership(self):
        """
        Test that get_discord_id returns None when the character has no character ownership.

        :return:
        :rtype:
        """

        mock_character = mock.Mock()
        mock_character.character_ownership = None

        result = get_discord_id(mock_character)

        self.assertIsNone(result)

    def test_returns_none_when_character_is_none(self):
        """
        Test that get_discord_id returns None when the character is None.

        :return:
        :rtype:
        """

        result = get_discord_id(None)

        self.assertIsNone(result)


class TestHelperUnloadCog(BaseTestCase):
    """
    Tests for the unload_cog function.
    """

    def test_unloads_cog_successfully(self):
        """
        Test that unload_cog successfully unloads a cog.

        :return:
        :rtype:
        """

        mock_bot = mock.Mock()

        unload_cog(mock_bot, "example_cog")
        mock_bot.remove_cog.assert_called_once_with(name="example_cog")

    def test_prints_error_message_when_unload_fails(self):
        """
        Test that unload_cog prints an error message when unloading fails.

        :return:
        :rtype:
        """

        mock_bot = mock.Mock()
        mock_bot.remove_cog.side_effect = Exception("Unload error")

        with mock.patch("builtins.print") as mock_print:
            unload_cog(mock_bot, "example_cog")
            mock_print.assert_called_once_with(
                "Failed to unload example_cog: Unload error"
            )
