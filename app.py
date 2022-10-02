from flask import Flask
from flask import request
from redis import Redis
import json

from utils import *

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

LOAD_DATA = "load_data"


@app.route('/get_load_data', methods=["GET", "POST"])
def get_load():
    data = {
        'method': request.method,
        'timestamp': get_timestring()
    }
    info = load_info()
    timestamp = get_unixtimestamp(data['timestamp'])

    if request.method == 'POST':
        try:
            load_types = request.json['load_types']
            for key in info.copy().keys():
                if key not in load_types:
                    info.pop(key, None)
        except KeyError:
            return 'Поле load_types является обязательным.'
    data['info'] = info
    data = json.dumps(data)
    redis.zadd(LOAD_DATA, {data: timestamp})
    return json.dumps(info)


@app.route('/get_all_data', methods=["GET"])
def get_all_data():
    data = redis.zrange(LOAD_DATA, 0, -1)
    response = {}
    for d in data:
        d = json.loads(d.decode('utf-8'))
        timestamp = d.pop('timestamp')
        response[timestamp] = d
    return json.dumps(response)


@app.route('/remove_data', methods=["POST"])
def remove_data():
    try:
        data = request.json
        start, end = data.get('start'), data.get('end')
        if start and end:
            redis.zremrangebyscore(LOAD_DATA, get_unixtimestamp(start), get_unixtimestamp(end))
            return f'Записи с {start} по {end} успешно удалены.'
        start = redis.zrange(LOAD_DATA, 0, -1, withscores=True)[0][1]
        end = redis.zrange(LOAD_DATA, 0, -1, withscores=True)[-1][1]
        redis.zremrangebyscore(LOAD_DATA, start, end)
        return f'Все записи успешно удалены.'
    except IndexError:
        return 'Записей нет, удалять нечего.'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
