from http import HTTPStatus

import pytest
from functional.api.types import AsyncRequest
from functional.api.utils import generate_jwt_token_header
from functional.api.v1.urls import LOGIN_URL, ROLES_URL
from functional.factories.user import FakeUser

TEST_ROLE = "test_role"


@pytest.mark.asyncio
class TestRoles:
    async def test_roles_get(self, make_post_request: AsyncRequest, make_get_request, super_user: FakeUser) -> None:
        response = await make_post_request(LOGIN_URL, json=super_user.dict())
        auth_header = generate_jwt_token_header(response.body["access_token"])

        response = await make_get_request(ROLES_URL, headers=auth_header)
        assert response.status == HTTPStatus.OK
        assert len(response.body) > 0
