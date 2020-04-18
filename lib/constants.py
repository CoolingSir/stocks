import time

SRC_PATH = 'D:\\Stocks\\history\\stock\\'
DEFAULT_DATE = time.strftime("%Y-%m-%d", time.localtime())
DEFAULT_PARTITION = 1 if int(time.strftime("%H", time.localtime())) < 13 else 2

DEFAULT_CHANGE = 3
DEFAULT_NET_BUY = 15
DEFAULT_TOTAL_BIG_BUY = 50
DEFAULT_TOTAL_BIG_TRAN = 80
DEFAULT_BIG_DIFF = 5

DEFAULT_ONE_DAY = 1
DEFAULT_HISTORY_DAYS = 10
