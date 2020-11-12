import configparser
import os
import datetime
import logging
import time
import jwt
import paho.mqtt.client as mqtt
import ssl
import threading
import random

CONFIG_ENV = os.environ.get("CONFIG_ENV") if os.environ.get("CONFIG_ENV") else "DEV"
CONFIG_FOLDER = os.environ.get("CONFIG_FOLDER") if os.environ.get("CONFIG_FOLDER") else "configs"
CONFIG_FILENAME = os.environ.get("CONFIG_FILENAME") if os.environ.get("CONFIG_FILENAME") else "environment.cfg"
CONFIG_FILEPATH = os.path.join(os.getcwd(), CONFIG_FOLDER, CONFIG_FILENAME)

cfg = configparser.RawConfigParser()
cfg.read(CONFIG_FILEPATH)

ALGORITHM = str(cfg.get(CONFIG_ENV, "ALGORITHM"))
CA_CERTS = str(cfg.get(CONFIG_ENV, "CA_CERTS"))
CLOUD_REGION = str(cfg.get(CONFIG_ENV, "CLOUD_REGION"))
JWT_EXPIRES_MINUTES = int(cfg.get(CONFIG_ENV, "JWT_EXPIRES_MINUTES")) if cfg.get(CONFIG_ENV, "JWT_EXPIRES_MINUTES") else 20
LISTEN_DURATION = int(cfg.get(CONFIG_ENV, "LISTEN_DURATION")) if cfg.get(CONFIG_ENV, "LISTEN_DURATION") else 60
MQTT_BRIDGE_HOSTNAME = str(cfg.get(CONFIG_ENV, "MQTT_BRIDGE_HOSTNAME")) if cfg.get(CONFIG_ENV, "MQTT_BRIDGE_HOSTNAME") else "mqtt.googleapis.com"
MQTT_BRIDGE_PORT = int(cfg.get(CONFIG_ENV, "MQTT_BRIDGE_PORT")) if cfg.get(CONFIG_ENV, "MQTT_BRIDGE_PORT") else 8883
PRIVATE_KEY_FILE = str(cfg.get(CONFIG_ENV, "PRIVATE_KEY_FILE"))
PROJECT_ID = str(cfg.get(CONFIG_ENV, "PROJECT_ID"))
REGISTRY_ID = str(cfg.get(CONFIG_ENV, "REGISTRY_ID"))
SERVICE_ACCOUNT_JSON = str(cfg.get(CONFIG_ENV, "SERVICE_ACCOUNT_JSON")) if cfg.get(CONFIG_ENV, "SERVICE_ACCOUNT_JSON") else os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)


def create_jwt(project_id, private_key_file, algorithm):
    token = {
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRES_MINUTES),
        'aud': PROJECT_ID
    }

    with open(private_key_file, 'r') as file:
        private_key = file.read()

    print("Creating JWT using {} and private key file at {}".format(algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))


class Device:

    def __init__(self, project_id, cloud_region, registry_id, device_id, private_key_file,
                 algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):
        self.should_backoff = False
        self.minimum_backoff_time = 1
        self.maximum_backoff_time = 32
        self.project_id = project_id
        self.cloud_region = cloud_region
        self.registry_id = registry_id
        self.device_id = device_id
        self.private_key_file = private_key_file
        self.algorithm = algorithm
        self.ca_certs = ca_certs
        self.mqtt_bridge_hostname = mqtt_bridge_hostname
        self.mqtt_bridge_port = mqtt_bridge_port

        self.client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(self.project_id, self.cloud_region, self.registry_id, self.device_id)
        print("Client ID is: {}".format(self.client_id))

        self.client = mqtt.Client(client_id=self.client_id)

        self.client.username_pw_set(
            username='unused',
            password=create_jwt(self.project_id, self.private_key_file, self.algorithm)
        )

        self.client.tls_set(ca_certs=self.ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message

        self.client.connect(self.mqtt_bridge_hostname, self.mqtt_bridge_port)

        self.mqtt_config_topic = '/devices/{}/config'.format(self.device_id)
        self.client.subscribe(self.mqtt_config_topic, qos=1)

        self.mqtt_command_topic = '/devices/{}/commands/#'.format(self.device_id)

        print("Subscribing to {}".format(self.mqtt_command_topic))
        self.client.subscribe(self.mqtt_command_topic, qos=1)

        print("Device setup done!")

    def reconnect(self):
        self.client.connect(self.mqtt_bridge_hostname, self.mqtt_bridge_port)
        self.client.subscribe(self.mqtt_config_topic, qos=1)
        self.client.subscribe(self.mqtt_command_topic, qos=1)

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        print('on_connect', mqtt.connack_string(rc))
        self.should_backoff = False
        self.minimum_backoff_time = 1

    def on_disconnect(self, unusued_client, unused_userdata, rc):
        print('on_disconnect', error_str(rc))
        self.should_backoff = True

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        print('on_publish')

    def on_message(self, unused_client, unused_userdata, message):
        payload = str(message.payload.decode('utf-8'))
        print('Received message \'{}\' on topic \'{}\' with QoS {}'.format(
            payload, message.topic, str(message.qos)
        ))

def client_loop_thread(name, device):
    print("Starting thread {}".format(name))

    for i in range(1, 60):
        logging.info(i)
        time.sleep(1)
        device.client.loop()

        if device.should_backoff:
            print("DEVICE DISCONNECTED!")

            if device.minimum_backoff_time > device.maximum_backoff_time:
                print("EXCEEDED MAXIMUM BACKOFF TIME! GIVING UP!")
                break

            delay = device.minimum_backoff_time + random.randint(0, 1000)/10000.0
            print("Waiting for {} before reconnecting.".format(delay))
            time.sleep(delay)
            device.minimum_backoff_time = device.minimum_backoff_time * 2
            device.reconnect()


if __name__ == '__main__':
    device_id = str(input("Enter device id: "))

    mqtt_topic = '/devices/{}/events'.format(device_id)

    device = Device(project_id=PROJECT_ID, cloud_region=CLOUD_REGION, registry_id=REGISTRY_ID,
                    device_id=device_id, private_key_file=PRIVATE_KEY_FILE, algorithm=ALGORITHM,
                    ca_certs=CA_CERTS, mqtt_bridge_hostname=MQTT_BRIDGE_HOSTNAME, mqtt_bridge_port=MQTT_BRIDGE_PORT)

    device.client.loop()

    thread = threading.Thread(target=client_loop_thread, args=('listen_thread', device))
    thread.start()

    for i in range(1, 60):
        device.client.loop()

        if device.should_backoff:
            print("DEVICE DISCONNECTED!")

            if device.minimum_backoff_time > device.maximum_backoff_time:
                print("EXCEEDED MAXIMUM BACKOFF TIME! GIVING UP!")
                break

            delay = device.minimum_backoff_time + random.randint(0, 1000)/10000.0
            print("Waiting for {} before reconnecting.".format(delay))
            time.sleep(delay)
            device.minimum_backoff_time = device.minimum_backoff_time * 2
            device.reconnect()

        # data = str(input("Enter data to publish: "))
        #
        # print('Publishing message: {}'.format(data))
        # device.client.publish(mqtt_topic, payload=data, qos=1)

        time.sleep(1)