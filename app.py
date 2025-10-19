import json
from flask import Flask, request, jsonify
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Initialize Flask app
app = Flask(__name__)

# --- Kafka Producer Configuration ---
# This configuration assumes Kafka is running on localhost:9092.
# The value_serializer lambda function serializes dictionary data to a 
JSON formatted byte string.
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except KafkaError as e:
    print(f"Error connecting to Kafka: {e}")
    # In a real app, you might want to handle this more gracefully
    # For this example, we'll exit if we can't connect.
    producer = None

# --- API Endpoint Definition ---
@app.route('/api/iot', methods=['POST'])
def publish_iot_data():
    """
    Receives JSON data from an IoT device and publishes it to a Kafka 
topic.
    """
    if not producer:
        return jsonify({"status": "error", "message": "Kafka producer not 
available"}), 503

    # Get the JSON data from the request body
    try:
        iot_data = request.get_json()
        if not iot_data:
            return jsonify({"status": "error", "message": "No data 
provided in request"}), 400
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON 
format"}), 400

    # Define the Kafka topic to publish to
    kafka_topic = 'iot-device-data'

    try:
        # Send the data to the Kafka topic
        # The .get(timeout=10) call blocks until the message is sent or 
times out
        future = producer.send(kafka_topic, value=iot_data)
        record_metadata = future.get(timeout=10)

        print(f"Message sent successfully to topic 
'{record_metadata.topic}' partition {record_metadata.partition} at offset 
{record_metadata.offset}")

        # Return a success response
        # 202 Accepted is a good status code for asynchronous processing
        return jsonify({
            "status": "success",
            "message": "Data received and sent to processing queue."
        }), 202

    except KafkaError as e:
        # Handle potential Kafka errors (e.g., broker not available)
        print(f"Error sending message to Kafka: {e}")
        return jsonify({"status": "error", "message": "Failed to send data 
to Kafka"}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"status": "error", "message": "An unexpected error 
occurred"}), 500


# --- Main Execution ---
if __name__ == '__main__':
    # Run the Flask app on port 5001
    app.run(host='0.0.0.0', port=5001, debug=True)
