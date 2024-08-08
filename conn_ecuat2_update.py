# docker run -it --rm -v $HOME/ai_codes/fastapi-vm/service/config/config.yml:/app/config/config.yml jiechau/python
# while true; do echo $(date +'%Y/%m/%d %H:%M:%S') $(p conn_ecuat2_update.py); sleep 30; done

import pandas as pd
import cx_Oracle
import yaml
import os
import random

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
    # check existed first
    select_query = "SELECT COUNT(*) FROM ec_apuser.cdc_test WHERE a_str = 'jie-cdc-test'"
    insert_query = "INSERT INTO ec_apuser.cdc_test (id, a_str) VALUES (99, 'jie-cdc-test')"
    cur_boseg.execute(select_query)
    row_count = cur_boseg.fetchone()[0]
    if row_count < 1:
        print('< 1')
        cur_boseg.execute(insert_query)
        conn_boseg.commit()
    # random update
    random_number = random.randint(1000, 9999)
    print(str(random_number), 'ecuat2 set')
    update_query = "UPDATE ec_apuser.cdc_test SET a_v_str = '" + str(random_number) + "' WHERE a_str = 'jie-cdc-test'"    cur_boseg.execute(update_query)
    conn_boseg.commit()
    # close it
    get_close_oracle(conn_boseg, cur_boseg)

    # docker run --network host -it --rm -v $HOME/ai_codes/fastapi-vm/service/config/config.yml:/app/config/config.yml jiechau/python
    # while true; do echo $(date +'%Y/%m/%d %H:%M:%S') $(p -W ignore conn_postgresql.py); echo $(date +'%Y/%m/%d %H:%M:%S') $(p -W ignore conn_ecuat2_update.py); sleep 60; done
    
