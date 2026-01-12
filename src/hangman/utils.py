import importlib.resources
import requests
import uvicorn
from uvicorn.config import LOGGING_CONFIG

PACKAGE = __package__

def copy_text_resource(resource: str, dest_path: str):
    with (
            importlib.resources.open_text(f"{PACKAGE}.res", resource, encoding='utf-8') as src,
            open(dest_path, 'w', encoding='utf-8') as dst
    ):
        for line in src:
            dst.write(line)

def request_factory(server_url: str):
    def request(method: str, endpoint: str, data: dict = None) -> dict:
        url = server_url + endpoint
        response = requests.request(method=method, url=url, json=data)
        response.raise_for_status()
        return response.text
    return request

def uvicorn_serve(
        module_name: str,
        port: int,
        host: str,
        service_name: str,
):
    """Serve using Uvicorn."""
    log_config = LOGGING_CONFIG.copy()
    log_config["formatters"]["access"]["fmt"] = f"[{service_name}] %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(msecs)03dms %(status_code)s"
    log_config["formatters"]["default"]["fmt"] = f"[{service_name}] %(levelprefix)s %(message)s"

    uvicorn.run(
        app=f"{PACKAGE}.{module_name}:app",
        host=host,
        port=port,
        reload=True,
        log_config=log_config,
    )