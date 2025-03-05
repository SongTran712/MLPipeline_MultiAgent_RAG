import asyncio
import json
from aiokafka import AIOKafkaProducer


async def send_stream_of_messages(message ,id ):
    # Initialize the producer
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize value to JSON
        key_serializer=lambda k: str(k).encode('utf-8')  # Serialize key to string (ensure it's bytes)
    )

    # Start the producer
    await producer.start()

    try:
        # Send a stream of messages
        # for i in range(1, 11):  # Change range for how many messages you want to send
        #     message = {"key": f"value{i}", "message": f"Hello, Kafka! This is message number {i}"}
        
        await producer.send_and_wait('hello', value=message, key=id)
        print(f"Message sent successfully with key: {id} and value: {message}")
            # print(f"Sent message {i}")

    except Exception as e:
        print(f"Error sending messages: {e}")
    finally:
        # Stop the producer gracefully
        await producer.stop()

# Run the asyncio event loop
if __name__ == '__main__':
    asyncio.run(send_stream_of_messages("123"))
