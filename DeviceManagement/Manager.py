import os
import random
import string

from google.cloud import iot_v1
from google.api_core import exceptions
from RSA.RSACipher import RSACipher
from AES.AESCipher import AESCipher


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

            RSAObject = RSACipher()
            RSAObject.set_public_key(public_key_file="keys/RSA/public.pem")

            for credential in device.credentials:
                aes_key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20))
                encrypted_key = RSAObject.encrypt(plain_text=aes_key)
                AESObject = AESCipher(key=aes_key)
                encrypted_public_key_file = AESObject.encrypt(plain_text=credential.public_key.key)

                device_data["credentials"].append({
                    "public_key": {
                        "format": "RSA_X509_PEM",
                        "key": encrypted_public_key_file,
                        "secret": encrypted_key
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
