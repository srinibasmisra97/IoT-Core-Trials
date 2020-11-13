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

## Command Sender Code

To send command through the sender:
```bash
python command_sender.py \
--project dev-trials-project \
--region asia-east1 \
--registry iot-device-registry \
--device device-1 \
--command "test command for device 1"
```

2. __POST /device__
To add a new device to the registry.
Request:
```json
{
    "id": "device-1",
    "secret": "1d6fd0dc6c56e736593e43996607f210e49abd8d4d2f41e8fe3bc17bd2ed54e61a2ed43c08dd7b80a61c0ae1b41aef9127b9c5b97d8bbee1426ad72653722ab80753237df9332217d1f70bf4ee13cbb3e2f410ae3dd8592fc522c4c2ae83d37ea9652658660693d4a61ec63df1e0dc45f9fed90acf1ac215b4b19e6d7f2e3faf6f85a2d7f04d89627c15c75094240b556030b56846d27ef12bf2cb97d5e9f296f4df43fd744e055328a60ecd8c78d4734ecf7a98646e945e3338e2ccbba863809fdafba769c1a7ac0f157de408f476f1dc48095745cc806d5a3841843ec7e65eb9cae4f9bc4f1520edb7d5ea0d084346bc1107422acd17b2b2e80d7ea7c78ed9",
    "key": "/IyfK+qs7Uc1JuYznRDGZoQselJuIcm/khO0Jx/I9NFMQ639E8ue25n8KbuNKBQ68XwXIkozPzu2+Bx2TSde83KzsOSLn0cS18E5U+/FBm1mxJ7/UUp+f0MZEpYPS30GtXOgupPZzOQrWCZgj/1yH3jrFFVs+P48XOdSzAizYDCJhsshQAXEtsQzMGxuE+FL+gIqCtiYnZylw8uLVk3BkhqGRnanPwN2fLREqRwDN6eDcw+3qZt2oSRLtSPSjHy4JCSFta49YvQHqmR1IKBnDbZYbcsQQql3DsnBqsQDFWA2TYeddkLhXWRYZ6OMthdHzJy/Rjs+lnyvjmNi/zyxHATogjusu69RwzSgZH/lFpEDwgAtuEiNYHKtTDYosJC0JUZ8gA3+Umjl5DIRy/G4nb1AEiGxHpg5t4FmwDlehazfxLIwE2T2lZHmmKTphNtYAUB22eK/siDTD9u5x3xED92HKOyvmi+wXyItlS4EUCVMywzCLOXTEaaqKM7QNhAjTECynUBtYilMGeu7nl7YD6OdOAvdARBw6p4nHeS9o5uCfvkKhEqIXmpc+gVM/3CjNAc/vPrvEKrohsWNOiHqeN5f9B9bBeezGLUVS4kZfRHybfu3XJKQpBfxHjMEF1yGteFVZUp9aDpVjRQ7KZMIWtq1vKDqGogOIKJz2Zbm9nbwzcVDHarWhsuE6e6nFokyeBZVxrGQ1FeVx6MnoTFit3LMN6eZH9908uYgIIf+dpb1XFaCP0V6ACEI4kdN18ZX/FU3FiSKrxYWu+d2HdMcij3YTTPNGqGQpRd8VItX2mrE4tAumywt+Zp2maaxX2Ku2gqaZ4YuaTsaPqkvKPkmHiOaly9aZx27QBWwsIqSAa19K6grMtxbQJ34KSJnipi+s3lvsZ4cqcpVvMrve1f2THQWx0vscN9+hIC7ZGdAn9psw1LonHwY5mnmq/+JzOqZjeLLr3MgiHVJVMEFsDzR5RX5M7iqXPnsuPUYIKHPSKd5GtmuGPNzf6v1/gJ6v0v0iStU6XPS5L4Fgo65RsVmEdQ2UgHsP2yWUXHBSJ7ydi4T2vViGjRpGSUa0QXI6F+fm5KMCDueyUBdCQw3G5mTRkhXTJ/yOuZwPlRxNTSykoBfHht6UjzXjXuZY1ADCZYUoLxHVvb5yb/zuDpk52YJUuGhTzmwfHpDwm7lPRmFH69iQmdNGL/VFy1zM4cNBBqfQmqqGDr2dVCWH00oL4i7+Tvb5cwdGYm3641UYL7QFagrWYh/5L0RICZWOJjFxH4OYHQgVXDRRWsGUpvnq2Yke4ivIqxf/Ihnbp50ixsCU3E="
}
```

