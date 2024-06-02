
# rabbitmq producer
# AMQP
#
# setup server
# https://www.rabbitmq.com/install-rpm.html
# or
# https://www.rabbitmq.com/kubernetes/operator/operator-overview.html

import pika
import json
import time
import random


#%% myconfig
def get_myconfig(_myconfig_file):
    ## read custom params from config.yaml 
    with open(_myconfig_file, 'r') as stream:
        _myconfig = yaml.load(stream, Loader=yaml.CLoader)
    return _myconfig

# consumer
def callback(ch, method, properties, body):
    data = json.loads(body)
    #print(f"Received number: {data['age']}. name: {data['first name']}. addr: {data['addr']}.")
    print(data)
    #time.sleep(1)

#%% main
if __name__ == '__main__':

    myconfig = get_myconfig('config/config.yml')
    ip_address = myconfig['RabbitMQ']['ip_address']
    port_number = myconfig['RabbitMQ']['port_number']
    username = myconfig['RabbitMQ']['username']
    password = myconfig['RabbitMQ']['password']
    credentials = pika.PlainCredentials(username, password) 
    connection_parameters = pika.ConnectionParameters(ip_address, 
      port_number, 
      '/', 
      credentials,
      socket_timeout=1)

    # producer
    try:
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        channel.queue_declare(queue='/topic/test/test0') # 這個名字可以自己取
        data = {'age': 30, 'first name': 'jie', 'addr': 'taipei'}
        #json_bytes = json.dumps(data).encode('utf-8') 
        json_bytes = json.dumps(data)
        channel.basic_publish(exchange='',
                          routing_key='/topic/test/test0',
                          body=json_bytes)
        channel.close()
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print('ttt')
        channel.close()
        connection.close()
    except Exception as e:
        print('sss')
        channel.close()
        connection.close()
    except KeyboardInterrupt as e:
        print('sss')
        channel.close()
        connection.close()

    # comsumer
    try:
      connection = pika.BlockingConnection(connection_parameters)
      channel = connection.channel()
      # 確認隊列存在
      channel.queue_declare(queue='/topic/test/test0') # topic 自己取
      channel.basic_consume(queue='/topic/test/test0', on_message_callback=callback, auto_ack=True)
      print(' [*] Waiting for messages. To exit press CTRL+C')
      channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        print('ttt')
        channel.close()
        connection.close()
    except Exception as e:
        print('sss')
        channel.close()
        connection.close()
    except KeyboardInterrupt as e:
        print('sss')
        channel.close()
        connection.close()