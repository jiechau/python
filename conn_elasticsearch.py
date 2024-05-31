import yaml
from elasticsearch import Elasticsearch

def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml
    with open(_myconfig_file, 'r', encoding="utf-8") as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig


if __name__ == '__main__':

    myconfig = get_myconfig("config/config.yml")
    es_url_dev = myconfig['elasticsearch']['url_dev']
    es_key_dev = myconfig['elasticsearch']['api_key_dev']
    es = Elasticsearch(es_url_dev, api_key=(es_key_dev))

    query = {"match_all": {}}
    sort = { '@timestamp' : 'desc' }
    size = 5
    json_res = es.search(index='nginx_access_'  + '01' +  '*', query=query, sort=sort, size=size)
    original_dt_str = json_res["hits"]["hits"][0]["_source"]['@timestamp']
    print(original_dt_str)
 




