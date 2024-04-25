import requests
import json
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def rispondi_testo(update, context, openai_api_key, openai_api_url):
    messaggio = update.message.text
    chat_id = update.message.chat_id    
    
    risposta = chiamata_api_openai(messaggio, openai_api_key, openai_api_url)
    if risposta:
        context.bot.send_message(chat_id=chat_id, text=risposta)
    else:
        context.bot.send_message(chat_id=chat_id, text="Mi dispiace, non sono in grado di rispondere a questa domanda.")

def chiamata_api_openai(messaggio, openai_api_key, openai_api_url):
    payload = {
        'prompt': messaggio,
        'max_tokens': 50
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }
    try:
        risposta = requests.post(openai_api_url, data=json.dumps(payload), headers=headers)
        risposta.raise_for_status()  
        return risposta.json()['choices'][0]['text'].strip()
    except Exception as e:
        logger.error(f"Errore durante la chiamata all'API di OpenAI: {e}")
        return None

def inizia(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao! Sono il tuo assistente virtuale. Puoi chiedermi qualsiasi cosa.")

def principale(openai_api_key, openai_api_url, telegram_bot_token):
    updater = Updater(token=telegram_bot_token, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", inizia))
    
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: rispondi_testo(update, context, openai_api_key, openai_api_url)))
   
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    openai_api_key = input("Inserisci la tua chiave API di OpenAI: ")
    openai_api_url = input("Inserisci l'URL dell'API di OpenAI: ")
    telegram_bot_token = input("Inserisci il token del tuo bot Telegram: ")
    principale(openai_api_key, openai_api_url, telegram_bot_token)
