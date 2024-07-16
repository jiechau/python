import pandas as pd
import sqlalchemy
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
    engine = sqlalchemy.create_engine(myconfig['Database_connection']['postgresql'], pool_size=5, max_overflow=0)
    conn = engine.connect()
    sql = "select * from logschema.b_control"
    try:
        df = pd.read_sql(sql, conn)
        print(df)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        engine.dispose()
