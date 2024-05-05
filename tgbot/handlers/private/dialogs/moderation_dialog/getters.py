import datetime
from datetime import date
from typing import List, Dict

from aiogram_dialog import DialogManager

from data.l10n.translator import LocalizedTranslator
from domain.models.business_models import TopchanModel, TopchanReservationModel
from domain.repositories.db_repo.requests import RequestsRepo
from tgbot.handlers.private.dialogs.custom_calendar_widget import SELECTED_DAYS_KEY


async def overall_moderation_topchans_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")

    topchan_models: List[TopchanModel] = await repo.topchans.get_all_topchans()

    topchans: List[Dict] = []
    for topchan_model in topchan_models:
        topchans.append(
            {
                "id": topchan_model.topchan_id,
                "name": l10n.get_text(
                    key="topchan-btn",
                    args={"index": topchan_model.topchan_id}
                )
            }
        )

    data = {
        "topchans": topchans,
    }

    return data


def moderation_topchan_id_getter(topchan: Dict) -> str:
    return str(topchan.get("id"))


async def chosen_topchan_moderation_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")

    chosen_topchan_id: int = int(dialog_manager.dialog_data.get("chosen_topchan_id"))
    topchan_model: TopchanModel = await repo.topchans.get_topchan(topchan_id=chosen_topchan_id)

    dialog_manager.dialog_data.update(
        longitude=topchan_model.longitude,
        latitude=topchan_model.latitude,
    )

    data = {
        "chosen_topchan_text": l10n.get_text(
            key="chosen-topchan-msg",
            args={
                "index": chosen_topchan_id,
                "cost": topchan_model.cost_per_day
            }
        ),
        "topchan_location_btn_text": l10n.get_text(key="location-btn"),
        "back_btn_text": l10n.get_text(key="back-btn"),
    }

    return data


async def topchan_reservation_dates_getter(dialog_manager, **_):
    selected = dialog_manager.dialog_data.get(SELECTED_DAYS_KEY, [])
    return {
        "selected": ", ".join(sorted(selected)),
    }

