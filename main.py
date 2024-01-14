import requests
import json
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
import time
import google.generativeai as genai

# Set up the Google Generative AI model
genai.configure(api_key="GEMINI API KEY")

generation_config = {
    "temperature": 0.05,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 10000,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    }
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Telegram bot configuration
TOKEN = 'BOT TOKEN'

# Initialize last_request_time to 0
last_request_time = 0

def send_typing_animation(context, user_id):
    context.bot.send_chat_action(chat_id=user_id, action="typing")

def send_spawning_animation(context, user_id):
    # Add your spawning animation logic here
    pass

def message(update: Update, context):
    global last_request_time

    user_id = update.effective_chat.id
    message_text = update.message.text

    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': 'YOUR_GOOGLE_API_KEY'
    }

    try:
        # Add typing animation
        send_typing_animation(context, user_id)

        # Check the time since the last request
        elapsed_time = time.time() - last_request_time

        # Implement rate limiting - wait if needed
        if elapsed_time < 1.0:  # Adjust this value based on your rate limits
            time.sleep(1.0 - elapsed_time)

        # Add spawning animation
        send_spawning_animation(context, user_id)

        # Use Google Generative AI for generating content
        response = model.generate_content([message_text])

        context.bot.send_message(chat_id=user_id, text="Bot: " + response.text)

    except requests.exceptions.RequestException as e:
        context.bot.send_message(chat_id=user_id, text="An error occurred while contacting the API.")
        print("Request Exception:", e)

    except Exception as e:
        context.bot.send_message(chat_id=user_id, text="An error occurred while processing the response.")
        print("Error:", e)

    finally:
        # Update the last request time
        last_request_time = time.time()

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    message_handler = MessageHandler(Filters.text & ~Filters.command, message)
    dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
