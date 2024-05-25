import pandas as pd
import psycopg2
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
    postgresql = myconfig['Database_connection']['postgresql']
    conn = psycopg2.connect(postgresql)
    sql = "select * from logschema.b_control"
    try:
        df = pd.read_sql(sql, conn)
        print(df)
    except Exception as e:
        print(e)
    finally:
        conn.close()
