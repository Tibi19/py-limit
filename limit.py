import subprocess
import datetime
from apscheduler.schedulers.background import BlockingScheduler

process_to_limit = "Acrobat.exe"
scheduler = BlockingScheduler()

def limit_process():
    subprocess.call(f"TASKKILL /F /IM \"{process_to_limit}\"", shell=True)

def stop_script():
    scheduler.shutdown(wait=False)

now = datetime.datetime.now()
trigger_time = now + datetime.timedelta(minutes=1)
stop_script_time = trigger_time + datetime.timedelta(seconds=1)
scheduler.add_job(limit_process, 'date', run_date=trigger_time)
scheduler.add_job(stop_script, 'date', run_date=stop_script_time)
scheduler.start()