from lib import filter

for date, data_map in filter.limit_up_filter(last_days=1, partition_f=2).items():
    print(date + ": " + str(len(data_map)))
    print('\n'.join([str(item) for item in data_map]))
