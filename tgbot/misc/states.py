from aiogram.fsm.state import State, StatesGroup


class FeedbackSG(StatesGroup):
    get_feedback = State()
    get_answer_to_user = State()


class UserRegistrationSG(StatesGroup):
    get_phone = State()


class SettingsSG(StatesGroup):
    overall_settings = State()
    change_language = State()
    change_phone = State()


class NotifyUsersSG(StatesGroup):
    get_target_language_code = State()
    get_notify_media = State()
    notify_approve = State()


class RentTopchanSG(StatesGroup):
    overall_topchans = State()
    chose_topchan_rent_date = State()
    approve_rent = State()


class ModerationMenuSG(StatesGroup):
    overall_topchans = State()
    topchan_menu = State()
    topchan_dates_reservation = State()
    get_client_phone = State()
