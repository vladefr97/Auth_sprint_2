from http import HTTPStatus

import pytest
from functional.api.utils import generate_jwt_token_header
from functional.api.v1.urls import LOGIN_CHANGE_URL, LOGIN_URL, PASSWORD_CHANGE_URL
from functional.factories.user import FakeUser


@pytest.mark.asyncio
class TestChangeCredentials:
    async def test_change_password(self, make_post_request, make_put_request, fake_registered_user: FakeUser):
        response = await make_post_request(LOGIN_URL, json=fake_registered_user.dict())

        assert response.status == HTTPStatus.OK
        assert response.body["access_token"]
        assert response.body["refresh_token"]

        auth_header = generate_jwt_token_header(response.body["access_token"])
        fake_registered_user.password = fake_registered_user.password + "_new"

        response = await make_put_request(
            PASSWORD_CHANGE_URL, headers=auth_header, json={"new_password": fake_registered_user.password}
        )

        assert response.status == HTTPStatus.OK

    async def test_change_login(self, make_post_request, make_put_request, fake_registered_user: FakeUser):
        response = await make_post_request(LOGIN_URL, json=fake_registered_user.dict())

        assert response.status == HTTPStatus.OK
        assert response.body["access_token"]
        assert response.body["refresh_token"]

        auth_header = generate_jwt_token_header(response.body["access_token"])
        fake_registered_user.login = fake_registered_user.login + "_new"

        response = await make_put_request(
            LOGIN_CHANGE_URL, headers=auth_header, json={"new_login": fake_registered_user.login}
        )

        assert response.status == HTTPStatus.OK
