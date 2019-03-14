from sqlalchemy import desc
from models import *
import datetime

session = DBSession()


# 存入ip
def create_proxy(**kwargs):
    try:
        session.add(Proxy(ip=kwargs['ip'], port=kwargs['port'], code=kwargs['code'], country=kwargs['country'],
                          anonymity=kwargs['anonymity'], https=kwargs['https']))
        session.flush()
    except Exception as e:
        session.rollback()


# 取出所有ip
def get_ip():
    iplist = []
    i = session.query(Proxy.ip, Proxy.port).all()
    for _ in i:
        iplist.append(str(_[0]) + ':' + str(_[1]))
    return iplist


# 删除ip
def del_ip(ip):
    try:
        i = session.query(Proxy).filter_by(ip=ip).first()
        session.delete(i)
        session.flush()
    except:
        session.rollback()


# 随机选择一个代理
def random_ip():
    ip = session.query(Proxy.ip, Proxy.port).order_by(func.random()).first()
    return ip[0] + ':' + ip[1]


def random_overseas_ip():
    ip = session.query(Proxy.ip, Proxy.port).filter(Proxy.country != 'China').order_by(func.random()).first()
    return ip[0] + ':' + ip[1]


if __name__ == '__main__':
    import time
    # a = random_ip()
    start = time.time()
    a = random_overseas_ip()
    print(a)
    end = time.time()
    print('Cost time:', end - start)


    """
    0.06
    """



