import greengrasssdk
import platform
import time
import json

client = greengrasssdk.client('iot-data')
output_topic="bulb/color"

def function_handler(event, context):
	topic = context.client_context.custom['subject']
	obj = event['object']
	if obj=="car":
		color="green"
	elif obj=="bus":
		color="blue"
	else:
		color="none"
	client.publish(topic=output_topic, payload=color)
	return