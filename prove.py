import aiohttp
import asyncio
import time
from db_access import get_ip, del_ip
import requests
from settings import *
import logging
import schedule
try:
    from aiohttp import ClientError, ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOGGING_TEXT, level=logging.ERROR, format=LOG_FORMAT)


class ProveIp:
    async def test_ip(self, proxy):
        try:
            async with aiohttp.ClientSession() as session:
                real_proxy = 'http://' + proxy
                async with session.get("http://www.httpbin.org/ip", proxy=real_proxy, timeout=20) as response:
                    if response.status != 200:
                        del_ip(proxy.split(':')[0])
        except (ClientError, ClientConnectorError, TimeoutError, AttributeError, TimeoutError):
            try:
                requests.get('http://www.httpbin.org/ip', proxies={'http': proxy}, timeout=10)
            except:
                del_ip(proxy.split(':')[0])
        except Exception as e:
            logging.debug(e)

    def run(self):
        res = requests.get('http://www.httpbin.org/ip')
        if res.status_code == 200:
            try:
                proxies = get_ip()
                loop = asyncio.get_event_loop()
                tasks = [self.test_ip(i) for i in proxies]
                loop.run_until_complete(asyncio.wait(tasks))
            except Exception as e:
                logging.error('prove error,{}'.format(e.args))
        else:
            logging.error('prove error httpbin requests error')
            time.sleep(300)
            self.run()


def prove_ip():
    schedule.every(PROVE_INTERVAL).hours.do(ProveIp().run)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    ProveIp().run()


