from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    cash_balance: Mapped[float] = mapped_column(Float, default=100000.0)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    holdings: Mapped[list["Holding"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    trades: Mapped[list["Trade"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    watchlist_items: Mapped[list["WatchlistItem"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"
    __table_args__ = (UniqueConstraint("user_id", "symbol", name="uq_watchlist_user_symbol"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    symbol: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="watchlist_items")


class Holding(Base):
    __tablename__ = "holdings"
    __table_args__ = (UniqueConstraint("user_id", "symbol", name="uq_holding_user_symbol"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    symbol: Mapped[str] = mapped_column(String(10), index=True)
    quantity: Mapped[float] = mapped_column(Float, default=0)
    avg_cost: Mapped[float] = mapped_column(Float, default=0)

    user: Mapped[User] = relationship(back_populates="holdings")


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    symbol: Mapped[str] = mapped_column(String(10), index=True)
    side: Mapped[str] = mapped_column(String(4))
    quantity: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    notional: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="trades")


class FriendRequest(Base):
    __tablename__ = "friend_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Friendship(Base):
    __tablename__ = "friendships"
    __table_args__ = (UniqueConstraint("user_id", "friend_id", name="uq_friend_pair"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    is_close_friend: Mapped[bool] = mapped_column(Boolean, default=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    room: Mapped[str] = mapped_column(String(80), index=True, default="global")
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LearningModule(Base):
    __tablename__ = "learning_modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    content: Mapped[str] = mapped_column(Text)
    xp_reward: Mapped[int] = mapped_column(Integer, default=20)


class LearningProgress(Base):
    __tablename__ = "learning_progress"
    __table_args__ = (UniqueConstraint("user_id", "module_id", name="uq_progress_user_module"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("learning_modules.id"), index=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    quiz_score: Mapped[int] = mapped_column(Integer, default=0)


class RewardLedger(Base):
    __tablename__ = "reward_ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    reason: Mapped[str] = mapped_column(String(120))
    amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
