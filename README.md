# IoT-Core-Trials
Repository for IoT Core Trials.

## Sample Code

Generate the public, private key pair.
```bash
openssl req -x509 -newkey rsa:2048 -keyout private_key.pem -nodes -out public_key.pub -subj "/CN=unused"
```

Use the public key to register a new device on to the IoT Core Registry.

To tryout the code run:
```bash
python sample.py \
--registry_id=iot-device-registry \
--cloud_region=asia-east1 \
--project_id=dev-trials-project \
--device_id=device-0 \
--algorith=RS256 \
--private_key_file=keys/private_key.pem \
--service_account_json=configs/iot-device-publish.json \
--ca_certs=keys/roots.pem \
--num_messages=1 \
--data="hello this is test data"
```

To know about the sample code, check [this](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/iot/api-client/mqtt_example).