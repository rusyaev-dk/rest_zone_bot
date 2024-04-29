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
