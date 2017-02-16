from django.conf import settings
from re import findall
import requests
import json
import pexpect

DEFAULT_VALUE = 9999.99


def get_latency_of_address(address='127.0.0.1', times=4, timeout=5):
    result = {
            'location': settings.LOCATION, 'status': 'Unknow server',
            'max': DEFAULT_VALUE, 'avg': DEFAULT_VALUE, 'min': DEFAULT_VALUE,
            'mdev': DEFAULT_VALUE
    }
    pingResult = pexpect.spawn('ping -c %s %s' % (str(times), address), timeout=5)
    valueList = []
    try:
        for line in pingResult:
            if 'rtt' in line.decode('utf-8'):
                valueList = line[23:-5].decode('utf-8').split('/', 3)
                result['min'] = float(valueList[0])
                result['avg'] = float(valueList[1])
                result['max'] = float(valueList[2])
                result['mdev'] = float(valueList[3])
                result['status'] = 'OK'
                break
    except pexpect.exceptions.TIMEOUT:
        result['status'] = 'Time out'
    print(result)
    return result


def send_distributed_ping_request(server, address, result):
    r = requests.post(
        server,
        json.dumps({'address': address}, ensure_ascii=False),
    )
    temp = {}
    try:
        temp = json.loads(r.content.decode('utf-8'))
        temp['alive'] = True
    except:
        temp['alive'] = False
    result['server'].append(temp)
    return json.loads(r.content.decode('utf-8').replace('\\', ''))


if __name__ == '__main__':
    print(get_latency_of_address('baidu.com', 4, 5))
