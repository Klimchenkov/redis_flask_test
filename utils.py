import GPUtil
import psutil
from datetime import datetime


def load_info():
    gpus = GPUtil.getGPUs()
    gpu_load = gpus[0].load if gpus else None
    ram_load = psutil.virtual_memory().percent
    cpu_load = psutil.cpu_percent()
    return {
        'cpu': cpu_load,
        'ram': ram_load,
        'gpu': gpu_load
    }


def get_timestring():
    now = datetime.now()
    t_format = "%d:%m:%H:%M:%S"
    time_string = now.strftime(t_format)
    return time_string


def get_unixtimestamp(time_string):
    BASE_YEAR = 1970
    t_format = "%d:%m:%H:%M:%S"
    dt = datetime.strptime(time_string, t_format)
    timestamp = round(dt.replace(year=BASE_YEAR).timestamp())
    return timestamp
