#! python3

from __future__ import print_function
import json, requests, sys
import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

url ="https://graph.facebook.com/v2.9/256389754771285?fields=feed.limit(5)&access_token=EAAZAqbJrNGSYBAA47PeI9yhvlw3lz0NWSHnFU7hJTDuXqdgnZB5SWnFFrO1pjVZCAZBvbTBomrry9iW9T5UODGjJVcnLrznPrVxDQguvYW9dTEoLTgucPYXakapr8BKJpG5irAxz6TRhbwzq4x1ZBphOJ9ZClbDTMZD"
response = requests.get(url)
response.raise_for_status()

feed = json.loads(response.text)
f = feed['feed']['data']

fname = 'date.txt'
File = open( fname ,'w')

k=1
for i in range(len(f)):
	if 'message' in f[i] :
		File.write( f[i]['message'])
		k=k+1
File.close()

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

FILES = (
    (fname, None),
    (fname, 'application/vnd.google-apps.document'),
)

for filename, mimeType in FILES:
    metadata = {'name': filename}
    if mimeType:
        metadata['mimeType'] = mimeType
    res = DRIVE.files().create(body=metadata, media_body=filename).execute()
    if res:
        print('Uploaded "%s" (%s)' % (filename, res['mimeType']))

if res:
    MIMETYPE = 'application/pdf'
    data = DRIVE.files().export(fileId=res['id'], mimeType=MIMETYPE).execute()
    if data:
        fn = '%s.pdf' % os.path.splitext(filename)[0]
        with open(fn, 'wb') as fh:
            fh.write(data)
        print('Downloaded "%s" (%s)' % (fn, MIMETYPE))


print ( " END " )




