from http import HTTPStatus

import pytest
from functional.api.types import AsyncRequest
from functional.api.v1.urls import REGISTRATION_URL
from functional.factories.user import FakeUser


@pytest.mark.asyncio
class TestRegistration:
    async def test_user_registration(self, make_post_request: AsyncRequest, fake_user: FakeUser):
        response = await make_post_request(REGISTRATION_URL, json=fake_user.dict())

        assert response.status == HTTPStatus.CREATED
        assert response.body["access_token"]
        assert response.body["refresh_token"]

    async def test_user_registration_with_empty_login_or_password(self, make_post_request: AsyncRequest):
        # TODO: сделать чтобы не сохранялся пользователь с пустым логином
        empty_user = FakeUser(login="", password="")

        response = await make_post_request(REGISTRATION_URL, json=empty_user.dict())

        assert response.status == HTTPStatus.BAD_REQUEST

    async def test_user_registration_without_login_or_password(self, make_post_request: AsyncRequest):
        # TODO: сделать чтобы не сохранялся пользователь с пустым логином
        response = await make_post_request(REGISTRATION_URL, json={})

        assert response.status == HTTPStatus.BAD_REQUEST

    async def test_already_existing_user_registration(self, make_post_request: AsyncRequest, fake_user: FakeUser):
        # TODO: сделать чтобы возвращался код ошибки, если пытаем зарегать существующего пользователя
        response = await make_post_request(REGISTRATION_URL, json=fake_user.dict())

        assert response.status == HTTPStatus.CONFLICT