3. __DELETE /device?id=<device-id>__
To delete a device from the registry.

## AES Encryption
[AESCipher.py](AES/AESCipher.py) can be used to perform the AES encryption.

An object needs to be created and the AES secret key needs to be set.
```python
from AES.AESCipher import AESCipher

aes = AESCipher(key="<your-aes-key>")
```

You can then use the `encrypt` and `decrypt` functions.
```python
encrypted_data = aes.encrypt(plain_text="<your-plain-text-data>")
decrypted_data = aes.decrypt(encrypted_text="<your-encrypted-data>")
```

## RSA Encryption
[RSACipher.py](RSA/RSACipher.py) can be used to perform the RSA encryption.

An object needs to be created before performing either of the encryption or the decryption.

```python
from RSA.RSACipher import RSACipher

rsa = RSACipher()
```

To encrypt data:
```python
rsa.set_public_key(public_key_file="/path/to/public/key")
encrypted_data = rsa.encrypt(plain_text="<your-plain-text>")
```

To decrypt data:
```python
rsa.set_private_key(private_key_file="/path/to/private/key")
decrypted_data = rsa.decrypt(encrypted_text="<your-encrypted-data>")
```

## Encryption Mechanism
General encryption flow used here for the public keys to be sent is,
1. Generate a random string to be used for AES as a secret key.
2. Encrypt the random AES secret key with RSA.

Both the AES encrypted Public Key and the RSA encrypted secret key would be sent.

## Device Setup

device_setup.py would be used by the device to register into the device registry.

## API Server

There are three APIs:
1. __GET /device__
Would return a list of all the devices in the registry.

Response:
```json
{
  "devices": [
    {
      "id": "device-0", 
      "name": "", 
      "num_id": 3237902273983036
    }
  ], 
  "error": "", 
  "success": true
}
```

We can add a query parameter `id` to get data about a specific device.

