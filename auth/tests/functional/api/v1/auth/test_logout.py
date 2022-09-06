from http import HTTPStatus

import pytest
from functional.api.utils import generate_jwt_token_header
from functional.api.v1.urls import LOGIN_URL, LOGOUT_URL
from functional.factories.user import FakeUser


@pytest.mark.asyncio
class TestLogout:
    async def test_user_login_and_than_logout(self, make_post_request, fake_registered_user: FakeUser):
        response = await make_post_request(LOGIN_URL, json=fake_registered_user.dict())
        assert response.status == HTTPStatus.OK
        assert response.body["access_token"]
        assert response.body["refresh_token"]

        auth_header = generate_jwt_token_header(response.body["access_token"])
        response = await make_post_request(LOGOUT_URL, headers=auth_header)
        assert response.status == HTTPStatus.OK
