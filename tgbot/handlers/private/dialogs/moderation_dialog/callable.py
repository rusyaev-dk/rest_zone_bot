import re
from datetime import date, datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Calendar, ManagedCalendar

from data.l10n.translator import LocalizedTranslator
from domain.repositories.db_repo.requests import RequestsRepo
from tgbot.handlers.private.dialogs.custom_calendar_widget import SELECTED_DAYS_KEY
from tgbot.misc.states import ModerationMenuSG


async def close_moderation_menu(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    await call.message.delete()
    await call.message.answer(l10n.get_text(key='main-menu-msg'))
    await dialog_manager.done()
    await dialog_manager.reset_stack()


async def switch_to_topchan_moderation(
        call: CallbackQuery,
        select: Select,
        dialog_manager: DialogManager,
        topchan_id: str,
):
    dialog_manager.dialog_data.update(chosen_topchan_id=topchan_id)
    await dialog_manager.switch_to(ModerationMenuSG.topchan_menu)


async def cancel_to_moderation_menu(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.clear()


async def switch_to_topchan_reservation(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ModerationMenuSG.topchan_dates_reservation)


async def cancel_topchan_dates_reservation(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ModerationMenuSG.topchan_menu)


async def on_reservation_date_selected(
    callback: ChatEvent,
    widget: ManagedCalendar,
    dialog_manager: DialogManager,
    clicked_date: date, /,
):
    selected = dialog_manager.dialog_data.setdefault(SELECTED_DAYS_KEY, [])
    serial_date = clicked_date.isoformat()
    if serial_date in selected:
        selected.remove(serial_date)
    else:
        selected.append(serial_date)


async def on_make_reservation(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    await dialog_manager.switch_to(ModerationMenuSG.get_client_phone)


async def correct_phone_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager,
) -> None:
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    chosen_topchan_id: int = int(dialog_manager.dialog_data.get("chosen_topchan_id"))

    selected_dates = dialog_manager.dialog_data.setdefault(SELECTED_DAYS_KEY, [])
    selected_dates_datetime = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in selected_dates]
    sorted_dates = sorted(selected_dates_datetime)

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
        pattern = r'^\+?998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$'

        if not re.match(pattern, phone):
            return
        elif phone[0] != '+':
            phone = "+" + phone

    await repo.reservations.add_reservation(
        topchan_id=chosen_topchan_id,
        check_in=sorted_dates[0],
        check_out=sorted_dates[-1],
        user_id=message.from_user.id,
        user_phone=phone,
    )
    await message.answer("✅ Бронь внесена")
    await dialog_manager.switch_to(ModerationMenuSG.overall_topchans)