Response:
```json
{
  "device": {
    "config": {
      "cloud_update_time": "2020-11-13 10:14:11.524877+00:00", 
      "device_ack_time": "2020-11-13 10:17:31.811033+00:00", 
      "version": 2
    }, 
    "credentials": [
      {
        "expiration_time": {}, 
        "public_key": {
          "format": "RSA_X509_PEM", 
          "key": "Hwkd+ClauYZKc9c8NZOupuls9PHMEDLmSLLwjaCa/jci0ClP8dz8hYvtzkL7Y5L3whQWZ3dLjRwArvKIHbzrd5pK3KRESpVGqVXObZ1tOI9WsMa3dsjYvo4fNgaudjpT5RLzFDPye5EI5aCvAIA+28T0ntV6fnHUZuFsQTiDjw7rmxEHqoI8/htrSB6DTK8x6/h0k4gh0GG4Bwj9vjjSbapcT6wGSGxwTkXV5qOW0EZezhtFH0ZWH4JT6LMcn+yUDuVbj5atwxtNLLmEDEA0Zh+4K8QZdG4Ezmccu9DSn7/Cb39akn4Sr7ergizFHZQeBxl3VbxHeejNLDB0OYeE0oauTX6MuELrxTXSCZMC1XtWHo2a3HgK4fwHgRt76hd0tEWQn068La1JXXO5oZlZD3lPRiAo0xlPDT77+4aMHhZmF6ePWhlXPfKhwJ4/pXAf0fOfVa976xFfd0VDCtI2YG0+IlIQLtGgAYiSwTLyWsbbvRt1vemMveenk0dO7FW4EOMNDyPmpmeBmJIn7lH/OhmNNiiwtgiERPUXDMTEHv7gheJqOEnAd50nvnmhjV2GDk/f0R/D9GT0LHunkDKr7kAnTo6oNxVbR+BPnf0C92lu2iknpGGhx3BqePLVrTGTnY5Hok0Dg94nyKXjeOPedMkmR/LaDf3SASaLcZbO82b10ZuJS0pGO0s58pobt6/B1IiGKwV9VpVb+o2sgCpn3jmUSYnvX638eezCH/ABtmYc3m1K4lb/aLCRMl5FHIMj4Yo97LW4ZIl62EysZmu0N9kSwoH/G3qqO25gYfptQT5mPLqxoXdIX+vqLFLo4xS36IIPB176PSw+ShtXXAUK79ZgYlLIJh/j3UsUnaHIP0JNn0NKKNn5y01J7o0YjSLKVNYHyzO+bKKhs+85+BgSgIRZFacBO33UTaFVNA8S13FNAL3QM2O0lAkoS3leKVPGJDlHy+Q7FnFTRfQ+1/r4oLxlKtOLZLrH8k3pzmhRdoql/mzlcd79BAsMJ0EfwwazX7ZOgWfK5+CoqGiltMbOsFxylnz8CfP/0cT8SGcUZPQ7uEawTPWJHF1Gj0eoFvTXh5IESA3tUjOg6McHsgTU5kBkxpo0LpHC0EbGjbkxcgP4XYakufPmQIPigr2VAgIHeVQ5OuDJ/fQriw5JpcOpxxRXG8H+y+WXiquW+vjuFZlAEH6c5AX8NaIeK6JgKsT+V/7bz/S+MO6VzqA0hHIWxp8xwQifGABc+AtKAqVuNoU/nmeOLXby4q8/XYBviA0UnZsZASG8kdzLRZ54Ezw9yPUfc05Tlp2mmyd45+BmRJk=", 
          "secret": "c985eb96f3f42f7ef89d40213bfd66d1ca6213c5b273fdea319b695508e88d1a3845e599f97bd0578c453c5af78b0a26ab2f59c5e6ed1d51bc4defaf10adde7297fc597f029e05528d353cc5394a112a9298a264d6ae1ac7c9a99027076758305f083d9e0cbd29edbc18ab4033a955c3642562c442da079737748f8b0c0a2ff6a1d311ffa4371926691c8cfaf4c0776419b21d171825af9fa9e2dc1fb1f21d5db7bc354a575b4c75a5db641b038b7485c060d17b86d023fc595df5831e4ddb8611317184ab88c05e9c87bd57f6f419aae0e1550cb64937b98d5f9ec35e5e3961b791236571641314eb1bc111213fcc690acd1cfc74e4442aaca895896ecdb577"
        }
      }
    ], 
    "gateway_config": {}, 
    "id": "device-0", 
    "last_config_ack_time": "2020-11-13 10:17:31.808342+00:00", 
    "last_config_send_time": "2020-11-13 10:17:31.808457+00:00", 
    "last_error_status": {
      "code": 9, 
      "message": ""
    }, 
    "last_error_time": "2020-11-13 10:14:27.511814+00:00", 
    "last_event_time": "1970-01-01 00:00:00+00:00", 
    "last_heartbeat_time": "1970-01-01 00:00:00+00:00", 
    "last_state_time": "None", 
    "log_level": "LogLevel.LOG_LEVEL_UNSPECIFIED", 
    "name": "projects/dev-trials-project/locations/asia-east1/registries/iot-device-registry/devices/3237902273983036", 
    "num_id": 3237902273983036
  }, 
  "error": "", 
  "success": true
}
```
