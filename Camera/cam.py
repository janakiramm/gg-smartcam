from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import argparse
import json

import numpy as np, cv2, sys
from hsapi import ObjectDetector
## Get Horned Sungem SDK from https://github.com/HornedSungem/SungemSDK

rootCAPath = "<ROOT_CA_PATH>"
certificatePath = "<CERT_PATH>"
privateKeyPath = "<PRIVATE_KEY_PATH"
host = "<AWS_IOT_CORE_ENDPOINT>"
port = 8883
clientId = "cam1"
topic = "camera/infer"

net = ObjectDetector(zoom = True, verbose = 2)
video_capture = cv2.VideoCapture(0)

camMQTTClient = AWSIoTMQTTClient(clientId)
camMQTTClient.configureEndpoint(host, port)
camMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

camMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
camMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
camMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
camMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
camMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

camMQTTClient.connect()

loopCount = 0
label=""
while True:
    _, img = video_capture.read()
    result = net.run(img)
    if(len(result[1])):
        label = net.labels[result[1][0][0]]
        print(label)
        time.sleep(1)
    else:
        label="none"
    message = {}
    message['object'] = label
    message['sequence'] = loopCount
    messageJson = json.dumps(message)
    camMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    
    loopCount += 1        