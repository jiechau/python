import pandas as pd
import redis
import yaml

#%% myconfig
def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml 
    with open(_myconfig_file, 'r') as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig

#%% main
if __name__ == "__main__":
    myconfig = get_myconfig('config/config.yml')
    redis_url = myconfig['Redis']['host']
    redis_port = myconfig['Redis']['port']
    redis_password = myconfig['Redis']['password']
    key = '/ktop/main'

    # 連接到 Redis
    client = redis.StrictRedis(
        host=redis_url,
        port=redis_port,
        password=redis_password,
        decode_responses=True  # 這個參數確保返回的數據是字符串
    )

    try:
        value = client.get(key)
        df = pd.read_json(value, orient='records')
        print(df.head(5))
    finally:
        client.connection_pool.disconnect()

