"""
Providers
"""

# Standard Library
import logging
import typing
from typing import Any

# Third Party
from aiopenapi3 import ContentTypeError, RequestError
from httpx import Response

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from esi.exceptions import HTTPClientError, HTTPNotModified
from esi.models import Token
from esi.openapi_clients import ESIClientProvider, EsiOperation

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs import (
    __esi_compatibility_date__,
    __github_url__,
    __title__,
    __version__,
)

if typing.TYPE_CHECKING:
    # Alliance Auth
    from esi.stubs import (
        CharactersCharacterIdLocationGet,
        CharactersCharacterIdOnlineGet,
        CharactersCharacterIdShipGet,
    )

# ESI client
esi = ESIClientProvider(
    # Use the latest compatibility date, see https://esi.evetech.net/meta/compatibility-dates
    compatibility_date=__esi_compatibility_date__,
    # User agent for the ESI client
    ua_appname=__title__,
    ua_version=__version__,
    ua_url=__github_url__,
    operations=[
        # Location
        "GetCharactersCharacterIdOnline",
        "GetCharactersCharacterIdLocation",
        "GetCharactersCharacterIdShip",
    ],
)


class ESIHandler:
    """
    Handler for ESI operations, providing a method to retrieve results while handling exceptions.
    """

    @classmethod
    def result(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        cls,
        operation: EsiOperation,
        use_etag: bool = True,
        return_response: bool = False,
        force_refresh: bool = False,
        use_cache: bool = True,
        **extra,
    ) -> tuple[Any, Response] | Any:
        """
        Retrieve the result of an ESI operation, handling HTTPNotModified exceptions.

        :param operation: The ESI operation to execute.
        :type operation: EsiOperation
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :param return_response: Whether to return the full response object.
        :type return_response: bool
        :param force_refresh: Whether to force a refresh of the data.
        :type force_refresh: bool
        :param use_cache: Whether to use cached data.
        :type use_cache: bool
        :param extra: Additional parameters to pass to the operation.
        :type extra: dict
        :return: The result of the ESI operation, optionally with the response object.
        :rtype: tuple[Any, Response] | Any
        """

        logger.debug(f"Handling ESI operation: {operation.operation.operationId}")

        try:
            esi_result = operation.result(
                use_etag=use_etag,
                return_response=return_response,
                force_refresh=force_refresh,
                use_cache=use_cache,
                **extra,
            )
        except HTTPNotModified:
            logger.debug(
                f"ESI returned 304 Not Modified for operation: {operation.operation.operationId} - Skipping update."
            )

            esi_result = None
        except ContentTypeError:
            logger.warning(
                msg="ESI returned gibberish (ContentTypeError) - Skipping update."
            )

            esi_result = None
        except (HTTPClientError, RequestError) as exc:
            logger.error(msg=f"Error while fetching data from ESI: {str(exc)}")

            esi_result = None

        return esi_result

    @classmethod
    def get_characters_character_id_online(
        cls, character_id: int, token: Token, use_etag: bool = True
    ) -> "CharactersCharacterIdOnlineGet | None":
        """
        Get characters online status from ESI.

        :param character_id: The charater ID to check
        :type character_id: int
        :param token: The characters token
        :type token: Token
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: The characters online status or None if an error occurred.
        :rtype: CharactersCharacterIdOnlineGet | None
        """

        logger.debug(
            f"Fetching online status for character ID {character_id} from ESI…"
        )

        return cls.result(
            operation=esi.client.Location.GetCharactersCharacterIdOnline(
                character_id=character_id, token=token
            ),
            use_etag=use_etag,
        )

    @classmethod
    def get_characters_character_id_location(
        cls, character_id: int, token: Token, use_etag: bool = True
    ) -> "CharactersCharacterIdLocationGet | None":
        """
        Get characters location status from ESI.

        :param character_id: The charater ID to check
        :type character_id: int
        :param token: The characters token
        :type token: Token
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :return: The characters location status or None if an error occurred.
        :rtype: CharactersCharacterIdLocationGet | None
        """

        logger.debug(f"Fetching location for character ID {character_id} from ESI…")

        return cls.result(
            operation=esi.client.Location.GetCharactersCharacterIdLocation(
                character_id=character_id, token=token
            ),
            use_etag=use_etag,
        )

    @classmethod
    def get_characters_character_id_ship(
        cls, character_id: int, token: Token, use_etag: bool = True
    ) -> "CharactersCharacterIdShipGet | None":

        logger.debug(f"Fetching ship for character ID {character_id} from ESI…")

        return cls.result(
            operation=esi.client.Location.GetCharactersCharacterIdShip(
                character_id=character_id, token=token
            ),
            use_etag=use_etag,
        )


class AppLogger(logging.LoggerAdapter):
    """
    Custom logger adapter that adds a prefix to log messages.

    Taken from the `allianceauth-app-utils` package.
    Credits to: Erik Kalkoken
    """

    def __init__(self, my_logger, prefix):
        """
        Initializes the AppLogger with a logger and a prefix.

        :param my_logger: Logger instance
        :type my_logger: logging.Logger
        :param prefix: Prefix string to add to log messages
        :type prefix: str
        """

        super().__init__(my_logger, {})

        self.prefix = prefix

    def process(self, msg, kwargs):
        """
        Prepares the log message by adding the prefix.

        :param msg: Log message
        :type msg: str
        :param kwargs: Additional keyword arguments
        :type kwargs: dict
        :return: Prefixed log message and kwargs
        :rtype: tuple
        """

        return f"[{self.prefix}] {msg}", kwargs


logger = AppLogger(my_logger=get_extension_logger(name=__name__), prefix=__title__)
