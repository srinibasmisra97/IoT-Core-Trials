import uuid
import os
import json
import random
import string
from AES.AESCipher import AESCipher
from RSA.RSACipher import RSACipher
from DeviceManagement.Manager import DeviceManager
from flask import Flask, jsonify, request

app = Flask(__name__)

manager = DeviceManager(service_account_file_path="configs/iot-device-publish.json",
                            project_id="dev-trials-project",
                            cloud_region="asia-east1",
                            registry_id="iot-device-registry")


@app.route("/device", methods=['GET', 'POST', 'DELETE'])
def device_handler():
    if request.method == 'GET':
        if request.args.get("id") is None:
            devices, state = manager.list_devices()
            return jsonify({
                "success": state['success'],
                "devices": devices if state['success'] else [],
                "error": state['message'] if not state['success'] else ""
            })
        else:
            device, state = manager.get_device(device_id=request.args.get("id"))
            return jsonify({
                "success": state['success'],
                "device": device if state['success'] else {},
                "error": state['message'] if not state['success'] else ""
            })
    elif request.method == 'DELETE':
        if request.args.get("id") is None:
            return jsonify({
                "success": False,
                "error": "no device id provided"
            })

        result = manager.delete_device(device_id=request.args.get("id"))
        return jsonify(result)
    elif request.method == 'POST':
        request_data = request.get_json()

        if "id" not in request_data:
            return jsonify({
                "success": False,
                "error": "no device id provided"
            })

        if "key" not in request_data:
            return jsonify({
                "success": False,
                "error": "no public key provided"
            })

        if "secret" not in request_data:
            return jsonify({
                "success": False,
                "error": "no secret provided"
            })

        encrypted_public_key = request_data["key"]
        aes_key = request_data["secret"]
        device_id = request_data["id"]

        RSAObject = RSACipher()
        RSAObject.set_private_key(private_key_file="keys/RSA/private.pem")
        decrypted_aes_key = RSAObject.decrypt(encrypted_text=aes_key)
        AESObject = AESCipher(key=decrypted_aes_key)
        decrypted_public_key_file = AESObject.decrypt(encrypted_text=encrypted_public_key)

        response = manager.create_device(device_id=device_id, public_key=decrypted_public_key_file)
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)