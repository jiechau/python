from confluent_kafka import Consumer, KafkaException, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
import json
import yaml

#%% myconfig
def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml 
    with open(_myconfig_file, 'r') as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig

#%% main
if __name__ == '__main__':

    myconfig = get_myconfig('config/config.yml')
    bootstrap_servers = myconfig['KafkaCDC']['bootstrap_servers']
    schema_registry_url = myconfig['KafkaCDC']['schema_registry_url']

    # Kafka consumer configuration
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'jie',
        'auto.offset.reset': 'earliest',
        'schema.registry.url': schema_registry_url
    }

    # Initialize Schema Registry client
    schema_registry_client = SchemaRegistryClient({'url': conf['schema.registry.url']})

    # Get the schema for the value (you can adjust the subject name as needed)
    key_schema_str = schema_registry_client.get_latest_version('oracle-cdc-uat2-avro.EC_APUSER.CDC_TEST-key').schema.schema_str
    value_schema_str = schema_registry_client.get_latest_version('oracle-cdc-uat2-avro.EC_APUSER.CDC_TEST-value').schema.schema_str
    key_deserializer = AvroDeserializer(schema_str=key_schema_str, schema_registry_client=schema_registry_client)
    value_deserializer = AvroDeserializer(schema_str=value_schema_str, schema_registry_client=schema_registry_client)

    # Initialize the Kafka Consumer
    consumer = Consumer({
        'bootstrap.servers': conf['bootstrap.servers'],
        'group.id': conf['group.id'],
        'auto.offset.reset': conf['auto.offset.reset']
    })

    consumer.subscribe(['oracle-cdc-uat2-avro.EC_APUSER.CDC_TEST'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    raise KafkaException(msg.error())
            #key = msg.key() if msg.key() else None
            key = key_deserializer(msg.key(), None)
            value = value_deserializer(msg.value(), None)
            print(f"Key: {key}, Value: {value}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
