from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import List

from sqlalchemy import (ARRAY, DECIMAL, TIMESTAMP, Date, DateTime, ForeignKey,
                        Integer, String, UniqueConstraint, func, text)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class CurrencyType(StrEnum):
    USD = "USD"
    EUR = "EUR"
    KZT = "KZT"
    RUB = "RUB"

class Links(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255))
    parsed: Mapped[bool] = mapped_column(default=text("false"))

    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Cars(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(unique=True, nullable=False, index=True)
    url: Mapped[str] = mapped_column(index=True)

    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    brand: Mapped[str] = mapped_column(nullable=False, index=True)
    model: Mapped[str] = mapped_column(nullable=False, index=True)
    generation: Mapped[str | None] = mapped_column(nullable=True)

    year: Mapped[int] = mapped_column(nullable=False, index=True)

    price: Mapped[int] = mapped_column(nullable=False, index=True)
    currency: Mapped[CurrencyType] = mapped_column(nullable=False)

    city: Mapped[str] = mapped_column(nullable=False, index=True)
    region: Mapped[str | None] = mapped_column(nullable=True)

    body_type: Mapped[str] = mapped_column(String(50), index=True)

    engine_volume: Mapped[float | None]  = mapped_column(nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    transmission: Mapped[str] = mapped_column(String(50), index=True)

    drive: Mapped[str] = mapped_column(String(50), index=True)

    steering: Mapped[str] = mapped_column(String(20), nullable=False)

    color: Mapped[str | None] = mapped_column(nullable=True)

    customs_cleared: Mapped[bool]

    description: Mapped[str | None] = mapped_column(nullable=True)

    seller_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)

    options: Mapped[List[str]] = mapped_column(ARRAY(String))

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())

    views: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)

    images: Mapped[List["CarImage"]] = relationship(
        back_populates="car",
        cascade="all, delete, delete-orphan",
    )

    favorites: Mapped[List["Favorites"]] = relationship("Favorites", back_populates="car")
    price_history: Mapped[List["PriceHistory"]] = relationship("PriceHistory", back_populates="car")


class CarImage(Base):
    __tablename__ = 'car_image'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.car_id"))

    position: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str]

    car = relationship(
        "Cars",
        back_populates="images"
    )


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

    favorites: Mapped[List["Favorites"]] = relationship("Favorites", back_populates="user")

    refresh_tokens: Mapped[List["RefreshTokens"]] = relationship(
        "RefreshTokens",
        back_populates="user",
        cascade="all, delete-orphan",
    )

class Favorites(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    car_id: Mapped[int]  = mapped_column(ForeignKey("cars.car_id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="favorites"
    )

    car: Mapped["Cars"] = relationship(
        "Cars",
        back_populates="favorites"
    )

class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)

    expired: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

    user: Mapped["Users"] = relationship(
        "Users",
        back_populates="refresh_tokens"
    )

class Currency(Base):
    __tablename__ = 'currency'

    id: Mapped[int] = mapped_column(primary_key=True)
    base_currency: Mapped[CurrencyType] = mapped_column(nullable=False)
    quote_currency: Mapped[CurrencyType] = mapped_column(nullable=False)

    rate: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    rate_updated_at: Mapped[date] = mapped_column(Date)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())

class APIUsers(Base):
    __tablename__ = 'api_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), onupdate=func.now())

    refresh_tokens: Mapped[List["APIRefreshTokens"]] = relationship(
        "APIRefreshTokens",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Plans(Base):
    __tablename__ = 'plans'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    requests_per_day: Mapped[int] = mapped_column(nullable=False)
    requests_per_minute: Mapped[int] = mapped_column(nullable=False)

    max_requests: Mapped[int] = mapped_column(nullable=False)

class APIKeys(Base):
    __tablename__ = 'api_keys'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("api_users.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    key_hash: Mapped[str] = mapped_column(nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

class APIRefreshTokens(Base):
    __tablename__ = 'api_refresh_tokens'

    user_id: Mapped[int] = mapped_column(ForeignKey("api_users.id"), primary_key=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)

    expired: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now())

    user: Mapped["APIUsers"] = relationship(
        "APIUsers",
        back_populates="refresh_tokens"
    )

class CarViews(Base):
    __tablename__ = 'car_views'

    id: Mapped[int] = mapped_column(primary_key=True)

    car_id: Mapped[int] = mapped_column(
        ForeignKey("cars.car_id", ondelete="CASCADE"),
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    viewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("car_id", "user_id"),
    )

class PriceHistory(Base):
    __tablename__ = 'price_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.car_id"), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    car: Mapped["Cars"] = relationship(
        "Cars",
        back_populates="price_history"
    )