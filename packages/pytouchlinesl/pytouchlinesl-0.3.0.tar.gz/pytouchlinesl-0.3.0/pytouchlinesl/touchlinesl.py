"""Provides an API client for a specific Roth TouchlineSL account.

This is the top-level construct expected to be used for interacting
with the TouchlineSL API. It provides a way to list the heating
modules associated with a given account, the authentication details
for which are provided by a RothAPI instance.

Typical usage example:

    import os
    from pytouchlinesl import TouchlineSL

    tsl = TouchlineSL(username"foo@bar.com", password="deadbeef")
    modules = await tsl.modules()
"""

import logging

from pytouchlinesl.client import BaseClient, RothAPI
from pytouchlinesl.module import Module

logger = logging.getLogger(__name__)


class TouchlineSL:
    """An API client for a specific Roth TouchlineSL account."""

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        client: BaseClient | None = None,
        cache_validity: int = 30,
    ):
        """Construct the instance with either credentials or an authenticated client.

        Args:
            username:       (Optional) Username for TouchlineSL account. Ignored if client is passed.
            password:       (Optional) Password for TouchlineSL account. Ignored if client is passed.
            client:         (Optional) An instance of a RothAPI class.
            cache_validity: (Optional) The number of seconds for which module data should be cached.
        """
        self._modules: list[Module] = []

        if client:
            if username or password:
                logger.warning(
                    "username and password arguments will be ignored because a client was passed"
                )
            self._client = client
        else:
            if username is None or password is None:
                raise TypeError("username and password must be strings if no client is provided")
            self._client = RothAPI(username=username, password=password)

        self._cache_validity = cache_validity

    async def user_id(self) -> int:
        """Return the unique user ID of the authenticated account."""
        return await self._client.user_id()

    async def modules(self, *, refresh: bool = False) -> list[Module]:
        """Report a list of Roth TouchlineSL modules associated with the account.

        Args:
            refresh: Force the API client to refresh cached module data
        """
        if not self._modules or refresh:
            data = await self._client.modules()
            self._modules = [
                Module(client=self._client, module_data=m, cache_validity=self._cache_validity)
                for m in data
            ]

        return self._modules

    async def module(self, *, module_id: str, refresh: bool = False) -> Module | None:
        """Fetch a specific module, by module ID.

        Args:
            module_id: The unique identifier of the TouchlineSL module to fetch
            refresh:   Force the API client to refresh cached module data
        """
        modules = await self.modules(refresh=refresh)
        return next((m for m in modules if m.id == module_id), None)
