#coding:utf-8
import logging.handlers
import os.path

'''
logger 日志初始化
'''
logger = logging.getLogger(__file__ + ".log")
#loggerPath = os.path.join(os.path.dirname(os.getcwd()),"log")
loggerPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"logs")
if not os.path.exists(loggerPath):
    os.makedirs(loggerPath)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s %(levelno)s %(filename)s [%(lineno)d]: %(message)s")  ## s 表示字符串类型，d 表示数值类型

#  backupCount :  If backupCount is > 0, when rollover is done, no more than backupCount files are kept - the oldest ones are deleted.
## when = 'd' 或者 'midnight'  ，都是表示文件按天生成，文件命名的方式是Y-m-d
rf_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(loggerPath,"all.log"), when='midnight', interval=1, backupCount=30, encoding="utf8" )
rf_handler.setFormatter(fmt)

err_handle = logging.FileHandler(os.path.join(loggerPath,'error.log'))
err_handle.setLevel(logging.ERROR)
err_handle.setFormatter(fmt)


## 添加handler

logger.addHandler(rf_handler)
logger.addHandler(err_handle)


# logger.debug('test debug')
# logger.error('error now')
# logger.info('info msg')
# logger.warning("warning info")
# logger.critical('critical info',exc_info = 1)



