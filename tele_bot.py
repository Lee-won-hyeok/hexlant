import telebot

bot = telebot.TeleBot("1344514128:AAGLLNrfIgMME0CXcqDQbXFz7y--Hl7MJto")

@bot.message_handler(commands=['start', 'help'])
def test(message):
	bot.reply_to(message, "test")

bot.polling()