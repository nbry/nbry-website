"""Master application with subdomain routing."""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from nbry_website.config import SiteSettings
from nbry_website.sites.landing import app as landing_app
from nbry_website.sites.lifting import app as lifting_app
from nbry_website.sites.mycareer import app as mycareer_app

# Master app (root)
app = FastAPI(title="NBRY Multi-Site Platform")
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
        # Examples:
        #   "localhost:8000" -> "" (root)
        #   "lifting.localhost:8000" -> "lifting"
        #   "lifting.nbry.net" -> "lifting"
        #   "nbry.local:8000" -> "" (root)
        #   "lifting.nbry.local:8000" -> "lifting"

        # Remove port if present
        host_without_port = host.split(":")[0]
        parts = host_without_port.split(".")

        # Determine subdomain
        if len(parts) == 1:
            # Just "localhost" or single domain -> root
            subdomain = ""
        elif len(parts) == 2:
            # "nbry.net" or "nbry.local" -> root
            subdomain = ""
        else:
            # "lifting.nbry.net" or "lifting.nbry.local" -> "lifting"
            subdomain = parts[0]

        # Get the target app
        target_app = SITE_APPS.get(subdomain)

        if target_app is None:
            # Unknown subdomain - redirect to landing
            base_url = f"{request.url.scheme}://{site_settings.base_domain}"
            return RedirectResponse(url=base_url, status_code=302)

        # Store site info in request state
        request.state.site = subdomain or "landing"
        request.state.root_app = app

        # Inject site URLs into request state for templates
        request.state.site_urls = {
            "landing": f"{request.url.scheme}://{site_settings.base_domain}",
            "lifting": f"{request.url.scheme}://lifting.{site_settings.base_domain}",
            "coffee": f"{request.url.scheme}://coffee.{site_settings.base_domain}",
            "mycareer": f"{request.url.scheme}://mycareer.{site_settings.base_domain}",
        }

        # Call the target app
        # Note: We need to handle the app call directly for subdomain routing
        response = await call_next(request)
        return response


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
