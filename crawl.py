import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import asyncio
import aiohttp
import urllib3
import threading
import logging
import schedule
from db_access import *
from settings import *


header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=LOGGING_TEXT, level=logging.ERROR, format=LOG_FORMAT)


class TestIp:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.proxy = {
            'http': '{}:{}'.format(self.ip, self.port),
            'https': '{}:{}'.format(self.ip, self.port),
        }
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.test_ip())

    async def test_ip(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://www.httpbin.org/ip", proxy=self.proxy) as response:
                    res = await response.json()
                    if response.status == 200 and res.get("origin"):
                        if self.ip == res.get("origin").split(',')[0]:
                            return True
        except Exception as e:
            return False


async def test_ip(proxy):
    async with aiohttp.ClientSession() as session:
        proxies = 'http://' + str(proxy['ip']) + ':' + str(proxy['port'])
        try:
            async with session.get("http://www.httpbin.org/ip", proxy=proxies, timeout=20) as response:
                res = await response.json()
                if response.status == 200 and res.get("origin"):
                    if proxy['ip'] == res.get("origin").split(',')[0]:
                        create_proxy(**proxy)
        except Exception as e:
            pass


class Didsoft:
    def __init__(self):
        self.address_list = [
            'https://free-proxy-list.net',
            'https://www.sslproxies.org',
            'https://www.us-proxy.org',
        ]
        for address in self.address_list:
            try:
                loop_ip = asyncio.get_event_loop()
                tasks = [test_ip(_) for _ in self.didsoft(address)]
                loop_ip.run_until_complete(asyncio.wait(tasks))
            except Exception as e:
                logging.error('crawl address error,{}'.format(e.args))
                continue

    def didsoft(self, address):
        try:
            page = requests.get(address, headers=header, verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')
            tbody = soup.find('tbody')
            td = tbody.findAll('td')
            for x in range(0, len(td), 8):
                ip = td[x].text
                port = td[x + 1].text
                code = 'overseas'
                country = td[x + 3].text
                anonymity = td[x + 4].text
                https = td[x + 6].text
                proxy_info = {
                    "ip": ip,
                    "port": port,
                    "code": code,
                    "country": country,
                    "anonymity": anonymity,
                    "https": https,
                }
                yield proxy_info
        except Exception as e:
            logging.error('crawl {} error,{}'.format(address, e.args))


class Gatherproxy:
    def __init__(self):
        try:
            countries = self.getCountries()
        except Exception as e:
            logging.error('crawl gatherproxy country error,{}'.format(e.args))
            return
        for country in countries:
            try:
                self.proxybyCountry(country)
                time.sleep(10)
            except Exception as e:
                logging.error('crawl gatherproxy error ,{}', format(e.args))
                continue

    def proxybyCountry(self, country):
        country = country.strip()
        maxIndex = self.totalPages(country)
        for index in range(1, maxIndex+1):
            try:
                # self.getProxies(country, index)
                time.sleep(5)
                loop = asyncio.get_event_loop()
                tasks = [test_ip(_) for _ in self.getProxies(country, index)]
                loop.run_until_complete(asyncio.wait(tasks))
            except:
                continue

    # 获取所有国家
    def getCountries(self):
        url = 'http://www.gatherproxy.com/proxylistbycountry'
        r = requests.get(url, headers=header, timeout=10)
        tree = html.fromstring(r.content)
        countries = [country.split('(')[0] for country in tree.xpath('//*[@class="pc-list"]/li/a/text()')]
        return countries

    # 获取ip代理页面
    def connect(self, country, index):
        url = 'http://www.gatherproxy.com/proxylist/country/?c=%s' % country
        data = {'Country': country, 'Filter': '', 'PageIdx': index, 'Uptime': 0}
        r = requests.post(url, data=data, timeout=10)
        return r.content

    # 获取国家页数
    def totalPages(self, country):
        try:
            content = self.connect(country, 1)
            tree = html.fromstring(content)
            maxIndex = tree.xpath('//*[@id="psbform"]/div/a/text()')
            if maxIndex:
                return int(maxIndex[-1])
            else:
                return 0
        except Exception as e:
            pass

    # 获取代理
    def getProxies(self, country, index):
        content = self.connect(country, index)
        tree = html.fromstring(content)
        ips = tree.xpath('//*[@id="tblproxy"]/tr')
        for _ in ips[2:]:
            ip = _.xpath('./td[2]/script/text()')[0].split("document.write('")[1].split("')")[0]
            port = _.xpath('./td[3]/script/text()')[0].replace("document.write(gp.dep('", "").split("')")[0]
            port = int(port, 16)
            country = _.xpath('./td[5]/text()')[0]
            anonymity = _.xpath('./td[4]/text()')[0].lower()
            https = 'no'
            code = 'overseas'
            proxy_info = {
                "ip": ip,
                "port": port,
                "code": code,
                "country": country,
                "anonymity": anonymity,
                "https": https,
            }
            yield proxy_info


def run():
    proxies = get_ip()
    if len(proxies) <= MIN_NUM_PROXY:
        try:
            t1 = threading.Thread(target=Didsoft().__init__())
            t2 = threading.Thread(target=Gatherproxy().__init__())
            t1.start()
            t2.start()
        except Exception as e:
            logging.error('crawl thread error,{}'.format(e.args))


def crawl_ip():
    if len(get_ip()) != 0:
        schedule.every(CRAWL_INTERVAL).hours.do(run)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        run()
        time.sleep(100)
        crawl_ip()


if __name__ == '__main__':
    run()
    # crawl_ip()