"""
ESI Client Provider
"""

# Alliance Auth
from esi.openapi_clients import ESIClientProvider

# Terra Nanotech Discordbot Cogs
from tnnt_discordbot_cogs import (
    __esi_compatibility_date__,
    __github_url__,
    __title__,
    __version__,
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
