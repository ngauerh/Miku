import sys
from multiprocessing import Process

sys.path.append('.')
sys.path.append('..')

from app import run as ProxyApiRun
from crawl import crawl_ip as CrawlRun
from prove import prove_ip as ProveIP


def run():
    p_list = list()
    p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
    p_list.append(p1)
    p2 = Process(target=CrawlRun, name='CrawlRun')
    p_list.append(p2)
    p3 = Process(target=ProveIP, name='ProveIP')
    p_list.append(p3)

    for p in p_list:
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()


if __name__ == '__main__':
    run()

