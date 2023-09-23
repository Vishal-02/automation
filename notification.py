from plyer import notification as n

n.notify(
    title="Title",
    message="This better fucking work this time",
    app_name="Vishal Inc.",
    timeout=1
)

"""
if you want to schedule a task to run once, try this out
the 'schedule' library is not installed
i still don't get the point of the loop

import schedule
import time

def job_that_executes_once():
    # Do some work that only needs to happen once...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)

while True:
    schedule.run_pending()
    time.sleep(1)


check this out too: 

from schedule import every, repeat, run_pending
import time

@repeat(every(10).minutes)
def job():
    print("I am a scheduled job")

while True:
    run_pending()
    time.sleep(1)
"""