import math
import os
from decimal import Decimal, InvalidOperation

import pandas as pd

from lib import constants as C


def get_by_id(stock_id, date_f=None, partition_f=C.DEFAULT_PARTITION):
    target_date = date_f
    if date_f is None:
        files = os.listdir(C.SRC_PATH)
        files.sort(reverse=True)
        target_date = files[0][0:-8]
        total_data = load_data(files[0][0:-8], int(files[0][-7]))
    else:
        total_data = load_data(date_f, partition_f)
    stock_res = {'日期': target_date}
    stock_res.update(get_from_data(total_data, stock_id))
    return stock_res


def get_his(stock_id, stock_name="", last_days=C.DEFAULT_HISTORY_DAYS, partition_f=C.DEFAULT_PARTITION):
    day_count = 1
    stock_his = []
    files = os.listdir(C.SRC_PATH)
    files.sort(reverse=True)
    for f in files:
        if f[-7] == str(partition_f) and f[-5] == '1' and day_count <= last_days:
            day_count += 1
            stock_his.append({'日期': f[0:-8],
                              '数据': get_from_data(load_data(date_f=f[0:-8], partition_f=partition_f), stock_id,
                                                  stock_name=stock_name)})
    return stock_his


def load_data(date_f=C.DEFAULT_DATE, partition_f=C.DEFAULT_PARTITION):
    base_path = C.SRC_PATH + date_f + '-' + str(partition_f) + '-1.xls'
    dde_path = C.SRC_PATH + date_f + '-' + str(partition_f) + '-2.xls'

    base_data = pd.read_csv(base_path, encoding='gbk', delimiter='\t')
    dde_data = pd.read_csv(dde_path, encoding='gbk', delimiter='\t')

    total = pd.merge(base_data, dde_data, on='代码')
    return total


def load_his(last_days=C.DEFAULT_ONE_DAY, partition_f=C.DEFAULT_PARTITION):
    day_count = 1
    his_data = {}
    files = os.listdir(C.SRC_PATH)
    files.sort(reverse=True)
    for f in files:
        if f[-7] == str(partition_f) and f[-5] == '1' and day_count <= last_days:
            day_count += 1
            format_stock_list = []
            total = load_data(f[0:-8], partition_f)
            for index, row in total.iterrows():
                try:
                    format_stock_list.append(format_row(row))
                except InvalidOperation:
                    pass
                continue
            his_data[f[0:-6]] = format_stock_list
    return his_data


def get_from_data(current_data, stock_id, stock_name=""):
    for index, row in current_data.iterrows():
        try:
            if stock_id in str(row['代码']) or (stock_name != "" and stock_name in str(row['名称_x'])):
                return format_row(row)
        except ValueError:
            pass
        continue


def format_row(row):
    stock_info = {'代码': "".join(filter(str.isdigit, str(row['代码']))), '名称': str(row['名称_x'])}

    large_buy = Decimal(row['特大买入%'])
    big_buy = Decimal(row['大单买入%'])
    large_sell = Decimal(row['特大卖出%'])
    big_sell = Decimal(row['大单卖出%'])
    total_big_sell = large_sell + big_sell
    total_big_buy = large_buy + big_buy
    total_small_sell = Decimal('100') - total_big_sell
    total_small_buy = Decimal('100') - total_big_buy
    total_big_tran = total_big_buy + total_big_sell
    total_small_tran = total_small_sell + total_small_buy
    net_buy = Decimal(row['特大单净比%']) + Decimal(row['大单净比%'])
    stock_info.update({
        '涨幅': Decimal(row['涨幅%_x']),
        '换手': Decimal(row['换手%']),
        '大单净买': net_buy,
        '大单交易占比': total_big_tran,
        '大单买入占比': total_big_buy,
        '大单卖出占比': total_big_sell,
        '小单交易占比': total_small_tran,
        '小单买入占比': total_small_buy,
        '小单卖出占比': total_small_sell,
        '特大买入': large_buy,
        '大单买入': big_buy
    })

    stock_info['ST'] = True if 'ST' in stock_info['名称'] else False
    stock_info['科创板'] = True if str(stock_info['代码']).startswith('688') else False

    current_price = Decimal(row['最新_x'])
    yesterday_price = Decimal(row['昨收'])
    limit_ratio = Decimal('0.05') if stock_info['ST'] else Decimal('0.2') if stock_info['科创板'] else Decimal('0.1')

    stock_info['涨停'] = True if str(
        current_price.compare(round_util(yesterday_price * (Decimal('1') + limit_ratio)))) == '0' else False
    stock_info['跌停'] = True if str(
        current_price.compare(round_util(yesterday_price * (Decimal('1') - limit_ratio)))) == '0' else False
    return stock_info


def round_util(n, decimals=Decimal('2')):
    multiplier = Decimal('10') ** decimals
    return math.floor(n * multiplier + Decimal('0.5')) / multiplier
