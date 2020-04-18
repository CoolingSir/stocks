from lib import get

if __name__ == '__main__':
    for i in get.get_his("600268", stock_name="国电南自", partition_f=2, last_days=5):
        print(i)
