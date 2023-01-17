import logging

from aiogram import Dispatcher, Router, F
from aiogram_dialog import DialogRegistry

from tgbot.filters.admin import IsAdmin
from tgbot.handlers.admin.admin import register_admin_router
from tgbot.handlers.user import main_menu
from tgbot.handlers.user.start import register_user_router
from tgbot.middlewares.db import DbSessionMiddleware
from tgbot.middlewares.deny_access import AccessMiddleware
from tgbot.middlewares.maintenance import MaintenanceMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


def register_middlewares(dp: Dispatcher, db_pool):
    dp.message.outer_middleware(DbSessionMiddleware(db_pool))
    dp.message.middleware(DbSessionMiddleware(db_pool))
    dp.callback_query.middleware(DbSessionMiddleware(db_pool))
    dp.inline_query.middleware(DbSessionMiddleware(db_pool))
    dp.message.middleware(MaintenanceMiddleware())
    dp.callback_query.middleware(MaintenanceMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())
    dp.message.middleware(AccessMiddleware())
    dp.callback_query.middleware(AccessMiddleware())
    logger.info('Middlewares successfully registered')


def register_dialogs(dp: Dispatcher, dialogs_router: Router):
    dialog_registry = DialogRegistry(dp)

    # ========= Admin dialogs =========
    admin_router = Router()

    # ========= Trader dialogs =========
    trader_router = Router()

    # ========= User dialogs =========
    user_router = Router()
    dialog_registry.register(main_menu.main_menu_dialog, router=user_router)
    dialogs_router.include_router(admin_router)
    dialogs_router.include_router(trader_router)
    dialogs_router.include_router(user_router)
    logger.info('Dialogs successfully registered')
    return dialog_registry


def register_handlers(dp: Dispatcher):
    user_router = Router()
    trader_router = Router()
    admin_router = Router()
    dialogs_router = Router()
    dialogs_router.message.filter(F.chat.type == "private")
    admin_router.message.filter(IsAdmin())

    register_admin_router(admin_router)
    register_user_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(trader_router)
    dp.include_router(user_router)
    user_router.include_router(dialogs_router)
    registy: DialogRegistry = register_dialogs(dp, dialogs_router)
    logger.info('Handlers successfully registered')
    return registy
