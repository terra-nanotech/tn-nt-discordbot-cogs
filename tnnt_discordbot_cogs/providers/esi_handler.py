"""
ESI Handler Provider
"""

# Standard Library
import typing
from typing import Any

# Third Party
from aiopenapi3 import ContentTypeError, RequestError
from httpx import Response

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from esi.exceptions import HTTPClientError, HTTPNotModified
from esi.models import Token
from esi.openapi_clients import EsiOperation

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs.providers.applogger import AppLogger
from tnnt_discordbot_cogs.providers.esi_client import esi

logger = AppLogger(my_logger=get_extension_logger(__name__))


if typing.TYPE_CHECKING:
    # Alliance Auth
    from esi.stubs import (
        CharactersCharacterIdLocationGet,
        CharactersCharacterIdOnlineGet,
        CharactersCharacterIdShipGet,
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
    ) -> Any | tuple[Any, Response] | None:
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
        :return: The result of the ESI operation.
        :rtype: Any | tuple[Any, Response] | None
        """

        logger.debug(f"Handling ESI operation: {operation.operation.operationId}")
        logger.debug(
            f"Operation parameters: use_etag={use_etag}, return_response={return_response}, force_refresh={force_refresh}, use_cache={use_cache}, extra={extra}"
        )

        response: Response | None = None

        try:
            # Call operation.result differently depending on whether the caller
            # requested the raw Response object. Some implementations return a
            # single result when return_response is False and a (result, response)
            # tuple when True, so only unpack when return_response is True.
            if return_response:
                esi_result, response = operation.result(
                    use_etag=use_etag,
                    return_response=return_response,
                    force_refresh=force_refresh,
                    use_cache=use_cache,
                    **extra,
                )

                logger.debug(
                    f"ESI Response for operation: {operation.operation.operationId}: {response}"
                )
            else:
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

        # If caller requested the raw response, return a tuple (result, response)
        if return_response:
            return esi_result, response

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
