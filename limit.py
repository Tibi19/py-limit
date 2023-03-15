import subprocess
import datetime
import tzlocal
from apscheduler.schedulers.background import BlockingScheduler

### SETTINGS

process_to_limit = "Acrobat.exe"
duration_until_limit_warning = datetime.timedelta(minutes = 80)
duration_until_limit = datetime.timedelta(minutes = 90)

### SCRIPT

timezone=str(tzlocal.get_localzone())
scheduler = BlockingScheduler(timezone = timezone)

def limit_process():
    subprocess.call(f"TASKKILL /F /IM \"{process_to_limit}\"", shell=True)

def stop_script():
    scheduler.shutdown(wait=False)

def limit_warning():
    subprocess.Popen(['start','alarm.wav'], shell=True)
    
start = datetime.datetime.now()
limit_time = start + duration_until_limit
warning_time = start + duration_until_limit_warning
stop_script_time = limit_time + datetime.timedelta(seconds=1)

def round_time(time: datetime.timedelta):
    total_seconds = time.seconds
    minutes = int(total_seconds / 60)
    seconds = total_seconds % 60
    minutes = minutes + 1 if seconds >= 30 else minutes
    hours = int(minutes / 60)
    minutes = minutes % 60
    return datetime.timedelta(hours=hours, minutes=minutes)

def log_time_left():
    now = datetime.datetime.now()
    time_left = limit_time - now
    print(round_time(time_left))

scheduler.add_job(limit_warning, 'date', run_date=warning_time)
scheduler.add_job(limit_process, 'date', run_date=limit_time)
scheduler.add_job(stop_script, 'date', run_date=stop_script_time)
scheduler.add_job(log_time_left, 'interval', minutes=1)
scheduler.start()