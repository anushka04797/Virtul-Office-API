#========================================
# Scheduler Jobs
#========================================
import time

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)

# jobs
import scheduler_jobs

# scheduler.add_job(scheduler_jobs.FirstCronTest,)
# scheduler.add_job(scheduler_jobs.FlatReadingCronTest, 'interval', seconds=3)
# scheduler.add_job(scheduler_jobs.NotSetToZero, 'interval', seconds=3)
# scheduler.add_job(scheduler_jobs.AbnormalDeviceReading, 'interval', seconds=3)
scheduler.add_job(scheduler_jobs.Hello, 'interval', seconds=3)




scheduler.start()

#===========================================