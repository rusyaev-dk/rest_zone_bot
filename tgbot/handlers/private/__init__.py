from .bot_start import start_router
from .main_menu import menu_router
from .feedback import feedback_router
from .admin_commands import admin_router
from .dialogs.settings_dialog.dialogs import overall_settings_dialog
from .dialogs.tapchan_rent_dialog.dialogs import topchan_rent_dialog
from .dialogs.moderation_dialog.dialogs import moderation_menu_dialog

private_routers = [
    start_router,
    admin_router,
    menu_router,
    feedback_router,
    topchan_rent_dialog,
    overall_settings_dialog,
    moderation_menu_dialog
]

__all__ = [
    "private_routers",
]
