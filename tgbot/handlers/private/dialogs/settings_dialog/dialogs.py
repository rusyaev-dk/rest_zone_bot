from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Row
from aiogram_dialog.widgets.text import Format, Const

from tgbot.handlers.private.dialogs.settings_dialog.callable import close_settings, change_user_language, \
    correct_phone_handler
from tgbot.handlers.private.dialogs.settings_dialog.getters import overall_settings_getter, change_language_getter, \
    change_phone_getter
from tgbot.misc.constants import SET_USER_LANGUAGE_TEXT
from tgbot.misc.states import SettingsSG

overall_settings_window = Window(
    Format("{overall_settings_text}"),
    SwitchTo(
        text=Format("{change_language_btn_text}"),
        id="change_language",
        state=SettingsSG.change_language
    ),
    SwitchTo(
        text=Format("{change_phone_btn_text}"),
        id="change_phone",
        state=SettingsSG.change_phone
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
    SwitchTo(
        text=Format("{back_btn_text}"),
        id='cancel_language_setting',
        state=SettingsSG.overall_settings
    ),
    getter=change_language_getter,
    state=SettingsSG.change_language
)


change_user_phone_window = Window(
    Format('{send_phone_msg_text}'),
    MessageInput(
        func=correct_phone_handler,
        content_types=[ContentType.TEXT, ContentType.CONTACT],
    ),
    SwitchTo(
        text=Format("{back_btn_text}"),
        id='cancel_phone_setting',
        state=SettingsSG.overall_settings
    ),

    getter=change_phone_getter,
    state=SettingsSG.change_phone
)


overall_settings_dialog = Dialog(
    overall_settings_window,
    change_user_language_window,
    change_user_phone_window,
)
