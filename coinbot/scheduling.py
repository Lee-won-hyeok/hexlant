from apscheduler.schedulers.blocking import BlockingScheduler
from bithumb import bithumb
from coinone import coinone
from upbit import upbit
from korbit import korbit

if __name__ == '__main__':

    bithumb_obj = bithumb()
    coinone_obj = coinone()
    upbit_obj = upbit()
    korbit_obj = korbit()

    #bithumb_obj.dbbuild()
    #coinone_obj.dbbuild()
    #upbit_obj.dbbuild()
    #korbit_obj.dbbuild()

    sched = BlockingScheduler()
    sched.add_job(bithumb_obj.send(), 'interval', minutes = 10)
    sched.add_job(coinone_obj.send(), 'interval', minutes = 10)
    sched.add_job(upbit_obj.send(), 'interval', minutes = 10)
    sched.add_job(korbit_obj.send(), 'interval', minutes = 10)
    sched.start()