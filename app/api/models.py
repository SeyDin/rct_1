import asyncio
from typing import Optional
import uuid

from databases import Database
from sqlalchemy import (String, ForeignKey)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

DATABASE_URL = 'postgresql+asyncpg://pets_admin:pets_password@localhost/pet_project_storage'

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "accounts"

    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(140))
    pets: Mapped[list['Pet']] = relationship(
        "Pet",
        back_populates="account",
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"Account(account_id={self.account_id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Pet(Base):
    __tablename__ = "pets"

    pet_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30))
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("accounts.account_id"),
    )
    account: Mapped[Account] = relationship(
        "Account",
        back_populates="pets",
    )

    def __repr__(self) -> str:
        return f"Pet(id={self.pet_id!r}, name={self.name!r})"


database = Database(DATABASE_URL)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())
