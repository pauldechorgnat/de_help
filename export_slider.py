from googleapiclient.discovery import build
from googleapiclient._auth import apply_credentials
from GoogleApiSupport.auth import get_service, service_credentials_path
from google.oauth2.credentials import Credentials
import json
with open('credentials.auth', 'r') as file:
    credentials = json.load(file)
with open('google_credentials.auth', 'r') as file:
    google_credentials = json.load(file)
#
# service_credentials_path.append('/home/paul/PycharmProjects/de_help/credentials.auth')



if __name__ == '__main__':
    keys = Credentials(token=None, token_uri=credentials['token_uri'], client_id=credentials['client_x509_cert_url'])

    service = build(serviceName='slides', version='v1', developerKey=google_credentials['api_key'])

    print(service.presentations())
    # a = service.presentations().get(presentationId=google_credentials['presentation_id']).execute()
    # print(a.__dict__.keys())
    # print(type(a))
    # slide_service = get_service('https://www.googleapis.com/auth/drive')
    # print(slide_service)