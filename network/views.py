from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from network.netapi import send_distributed_request
import logging
import requests
import threading
import json
import subprocess
import shlex
import re
import os


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] \
        %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='views.log',
    filemode='a+'
)

# define a Handler which writes INFO messages or higher to the sys.stderr
logger = logging.getLogger('CyApi')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# add the handler to the root logger
logger.addHandler(console)


# Create your views here.
def ping(request):
    print(request.body)
    result = {}
    if request.method == 'POST':
        r = json.loads(request.body.decode(encoding='utf-8'))
        if('address' in r):
            times = 4
            if('times' in r):
                times = r['times']
                times = 4
            pingResult = subprocess.Popen(
                    ['ping', '-c', str(times), r['address']],
                    stdout=subprocess.PIPE)
            grepResult = subprocess.Popen(
                        shlex.split('grep rtt'), stdin=pingResult.stdout,
                        stdout=subprocess.PIPE)
            output, err = grepResult.communicate()
            data = re.findall("\d+\.\d+", output.decode('utf-8'))
            result['min'] = float(data[0])
            result['avg'] = float(data[1])
            result['max'] = float(data[2])
            result['mdev'] = float(data[3])
            result = json.dumps(result, ensure_ascii=False)
            # print(result)
            return HttpResponse(result.encode('utf-8'))
        else:
            logger.info('No address requests recived.')
            return HttpResponse('233 - 怕是姿势不对噢.'.encode('utf-8'))
    else:
        logger.info('Get request recived.')
        return HttpResponse('233 - 怕是姿势不对噢.'.encode('utf-8'))


def latency(request):
    result = {'server': []}
    f = open(os.path.join(settings.BASE_DIR, 'server.json'), 'r')
    serverList = json.loads(f.read())
    if request.method == 'POST':
        address = json.loads(request.body.decode(encoding='UTF-8'))['address']
        logger.info('Latency request to %s recived.' % address)
        jobs = []
        for server in serverList['servers']:
            t = threading.Thread(
                target=send_distributed_request,
                args=(server['url'], address, result, server['location']))
            t.start()
            jobs.append(t)
            logger.debug('    Ping request has been send to ' + server['url'])
        for t in jobs:
            t.join()
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'))
