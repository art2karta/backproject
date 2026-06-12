import httpx


USER_SERVICE_URL = "http://user-service:8000"


def get_user_by_email(email: str):
    response = httpx.get(
        f"{USER_SERVICE_URL}/users/email/{email}"
    )

    if response.status_code != 200:
        return None

    return response.json()