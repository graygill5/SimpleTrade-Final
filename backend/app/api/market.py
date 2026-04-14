from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models import User
from app.services.market_service import market_news, market_snapshot

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/overview")
def overview(_: User = Depends(get_current_user)):
    return {
        "snapshots": market_snapshot(),
        "news": market_news(),
    }
