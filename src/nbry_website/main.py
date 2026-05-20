"""Master application with subdomain routing."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import Message

from nbry_website.config import SiteSettings
from nbry_website.sites.landing import app as landing_app
from nbry_website.sites.lifting import app as lifting_app
from nbry_website.sites.mycareer import app as mycareer_app

# Master app (root)
app = FastAPI(title="nbry Multi-Site Platform")
site_settings = SiteSettings()


# Subdomain to app mapping
def get_site_apps() -> dict[str, FastAPI]:
    """Get mapping of subdomains to site apps."""
    apps = {
        "": landing_app.app,  # nbry.net (root)
    }

    # Add enabled sites
    if site_settings.lifting_site_enabled:
        apps["lifting"] = lifting_app.app

    if site_settings.mycareer_site_enabled:
        apps["mycareer"] = mycareer_app.app

    # Future sites will be added here when enabled
    # if site_settings.coffee_site_enabled:
    #     apps["coffee"] = coffee_app.app

    return apps


SITE_APPS = get_site_apps()


class SubdomainRoutingMiddleware(BaseHTTPMiddleware):
    """Middleware to route requests based on subdomain."""

    async def dispatch(self, request: Request, call_next):  # type: ignore
        """Route requests to appropriate site based on subdomain."""
        host = request.headers.get("host", "")

        # Extract subdomain
        host_without_port = host.split(":")[0]
        parts = host_without_port.split(".")

        # Determine subdomain
        if len(parts) <= 2:
            subdomain = ""  # root domain
        else:
            subdomain = parts[0]  # first part is subdomain

        # Get the target app
        target_app = SITE_APPS.get(subdomain)

        if target_app is None:
            # Unknown subdomain - redirect to landing
            base_url = f"{request.url.scheme}://{site_settings.base_domain}"
            return RedirectResponse(url=base_url, status_code=302)

        # If target_app is the same as the master app, continue normally
        if target_app == app:
            return await call_next(request)

        # Store site info in request state for templates
        request.state.site = subdomain or "landing"
        request.state.site_urls = {
            "landing": f"{request.url.scheme}://{site_settings.base_domain}",
            "lifting": f"{request.url.scheme}://lifting.{site_settings.base_domain}",
            "coffee": f"{request.url.scheme}://coffee.{site_settings.base_domain}",
            "mycareer": f"{request.url.scheme}://mycareer.{site_settings.base_domain}",
        }

        # Call the target sub-app directly using ASGI protocol
        status_code = 200
        response_headers: list[tuple[bytes, bytes]] = []
        body_parts: list[bytes] = []

        async def send(message: Message) -> None:
            nonlocal status_code, response_headers, body_parts
            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_headers = message.get("headers", [])
            elif message["type"] == "http.response.body":
                body_parts.append(message.get("body", b""))

        await target_app(request.scope, request.receive, send)

        # Build the response
        body = b"".join(body_parts)
        headers_dict = {k.decode(): v.decode() for k, v in response_headers}
        return Response(content=body, status_code=status_code, headers=headers_dict)


# Add middleware
app.add_middleware(SubdomainRoutingMiddleware)


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Health check endpoint for load balancer."""
    return {
        "status": "healthy",
        "sites": list(SITE_APPS.keys()),
        "environment": site_settings.site_mode.value,
    }
