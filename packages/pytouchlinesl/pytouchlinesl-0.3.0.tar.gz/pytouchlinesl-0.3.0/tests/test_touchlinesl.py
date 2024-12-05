import pytest

from pytouchlinesl import Module, TouchlineSL
from pytouchlinesl.client import RothAPI

from . import FakeRothAPI


def test_construct_touchlinesl_credentials():
    TouchlineSL(username="foo", password="bar")


def test_construct_touchlinesl_client():
    fake_client = FakeRothAPI()
    TouchlineSL(client=fake_client)

    real_client = RothAPI(username="foo", password="bar")
    TouchlineSL(client=real_client)


def test_construct_touchlinesl_client_and_creds(caplog):
    TouchlineSL(username="foo", password="bar", client=FakeRothAPI())
    assert (
        "username and password arguments will be ignored because a client was passed"
        in caplog.text
    )


@pytest.mark.parametrize("username,password", [(None, None), ("Foo", None), (None, "Foo")])
def test_construct_touchlinesl_bad_args(username, password):
    try:
        TouchlineSL(username=username, password=password)
    except Exception as e:
        assert isinstance(e, TypeError)
        assert str(e) == "username and password must be strings if no client is provided"


@pytest.mark.asyncio
async def test_modules(test_touchlinesl: TouchlineSL):
    modules = await test_touchlinesl.modules()
    for m in modules:
        assert isinstance(m, Module)
        assert m._cache_validity == 30000


@pytest.mark.asyncio
async def test_modules_short_cache(test_touchlinesl_short_cache: TouchlineSL):
    modules = await test_touchlinesl_short_cache.modules()
    for m in modules:
        assert isinstance(m, Module)
        assert m._cache_validity == 100


@pytest.mark.asyncio
async def test_module_bad_module_id(test_touchlinesl: TouchlineSL):
    module = await test_touchlinesl.module(module_id="123")
    assert module is None


@pytest.mark.asyncio
async def test_module_good_module_id(test_touchlinesl: TouchlineSL):
    module = await test_touchlinesl.module(module_id="1234a5678a9123a456a7891234a56789")
    assert isinstance(module, Module)
