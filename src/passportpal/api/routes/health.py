from fastapi import APIRouter, Response

from passportpal.api.deps import SettingsDep, StoreDep

router = APIRouter(tags=["health"])


@router.get("/health")
def health(settings: SettingsDep) -> dict[str, str]:
    """Liveness check."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
    }


@router.head("/health")
def health_head() -> Response:
    """Support HEAD requests from monitoring services."""
    return Response(status_code=200)


@router.get("/ready")
def ready(store: StoreDep, response: Response) -> dict:
    """Readiness check."""
    checks = {"records_loaded": store.ready}
    ok = all(checks.values())

    if not ok:
        response.status_code = 503

    return {
        "status": "ready" if ok else "not_ready",
        "checks": checks,
    }
