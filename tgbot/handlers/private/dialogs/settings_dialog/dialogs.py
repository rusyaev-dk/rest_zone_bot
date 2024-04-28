from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group, Row, Select
from aiogram_dialog.widgets.text import Format, Const

from tgbot.handlers.private.dialogs.settings_dialog.callable import close_settings, change_user_language
from tgbot.handlers.private.dialogs.settings_dialog.getters import overall_settings_getter, change_language_getter
from tgbot.misc.constants import SET_USER_LANGUAGE_TEXT
from tgbot.misc.states import SettingsSG

overall_settings_window = Window(
    Format("{choose_option_text}"),
    SwitchTo(
        text=Format("{change_language_btn_text}"),
        id="change_language",
        state=SettingsSG.change_language
    ),
    Button(
        text=Format("{close_btn_text}"),
        id="close_settings",
        on_click=close_settings
    ),
    getter=overall_settings_getter,
    state=SettingsSG.overall_settings
)


change_user_language_window = Window(
    Const(SET_USER_LANGUAGE_TEXT),
    Row(
        Button(
            text=Const("🇷🇺 Русский"),
            id='ru_language',
            on_click=change_user_language
        ),
        Button(
            text=Const("🇺🇿 O'zbek"),
            id='uz_language',
            on_click=change_user_language
        )
    ),
    Button(
        text=Const("🇬🇧 English"),
        id='en_language',
        on_click=change_user_language
    ),
    SwitchTo(
        text=Format("{back_btn_text}"),
        id='cancel_language_setting',
        state=SettingsSG.overall_settings
    ),
    getter=change_language_getter,
    state=SettingsSG.change_language
)

overall_settings_dialog = Dialog(
    overall_settings_window,
    change_user_language_window,
)
