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

############# build ##############
#    bithumb_obj.dbbuild()
#    coinone_obj.dbbuild()
#    upbit_obj.dbbuild()
#    korbit_obj.dbbuild()

############# start ##############
    sched = BlockingScheduler()
    bithumb_obj.refresh()
    coinone_obj.refresh()
    upbit_obj.refresh()
    korbit_obj.refresh()

############# refresh ##############
    sched.add_job(bithumb_obj.refresh, 'interval', minutes = 5)
    sched.add_job(coinone_obj.refresh, 'interval', minutes = 5)
    sched.add_job(upbit_obj.refresh, 'interval', minutes = 5)
    sched.add_job(korbit_obj.refresh, 'interval', minutes = 5)
    sched.start()