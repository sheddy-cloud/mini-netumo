from api.routers import (alert, auth, certificate_check, domain_check,
                         status_log, target, user)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scheduler import scheduler

app = FastAPI(
    title="Mini Netumo API",
    description="Backend API for uptime & SSL monitoring",
    version="1.0.0",
)

# Optional: CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Badili kama unataka kuzuia baadhi ya origins tu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Mini Netumo API is running"}

# Include all routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(target.router)
app.include_router(alert.router)
app.include_router(status_log.router)
app.include_router(domain_check.router)
app.include_router(certificate_check.router)
