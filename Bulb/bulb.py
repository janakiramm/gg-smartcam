from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json

from qhue import Bridge, QhueException, create_new_username

bridge='<PHILIPS_HUE_BRIDE_IP>'
user='<PHILIPS_HUE_BRIDE_TOKEN>'
b = Bridge(bridge, user)
lights = b.lights

def bulbCallback(client, userdata, message):
    color=message.payload
    print("Received message: " + color)
    if color=="green":
    	b.lights[2].state(on=True, bri=250, sat=250, hue=23000)
    elif color=="blue":
    	b.lights[2].state(on=True, bri=250, sat=250, hue=45000)
    else:
    	b.lights[2].state(on=False)


rootCAPath = "<ROOT_CA_PATH>"
certificatePath = "<CERT_PATH>"
privateKeyPath = "<PRIVATE_KEY_PATH"
host = "<AWS_IOT_CORE_ENDPOINT>"
port = 8883
clientId = "bulb1"
topic = "bulb/color"


bulbMQTTClient = AWSIoTMQTTClient(clientId)
bulbMQTTClient.configureEndpoint(host, port)
bulbMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

bulbMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
bulbMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
bulbMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
bulbMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
bulbMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

bulbMQTTClient.connect()

bulbMQTTClient.subscribe(topic, 1, bulbCallback)
while True:
    time.sleep(1)