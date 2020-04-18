from lib import filter

if __name__ == '__main__':
    for date, data_map in filter.fund_filter(last_days=10, partition_f=1, change_f=4, big_diff_f=5).items():
        print(date + ": " + str(len(data_map)))
        print('\n'.join([str(item) for item in data_map]))
