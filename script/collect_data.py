# coding: utf-8
'''
 通过接口获取股票数据
'''
from time import sleep
import sys
sys.path.append("..")

from script.mysql_util import insert


def checkTransactionTime():
    '''
    判断当前时间是否在交易时间段内(上午9:30--11:30  下午 13:00 -- 15:00。周六周日不交易)
    :return:  True : 正常交易时间  False: 非正常交易时间
    '''
    import datetime
    dt = datetime.datetime.now()
    if dt.weekday() > 5:
        return False
    strTime = dt.time().strftime('%H:%M')
    if ( '09:30' <= strTime <= '11:30') or ( '13:00' <= strTime <= '15:00'):
        return True
    else:
        return False


def loadAPIData(stockCode='sh601808'):
    import urllib3
    ## 只获取交易时间段内的数据
    if not checkTransactionTime(): return
    url = "http://hq.sinajs.cn/list=" + stockCode.lower()
    manager = urllib3.PoolManager(num_pools=10)
    response = manager.urlopen('GET',url)
    content = []
    if response.status == 200:
        data = str(response.data , encoding='gbk')
        result = data[data.index("=") + 2 : -6]
        if result:
            fields = result.split(",")
            content.append(stockCode)
            content.append(fields[0])
            content.append(fields[-2])
            content.append(fields[-1])
            content.extend(fields[1:-2])
    return content



if __name__ == '__main__':
    while True:
        data = loadAPIData()
        insert(data)
        sleep(60)


