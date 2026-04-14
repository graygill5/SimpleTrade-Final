from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.models import Asset, ChatMembership, ChatRoom, User, WatchlistItem
from app.services.learning_service import seed_learning


def seed_data(db: Session):
    if db.query(User).count() == 0:
        alice = User(username="demo", email="demo@simpletrade.dev", hashed_password=get_password_hash("demo1234"), cash_balance=100000)
        bob = User(username="traderjoe", email="joe@simpletrade.dev", hashed_password=get_password_hash("demo1234"), cash_balance=100000)
        db.add_all([alice, bob])
        db.commit()

    if db.query(Asset).count() == 0:
        db.add_all(
            [
                Asset(symbol="AAPL", name="Apple", asset_type="stock", last_price=212),
                Asset(symbol="MSFT", name="Microsoft", asset_type="stock", last_price=425),
                Asset(symbol="SPY", name="SPDR S&P 500 ETF", asset_type="etf", last_price=531),
                Asset(symbol="BTC", name="Bitcoin", asset_type="crypto", last_price=69500),
            ]
        )
        db.commit()

    if db.query(ChatRoom).count() == 0:
        names = [
            "General Markets",
            "Stocks",
            "ETFs",
            "Crypto",
            "Day Trading",
            "Long-Term Investing",
            "Options",
        ]
        for n in names:
            db.add(ChatRoom(name=n, room_type="channel"))
        db.commit()
        demo = db.query(User).filter_by(username="demo").first()
        if demo:
            for room in db.query(ChatRoom).all():
                db.add(ChatMembership(room_id=room.id, user_id=demo.id, role="admin"))
            db.commit()

    demo = db.query(User).filter_by(username="demo").first()
    if demo and db.query(WatchlistItem).filter_by(user_id=demo.id).count() == 0:
        db.add_all([WatchlistItem(user_id=demo.id, symbol="AAPL"), WatchlistItem(user_id=demo.id, symbol="SPY")])
        db.commit()

    seed_learning(db)


if __name__ == "__main__":
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        seed_data(db)
        print("Seed complete")
    finally:
        db.close()
