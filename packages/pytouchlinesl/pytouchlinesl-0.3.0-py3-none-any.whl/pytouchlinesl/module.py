"""Provides a representation of a single Roth TouchlineSL module.

In reality, this usually represents the underfloor heating for
a specific building. It masks the upstream Roth API, which provides
relatively few methods for fetching details about particular zones
and schedules by providing methods to query them directly.

Because of the upstream API design, there is an inbuilt caching
mechanism that's used to prevent making too many calls to the
modules endpoint. The cache can be invalidated to ensure that
new data is fetched using the `invalidate_cache` method.

Typical usage:

    import os
    from pytouchlinesl import TouchlineSL

    tsl = TouchlineSL(username"foo@bar.com", password="deadbeef")

    modules = await tsl.modules()
    if modules:
        module = modules[0]
        zone = await module.zone_by_name("Kitchen")
"""

import time

from pytouchlinesl.client import BaseClient
from pytouchlinesl.client.models import GlobalScheduleModel, ModuleModel
from pytouchlinesl.client.models.models import AccountModuleModel
from pytouchlinesl.zone import Zone


class Module:
    """A representation of a single Roth TouchlineSL module."""

    def __init__(
        self,
        *,
        client: BaseClient,
        module_data: AccountModuleModel,
        cache_validity: int = 30,
    ):
        """Construct an instance of a module.

        Args:
            client:         The underlying API client to use for fetching data.
            module_data:    A raw representation of the Module returned from a client instance.
            cache_validity: (Optional) The number of seconds for which module data should be cached.

        """
        self._client: BaseClient = client

        # Information about the module itself
        self.id = module_data.udid
        self.name = module_data.name
        self.email = module_data.email
        self.type = module_data.type
        self.version = module_data.version

        # Raw data about the zones, schedules, tiles in the module
        self._raw_data: ModuleModel
        # Unix timestamp representing the last time the _raw_data was fetched
        self._last_fetched = 0
        self._cache_validity = cache_validity * 1000

        self._zones: list[Zone] = []
        self._schedules: list[GlobalScheduleModel] = []

    async def _data(self, *, refresh: bool = False) -> ModuleModel:
        """Get the raw representation of the module from the upstream API.

        If the data has never been fetched from upstream, or the data is older
        than the cache validity period, then the data is refreshed using the
        upstream API.

        Args:
            refresh: (Optional): Force the data to be refreshed using the API.
        """
        if refresh or (round(time.time() * 1000) - self._last_fetched) > self._cache_validity:
            self._raw_data = await self._client.module(self.id)
            self._last_fetched = round(time.time() * 1000)

        return self._raw_data

    def invalidate_cache(self):
        """Reset the cache, ensuring new data is fetched the next time its accessed."""
        self._last_fetched = 0
        self._zones = []
        self._schedules = []

    async def zones(self, *, include_off: bool = False, refresh: bool = False) -> list[Zone]:
        """Return a list of zones, optionally including those which are disabled.

        Args:
            include_off: (Optional) Include zones which are switched off in the results.
            refresh:     (Optional) Force the data to be refreshed using the API.
        """
        data = await self._data(refresh=refresh)

        self._zones = []
        for z in data.zones.elements:
            schedule = await self.schedule_by_idx(z.mode.schedule_index)
            zone = Zone(module=self, client=self._client, zone_data=z, schedule=schedule)
            self._zones.append(zone)

        if include_off:
            return self._zones

        return [z for z in self._zones if z.enabled]

    async def zone(self, zone_id: int, *, refresh: bool = False) -> Zone | None:
        """Return a specific zone, by ID.

        Args:
            zone_id: The ID of the desired zone.
            refresh: (Optional) Force the data to be refreshed using the API.
        """
        zones = await self.zones(include_off=True, refresh=refresh)
        return next((z for z in zones if z.id == zone_id), None)

    async def zone_by_name(self, zone_name: str, *, refresh: bool = False) -> Zone | None:
        """Return a specific zone, by name.

        Args:
            zone_name:   The name of the desired zone.
            include_off: (Optional) Include zones which are switched off in the results.
            refresh:     (Optional) Force the data to be refreshed using the API.
        """
        zones = await self.zones(include_off=True, refresh=refresh)
        return next((z for z in zones if z.name == zone_name), None)

    async def schedules(self, *, refresh: bool = False) -> list[GlobalScheduleModel]:
        """Return a list of the module's global schedules.

        Args:
            refresh: (Optional) Force the data to be refreshed using the API.
        """
        data = await self._data(refresh=refresh)
        self._schedules = data.zones.global_schedules.elements

        return self._schedules

    async def schedule(
        self, schedule_id: int, *, refresh: bool = False
    ) -> GlobalScheduleModel | None:
        """Return a specific global schedule, by ID.

        Args:
            schedule_id: The ID of the desired schedule.
            refresh:     (Optional) Force the data to be refreshed using the API.
        """
        schedules = await self.schedules(refresh=refresh)
        return next((s for s in schedules if s.id == schedule_id), None)

    async def schedule_by_idx(
        self, schedule_idx: int, *, refresh: bool = False
    ) -> GlobalScheduleModel | None:
        """Return a specific global schedule, by index.

        Args:
            schedule_idx: The index of the desired schedule.
            refresh:      (Optional) Force the data to be refreshed using the API.
        """
        schedules = await self.schedules(refresh=refresh)
        return next((s for s in schedules if s.index == schedule_idx), None)

    async def schedule_by_name(
        self, schedule_name: str, *, refresh: bool = False
    ) -> GlobalScheduleModel | None:
        """Return a specific global schedule, by name.

        Args:
            schedule_name: The name of the desired schedule.
            refresh:       (Optional) Force the data to be refreshed using the API.
        """
        schedules = await self.schedules(refresh=refresh)
        return next((s for s in schedules if s.name == schedule_name), None)
