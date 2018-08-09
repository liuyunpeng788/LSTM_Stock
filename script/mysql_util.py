#coding: utf-8
'''
数据库操作
'''
import sys
sys.path.append("..")
from DBUtils.PersistentDB import PersistentDB
import pymysql
from script.logger import logger

PooL = PersistentDB(
    creator = pymysql,  #使用链接数据库的模块
    maxusage = None, #一个链接最多被使用的次数，None表示无限制
    setsession = [], #开始会话前执行的命令
    ping = 0, #ping MySQL服务端,检查服务是否可用
    closeable = False, #conn.close()实际上被忽略，供下次使用，直到线程关闭，自动关闭链接，而等于True时，conn.close()真的被关闭
    threadlocal = None, # 本线程独享值的对象，用于保存链接对象
    host = '10.151.2.101',
    port = 3306,
    user = 'root',
    password = 'Fosun#1234',
    database = 'liumch_test',
    charset = 'utf8'
)

def insert(data):
    if not data or len(data) == 0: return
    try:
        conn = PooL.connection()
        cursor = conn.cursor()
        sql = "insert into stock_data values(null,"  ## 因为第一个字段为自增的id,所以此处设置为null,否则会报字段数不对的问题
        for index, value in enumerate(data):
            if index < 4:
                sql += "'" + value + "',"
            else:
                sql += value + ","
        sql = sql[:-1] + ");"
        logger.info(sql)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    except :
        logger.error('insert data into mysql exception' ,exc_info = 1)

