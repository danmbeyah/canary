import json
from kafka import KafkaConsumer

# Configure the consumer
# The value_deserializer decodes the JSON byte string back into a dictionary
consumer = KafkaConsumer(
    'iot-device-data', # The topic to subscribe to
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', # Start reading at the earliest message
    group_id='iot-monitor-group', # Consumer group ID
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening for messages on topic 'iot-device-data'...")

# Poll for new messages
for message in consumer:
    print(f"Received message: {message.value}")
    # Example output:
    # Received message: {'sensor_id': 'temp-sensor-102', 'location': 'greenhouse-3', 'reading': {'temperature': 24.5, 'humidity': 68.2}, 'timestamp': '2025-10-18T17:35:00Z'}