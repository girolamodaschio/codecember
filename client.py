import sys
from pyicloud import PyiCloudService
from src.config import ACCOUNT, PASSWORD
import os
import datetime

api = PyiCloudService(ACCOUNT, PASSWORD)
if api.requires_2fa:
    print("Two-factor authentication required.")
    code = input("Enter the code you received of one of your approved devices: ")
    result = api.validate_2fa_code(code)
    print("Code validation result: %s" % result)

    if not result:
        print("Failed to verify security code")
        sys.exit(1)

    if not api.is_trusted_session:
        print("Session is not trusted. Requesting trust...")
        result = api.trust_session()
        print("Session trust result %s" % result)

        if not result:
            print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
elif api.requires_2sa:
    import click
    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print(
            "  %s: %s" % (i, device.get('deviceName',
            "SMS to %s" % device.get('phoneNumber')))
        )

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)

print('Login was successful')
print('Next step: download all photos in memory')

counter = 0

print(datetime.datetime.now())
for photo in api.photos.albums['All Photos']:
    download = photo.download()
    with open(os.path.join('data', photo.filename), 'wb') as opened_file:
        opened_file.write(download.raw.read())
        print(f"{photo.filename}, {counter}")
        counter +=1

print(datetime.datetime.now())
print(f"Downloaded: {counter}")