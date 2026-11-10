from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes_auth import router as auth_router
from app.api.routes_admin import router as admin_router

app = FastAPI(title=settings.app_name, version="0.1.0", description="Nangarhar University Digital Library API")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True,
                   allow_methods=["GET", "POST", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type"])
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(admin_router, prefix=settings.api_v1_prefix)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "NUDL API"}
