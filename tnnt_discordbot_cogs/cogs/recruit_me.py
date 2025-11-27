"""
RecruitMe Cog
"""

# Standard Library
import logging
from enum import Enum

# Third Party
from discord import ButtonStyle, ChannelType, Embed, Interaction, Member, ui
from discord.ext import commands

# Django
from django.utils import timezone

# Alliance Auth Discord Bot
from aadiscordbot import app_settings
from aadiscordbot.utils import auth

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.helper import reverse_absolute, unload_cog
from tnnt_discordbot_cogs.models.setting import Setting

logger = logging.getLogger(__name__)

# Discord Bot Settings
# Audit System
AUDIT_SYSTEM_NAME = "Character Audit"
AUDIT_SYSTEM_URL = reverse_absolute(viewname="corptools:react")
AUDIT_SYSTEM_URL_MD = f"[{AUDIT_SYSTEM_NAME}]({AUDIT_SYSTEM_URL})"

# Groups Page URL
GROUPS_PAGE_URL = reverse_absolute(viewname="groupmanagement:groups")

# Roles
APPLICANT_ROLE_NAME = Setting.get_setting(Setting.Field.APPLICANT_ROLE_NAME.value)
APPLICANT_ROLE_ID = Setting.get_setting(Setting.Field.APPLICANT_ROLE_ID.value)
RECRUITER_ROLE_ID = Setting.get_setting(Setting.Field.RECRUITER_ROLE_ID.value)
LEADERSHIP_ROLE_ID = Setting.get_setting(Setting.Field.LEADERSHIP_ROLE_ID.value)

# Channels
RECRUITING_CHANNEL = Setting.get_setting(Setting.Field.RECRUITING_CHANNEL.value).channel


class BotResponse(str, Enum):
    """
    Bot responses for the RecruitMe cog
    """

    # Not in the application group
    NOT_IN_APPLICATION_GROUP = (
        f"**You are not in the `{APPLICANT_ROLE_NAME}` group.**\n\n"
        f"Please open the [groups page]({GROUPS_PAGE_URL}) and "
        f"join the `{APPLICANT_ROLE_NAME}` group first …"
    )

    # Member not in the application group
    MEMBER_NOT_IN_APPLICATION_GROUP = (
        "**{MEMBER} is not in the "
        f"`{APPLICANT_ROLE_NAME}` group.**\n\n"
        "Please let them know to open the "
        f"[groups page]({GROUPS_PAGE_URL}) and join the "
        f"`{APPLICANT_ROLE_NAME}` group first …"
    )

    # Not a recruiter
    NOT_A_RECRUITER = (
        "You are not a recruiter for Terra Nanotech and "
        "cannot use this command on this user …"
    )

    # Private thread guide title and body
    PRIVATE_THREAD_GUIDE_TITLE = "Private Thread Guide"
    PRIVATE_THREAD_GUIDE_BODY = (
        "To add a person to this thread simply `@ping` them. "
        "This works with `@groups` as well to bulk add people to the channel. "
        "Use wisely, abuse will not be tolerated."
    )

    # Recruitment thread title and body
    RECRUITMENT_THREAD_TITLE = "{MAIN_CHARACTER} | Recruitment | {DATE}"
    RECRUITMENT_THREAD_BODY = (
        "Hello <@{MEMBER_ID}>, and welcome! :wave:\n\n"
        "We're excited that you're interested in joining Terra Nanotech!\n\n"
        f"Before we get started, please ensure **all** your characters are added to {AUDIT_SYSTEM_URL_MD}.\n"
        "This includes your main character as well as all other characters you have.\n\n"
        'Once that\'s done, please click the "**Continue**" button below to notify a recruiter.\n'
        "If you are not certain yet and just want to ask some questions first to help "
        'you to decide, click the "**Omit This Step**" button.'
    )

    # Recruitment thread created message
    RECRUITMENT_THREAD_CREATED = "Recruitment thread created!"


class RecruitmentThreadIntroduction(ui.View):
    """
    View for the recruitment thread introduction
    """

    embed = Embed(
        title=BotResponse.PRIVATE_THREAD_GUIDE_TITLE.value,
        description=BotResponse.PRIVATE_THREAD_GUIDE_BODY.value,
    )

    @ui.button(label="Continue", row=0, style=ButtonStyle.success)
    async def continue_button_callback(self, button, interaction):
        self.disable_all_items()

        await interaction.channel.send(
            content=(
                "Thank you for reaching out!\n\n"
                f"A member of the <@&{RECRUITER_ROLE_ID}> will be with you shortly to "
                "guide you through the next steps of the recruitment process, which "
                "may include an interview for further assessments.\n"
                "In the meantime, while we conduct the usual background checks, "
                "feel free to ask any questions you may have about Terra Nanotech, "
                "and of course, introduce yourself!.\n\n"
                "Thank you for your patience!\n\n"
                f"(Adding <@&{LEADERSHIP_ROLE_ID}> to the thread for visibility.)"
            ),
            embed=self.embed,
        )
        await interaction.response.edit_message(view=self)

    @ui.button(label="Omit This Step", row=0, style=ButtonStyle.secondary)
    async def omit_button_callback(self, button, interaction):
        self.disable_all_items()

        await interaction.channel.send(
            content=(
                "Thank you for reaching out!\n\n"
                f"A member of the <@&{RECRUITER_ROLE_ID}> will be with you shortly "
                "to answer any questions you may have.\n\n"
                "Thank you for your patience!\n\n"
                f"(Adding <@&{LEADERSHIP_ROLE_ID}> to the thread for visibility.)"
            ),
            embed=self.embed,
        )
        await interaction.response.edit_message(view=self)


