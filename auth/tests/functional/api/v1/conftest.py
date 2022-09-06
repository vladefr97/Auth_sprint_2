from typing import Dict, Optional

import asyncio
import os
from dataclasses import dataclass

import aiohttp
import pytest
from dotenv import load_dotenv
from functional.api.v1.urls import REGISTRATION_URL
from functional.factories.user import FakeUser, FakeUserFactory
from multidict import CIMultiDictProxy

load_dotenv()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None, headers: Optional[Dict[str, str]] = None) -> HTTPResponse:
        params = params or {}

        async with session.get(url, params=params, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
def make_post_request(session):
    async def inner(url: str, json: Optional[dict] = None, headers: Optional[Dict[str, str]] = None) -> HTTPResponse:
        json = json or {}

        async with session.post(url, json=json, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
def make_put_request(session):
    async def inner(url: str, json: Optional[dict] = None, headers: Optional[Dict[str, str]] = None) -> HTTPResponse:
        json = json or {}

        async with session.put(url, json=json, headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
async def fake_user() -> FakeUser:
    return FakeUserFactory.build()


@pytest.fixture(scope="session")
async def fake_registered_user(make_post_request) -> FakeUser:
    fake_user = FakeUserFactory.build()
    await make_post_request(REGISTRATION_URL, json=fake_user.dict())
    return fake_user


@pytest.fixture(scope="session")
async def super_user() -> FakeUser:
    return FakeUser(login=os.environ.get("SUPERUSER_LOGIN", ""), password=os.environ.get("SUPERUSER_PASSWORD", ""))
