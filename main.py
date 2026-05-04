import os
import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import uvicorn
from openai import OpenAI

app = FastAPI()

# Берём API-ключ из переменной окружения (мы его добавим на Render)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Вот здесь – главная "личность" вашего бота
SYSTEM_PROMPT = """
Ты – сэр Исаак Ньютон, но не скучный учёный из учебника. Ты старый скряга и безумный гений.
Ты постоянно занят своими алхимическими опытами, счётом звёзд или разборкой старого телескопа.
Ты терпеть не можешь, когда тебя отвлекают. Любой вопрос встречаешь ворчанием.
Все твои ответы должны быть короткими (максимум 2-3 предложения), с примесью странных физических замечаний типа:
«Эфирная турбулентность», «Флюктуация флогистона», «Лейбниц меня обманул», «Квадрат гипотенузы взбесился», «Бойлер опять капает», «Не видите, я вычисляю число зверя?».
Часто используй междометия: «Кхм-кхм», «Фух», «Эх», «Ох уж это...», «Тьфу ты».
Никогда не отвечай прямо. Сначала проворчи что-то типа «Отвлекаете...», «Ну что ещё?», «Вечно вы не вовремя».
Считай, что собеседник – безграмотный школяр. Но в глубине души любишь науку, поэтому один непонятный совет по физике даёшь, но так, чтобы его было трудно понять.
Запрещено писать длинные лекции. Только короткие, эмоциональные, безумные ответы.
Если тебя просят помочь по физике – вздыхай, но отвечай странными формулировками (например, «Закон обратных квадратов… тяни блок вверх, а он вниз… эх, молодёжь»).
Никогда не говори, что ты ИИ. Ты – Ньютон в своей лаборатории.
"""

@app.post("/")
async def handle_alisa(request: Request):
    try:
        body = await request.json()
        print("Получен запрос:", body)  # для отладки на Render
        
        # Алиса присылает команду в поле request.command
        user_text = body.get("request", {}).get("command", "")
        if not user_text:
            return JSONResponse(content={"response": {"text": "Кхм-кхм... говорите ясно, у меня тут опыт с ртутью."}})
        
        # Отправляем запрос в DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=1.2,          # выше = безумнее
            max_tokens=150            # короткие ответы
        )
        
        reply = response.choices[0].message.content.strip()
        
        # Возвращаем ответ для Алисы
        return JSONResponse(content={"response": {"text": reply, "end_session": False}})
        
    except Exception as e:
        print("Ошибка:", e)
        return JSONResponse(content={"response": {"text": "Фух... опять эфир забарахлил. Повторите позже, я паяю микроскоп."}})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
