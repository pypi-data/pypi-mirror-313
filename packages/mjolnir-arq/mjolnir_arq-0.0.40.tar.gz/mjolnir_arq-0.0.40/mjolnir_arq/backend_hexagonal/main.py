from fastapi import FastAPI
from src.core.config import settings
from src.core.middleware.user_rate_limit_middleware import UserRateLimitMiddleware
from src.infrastructure.web.routes.route import Route
""" from src.infrastructure.web.routes.route_business import RouteBusiness """
from src.core.middleware.cors_app import CorsAppConfigurator
from src.core.middleware.redirect_to_docs import RedirectToDocsMiddleware


app = FastAPI(
    title=settings.project_name,
    description=f"{settings.project_description} [{settings.app_environment}]",
    version=settings.project_version,
)

if settings.app_environment == "production":
    app.add_middleware(
        UserRateLimitMiddleware, default_limits=["100/hour"], login_limits=["20/hour"]
    )
    
app.add_middleware(RedirectToDocsMiddleware)
CorsAppConfigurator.setup_cors(app)
Route.set_routes(app)
""" RouteBusiness.set_routes(app) """
