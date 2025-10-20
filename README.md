# canary
A scalable, event-driven data streaming solution to monitor air quality, leveraging Kafka as streaming platform for real-time data pipelines, Arduino microcontroller and sensors for data collection in a pub-sub architecture.


Run docker in the background:

docker compose up -d

Install requirements:

pip install -r requirements.txt


Run publisher with endpoint to receive data and publish topic:

python app.py


Run consumer to read from Kafka:

python consumer.py


Send data to the endpoint: Open a new terminal and use curl to simulate an IoT device sending JSON data.
You should receive a 202 Accepted response from your service.

curl -X POST \
  http://localhost:5001/api/iot \
  -H "Content-Type: application/json" \
  -d '{
        "sensor_id": "temp-sensor-102",
        "location": "greenhouse-3",
        "reading": {
          "temperature": 24.5,
          "humidity": 68.2
        },
        "timestamp": "2025-10-18T17:35:00Z"
      }'