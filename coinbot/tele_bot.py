import telegram
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process, Queue
import crawling
import coindb

bot = telegram.Bot(token = "1344514128:AAGLLNrfIgMME0CXcqDQbXFz7y--Hl7MJto")
id_list = []

def id_updates():
	chat_id = bot.getUpdates()
	print(len(chat_id))
	for i in chat_id:
		if i.message.chat.id not in id_list:
			id_list.append(i.message.chat.id)
			print("update", i.message.chat.id)

def send():
	newnotice = coindb.new_notice()
	for i in id_list:
		print("send...", i)
		for j in newnotice:
			bot.sendMessage(chat_id = i, text = j)
		tmpmsg = "비트코인 :" + crawling.new_coinchart()['비트코인']
		bot.sendMessage(chat_id = i, text = tmpmsg)

if __name__ == '__main__':
	#coindb.startdb()
	sched = BlockingScheduler()
	id_updates()
	
	send()
	
	sched.add_job(id_updates, 'interval', minutes = 1)
	sched.add_job(send, 'interval', minutes = 1)
	sched.start()