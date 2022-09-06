from http import HTTPStatus

import pytest
from functional.api.utils import generate_jwt_token_header
from functional.api.v1.urls import LOGIN_URL, TOKEN_REFRESH_URL
from functional.factories.user import FakeUser


@pytest.mark.asyncio
class TestRefreshToken:
    async def test_user_login_and_than_refresh_token(self, make_post_request, fake_registered_user: FakeUser):
        response = await make_post_request(LOGIN_URL, json=fake_registered_user.dict())

        assert response.status == HTTPStatus.OK
        assert response.body["access_token"]
        assert response.body["refresh_token"]

        initial_access_token = response.body["access_token"]
        initial_refresh_token = response.body["refresh_token"]
        auth_header = generate_jwt_token_header(initial_refresh_token)

        response = await make_post_request(TOKEN_REFRESH_URL, headers=auth_header)

        assert response.status == HTTPStatus.OK
        assert response.body["access_token"] and response.body["access_token"] != initial_access_token
        assert response.body["refresh_token"] and response.body["refresh_token"] != initial_refresh_token

    async def test_refresh_with_access_token(self, make_post_request, fake_registered_user: FakeUser):
        response = await make_post_request(LOGIN_URL, json=fake_registered_user.dict())

        assert response.status == HTTPStatus.OK
        assert response.body["access_token"]
        assert response.body["refresh_token"]

        initial_access_token = response.body["access_token"]
        auth_header = generate_jwt_token_header(initial_access_token)

        response = await make_post_request(TOKEN_REFRESH_URL, headers=auth_header)

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
