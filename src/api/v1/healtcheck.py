import time

import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/ping")
async def ping():
    services = {
        "db": "http://localhost:5432",
        "cache": "http://localhost:6379"
    }

    response_times = {}

    for service_name, service_url in services.items():
        try:
            start_time = time.time()
            response = requests.get(service_url, timeout=5)
            end_time = time.time()

            response_time = end_time - start_time
            if response.status_code == 200:
                response_times[service_name] = response_time
            else:
                raise HTTPException(status_code=500,
                                    detail=f"{service_name} service is not available")

        except requests.RequestException:
            raise HTTPException(status_code=500,
                                detail=f"{service_name} service is not available")

    return response_times
