from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Integer,
    String,
    text,
    ForeignKey,
    BigInteger,
    SmallInteger,
)
from .database import Base
from sqlalchemy.orm import relationship


class Dog(Base):
    __tablename__ = "dogs"

    # auto generated
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)

    # user input : mandatory
    name = Column(String(length=100), nullable=False)
    description = Column(String(length=500), nullable=False)
    age_months = Column(SmallInteger, nullable=False, index=True)
    city = Column(String(length=100), nullable=False)
    country = Column(String(length=100), nullable=False)
    address = Column(String(length=250), nullable=False)

    # user input : optional
    disabled = Column(Boolean, server_default="FALSE", nullable=False)
    street_rescue = Column(Boolean, server_default="FALSE", nullable=False)
    potty_trained = Column(Boolean, server_default="FALSE", nullable=False)

    # Groups (months): 0-2: 1, 2-6: 2, 6-12: 3, 12-24: 4, 24-48: 5, 48-96: 6, 96+: 7
    # TODO: find a better way to do this
    age_group = Column(SmallInteger, nullable=False)

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
    id = Column(BigInteger, primary_key=True, index=True, nullable=False)

    # from user: mandatory
    url = Column(String(length=1000), nullable=False, unique=True)

    # from user: optional
    is_primary = Column(Boolean, server_default="FALSE", nullable=False)

    # to be taken automatically when dog is created
    dog_id = Column(
        BigInteger, ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False
    )

    dog = relationship("Dog", back_populates="images")


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    email = Column(String(length=500), nullable=False, unique=True)
    name = Column(String(length=100), nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String(length=50), nullable=False)
    is_admin = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class AdoptionRequest(Base):
    __tablename__ = "adoption_requests"

    # taken from dogs's owner_id
    requested_to_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    # taken from dogs's id
    dog_id = Column(
        BigInteger,
        ForeignKey("dogs.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    # taken from authenticated user's id or redirected to login
    requested_by_id = Column(
        BigInteger,
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
