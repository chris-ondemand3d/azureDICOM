import json
import requests
import pydicom
from pathlib import Path
from urllib3.filepost import encode_multipart_formdata, choose_boundary
from azure.identity import DefaultAzureCredential

def encode_multipart_related(fields, boundary=None):
    if boundary is None:
        boundary = choose_boundary()

    body, _ = encode_multipart_formdata(fields, boundary)
    content_type = str('multipart/related; boundary=%s' % boundary)

    return body, content_type

dicom_service_name = "testdicomweb"
path_to_dicoms_dir = "C:\\Dev\\azureDICOM\\docs\\dcms\\S0000000016"

base_url = f"https://kasterdicomtest-testdicomweb.dicom.azurehealthcareapis.com/v1"

study_uid = "1.2.826.0.1.3680043.8.498.13230779778012324449356534479549187420"; #StudyInstanceUID for all 3 examples
series_uid = "1.2.826.0.1.3680043.8.498.45787841905473114233124723359129632652"; #SeriesInstanceUID for green-square and red-triangle
instance_uid = "1.2.826.0.1.3680043.8.498.47359123102728459884412887463296905395"; #SOPInstanceUID for red-triangle


from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()

#print(credential.credentials) # this can be used to find the index of the AzureCliCredential
token = credential.credentials[4].get_token('https://dicom.healthcareapis.azure.com')
bearer_token = f'Bearer {token.token}'

client = requests.session()

headers = {"Authorization":bearer_token}
url= f'{base_url}/changefeed'

#print(headers, url)

response = client.get(url,headers=headers)
if (response.status_code != 200):
    print('Error! Likely not authenticated!')


"""
# ---------------------------------------------------------------------------------------------------------
# Store instances using multipart/related
# ---------------------------------------------------------------------------------------------------------

import gdcm

d = gdcm.Directory();
nfiles = d.Load(path_to_dicoms_dir);
if (nfiles > 0): 
    filenames = d.GetFilenames()

for aFile in filenames:
    # print(aFile)
    with open(aFile,'rb') as reader:
        rawfile = reader.read()
    files = {'file': ('dicomfile', rawfile, 'application/dicom')}

#encode as multipart_related
body, content_type = encode_multipart_related(fields = files)

headers = {'Accept':'application/dicom+json', "Content-Type":content_type, "Authorization":bearer_token}
url = f'{base_url}/studies'
response = client.post(url, body, headers=headers, verify=False)

print (response)
"""

"""
# ---------------------------------------------------------------------------------------------------------
# Store instances using multipart/related
# ---------------------------------------------------------------------------------------------------------
#upload blue-circle.dcm
filepath = Path(path_to_dicoms_dir).joinpath('blue-circle.dcm')

# Read through file and load bytes into memory 
files = {}
with open(filepath,'rb') as reader:
    rawfile = reader.read()
files.append({'file': ('dicomfile', rawfile, 'application/dicom')})

#encode as multipart_related
body, content_type = encode_multipart_related(fields = files)

headers = {'Accept':'application/dicom+json', "Content-Type":content_type, "Authorization":bearer_token}

url = f'{base_url}/studies'
response = client.post(url, body, headers=headers, verify=False)

print (response)
"""

"""
# ---------------------------------------------------------------------------------------------------------
# Store instances for a specific study
# ---------------------------------------------------------------------------------------------------------

filepath_red = Path(path_to_dicoms_dir).joinpath('red-triangle.dcm')
filepath_green = Path(path_to_dicoms_dir).joinpath('green-square.dcm')

# Open up and read through file and load bytes into memory 
with open(filepath_red,'rb') as reader:
    rawfile_red = reader.read()
with open(filepath_green,'rb') as reader:
    rawfile_green = reader.read()  
       
files = {'file_red': ('dicomfile', rawfile_red, 'application/dicom'),
         'file_green': ('dicomfile', rawfile_green, 'application/dicom')}

#encode as multipart_related
body, content_type = encode_multipart_related(fields = files)

headers = {'Accept':'application/dicom+json', "Content-Type":content_type, "Authorization":bearer_token}

url = f'{base_url}/studies'
response = client.post(url, body, headers=headers, verify=False)

print (response)
"""

"""
# ---------------------------------------------------------------------------------------------------------
# Store single instance
# ---------------------------------------------------------------------------------------------------------

#upload blue-circle.dcm
filepath = Path(path_to_dicoms_dir).joinpath('blue-circle.dcm')

# Open up and read through file and load bytes into memory 
with open(filepath,'rb') as reader:
    body = reader.read()

headers = {'Accept':'application/dicom+json', 'Content-Type':'application/dicom', "Authorization":bearer_token}

url = f'{base_url}/studies'
response = client.post(url, body, headers=headers, verify=False)
print(response)  # response should be a 409 Conflict if the file was already uploaded in the above request
"""


"""
# ---------------------------------------------------------------------------------------------------------
# Retrieve all instances within a Study
# ---------------------------------------------------------------------------------------------------------
url = f'{base_url}/studies/{study_uid}'
headers = {'Accept':'multipart/related; type="application/dicom"; transfer-syntax=*', "Authorization":bearer_token}
response = client.get(url, headers=headers) #, verify=False)
print (f"Retrieve all instance for Study {study_uid}: ",response)

import requests_toolbelt as tb
from io import BytesIO

mpd = tb.MultipartDecoder.from_response(response)
for part in mpd.parts:
    # Note that the headers are returned as binary!
    print(part.headers[b'content-type'])
    
    # You can convert the binary body (of each part) into a pydicom DataSet
    #   And get direct access to the various underlying fields
    dcm = pydicom.dcmread(BytesIO(part.content))
    print(dcm.PatientName)
    print(dcm.SOPInstanceUID)
"""

"""
# ---------------------------------------------------------------------------------------------------------
# Query DICOM
# ---------------------------------------------------------------------------------------------------------
"""
study_uid = "1.2.410.200034.0.97430517.0.11100.14645.20120517.41"
url = f'{base_url}/studies'
headers = {'Accept':'application/dicom+json', "Authorization":bearer_token}
params = {'StudyInstanceUID':study_uid}

response = client.get(url, headers=headers, params=params) #, verify=False)
print (f"Query for Study {study_uid}: ",response)
json_formatted_str = json.dumps(response.json(), indent=4)
print (json_formatted_str)

"""
url = f'{base_url}/instances'
headers = {'Accept':'application/dicom+json', "Authorization":bearer_token}
params = {}

response = client.get(url, headers=headers, params=params) #, verify=False)
print (f"Query all instance for Instance {instance_uid}: ",response)

json_formatted_str = json.dumps(response.json(), indent=4)
print (json_formatted_str)
"""