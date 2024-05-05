from datetime import date
from typing import Dict, List

from babel.dates import get_day_names, get_month_names

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Calendar, CalendarScope,
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView, CalendarMonthView,
    CalendarScopeView, CalendarYearsView,
    DATE_TEXT, TODAY_TEXT,
)
from aiogram_dialog.widgets.text import Format, Text

from domain.repositories.db_repo.requests import RequestsRepo

SELECTED_DAYS_KEY = "selected_dates"


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short", context='stand-alone', locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        repo: RequestsRepo = manager.middleware_data.get("repo")

        chosen_topchan_id: int = int(manager.dialog_data.get("chosen_topchan_id"))
        reservations = await repo.reservations.get_topchan_reservations_by_month(
            topchan_id=chosen_topchan_id,
            month=current_date.month
        )

        reserved_dates: List[date] = []
        for reservation in reservations:
            reserved_dates.append(reservation.check_in.date())
            reserved_dates.append(reservation.check_out.date())
        reserved_dates.sort()

        reserved: bool = reserved_dates[0] <= current_date <= reserved_dates[-1]

        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get(SELECTED_DAYS_KEY, [])

        if serial_date in selected or reserved:
            return self.mark
        return await self.other.render_text(data, manager)


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            'wide', context='stand-alone', locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                date_text=MarkedDay("🔴", DATE_TEXT),
                today_text=MarkedDay("⭕", TODAY_TEXT),
                header_text="~~~~~ " + Month() + " ~~~~~",
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
                config=self.config
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text="~~~~~ " + Format("{date:%Y}") + " ~~~~~",
                this_month_text="[" + Month() + "]",
                config=self.config
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
                config=self.config
            ),
        }
