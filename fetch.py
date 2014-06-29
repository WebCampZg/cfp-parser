import csv
import httplib2
import logging
import pprint
import sys

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from settings.local import *

logging.basicConfig()

def get_csv(client_email, client_key, document_id):

    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with the Credentials. Note that the first parameter, service_account_name,
    # is the Email address created for the Service account. It must be the email
    # address associated with the key that was created.
    scope = 'https://www.googleapis.com/auth/drive'
    credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, client_key, scope=scope)
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Url to download the file in CSV
    exportUrl = "https://docs.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=csv&gid=0" % DOCUMENT_ID

    print "Fetching: %s"  % exportUrl
    (headers, content) = http.request(exportUrl)

    if headers.status != 200:
        raise Exception("Error downloading CSV: %s" % content)

    print "Got %s bytes" % headers['content-length']

    return content

def main(argv):
    # Load the key
    with open(KEY_PATH, 'rb') as f:
        key = f.read()

    # Fetch the document as CSV
    csv = get_csv(CLIENT_EMAIL, key, DOCUMENT_ID)

    # Save it to disk
    with open('submissions.csv', 'w') as f:
        f.write(csv)

if __name__ == '__main__':
    main(sys.argv)
