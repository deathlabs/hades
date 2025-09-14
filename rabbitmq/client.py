import pika

try:
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost", port=5672,
            credentials=pika.PlainCredentials("hades", "hades"),
            virtual_host="/"
        )
    )
    print("✅ Connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

