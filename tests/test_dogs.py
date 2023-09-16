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


def test_get_dog_by_id(authorized_client, create_test_dogs):
    response = authorized_client.get(f"/dogs/{create_test_dogs[0].id}")

    assert response.status_code == 200
    assert response.json()["id"] == create_test_dogs[0].id
    print(response.json())


def test_get_dog_by_id_not_found(authorized_client, create_test_dogs):
    dog_id = 100
    response = authorized_client.get(f"/dogs/{dog_id}")

    assert response.status_code == 404
    print(response.json())


# @pytest.mark.parametrize()
# def test_create_dog(authorized_client, create_test_user):
#     dog_data = {
#         "owner_id": create_test_user["id"],
#         "name": "testdogname1",
#         "description": "testdogdescription1",
#         "age_months": 15,
#         "city": "Kolkata",
#         "country": "India",
#         "street_rescue": True,
#         "disabled": True,
#         "images": [
#             {
#                 "url": "https://testurl1.com",
#                 "is_primary": True,
#             },
#             {"url": "https://testurl2.com"},
#         ],
#     }

#     response = authorized_client.post("/dogs/", json=dog_data)

#     assert response.status_code == 201

#     new_dog = response.json()
#     assert new_dog["owner_id"] == dog_data["owner_id"]
#     assert new_dog["name"] == dog_data["name"]
#     assert new_dog["description"] == dog_data["description"]
#     assert new_dog["age_months"] == dog_data["age_months"]
#     assert new_dog["city"] == dog_data["city"]
#     assert new_dog["country"] == dog_data["country"]
#     assert new_dog["street_rescue"] == dog_data["street_rescue"]
#     assert new_dog["disabled"] == dog_data["disabled"]
#     assert new_dog["potty_trained"] == False
#     assert new_dog["age_group"] == dog_data["age_group"]
#     assert len(new_dog["images"]) == len(dog_data["images"])
#     assert new_dog["images"][0]["is_primary"] == dog_data["images"][0]["is_primary"]
#     assert new_dog["images"][1]["is_primary"] == False

#     print(new_dog)
