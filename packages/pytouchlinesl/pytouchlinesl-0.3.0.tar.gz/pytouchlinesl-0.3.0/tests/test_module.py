import asyncio

import pytest

from pytouchlinesl.client.models import GlobalScheduleModel
from pytouchlinesl.zone import Zone


@pytest.mark.asyncio
async def test_zones(test_module):
    zones = await test_module.zones()
    # There should be 10 enabled zones
    assert len(zones) == 10
    # Ensure that each of the zones has been correctly constructed by the
    # modules method.
    for z in zones:
        assert isinstance(z, Zone)
        if z.mode == "constantTemp":
            assert z.schedule is None
        else:
            assert isinstance(z.schedule, GlobalScheduleModel)


@pytest.mark.asyncio
async def test_zones_include_off(test_module):
    zones = await test_module.zones(include_off=True)
    # There should be 40 total zones, 10 enabled, 30 disabled
    assert len(zones) == 40


@pytest.mark.asyncio
async def test_zones_include_off_and_refresh(test_module):
    zones = await test_module.zones(include_off=True, refresh=True)
    # There should be 40 total zones, 10 enabled, 30 disabled
    assert len(zones) == 40


@pytest.mark.asyncio
async def test_zones_cache(test_module):
    await test_module.zones()
    initial_fetch_time = test_module._last_fetched
    await asyncio.sleep(0.5)

    await test_module.zones()
    assert initial_fetch_time == test_module._last_fetched


@pytest.mark.asyncio
async def test_zones_cache_expired(test_module_short_cache):
    await test_module_short_cache.zones()
    initial_fetch_time = test_module_short_cache._last_fetched
    await asyncio.sleep(0.25)

    await test_module_short_cache.zones()
    assert initial_fetch_time != test_module_short_cache._last_fetched


@pytest.mark.asyncio
async def test_zones_force_refresh(test_module):
    await test_module.zones()
    initial_fetch_time = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.zones(refresh=True)
    assert initial_fetch_time != test_module._last_fetched


@pytest.mark.asyncio
@pytest.mark.parametrize("id", [2335, 2354])  # test both enabled and disabled zones
async def test_zone(id, test_module):
    z = await test_module.zone(zone_id=id)
    assert z.id == id


@pytest.mark.asyncio
async def test_zone_non_existent(test_module):
    z = await test_module.zone(zone_id=1234)
    assert z is None


@pytest.mark.asyncio
async def test_zone_refresh(test_module):
    await test_module.zones()
    last_fetched = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.zone(zone_id=2335, refresh=True)
    assert last_fetched != test_module._last_fetched


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["Kitchen", "Zone 2"])  # test both enabled and disabled zones
async def test_zone_by_name(name, test_module):
    z = await test_module.zone_by_name(zone_name=name)
    assert z.name == name


@pytest.mark.asyncio
async def test_zone_by_name_non_existent(test_module):
    z = await test_module.zone_by_name(zone_name="Foobar")
    assert z is None


@pytest.mark.asyncio
async def test_zone_by_name_refresh(test_module):
    await test_module.zones()
    last_fetched = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.zone_by_name(zone_name="Kitchen", refresh=True)
    assert last_fetched != test_module._last_fetched


@pytest.mark.asyncio
async def test_schedules(test_module):
    schedules = await test_module.schedules()
    # There should be 10 enabled schedules
    assert len(schedules) == 5
    # Ensure that each of the schedules has been correctly constructed by the
    # modules method.
    for z in schedules:
        assert isinstance(z, GlobalScheduleModel)


@pytest.mark.asyncio
async def test_schedules_cache(test_module):
    await test_module.schedules()
    initial_fetch_time = test_module._last_fetched
    await asyncio.sleep(0.5)

    await test_module.schedules()
    assert initial_fetch_time == test_module._last_fetched


@pytest.mark.asyncio
async def test_schedules_cache_expired(test_module_short_cache):
    await test_module_short_cache.schedules()
    initial_fetch_time = test_module_short_cache._last_fetched
    await asyncio.sleep(0.5)

    await test_module_short_cache.schedules()
    assert initial_fetch_time != test_module_short_cache._last_fetched


@pytest.mark.asyncio
async def test_schedules_force_refresh(test_module):
    await test_module.schedules()
    initial_fetch_time = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.schedules(refresh=True)
    assert initial_fetch_time != test_module._last_fetched


@pytest.mark.asyncio
@pytest.mark.parametrize("id", [2948, 2967])  # test both enabled and disabled zones
async def test_schedule(id, test_module):
    z = await test_module.schedule(schedule_id=id)
    assert z.id == id


@pytest.mark.asyncio
async def test_schedule_non_existent(test_module):
    z = await test_module.schedule(schedule_id=1234)
    assert z is None


@pytest.mark.asyncio
async def test_schedule_refresh(test_module):
    await test_module.schedules()
    last_fetched = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.schedule(schedule_id=2948, refresh=True)
    assert last_fetched != test_module._last_fetched


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ["Living Spaces", "Bedrooms"])
async def test_schedule_by_name(name, test_module):
    z = await test_module.schedule_by_name(schedule_name=name)
    assert z.name == name


@pytest.mark.asyncio
async def test_schedule_by_name_non_existent(test_module):
    z = await test_module.schedule_by_name(schedule_name="Foobar")
    assert z is None


@pytest.mark.asyncio
async def test_schedule_by_name_refresh(test_module):
    await test_module.schedules()
    last_fetched = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.schedule_by_name(schedule_name="Holiday", refresh=True)
    assert last_fetched != test_module._last_fetched


@pytest.mark.asyncio
@pytest.mark.parametrize("idx", [0, 1])
async def test_schedule_by_idx(idx, test_module):
    z = await test_module.schedule_by_idx(schedule_idx=idx)
    assert z.index == idx


@pytest.mark.asyncio
async def test_schedule_by_idx_non_existent(test_module):
    z = await test_module.schedule_by_idx(schedule_idx=10)
    assert z is None


@pytest.mark.asyncio
async def test_schedule_by_idx_refresh(test_module):
    await test_module.schedules()
    last_fetched = test_module._last_fetched
    await asyncio.sleep(0.5)
    await test_module.schedule_by_idx(schedule_idx="Holiday", refresh=True)
    assert last_fetched != test_module._last_fetched
