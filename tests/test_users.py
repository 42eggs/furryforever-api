from jose import jwt
from app import schemas
from app.config import settings
import pytest

# TODO: Add tests for user get, needs to login for it though


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "testmail1@gmail.com",
            "password": "testpassword1",
            "phone": "+11234567890",
            "name": "Test User",
        },
    )
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "testmail1@gmail.com"
    assert new_user.name == "Test User"
    assert new_user.phone == "+11234567890"


@pytest.mark.parametrize(
    "email, phone",
    [
        ("invalidemail", "+232"),
        ("validmail@gmail", "+25435435345435343322"),
        ("invalidemail", "+2326997777"),
        (None, "0000"),
        ("invalidmail", None),
        (None, None),
        ("valid@gmail.com", None),
        (None, "+44666454344"),
    ],
)
def test_create_user_invalid_email_or_phone(client, email, phone):
    response = client.post(
        "/users/",
        json={
            "email": email,
            "password": "testpassword1",
            "phone": phone,
            "name": "Test User",
        },
    )
    assert response.status_code == 422


def test_login_user(client, create_test_user):
    response = client.post(
        "/login/",
        data={
            "username": create_test_user["email"],
            "password": create_test_user["password"],
        },
    )
    login_response = schemas.Token(**response.json())
    user_id = jwt.decode(
        login_response.access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    ).get("user_id")
    assert response.status_code == 200
    assert user_id == create_test_user["id"]
    assert login_response.token_type == "bearer"


def test_login_user_invalid_password(client, create_test_user):
    response = client.post(
        "/login/",
        data={
            "username": create_test_user["email"],
            "password": "invalidpassword",
        },
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "Invalid Credentials"


def test_login_user_invalid_email(client, create_test_user):
    response = client.post(
        "/login/",
        data={
            "username": "wrongtestmail@gmail.com",
            "password": create_test_user["password"],
        },
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "Invalid Credentials"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "testpassword1", 403),
        ("testmail1@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "testpassword1", 422),
        ("testmail1@gmail.com", None, 422),
        (None, None, 422),
        ("wrongemail@gmail.com", None, 422),
        (None, "wrongpassword", 422),
    ],
)
def test_incorrent_login(client, create_test_user, email, password, status_code):
    response = client.post(
        "/login/",
        data={
            "username": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
    if status_code == 403:
        assert response.json().get("detail") == "Invalid Credentials"
