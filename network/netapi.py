import json
import requests
import subprocess


def get_latency_of_address(address='127.0.0.1', times=1, mode=0, timeout=10):
    p = subprocess.Popen(
            ["ping", "-c", str(times), address],
            stdout=subprocess.PIPE)
    output, err = p.communicate()
    # print(output.decode("utf-8"))
    return output.decode("utf-8")


def send_distributed_request(server, address, result, location):
    r = requests.post(
        server,
        json.dumps(
            {'address': address}, ensure_ascii=False),
    )
    temp = json.loads(r.content.decode('utf-8'))
    temp['location'] = location
    result['server'].append(temp)
    return json.loads(r.content.decode('utf-8').replace('\\', ''))
