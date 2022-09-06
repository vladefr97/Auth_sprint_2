from typing import Dict


def generate_jwt_token_header(jwt_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {jwt_token}"}
