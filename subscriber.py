import paho.mqtt.client as mqtt
import time

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/test", qos=1)

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (you can create separate callbacks per subscribed topic)
def on_message(client, userdata, message):
    # It's good practice to decode the payload to a string.
    print('Received message: "' + str(message.payload.decode("utf-8")) + '" on topic "' +
          message.topic + '" with QoS ' + str(message.qos))

# 1. create a client instance.
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect("mqtt.eclipse.org")
try:
    client.connect('test.mosquitto.org')
except:
    print('Connection failed')
    exit() # Should quit if failed to connect

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

try:
    # 4. use publish() to publish messages to the broker.
    # and use subscribe() to subscribe to a topic and receive messages.
    # use disconnect() to disconnect from the broker.
    while True:
        # Ask user for a message to publish
        message = input("Enter a message to publish or type 'exit' to quit: ")
        if message.lower() == 'exit':
            break
        # Publish the message
        client.publish("ece180d/test", message, qos=1)

except KeyboardInterrupt:
    print("Script interrupted by user.")

finally:
    # 5. Cleanly disconnect from the broker
    print("Disconnecting from broker...")
    client.loop_stop()
    client.disconnect()

print("Script finished.")