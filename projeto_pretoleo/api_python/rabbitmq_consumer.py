import pika

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='logistica')

    def callback(ch, method, properties, body):
        print("[RabbitMQ] Mensagem recebida:", body.decode())

    channel.basic_consume(queue='logistica', on_message_callback=callback, auto_ack=True)
    print("Esperando mensagens da fila 'logistica'...")
    channel.start_consuming()
