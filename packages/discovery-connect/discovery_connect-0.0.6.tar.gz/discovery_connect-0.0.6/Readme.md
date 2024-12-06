# Discovery Connect

## Getting started

Install the required packages

```bash
pip install discovery-connect
```

Launch the demo script:

```bash
$ python upload.py -h

usage: upload.py [-h] -w WORKBOOK_UUID [-f FILE] [-a ACQUISITION_NAME] [-F [FILES ...]] -l LOGIN -p PASSWORD -u URL -k CLIENT_KEY -s CLIENT_SECRET

Upload file(s) to discovery

options:
  -h, --help            show this help message and exit
  -w WORKBOOK_UUID, --workbook_uuid WORKBOOK_UUID
                        UUID of the target workbook.
  -f FILE, --file FILE  Path to a single file to be uploaded.
  -a ACQUISITION_NAME, --acquisition_name ACQUISITION_NAME
                        Name for the zip archive for the files.
  -F [FILES ...], --files [FILES ...]
                        List of file names.
  -l LOGIN, --login LOGIN
                        Discovery login
  -p PASSWORD, --password PASSWORD
                        Discovery password
  -u URL, --url URL     Discovery URL
  -k CLIENT_KEY, --client_key CLIENT_KEY
                        Discovery client API key
  -s CLIENT_SECRET, --client_secret CLIENT_SECRET
                        Discovery client API secret
```

## Testing

To access the Discovery API, you will need:

- valid Discovery service account credentials
- valid API client credentials

When collaborating with Ikerian on a particular project, you will be issued
those credentials as part of the project setup. If you have not been issued
credentials, please reach out to your contact person.

Below is an example call for Linux / Mac:

```bash
URL='https://api.region.discovery.retinai.com' \
CLIENT_ID='12345678-1234-1234-1234-1234567890ab' \
CLIENT_SECRET='1234567890' \
USER='upload-service@example.com' \
PASS='abcdefghij' \
WORKBOOK_UUID='12345678-1234-1234-1234-1234567890ab' \
ACQUISITION_NAME='test-acquisition' \
python upload.py -u $URL -k $CLIENT_ID -s $CLIENT_SECRET -l $USER -p $PASS -w $WORKBOOK_UUID -a $ACQUISITION_NAME \
  -F 00000001.dcm 00000002.dcm 00000003.dcm 00000004.dcm
```

Below is an example call for Windows:

```bat
set URL='https://api.region.discovery.retinai.com'
set CLIENT_ID='12345678-1234-1234-1234-1234567890ab'
set CLIENT_SECRET='1234567890'
set USER='upload-service@example.com'
set PASS='abcdefghij'
set WORKBOOK_UUID='12345678-1234-1234-1234-1234567890ab'
set ACQUISITION_NAME='test-acquisition'
py upload.py -u %URL% -k %CLIENT_ID% -s %CLIENT_SECRET% -l %USER% -p %PASS% ^
    -w %WORKBOOK_UUID% -a %ACQUISITION_NAME% ^
    -F 00000001.dcm 00000002.dcm 00000003.dcm 00000004.dcm
```

## License

Copyright 2024 Ikerian AG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  <http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