class RecruitMe(commands.Cog):
    """
    Thread Tools for recruiting!
    """

    def __init__(self, bot):
        """
        Initialize the RecruitMe cog

        :param bot: The bot instance
        :type bot: discord.ext.commands.Bot
        """

        logger.info(msg="RecruitMe cog initialized")

        self.bot = bot

    async def open_ticket(self, ctx: Interaction, member: Member):
        """
        Open a recruitment ticket

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :param member: The member requesting a recruiter
        :type member: discord.Member
        :return: None
        :rtype: None
        """

        auth_user = auth.get_auth_user(user=member, guild=ctx.guild)
        main_character = auth_user.profile.main_character

        ch = ctx.guild.get_channel(RECRUITING_CHANNEL)
        th = await ch.create_thread(
            name=BotResponse.RECRUITMENT_THREAD_TITLE.value.format(
                MAIN_CHARACTER=main_character,
                DATE=timezone.now().strftime("%Y-%m-%d %H:%M"),
            ),
            auto_archive_duration=10080,
            type=ChannelType.private_thread,
            reason=None,
        )
        msg = BotResponse.RECRUITMENT_THREAD_BODY.value.format(
            LEADERSHIP_ROLE_ID=LEADERSHIP_ROLE_ID,
            RECRUITER_ROLE_ID=RECRUITER_ROLE_ID,
            MEMBER_ID=member.id,
        )

        await th.send(content=msg, view=RecruitmentThreadIntroduction())
        await ctx.response.send_message(
            content=BotResponse.RECRUITMENT_THREAD_CREATED.value,
            view=None,
            ephemeral=True,
        )

    @commands.slash_command(
        name="recruit_me",
        description="Get hold of a recruiter",
        guild_ids=app_settings.get_all_servers(),
    )
    async def slash_recruit_me(self, ctx):
        """
        Get hold of a recruiter

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :return: None
        :rtype: None
        """

        if APPLICANT_ROLE_ID not in [role.id for role in ctx.user.roles]:
            return await ctx.respond(
                BotResponse.NOT_IN_APPLICATION_GROUP.value, ephemeral=True
            )

        await self.open_ticket(ctx=ctx, member=ctx.user)

        return None

    @commands.message_command(
        name="Create Recruitment Thread", guild_ids=app_settings.get_all_servers()
    )
    async def reverse_recruit_msg_context(self, ctx, message):
        """
        Help a new guy get a recruiter

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :param message: The message that triggered the command
        :type message: discord.Message
        :return: None
        :rtype: None
        """

        # Check if the user is a recruiter and if the user is different from the target user
        if RECRUITER_ROLE_ID not in [role.id for role in ctx.user.roles] and int(
            ctx.user.id
        ) != int(message.author.id):
            return await ctx.respond(BotResponse.NOT_A_RECRUITER.value, ephemeral=True)

        # Check if the target user is in the Applicants group
        if APPLICANT_ROLE_ID not in [role.id for role in message.author.roles]:
            return await ctx.respond(
                BotResponse.MEMBER_NOT_IN_APPLICATION_GROUP.value.format(
                    MEMBER=message.author.mention,
                ),
                ephemeral=True,
            )

        await self.open_ticket(ctx=ctx, member=message.author)

        return None

    @commands.user_command(
        name="Recruit Member", guild_ids=app_settings.get_all_servers()
    )
    async def reverse_recruit_user_context(self, ctx, user):
        """
        Help a new guy get a recruiter

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :param user: The user that triggered the command
        :type user: discord.User
        :return: None
        :rtype: None
        """

        # Check if the user is a recruiter and if the user is different from the target user
        if RECRUITER_ROLE_ID not in [role.id for role in ctx.user.roles] and int(
            ctx.user.id
        ) != int(user.id):
            return await ctx.respond(BotResponse.NOT_A_RECRUITER.value, ephemeral=True)

        # Check if the target user is in the Applicants group
        if APPLICANT_ROLE_ID not in [role.id for role in user.roles]:
            return await ctx.respond(
                BotResponse.MEMBER_NOT_IN_APPLICATION_GROUP.value.format(
                    MEMBER=user.mention
                ),
                ephemeral=True,
            )

        await self.open_ticket(ctx=ctx, member=user)

        return None


def setup(bot):
    """
    Set up the RecruitMe cog

    :param bot:
    :type bot:
    :return:
    :rtype:
    """
    # Unload the RecruitMe cog from `aadiscordbot`, so we can load our own.
    unload_cog(bot=bot, cog_name="RecruitMe")

    # Add the RecruitMe cog to the bot
    bot.add_cog(RecruitMe(bot))
