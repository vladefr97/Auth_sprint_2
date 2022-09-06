from http import HTTPStatus

import pytest
from functional.api.types import AsyncRequest
from functional.api.v1.urls import LOGIN_URL
from functional.factories.user import FakeUser


@pytest.mark.asyncio
class TestLogin:
    async def test_user_login(self, make_post_request, fake_registered_user: FakeUser):
        response = await make_post_request(LOGIN_URL, json=fake_registered_user.dict())

        assert response.status == HTTPStatus.OK
        assert response.body["access_token"]
        assert response.body["refresh_token"]

    async def test_user_login_with_wrong_login(self, make_post_request: AsyncRequest, fake_registered_user: FakeUser):
        user_with_wrong_login = FakeUser(
            login=fake_registered_user.login + "_bad_", password=fake_registered_user.password
        )
        response = await make_post_request(LOGIN_URL, json=user_with_wrong_login.dict())

        assert response.status == HTTPStatus.NOT_FOUND

    async def test_user_login_with_wrong_password(
        self, make_post_request: AsyncRequest, fake_registered_user: FakeUser
    ):
        user_with_wrong_password = FakeUser(
            login=fake_registered_user.login, password=fake_registered_user.password + "_bad_"
        )
        response = await make_post_request(LOGIN_URL, json=user_with_wrong_password.dict())

        assert response.status == HTTPStatus.UNAUTHORIZED
