import requests
import uvicorn
from uvicorn.config import LOGGING_CONFIG

def request_factory(server_url: str):
    def request(*, method: str, endpoint: str, data: dict = None) -> dict:
        url = server_url + endpoint
        response = requests.request(method=method, url=url, json=data)
        response.raise_for_status()
        result = {}
        if response.text.strip() != "":    
            result = response.json()
        return result
    return request

def uvicorn_serve(
        app: str = "hangman:api",
        port: int = 8000,
        host: str = "localhost",
        service_name: str = "hangman_service",
):
    """Serve using Uvicorn."""
    log_config = LOGGING_CONFIG.copy()

    log_config["formatters"]["access"]["fmt"] = f"[{service_name}] %(levelprefix)s %(msecs)03dms %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    log_config["formatters"]["default"]["fmt"] = f"[{service_name}] %(levelprefix)s %(message)s"

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_config=log_config,
    )