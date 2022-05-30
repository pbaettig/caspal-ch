#!/usr/bin/env python3

import os.path
from tempfile import mktemp

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from hashlib import md5


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def oauth_authorize(token_fname='google_creds/token.json', creds_fname='google_creds/credentials.json'):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists(token_fname):
        creds = Credentials.from_authorized_user_file(token_fname, SCOPES)

    if creds and creds.valid:
        return creds

    # If there are no (valid) credentials available, let the user log in.
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not os.path.exists(creds_fname):
            raise ValueError(
                f'OAuth client information file "{creds_fname}" does not exist')
        flow = InstalledAppFlow.from_client_secrets_file(creds_fname, SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open(token_fname, 'w') as token:
        token.write(creds.to_json())

    return creds


def download_doc_pdf(drive_client, doc_id, fname):
    r = drive_client.files().export_media(fileId=doc_id, mimeType='application/pdf')
    with open(fname, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, r)
        done = False
        while done is False:
            status, done = downloader.next_chunk()


def compare_file_checksums(fname_1, fname_2) -> bool:
    hashes = []
    for fname in (fname_1, fname_2):
        try:
            h = md5(open(fname, 'rb').read()).hexdigest()
        except FileNotFoundError:
            hashes.append('')
        else:
            hashes.append(h)

    return hashes[0] == hashes[1]


def main():
    cv_fname = 'content/_site/assets/CV-en.pdf'
    cv_tmp = mktemp()
    file_id = '1at8R58RRQqrUVp_H7zpe41H9T9bHUwXMACaeCyYtBNM'
    creds = oauth_authorize()
    service = build('drive', 'v3', credentials=creds)

    download_doc_pdf(service, file_id, cv_tmp)

    if not compare_file_checksums(cv_tmp, cv_fname):
        print(f'updated {cv_fname}!')
        os.rename(cv_tmp, cv_fname)
    else:
        os.remove(cv_tmp)


if __name__ == '__main__':
    main()