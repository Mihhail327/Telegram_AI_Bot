from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot.states.states import QuizState
from bot.keyboards.inline import quiz_keyboard, quiz_status_keyboard, start_keyboard
from bot.services.quiz_ai import generate_quiz_question, check_answer, QuizQuestion
from bot.ui.quiz_ui import QuizUIManager

router = Router()
ui = QuizUIManager()

# 🎮 Старт квиза
@router.callback_query(F.data == "open_quiz")
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizState.waiting_for_question)
    await state.update_data({
        "score": 0,
        "level": 1,
        "used_questions": set(),
        "last_score_msg_id": None
    })

    question = await generate_quiz_question(level=1, used=set())
    await state.update_data({
        "current_question": question,
        "used_questions": {question.q}
    })

    level_bar = ui.render_progress_bar(1, 15)
    await callback.message.edit_text(
        f"{level_bar}\n💰 Очки: 0\n\n"
        f"💰 Уровень 1/15\n{question.q}",
        reply_markup=quiz_keyboard(question.options)
    )
    await callback.answer()

# ✅ Ответ на вопрос
@router.callback_query(F.data.startswith("quiz_answer_"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    question: QuizQuestion = data.get("current_question")
    score = data.get("score", 0)
    level = data.get("level", 1)

    answer_index = int(callback.data.removeprefix("quiz_answer_"))
    is_correct = check_answer(question, answer_index)
    points = question.points if is_correct else 0
    score += points

    await ui.cleanup_previous(callback.message.chat.id, state)

    level_bar = ui.render_progress_bar(level, 15)
    score_bar = f"💰 {score} / {15 * 100} очков"

    result_text = (
        f"{level_bar}\n{score_bar}\n\n"
        f"{'✅ Верно!' if is_correct else '❌ Неверно!'} +{points} очков\n\n"
        f"<i>{question.explain}</i>"
    )
    sent = await callback.message.answer(result_text, reply_markup=quiz_status_keyboard())

    await state.update_data({
        "score": score,
        "last_score_msg_id": sent.message_id
    })
    await callback.answer()

# ➡️ Следующий вопрос
@router.callback_query(F.data == "quiz_next")
async def next_question(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    level = data.get("level", 1) + 1
    score = data.get("score", 0)
    used = data.get("used_questions", set())

    if level > 15:
        await state.clear()
        await callback.message.edit_text(
            f"🏁 Игра завершена!\nТвой итоговый счёт: {score} очков",
            reply_markup=start_keyboard()
        )
        await callback.answer()
        return

    question = await generate_quiz_question(level=level, used=used)
    used.add(question.q)

    level_bar = ui.render_progress_bar(level, 15)
    await callback.message.edit_text(
        f"{level_bar}\n💰 Очки: {score}\n\n"
        f"💰 Уровень {level}/15\n{question.q}",
        reply_markup=quiz_keyboard(question.options)
    )
    await state.update_data({
        "level": level,
        "current_question": question,
        "used_questions": used
    })
    await callback.answer()

# 🛑 Завершить игру
@router.callback_query(F.data == "quiz_end")
async def end_quiz(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)
    await state.clear()

    await callback.message.edit_text(
        f"🏁 Игра завершена!\nТвой итоговый счёт: {score} очков",
        reply_markup=start_keyboard()
    )
    await callback.answer()

def register(dp):
    dp.include_router(router)