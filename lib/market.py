import os
from decimal import *
from lib import util

import pandas as pd

from lib import constants as C


def load_fund(fund_path):
    fund_data = pd.read_csv(fund_path, encoding='gbk', delimiter='\t')
    return fund_data


def fund_format(fund_data):
    fund_data_fmt = []
    for index, row in fund_data.iterrows():
        try:
            stock_fund = {
                '代码': "".join(filter(str.isdigit, str(row['代码']))),
                '名称': str(row['名称']),
                '最新': Decimal(row['最新']),
                '超大单流入': unit_format(str(row['超大单流入']).strip()),
                '超大单流出': unit_format(str(row['超大单流出']).strip()),
                '大单流入': unit_format(str(row['大单流入']).strip()),
                '大单流出': unit_format(str(row['大单流出']).strip()),
                '中单流入': unit_format(str(row['中单流入']).strip()),
                '中单流出': unit_format(str(row['中单流出']).strip()),
                '小单流入': unit_format(str(row['小单流入']).strip()),
                '小单流出': unit_format(str(row['小单流出']).strip())
            }
            fund_data_fmt.append(stock_fund)
        except InvalidOperation:
            pass
        continue
    return fund_data_fmt


def unit_format(fund_str):
    if fund_str[-1] == '亿':
        fund_flt = Decimal(fund_str[0:-1]) * Decimal('100000000')
    elif fund_str[-1] == '万':
        fund_flt = Decimal(fund_str[0:-1]) * Decimal('10000')
    else:
        fund_flt = Decimal(fund_str[0:-1])
    return fund_flt


def market_statistics(fund_data_fmt):
    large_buy, big_buy, mid_buy, small_buy, total_buy = Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'), Decimal(
        '0')
    for stock_fund in fund_data_fmt:
        large_buy += stock_fund['超大单流入']
        big_buy += stock_fund['大单流入']
        mid_buy += stock_fund['中单流入']
        small_buy += stock_fund['小单流入']
    total_buy = large_buy + big_buy + mid_buy + small_buy

    large_sell, big_sell, mid_sell, small_sell, total_sell = Decimal('0'), Decimal('0'), Decimal('0'), Decimal(
        '0'), Decimal('0')
    for stock_fund in fund_data_fmt:
        large_sell += stock_fund['超大单流出']
        big_sell += stock_fund['大单流出']
        mid_sell += stock_fund['中单流出']
        small_sell += stock_fund['小单流出']
    total_sell = large_sell + big_sell + mid_sell + small_sell

    market_fund = {
        '大单净比': util.round_util((large_buy + big_buy) / total_buy * Decimal('100') - (large_sell + big_sell) / total_sell * Decimal('100')),
        '大单总买': util.round_util((large_buy + big_buy) / total_buy * Decimal('100')),
        '大单总卖': util.round_util((large_sell + big_sell) / total_sell * Decimal('100')),
        '小单总买': util.round_util((mid_buy + small_buy) / total_buy * Decimal('100')),
        '小单总卖': util.round_util((mid_sell + small_sell) / total_sell * Decimal('100')),
        '超大单买': util.round_util(large_buy / total_buy * Decimal('100')),
        '大单买': util.round_util(big_buy / total_buy * Decimal('100')),
        '中单买': util.round_util(mid_buy / total_buy * Decimal('100')),
        '小单买': util.round_util(small_buy / total_buy * Decimal('100')),
        '超大单卖': util.round_util(large_sell / total_sell * Decimal('100')),
        '大单卖': util.round_util(big_sell / total_sell * Decimal('100')),
        '中单卖': util.round_util(mid_sell / total_sell * Decimal('100')),
        '小单卖': util.round_util(small_sell / total_sell * Decimal('100')),
        '总买': total_buy,
        '超大单流入': large_buy,
        '大单流入': big_buy,
        '中单流入': mid_buy,
        '小单流入': small_buy,
        '总卖': total_sell,
        '超大单流出': large_sell,
        '大单流出': big_sell,
        '中单流出': mid_sell,
        '小单流出': small_sell
    }
    return market_fund


def market_his(last_days=C.DEFAULT_ONE_DAY, partition_f=C.DEFAULT_PARTITION):
    market_fund_list = []
    files = os.listdir(C.SRC_PATH)
    files.sort(reverse=True)
    fund_files = [f for f in files if (f[-7] == str(partition_f) and f[-5] == '3')][0:last_days]
    for f in fund_files:
        per_market_fund = {'日期': f[0:-8]}
        per_market_fund.update(market_statistics(fund_format(load_fund(C.SRC_PATH + f))))
        market_fund_list.append(per_market_fund)
    return market_fund_list


if __name__ == '__main__':
    for i in market_his(10):
        print(i)
