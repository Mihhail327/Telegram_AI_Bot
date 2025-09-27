from aiogram import Router

from .start import router as start_router
from .random import router as random_router
from .gpt import router as gpt_router
from .idea import router as idea_router
from .callbacks import router as callbacks_router
from .image import router as image_router
from .algo import router as algo_router
from .personalities import router as personalities_router
from .quiz import router as quiz_router


# Единый агрегирующий роутер
all_handlers_router = Router()
all_handlers_router.include_router(start_router)
all_handlers_router.include_router(random_router)
all_handlers_router.include_router(gpt_router)
all_handlers_router.include_router(idea_router)
all_handlers_router.include_router(callbacks_router)
all_handlers_router.include_router(image_router)
all_handlers_router.include_router(algo_router)
all_handlers_router.include_router(personalities_router)
all_handlers_router.include_router(quiz_router)
