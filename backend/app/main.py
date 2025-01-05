from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from ipaddress import ip_address, ip_network
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)


@app.middleware("http")
async def validate_ip(request: Request, call_next):
    client_ip = ip_address(request.client.host)

    # IP 주소 확인
    is_allowed = any(
        client_ip in ip_network(allowed)
        for allowed in settings.ALLOWED_IPS
    )

    if not is_allowed:
        raise HTTPException(status_code=403, detail="Access denied")

    response = await call_next(request)
    return response