from lib import filter
from lib import get
from lib import market

stock_ids = "603160,002156,002178"

if __name__ == '__main__':
    print("自选列表")
    for stock_id in stock_ids.split(','):
        print(get.get_by_id(stock_id))

    for date, data_map in filter.fund_filter(change_f=3, big_diff_f=4).items():
        print("候选列表: " + date + " " + str(len(data_map)))
        print('\n'.join([str(item) for item in data_map]))

    market_fund = market.market_his()[0]
    print("大盘资金: " + market_fund['日期'])
    print(market_fund)

    for date, data_map in filter.limit_up_filter().items():
        print("涨停板列表: " + date + " " + str(len(data_map)))
        print('\n'.join([str(item) for item in data_map]))
