from lib import constants as C
from lib import get


def fund_filter(last_days=C.DEFAULT_ONE_DAY, partition_f=C.DEFAULT_PARTITION, change_f=C.DEFAULT_CHANGE,
                net_buy_f=C.DEFAULT_NET_BUY, total_big_buy_f=C.DEFAULT_TOTAL_BIG_BUY,
                total_big_tran_f=C.DEFAULT_TOTAL_BIG_TRAN, big_diff_f=C.DEFAULT_BIG_DIFF):
    his_data = get.load_his(last_days, partition_f)
    for date_key, per_data in his_data.items():
        his_data[date_key] = list(filter(
            lambda stock: stock['换手'] >= change_f and stock['大单净买'] >= net_buy_f and stock[
                '大单买入占比'] >= total_big_buy_f and stock['特大买入'] - stock['大单买入'] >= big_diff_f and stock[
                              '大单交易占比'] >= total_big_tran_f, per_data))
        his_data[date_key].sort(key=lambda k: (k.get('大单净买', 0)), reverse=True)
    return his_data


def limit_up_filter(last_days=C.DEFAULT_ONE_DAY, partition_f=C.DEFAULT_PARTITION, is_include_st=False, sort_key='大单净买'):
    his_data = get.load_his(last_days, partition_f)
    for date_key, per_data in his_data.items():
        his_data[date_key] = list(
            filter(lambda stock: stock['涨停'] and (is_include_st or not stock['ST']), per_data))
        his_data[date_key].sort(key=lambda k: (k.get(sort_key, 0)), reverse=True)
    return his_data


if __name__ == '__main__':
    for date, data_map in fund_filter(partition_f=2).items():
        print(date + ": " + str(len(data_map)))
        print('\n'.join([str(item) for item in data_map]))
