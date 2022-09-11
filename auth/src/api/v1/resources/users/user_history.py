from typing import Dict

from http import HTTPStatus

from api.extensions.rate_limit import rate_limiter
from api.v1.scheme import UserHistoryPaginationScheme, UserHistoryScheme
from db.relational.models.user_history import UserHistory
from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from flask_sqlalchemy import Pagination


class UserAllHistoryAPI(Resource):
    decorators = [rate_limiter.limit(limit_value="100 per hour")]

    @jwt_required()
    def get(self) -> tuple[UserHistoryPaginationScheme, int]:
        """
         Return list of user's login history
        ---
         tags:
           - auth
         parameters:
           - name: page
             in: query
             schema:
               properties:
                 page:
                   type: integer
                   description: page number
                   default: 1
           - name: limit
             in: query
             schema:
               properties:
                 limit:
                   type: integer
                   description: count of rec on the page
                   default: 5
         responses:
           200:
             description: Success user's list of logins
           400:
             description: Bad request response
           404:
             description: Not found
           429:
             description: Too many requests. Limit in interval seconds
        """
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        user_history: Pagination = UserHistory.query.filter_by(user_id=current_user.id).paginate(
            page=page, per_page=limit
        )
        history_items = [
            UserHistoryScheme(
                user_agent=user_history.user_agent,
                ip_address=user_history.ip_address,
                url=user_history.url,
                timestamp=str(user_history.timestamp),
            )
            for user_history in user_history.items
        ]

        pagination_schema = UserHistoryPaginationScheme(
            has_next=user_history.has_next,
            has_prev=user_history.has_prev,
            items=history_items,
            next_num=user_history.next_num,
            page=user_history.page,
            pages=user_history.pages,
            per_page=user_history.per_page,
            prev_num=user_history.prev_num,
        )

        return pagination_schema.dict(), HTTPStatus.OK

    def delete(self) -> Dict[str, str]:
        return UserHistory.delete_all()
