from aiogram import Router, flags, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from data.l10n.translator import LocalizedTranslator
from domain.repositories.db_repo.requests import RequestsRepo
from tgbot.keyboards.reply import feedback_kb
from tgbot.misc.states import FeedbackSG, SettingsSG

menu_router = Router()


@menu_router.message(F.text.in_(["Арендовать тапчан"]))
@flags.rate_limit(key="default")
async def rent_tapchan(
        message: Message,
        state: FSMContext,
        repo: RequestsRepo,
        l10n: LocalizedTranslator,
        dialog_manager: DialogManager
):
    await dialog_manager.reset_stack()


@menu_router.message(F.text.in_(["📩 Обратная связь", "📩 Fikr-mulohaza"]))
@flags.rate_limit(key="default")
async def feedback(
        message: Message,
        state: FSMContext,
        l10n: LocalizedTranslator,
        dialog_manager: DialogManager
):
    await dialog_manager.reset_stack()
    await message.answer(l10n.get_text(key="send-feedback"),
                         reply_markup=feedback_kb(l10n=l10n))
    await state.set_state(FeedbackSG.get_feedback)


@menu_router.message(F.text.in_(["🔧 Настройки", "🔧 Sozlamalar"]))
@flags.rate_limit(key="default")
async def settings(
        message: Message,
        dialog_manager: DialogManager
):
    await dialog_manager.start(
        state=SettingsSG.overall_settings,
        mode=StartMode.RESET_STACK,
    )
