from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Dog(Base):
    __tablename__ = "dogs"

    # auto generated
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # user input : mandatory
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    age_months = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # user input : optional
    disabled = Column(Boolean, server_default="FALSE", nullable=False)
    street_rescue = Column(Boolean, server_default="FALSE", nullable=False)
    potty_trained = Column(Boolean, server_default="FALSE", nullable=False)

    # Groups (months): 0-2: 1, 2-6: 2, 6-12: 3, 12-24: 4, 24-48: 5, 48-96: 6, 96+: 7
    # TODO: find a better way to do this
    age_group = Column(Integer, nullable=False)

    # to be taken automatically when user is authenticated
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # may be useful later
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

    images = relationship("DogImage", back_populates="dog")


class DogImage(Base):
    __tablename__ = "dog_images"

    # auto generated
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # from user: mandatory
    url = Column(String, nullable=False, unique=True)

    # from user: optional
    is_primary = Column(Boolean, server_default="FALSE", nullable=False)

    # to be taken automatically when dog is created
    dog_id = Column(Integer, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)

    dog = relationship("Dog", back_populates="images")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class AdoptionRequest(Base):
    __tablename__ = "adoption_requests"

    # taken from dogs's owner_id
    requested_to_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    # taken from dogs's id
    dog_id = Column(
        Integer,
        ForeignKey("dogs.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    # taken from authenticated user's id or redirected to login
    requested_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

    requested_by = relationship("User", foreign_keys="AdoptionRequest.requested_by_id")
    requested_to = relationship("User", foreign_keys="AdoptionRequest.requested_to_id")
    dog = relationship("Dog", foreign_keys="AdoptionRequest.dog_id")
