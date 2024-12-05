from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette_context import middleware, plugins

from starmallow.applications import StarMallow

app = StarMallow(
    title="My API",
    version="1.0.0",
    middleware=[
        # Order matters!
        Middleware(GZipMiddleware, minimum_size=500),
        Middleware(
            middleware.ContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin()
            ),
        ),
    ],
)
