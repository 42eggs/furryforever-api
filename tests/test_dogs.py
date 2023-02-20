from jose import jwt
from app import schemas
from app.config import settings
import pytest
from typing import List


def test_get_all_dogs(authorized_client, create_test_dogs):
    response = authorized_client.get("/dogs/")

    # Checks the number of Dog entries and data validity only for now
    assert len([schemas.DogResponse(**dog) for dog in response.json()]) == len(
        create_test_dogs
    )

    # TODO: Check the actual data of the Dog entries if needed

    assert response.status_code == 200
    print(response.json())
