from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button

from data.l10n.translator import LocalizedTranslator
from domain.repositories.db_repo.requests import RequestsRepo
from tgbot.misc.states import RentTopchanSG


async def close_overall_topchan_menu(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    await call.message.delete()
    await call.message.answer(l10n.get_text(key='main-menu-msg'))
    await dialog_manager.done()
    await dialog_manager.reset_stack()


async def switch_to_topchan(
        call: CallbackQuery,
        select: Select,
        dialog_manager: DialogManager,
        topchan_id: str,
):
    dialog_manager.dialog_data.update(chosen_topchan_id=topchan_id)
    await dialog_manager.switch_to(RentTopchanSG.chose_topchan_rent_date)


async def get_topchan_location(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):

    chosen_topchan_id: int = int(dialog_manager.dialog_data.get("chosen_topchan_id"))
    longitude = float(dialog_manager.dialog_data.get("longitude"))
    latitude = float(dialog_manager.dialog_data.get("latitude"))
    await call.message.delete()
    await call.bot.send_location(
        chat_id=call.from_user.id,
        latitude=latitude,
        longitude=longitude,
    )


async def cancel_to_overall_topchan_menu(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.clear()
