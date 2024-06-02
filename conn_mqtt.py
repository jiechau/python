'''
# start ther server by:
docker run -it -p 1883:1883 -p 9001:9001 -v ${PWD}/mosquitto-no-auth.conf:/mosquitto-no-auth.conf eclipse-mosquitto mosquitto -c /mosquitto-no-auth.conf

# but the content of ${PWD}/mosquitto-no-auth.conf is:

# Allow connections from any IP address
listener 1883
allow_anonymous true # this line is important

'''
import time
import random
import paho.mqtt.client as mqtt
import yaml
import threading

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

# Consumer function to run in a separate thread
def run_consumer(mqtt_broker, mqtt_port, mqtt_topic):
    client = mqtt.Client(client_id="consumer-2", clean_session=False) # client_id 請自己取自己的
    client.on_connect = on_connect_consumer
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port)
    client.loop_forever()

#%% main
if __name__ == '__main__':
    myconfig = get_myconfig('config/config.yml')
    mqtt_broker = myconfig['Mqtt']['mqtt_broker']
    mqtt_port = myconfig['Mqtt']['mqtt_port']

    mqtt_topic = "/topic/test/test1" # topic 自己取

    # Start the consumer thread
    consumer_thread = threading.Thread(target=run_consumer, args=(mqtt_broker, mqtt_port, mqtt_topic))
    consumer_thread.daemon = True
    consumer_thread.start()

    # Producer part
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    client.loop_start()

    try:
        while True:
            number = random.randint(1, 100)
            client.publish(mqtt_topic, str(number), qos=2)
            print(f"Published: {number}")
            time.sleep(1)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
    finally:
        client.disconnect()
        client.loop_stop()

