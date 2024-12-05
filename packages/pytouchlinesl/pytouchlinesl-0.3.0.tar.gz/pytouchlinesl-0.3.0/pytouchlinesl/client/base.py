"""Provides an abstract API client implementation for clients working with the Roth API."""

from abc import ABC, abstractmethod

from pytouchlinesl.client.models.models import AccountModuleModel

from .models import ModuleModel


class BaseClient(ABC):
    """Base API client implementation for Roth API clients."""

    @abstractmethod
    async def user_id(self) -> int:
        """Return the unique user id for the authenticated account."""
        pass

    @abstractmethod
    async def authenticated(self) -> bool:
        """Report whether or not the client is authenticated with the API."""
        pass

    @abstractmethod
    async def modules(self) -> list[AccountModuleModel]:
        """Return a list of TouchlineSL modules associated with the authenticated account."""
        pass

    @abstractmethod
    async def module(self, module_id: str) -> ModuleModel:
        """Return a specific module, by ID, that's associated with the authenticated account."""
        pass

    @abstractmethod
    async def set_zone_temperature(
        self, module_id: str, mode_id: int, zone_id: int, temperature: float
    ):
        """Set a constant target temperature for a specific zone, in a specific module."""
        pass

    @abstractmethod
    async def set_zone_schedule(self, module_id: str, zone_id: int, schedule_id: int):
        """Assign a specific zone to a specific global schedule in the module's configuration."""
        pass
