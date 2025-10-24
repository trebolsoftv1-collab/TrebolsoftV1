from app.api.v1.items import router as items_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.clients import router as clients_router
from app.api.v1.credits import router as credits_router
from app.api.v1.transactions import router as transactions_router

__all__ = ["items_router", "auth_router", "users_router", "clients_router", "credits_router", "transactions_router"]