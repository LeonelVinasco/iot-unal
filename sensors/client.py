import pika
import json

def callback(ch, method, properties, body):
    print("Method: {}".format(method))
    print("Properties: {}".format(properties))

    data = json.loads(body)
    print("Humedad: {}".format(data['humedad']))
    print("Temperatura: {}".format(data['temperatura']))
    print('Presion: {}'.format(data['presion']))

if __name__ == '__main__': 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.queue_declare(queue="queue")
    channel.basic_consume(callback, queue="queue",no_ack=True)
    channel.start_consuming()
    connection.close()

