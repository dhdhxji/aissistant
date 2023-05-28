import paho.mqtt.client as mqtt
import os
import time

# MQTT broker information
broker_address = os.getenv("MQTT_BROKER_ADDR")
broker_port = 8883
username = os.getenv("MQTT_USERNAME")
password = os.getenv("MQTT_PASSWORD")

# Function to retrieve retained message for a topic
def get_retained_message(topic):
    # Create a MQTT client instance
    client = mqtt.Client()

    # Set username and password
    client.username_pw_set(username, password)

    # Set TLS/SSL options
    # client.tls_set(ca_certs=ca_cert)
    client.tls_set()

    # Variable to store the retrieved retained message
    retained_message = None

    # Callback function for when the connection to the MQTT broker is established
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT broker")
        client.subscribe(topic)

    # Callback function for when a message is received
    def on_message(client, userdata, msg):
        nonlocal retained_message
        if msg.retain:
            retained_message = msg.payload.decode()
        client.disconnect()

    # Set the callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    print(broker_address)
    print(broker_port)
    client.connect(broker_address, broker_port, 60)

    # Start the MQTT client loop
    client.loop_start()
    
    time.sleep(0.2)
    client.loop_forever(5)

    # Stop the MQTT client loop
    client.loop_stop()

    return retained_message





if __name__ == "__main__":
    # Example usage
    topic_name = "/sensors/dht11/humidity"
    retained_msg = get_retained_message(topic_name)
    if retained_msg:
        print("Retained message for topic", topic_name, ":", retained_msg)
    else:
        print("No retained message found for topic", topic_name)
