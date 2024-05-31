import pandas as pd
import cx_Oracle
import yaml
import os

#%% myconfig
def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml 
    with open(_myconfig_file, 'r') as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig

#%% bo
def get_conn_oracle():
    myconfig = get_myconfig('config/config.yml')
    _boseg_connection_string = myconfig['Database_connection']['oracle_ecuat2']
    _conn_boseg = cx_Oracle.connect(_boseg_connection_string, encoding='UTF-8', nencoding='UTF-8')
    _cur_boseg = _conn_boseg.cursor()
    return [_conn_boseg, _cur_boseg]
def get_close_oracle(_conn_boseg, _cur_boseg):
    _conn_boseg.commit()
    _cur_boseg.close()
    _conn_boseg.close()

#%% main
if __name__ == '__main__':

    [conn_boseg, cur_boseg] = get_conn_oracle()
    # bo
    sql = "select * from ec_apuser.cdc_test WHERE a_str='jie-cdc-test'"
    df = pd.read_sql(sql, con=conn_boseg)
    print(df.head(5))
    # close it
    get_close_oracle(conn_boseg, cur_boseg)



