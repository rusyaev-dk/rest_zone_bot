from aiogram.fsm.state import State, StatesGroup


class FeedbackSG(StatesGroup):
    get_feedback = State()
    get_answer_to_user = State()


class UserRegistrationSG(StatesGroup):
    get_phone = State()


class SettingsSG(StatesGroup):
    overall_settings = State()
    change_language = State()
    change_notification_time = State()
