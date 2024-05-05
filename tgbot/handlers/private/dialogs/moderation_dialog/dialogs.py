from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Select, SwitchTo, Button
from aiogram_dialog.widgets.text import Format, Const

from tgbot.handlers.private.dialogs.custom_calendar_widget import CustomCalendar
from tgbot.handlers.private.dialogs.moderation_dialog.callable import close_moderation_menu, \
    switch_to_topchan_moderation, cancel_to_moderation_menu, \
    switch_to_topchan_reservation, cancel_topchan_dates_reservation, on_reservation_date_selected, on_make_reservation, \
    correct_phone_handler
from tgbot.handlers.private.dialogs.moderation_dialog.getters import overall_moderation_topchans_getter, \
    moderation_topchan_id_getter, chosen_topchan_moderation_getter, topchan_reservation_dates_getter
from tgbot.misc.states import ModerationMenuSG

overall_moderation_menu_window = Window(
    Const("⬇️ Выберите топчан:"),
    Group(
          Select(
            text=Format("{item[name]}"),
            items="topchans",
            item_id_getter=moderation_topchan_id_getter,
            id="select_topchan",
            on_click=switch_to_topchan_moderation
          ),
          width=2,
    ),
    Button(
        text=Const("Закрыть"),
        id="close_moderation_menu",
        on_click=close_moderation_menu
    ),
    state=ModerationMenuSG.overall_topchans,
    getter=overall_moderation_topchans_getter
)

chosen_topchan_moderation_window = Window(
    Format("{chosen_topchan_text}"),
    SwitchTo(
        text=Const("📌 Внести бронь"),
        id="make_topchan_reservation",
        on_click=switch_to_topchan_reservation,
        state=ModerationMenuSG.topchan_dates_reservation,
    ),
    SwitchTo(
        text=Const("↩️ Назад"),
        id="cancel_chosen_topchan",
        on_click=cancel_to_moderation_menu,
        state=ModerationMenuSG.overall_topchans,
    ),
    state=ModerationMenuSG.topchan_menu,
    getter=chosen_topchan_moderation_getter
)

topchan_reservation_dates_window = Window(
    Const("Выберите дату бронирования:"),
    CustomCalendar(
        id="topchan_reservation_calendar",
        on_click=on_reservation_date_selected,
    ),
    Button(
        text=Const("Внести бронь"),
        id="make_reservation",
        on_click=on_make_reservation,
        when=F["selected"],
    ),
    SwitchTo(
        text=Const("↩️ Назад"),
        id="cancel_topchan_dates_reservation",
        on_click=cancel_topchan_dates_reservation,
        state=ModerationMenuSG.topchan_menu,
    ),
    state=ModerationMenuSG.topchan_dates_reservation,
    getter=topchan_reservation_dates_getter
)

get_client_phone_window = Window(
    Const("Отправьте телефон клиента:"),
    MessageInput(
        func=correct_phone_handler,
        content_types=[ContentType.TEXT, ContentType.CONTACT],
    ),
    state=ModerationMenuSG.get_client_phone
)

moderation_menu_dialog = Dialog(
    overall_moderation_menu_window,
    chosen_topchan_moderation_window,
    topchan_reservation_dates_window,
    get_client_phone_window
)

# topchans_moderation_dialog = Dialog(
#
# )
