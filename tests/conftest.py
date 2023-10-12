from fastapi.testclient import TestClient
from app import models
from app.database import get_db
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import Base
import pytest
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def create_test_user(client):
    user_data = {
        "email": "logintestemail@gmail.com",
        "password": "logintestpassword",
        "phone": "+919876543210",
        "name": "Login Test User",
    }

    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture(scope="module")
def token(create_test_user):
    return create_access_token({"user_id": create_test_user["id"]})


@pytest.fixture(scope="module")
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture(scope="module")
def create_test_dogs(create_test_user, session):
    dogs_data = [
        {
            "owner_id": create_test_user["id"],
            "name": "testdogname1",
            "description": "testdogdescription1",
            "age_months": 12,
            "city": "Delhi",
            "country": "India",
            "address": "Saket",
            "street_rescue": True,
            "disabled": True,
            "potty_trained": True,
            "age_group": 3,
            "images": [
                {
                    "url": "https://images.pexels.com/photos/1851164/pexels-photo-1851164.jpeg",
                    "is_primary": True,
                },
                {
                    "url": "https://images.pexels.com/photos/1805164/pexels-photo-1805164.jpeg"
                },
                {
                    "url": "https://images.pexels.com/photos/733416/pexels-photo-733416.jpeg"
                },
            ],
        },
        {
            "owner_id": create_test_user["id"],
            "name": "testdogname2",
            "description": "testdogdescription2",
            "age_months": 2,
            "city": "New York",
            "country": "USA",
            "address": "Manhattan",
            "street_rescue": True,
            "potty_trained": True,
            "age_group": 1,
            "images": [
                {
                    "url": "https://images.pexels.com/photos/18512311464/pexels-photo-1851164.jpeg",
                    "is_primary": True,
                },
                {
                    "url": "https://images.pexels.com/photos/21321312/pexels-photo-1805164.jpeg"
                },
                {"url": "https://images.pexels.com/photos/44/pexels-photo-733416.jpeg"},
            ],
        },
        {
            "owner_id": create_test_user["id"],
            "name": "testdogname3",
            "description": "testdogdescription3",
            "age_months": 55,
            "city": "Moscow",
            "country": "Russia",
            "address": "lol",
            "disabled": True,
            "age_group": 6,
            "images": [
                {
                    "url": "https://images.pexels.com/photos/12312/pexels-photo-1851164.jpeg"
                },
                {
                    "url": "https://images.pexels.com/photos/18051132164/pexels-photo-1805164.jpeg",
                    "is_primary": True,
                },
                {
                    "url": "https://images.pexels.com/photos/7332312416/pexels-photo-733416.jpeg"
                },
            ],
        },
    ]

    for dog_data in dogs_data:
        images = dog_data.pop("images")
        dog = models.Dog(**dog_data)
        session.add(dog)
        session.commit()
        session.refresh(dog)
        session.add_all([models.DogImage(dog_id=dog.id, **image) for image in images])
        session.commit()

    # session.add_all([models.Dog(**dog) for dog in dogs_data])
    # session.commit()

    all_dogs = session.query(models.Dog).all()
    return all_dogs
