"""
Tests for auth_hooks.py
"""

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.auth_hooks import register_cogs
from tnnt_discordbot_cogs.tests import BaseTestCase


class TestAuthHooks(BaseTestCase):
    """
    Tests for auth_hooks.py
    """

    def test_returns_all_registered_cogs(self):
        """
        Test that all registered cogs are returned.

        :return:
        :rtype:
        """

        result = register_cogs()

        self.assertEqual(
            result,
            [
                "tnnt_discordbot_cogs.cogs.about",
                "tnnt_discordbot_cogs.cogs.admin",
                "tnnt_discordbot_cogs.cogs.auth",
                "tnnt_discordbot_cogs.cogs.locate",
                "tnnt_discordbot_cogs.cogs.lookup",
                "tnnt_discordbot_cogs.cogs.models",
                "tnnt_discordbot_cogs.cogs.price_check",
                "tnnt_discordbot_cogs.cogs.recruit_me",
                "tnnt_discordbot_cogs.cogs.welcome",
            ],
        )
