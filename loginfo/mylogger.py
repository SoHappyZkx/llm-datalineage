from datetime import datetime
from os import path,makedirs
from sys import stdout
from loguru import logger

class MyLogger(object):
    def __init__(self,log_name,level="INFO",dir_path='.logs') -> logger:
        logger.remove()
        fmt = '<level>{time:YYYY-MM-DD HH:mm:ss} | 【{level}】<{module}>@<{function}> | {message}</level>'
        logger.add(stdout,format=fmt)
        self.my_logger = logger
        _today = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        #判断是否当前目录下存在文件夹，如果不存在则创建一个
        if not path.exists(dir_path):
            makedirs(dir_path)
        log_path = f"{dir_path}/{log_name}{_today}.log"
        self.name = path.basename(log_path)
        self.my_logger.add(
            log_path,encoding="utf-8",
            retention='7 days',
            rotation="50 MB",
            compression='zip',
            format=fmt,
            enqueue=True,
            level=level)
    def info(self,content):
        self.my_logger.opt(depth=1).info(content)
    def debug(self,content):
        self.my_logger.opt(depth=1).debug(content)  
    def error(self,content,*args,**kwargs):
        self.my_logger.opt(depth=1).error(content)
        if len(args)>0 or len(kwargs)>0:
            self.exception("Error details:"*args,**kwargs)
    def exception(self,content,*args,**kwargs):
        self.my_logger.opt(depth=1).exception(content,*args,**kwargs)
    def warning(self,content):
        self.my_logger.opt(depth=1).warning(content)
        
def test1():
    mylogger=MyLogger("TEST")
    mylogger.debug("这个是在调试")
    mylogger.info("这个信息没问题")
    mylogger.warning("这可能存在风险")
    mylogger.error("这是个错误！")

    try:
        result = 1/0
    except Exception as e:
        mylogger.exception("这是一个异常",e)
if __name__ == "__main__":
    test1()