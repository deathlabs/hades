import pika

try:
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost", port=5672,
            credentials=pika.PlainCredentials(username="hades", password="hades"),
            virtual_host="/"
        )
    )
    print("[+] Connected successfully!")
    conn.close()
except Exception as error:
    print("[x] Connection failed:", error)
