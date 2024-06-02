#
# how to cached 
# https://iot.stackexchange.com/questions/4010/are-mqtt-brokers-able-to-retain-cache-some-data-for-a-certain-amount-of-time-and
#

import time
import random
import paho.mqtt.client as mqtt
import yaml

#%% myconfig
def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml 
    with open(_myconfig_file, 'r') as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Connection to MQTT Broker failed")


def on_connect_consumer(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(mqtt_topic, qos=2) 
    else:
        print("Connection to MQTT Broker failed")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    #time.sleep(2)

#%% main
if __name__ == '__main__':

    myconfig = get_myconfig('config/config.yml')
    mqtt_broker = myconfig['Mqtt']['mqtt_broker']
    mqtt_port = myconfig['Mqtt']['mqtt_port']

    mqtt_topic = "/topic/test/test1" # topic 自己取
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    client.loop_start()

    try:
        number = 1
        client.publish(mqtt_topic, str(number), qos=2) # this
        print(f"Published: {number}")
        time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
    finally:
        client.disconnect()
        client.loop_stop()


    #client = mqtt.Client() # 這樣才能 cached: client_id="consumer-1", clean_session=False
    mqtt_topic = "/topic/test/test1" # topic 自己取
    client = mqtt.Client(client_id="consumer-2", clean_session=False) # client_id 請自己取自己的
    client.on_connect = on_connect_consumer
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port)

    #client.loop_forever()
    while True:
    # 等待 MQTT server 發送訊息
    client.loop()
