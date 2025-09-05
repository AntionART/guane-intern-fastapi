# File: /guane-intern-fastapi/app/api/routes/__init__.py

from fastapi import APIRouter

router = APIRouter()

from . import dogs, users, auth, files

router.include_router(dogs.router, prefix="/dogs", tags=["dogs"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(files.router, prefix="/files", tags=["files"])