import os
import json

from google.cloud import iot_v1
from google.api_core import exceptions
from google.protobuf.json_format import MessageToJson


class DeviceManager:

    def __init__(self, service_account_file_path, project_id, cloud_region, registry_id):
        self.project_id = project_id
        self.cloud_region = cloud_region
        self.registry_id = registry_id

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_file_path
        self.client = iot_v1.DeviceManagerClient()

    def get_device(self, device_id):
        device_path = self.client.device_path(self.project_id, self.cloud_region, self.registry_id, device_id)

        try:
            device = self.client.get_device(request={
                "name": device_path
            })

            device_data = {
                "name": device.name,
                "id": device.id,
                "num_id": device.num_id,
                "last_heartbeat_time": str(device.last_heartbeat_time),
                "last_event_time": str(device.last_event_time),
                "last_error_time": str(device.last_error_time),
                "last_error_status": {
                    "code": device.last_error_status.code,
                    "message": device.last_error_status.message
                },
                "credentials": [],
                "config": {
                    "version": device.config.version,
                    "cloud_update_time": str(device.config.cloud_update_time),
                    "device_ack_time": str(device.config.device_ack_time),
                },
                "last_config_ack_time": str(device.last_config_ack_time),
                "last_config_send_time": str(device.last_config_send_time),
                "gateway_config": {},
                "last_state_time": str(device.last_state_time),
                "log_level": str(device.log_level)
            }

            for credential in device.credentials:
                device_data["credentials"].append({
                    "public_key": {
                        "format": "RSA_X509_PEM",
                        "key": credential.public_key.key
                    },
                    "expiration_time": {}
                })

            return device_data, {"success": True}
        except exceptions.NotFound:
            return {}, {"success": False, "message": "Device Not Found"}

    def list_devices(self):
        registry_path = self.client.registry_path(self.project_id, self.cloud_region, self.registry_id)

        try:
            devices = list(self.client.list_devices(request={
                "parent": registry_path
            }))

            device_data = []
            for device in devices:
                device_data.append({
                "name": device.name,
                "id": device.id,
                "num_id": device.num_id
            })

            return device_data, {"success": True}
        except exceptions.NotFound:
            return [], {"success": False, "message": "Registry Not Found"}

    def list_device_states(self, device_id, history=False):
        device_path = self.client.device_path(self.project_id, self.cloud_region, self.registry_id, device_id)

        try:
            if history:
                states = self.client.list_device_states(request={
                    "name": device_path
                }).device_states
                return states, {"success": True}
            else:
                state = self.client.get_device(request={
                    "name": device_path
                }).state
                return state, {"success": True}
        except exceptions.NotFound:
            return None, {"success": False, "message": "Device Not Found"}

    def create_device(self, device_id, public_key):
        parent = self.client.registry_path(self.project_id, self.cloud_region, self.registry_id)

        device_template = {
            "id": device_id,
            "credentials": [
                {
                    "public_key": {
                        "format": iot_v1.PublicKeyFormat.RSA_X509_PEM,
                        "key": public_key
                    }
                }
            ]
        }

        try:
            self.client.create_device(request={
                "parent": parent,
                "device": device_template
            })
            return {"success": True}
        except exceptions.AlreadyExists:
            return {"success": False, "message": "device already exists"}
        except exceptions.PermissionDenied:
            return {"success": False, "message": "permission denied"}
        except exceptions.Unauthorized:
            return {"success": False, "message": "unauthorized"}
        except exceptions.NotFound:
            return {"success": False, "message": "registry not found"}

    def delete_device(self, device_id):
        device_path = self.client.device_path(self.project_id, self.cloud_region, self.registry_id, device_id)

        try:
            self.client.delete_device(request={
                "name": device_path
            })
            return {"success": True}
        except exceptions.NotFound:
            return {"success": False, "message": "device not found"}
        except exceptions.Unauthorized:
            return {"success": False, "message": "unauthorized"}
        except exceptions.PermissionDenied:
            return {"success": False, "message": "permission denied"}


# if __name__ == '__main__':
#     manager = DeviceManager(service_account_file_path="../configs/iot-device-publish.json",
#                             project_id="dev-trials-project",
#                             cloud_region="asia-east1",
#                             registry_id="iot-device-registry")

    # device, state = manager.get_device(device_id="device-0")
    # if state['success']:
    #     print(device)
    # else:
    #     print(state['message'])

    # devices, state = manager.list_devices()
    # if state['success']:
    #     print(devices)
    # else:
    #     print(state['message'])

    # device_state, state = manager.list_device_states(device_id="device-0")
    # if state['success']:
    #     print(device_state)
    # else:
    #     print(state['message'])

    # device_states, state = manager.list_device_states(device_id="device-0", history=True)
    # if state['success']:
    #     print(device_states)
    # else:
    #     print(state['message'])

    # result = manager.create_device(device_id="device-2", public_key=open("../keys/public_key.pub", 'r').read())
    # print(result)

    # result = manager.delete_device(device_id="device-2")
    # print(result)