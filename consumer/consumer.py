import logging
import asyncio
from json import loads
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama
from typing import AsyncIterator
import base64
# Asynchronous stream function for tokens
async def data_stream(content):
    llm = model  # Assuming 'model' is defined

    run_response: AsyncIterator[RunResponse] = llm.run(content, stream=True)
    
    try:
        for response in run_response:
            if isinstance(response, RunResponse):
                # Extract the content from the RunResponse object
                response_content = response.content
                

                    # If the content is not a string, handle appropriately, e.g., if it's bytes
                yield response_content
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        print("Stream success")

# The function that sends the stream of messages to Kafka
async def send_stream_of_messages(content, key):
    # Initialize the Kafka producer
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:29092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: str(k).encode('utf-8')  # Serialize the key
    )

    # Start the producer
    await producer.start()

    try:
        # Get the token stream from data_stream
        async for token in data_stream(content):
            # Send each token as a message to the Kafka topic 'response'
            await producer.send_and_wait('response', value={'token': token}, key=key)
            logging.info(f"Sent token: {token}")  # Logging for debugging

    except Exception as e:
        logging.error(f"Error sending messages: {e}")
    finally:
        # Stop the producer gracefully
        await producer.stop()

# Function to consume messages from Kafka
async def consume_messages():
    # Initialize the consumer
    consumer = AIOKafkaConsumer(
        'hello',  # Topic to consume from
        bootstrap_servers='kafka:29092',
        value_deserializer=lambda x: loads(x.decode('utf-8')),  # Deserialize JSON values
        enable_auto_commit=False,  # Disable auto commit to manually commit offsets
        max_poll_records=100  # Maximum number of records to fetch in a single poll
    )

    # Start the consumer
    await consumer.start()

    try:
        # Consume messages
        async for message in consumer:
            print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")
            # Decode the key if present
            id = message.key.decode() if message.key else None
            print("ID: ", id)
            
            
            # Call send_stream_of_messages to process tokens
            await send_stream_of_messages(message.value, id)

            # Manually commit the offset after processing the message
            # await consumer.commit()
            logging.info(f"Committed offset {message.offset + 1} for partition {message.partition}")
    except Exception as e:
        logging.error(f"Error consuming message: {e}")
    finally:
        # Stop the consumer gracefully
        await consumer.stop()

if __name__ == '__main__':
    model = Agent(model=Ollama(id="llama3.2:1b", host="http://ollama:11434"))
    model.print_response("Hello world")
    
    try:
        asyncio.run(consume_messages())
    except Exception as e:
        logging.error(f'Connection failed: {e}')
