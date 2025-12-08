from fastapi import FastAPI
from app.api import whatsapp_webhook, webchat, health

def create_app() -> FastAPI:
    app = FastAPI(
        title="Assistant Gatekeeper API",
        version="0.1.0",
    )

    # Include routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(whatsapp_webhook.router, prefix="/webhook/whatsapp", tags=["whatsapp"])
    app.include_router(webchat.router, prefix="/webchat", tags=["webchat"])

    return app

app = create_app()
