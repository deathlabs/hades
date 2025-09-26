import pika

def callback(ch, method, properties, body):
    print(f"[+] {method.exchange} [{method.routing_key}]: {body.decode()}")

try:
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            credentials=pika.PlainCredentials(username="hades", password="hades"),
            virtual_host="/"
        )
    )
    print("[+] Connected successfully!")
    channel = conn.channel()
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    exchanges = ["amq.topic", "hades.inject.requests", "hades.inject.reports"]
    for exch in exchanges:
        if not exch.startswith("amq."):
            channel.exchange_declare(exchange=exch, exchange_type="topic", durable=False)
        channel.queue_bind(exchange=exch, queue=queue_name, routing_key="#")
    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

except Exception as error:
    print("[x] Connection failed:", error)
