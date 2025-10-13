"""
Tests for the Setting model.
"""

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.models.setting import Setting
from tnnt_discordbot_cogs.tests import BaseTestCase


class TestSettingModel(BaseTestCase):
    """
    Tests for the Setting model.
    """

    def test_retrieves_existing_setting_value(self):
        """
        Test that an existing setting value can be retrieved.

        :return:
        :rtype:
        """

        setting = Setting.get_solo()
        setting.applicant_role_name = "Applicant"
        setting.save()

        result = Setting.get_setting("applicant_role_name")

        self.assertEqual(result, "Applicant")

    def test_raises_key_error_for_nonexistent_setting(self):
        """
        Test that a KeyError is raised when trying to retrieve a nonexistent setting.

        :return:
        :rtype:
        """

        with self.assertRaises(KeyError) as context:
            Setting.get_setting("nonexistent_key")

        self.assertEqual(
            context.exception.args[0], "Setting key 'nonexistent_key' does not exist."
        )

    def test_returns_correct_string_representation(self):
        setting = Setting.get_solo()
        result = str(setting)
        self.assertEqual(result, "Settings")
