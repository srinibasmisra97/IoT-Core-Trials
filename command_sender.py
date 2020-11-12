import argparse
from google.cloud import iot_v1
import os


def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description='Sample command sender code.'
    )

    parser.add_argument(
        '--project',
        required=True,
        help='GCP Project ID.'
    )

    parser.add_argument(
        '--region',
        required=True,
        help='Region of IoT Registry.'
    )

    parser.add_argument(
        '--registry',
        required=True,
        help='Registry ID for the IoT devices.'
    )

    parser.add_argument(
        '--device',
        required=True,
        help='Device ID to send command to.'
    )

    parser.add_argument(
        '--command',
        required=True,
        help='Command to send to the device.'
    )

    return parser.parse_args()


def send():
    args = parse_command_line_args()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "configs/iot-device-publish.json"
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(args.project, args.region, args.registry, args.device)

    command = args.command
    data = command.encode('utf-8')

    return client.send_command_to_device(
        request={"name": device_path, "binary_data": data}
    )


if __name__ == '__main__':
    response = send()
    print(response)