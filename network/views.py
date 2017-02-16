from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import network.netapi as netapi
import logging
import requests
import threading
import json
import os


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] \
        %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='views.log',
    filemode='w+'
)

# define a Handler which writes INFO messages or higher to the sys.stderr
logger = logging.getLogger('CyApi')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# add the handler to the root logger
logger.addHandler(console)


def ping(request):
    returnString = '233 - 怕是姿势不对噢.'
    if request.method == 'POST':
        r = json.loads(request.body.decode(encoding='utf-8'))
        if('address' in r):
            result = netapi.get_latency_of_address(r['address'], settings.TIMES, settings.TIME_OUT)
            returnString = json.dumps(result, ensure_ascii=False)
        else:
            logger.info('No address requests recived.')
    else:
        logger.info('Get request recived.')
    return HttpResponse(returnString.encode('utf-8'))


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
                target=netapi.send_distributed_ping_request,
                args=(server, address, result))
            t.start()
            jobs.append(t)
            logger.debug('    Ping request has been send to ' + server)
        for t in jobs:
            t.join()
    return HttpResponse(json.dumps(result, ensure_ascii=False).encode('utf-8'))
