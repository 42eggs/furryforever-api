from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class Dogs(Base):
    __tablename__ = "dogs"

    # auto generated
    id = Column(Integer, primary_key=True, index=True, nullable=False)

    # user input : mandatory
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    age_months = Column(Integer, nullable=False)

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

    # Uncomment this to get the owner's details
    # owner = relationship("Users")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


class AdoptionRequests(Base):
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

    requested_by = relationship("Users", foreign_keys="Users.requested_by_id")
    dog = relationship("Dogs")
