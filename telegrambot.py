import telebot
import json
import server.endpoints as endpoints 
from server.utils import format_message
import requests
import os
import dotenv
dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN", None))

@bot.message_handler(commands=['ajuda'])
def ajuda(msg:telebot.types.Message):
    bot.reply_to(msg, "Hello, I'm a bot")

@bot.message_handler(commands=['total'])
def debito(msg:telebot.types.Message):
    bot.reply_to(msg, "Checkando total")
    response = requests.get(endpoints.BALANCE_ENDPOINT)
    bot.reply_to(msg, response.text, parse_mode="Markdown")

@bot.message_handler(commands=['debito'])
def debit(msg: telebot.types.Message):
    if msg.text.lower() == "/debito":
        bot.reply_to(msg, "Digite /debito <Motivo> <Valor> para creditar na nossa conta. Ex: /debito Mercado 1000")

    try:
        reason, value = format_message(msg)
        response = requests.post(endpoints.CHECK_INPUT_PROMPT, json={"text": f"/debito {reason} {value}"})
        if response.status_code != 200:
            bot.reply_to(msg, f'Erro: {response.text("error")}')
            return

        response = response.json()
        response = requests.post(endpoints.ADD_EXPENSE_ENDPOINT, json={"reason": response['reason'], "value": str(response['value']), "user": msg.from_user.first_name})
        response_json = response.json()
        response_messsage = f"ID: #{response_json['id']} \nMotivo: {response_json['reason']} \nValor: {response_json['value']} \nData: {response_json['created_at']}"
        bot.reply_to(msg, response_messsage)
    
    except Exception as e:
        print(f"Error processing credit score request: {e}")

@bot.message_handler(commands=['consulta'])
def consulta(msg:telebot.types.Message):
    text = msg.text.replace("/consulta", "").strip()
    reply = bot.reply_to(msg, "Consultando dados solicitados...")
    response = requests.post(endpoints.FREE_SQL_BUILDER, json={"text": text})
    print(response.text)
    response_text = response.text.replace("\\n", "\n")
    bot.edit_message_text(chat_id=msg.chat.id, message_id=reply.message_id, text=response_text)

if __name__ == "__main__":
    print("Telegram bot started..")
    bot.infinity_polling()
