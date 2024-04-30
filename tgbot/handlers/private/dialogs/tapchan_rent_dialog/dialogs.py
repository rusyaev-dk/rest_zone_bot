from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, Select, SwitchTo, Button
from aiogram_dialog.widgets.text import Format

from tgbot.handlers.private.dialogs.tapchan_rent_dialog.callable import switch_to_topchan, cancel_to_overall_topchans, \
    close_topchan_rent
from tgbot.handlers.private.dialogs.tapchan_rent_dialog.getters import overall_topchans_getter, topchan_id_getter, \
    chosen_topchan_getter
from tgbot.misc.states import RentTopchanSG

overall_topchans_window = Window(
    Format("{overall_topchans_text}"),
    Group(
          Select(
            text=Format("{item[name]}"),
            items="topchans",
            item_id_getter=topchan_id_getter,
            id="select_topchan",
            on_click=switch_to_topchan,

          ),
          width=2,
    ),
    Button(
        text=Format("{close_btn_text}"),
        id="close_topchan_rent",
        on_click=close_topchan_rent
    ),
    state=RentTopchanSG.overall_topchans,
    getter=overall_topchans_getter
)

chosen_topchan_window = Window(
    # Const("dasfads"),
    Format("{chosen_topchan_text}"),
    SwitchTo(
        text=Format("{back_btn_text}"),
        id="cancel_chosen_topchan",
        on_click=cancel_to_overall_topchans,
        state=RentTopchanSG.overall_topchans,
    ),
    state=RentTopchanSG.chose_topchan_rent_date,
    getter=chosen_topchan_getter
)

topchan_rent_dialog = Dialog(
    overall_topchans_window,
    chosen_topchan_window
)
