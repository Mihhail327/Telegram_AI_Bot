from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.states import QuizState
from bot.keyboards.inline import quiz_keyboard, start_keyboard
from bot.services.quiz_ai import generate_quiz_question

router = Router()

MAX_LEVEL = 15
POINTS = [100, 200, 300, 500, 800, 1000, 1500, 2000, 3000, 5000, 8000, 10000, 15000, 30000, 50000]
SAFE_LEVELS = {5: 1000, 10: 10000}

@router.callback_query(F.data == "open_quiz")
async def open_quiz(callback: CallbackQuery, state: FSMContext):
    await state.set_state(QuizState.waiting_for_question)
    await state.update_data({
        "level": 1,
        "score": 0,
        "used_questions": set()
    })
    await callback.message.answer("🎮 Квиз запущен!")
    await send_question(callback.message, state)
    await callback.answer()

async def send_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    level = data["level"]
    used = data.get("used_questions", set())

    q = await generate_quiz_question(level, used)
    used.add(q["q"])
    await state.update_data({"current_q": q, "used_questions": used})

    text = f"💰 Уровень {level}/{MAX_LEVEL}\n\n❓ {q['q']}"
    await msg.answer(text, reply_markup=quiz_keyboard(q["options"]))
    await state.set_state(QuizState.waiting_for_answer)

@router.callback_query(F.data.startswith("quiz_answer_"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    q = data["current_q"]
    level = data["level"]
    score = data["score"]
    chosen = int(callback.data.split("_")[-1])
    correct = q["answer"]

    if chosen == correct:
        gained = POINTS[level - 1]
        score += gained
        msg = f"✅ Верно! +{gained} очков\nℹ️ {q['explain']}"
        level += 1
        await state.update_data({"score": score, "level": level})
    else:
        safe = max([v for k, v in SAFE_LEVELS.items() if level > k], default=0)
        await state.clear()
        await callback.message.edit_text(
            f"❌ Неверно. Правильный ответ: {q['options'][correct]}\nℹ️ {q['explain']}\n\n"
            f"🏁 Игра окончена. Ты заработал: {max(score, safe)} очков",
            reply_markup=start_keyboard()
        )
        await callback.answer()
        return

    if level > MAX_LEVEL:
        await state.clear()
        await callback.message.edit_text(
            f"{msg}\n\n🏆 Поздравляем! Ты прошёл все уровни.\nИтог: {score} очков",
            reply_markup=start_keyboard()
        )
    else:
        await callback.message.edit_text(f"{msg}\n\n➡️ Следующий вопрос загружается...")
        await send_question(callback.message, state)

    await callback.answer()

@router.callback_query(F.data == "quiz_end")
async def end_quiz(callback: CallbackQuery, state: FSMContext):
    score = (await state.get_data()).get("score", 0)
    await state.clear()
    await callback.message.edit_text(f"🏁 Игра завершена. Твои очки: {score}", reply_markup=start_keyboard())
    await callback.answer()

def register(dp):
    dp.include_router(router)