from typing import List, Dict

from aiogram_dialog import DialogManager

from data.l10n.translator import LocalizedTranslator
from domain.models.business_models import TopchanModel
from domain.repositories.db_repo.requests import RequestsRepo


async def overall_topchans_getter(
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
                "name": l10n.get_text(key="topchan-btn", args={"index": topchan_model.topchan_id})
            }
        )

    data = {
        "overall_topchans_text": l10n.get_text(key="overall-topchans-msg"),
        "topchans": topchans,
        "close_btn_text": l10n.get_text(key='close-btn')
    }

    return data


def topchan_id_getter(topchan: Dict) -> str:
    return str(topchan.get("id"))


async def chosen_topchan_getter(
        dialog_manager: DialogManager,
        **kwargs
):
    l10n: LocalizedTranslator = dialog_manager.middleware_data.get("l10n")
    # repo: RequestsRepo = dialog_manager.middleware_data.get("repo")

    chosen_topchan_id: int = int(dialog_manager.dialog_data.get("chosen_topchan_id"))

    data = {
        "chosen_topchan_text": l10n.get_text(
            key="chosen-topchan-msg",
            args={"index": chosen_topchan_id}
        ),
        "back_btn_text": l10n.get_text(key="back-btn"),
    }

    return data
