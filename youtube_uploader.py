# -*- coding: utf-8 -*-
import json
import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import functions
scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def login_prompt(client_secrets_file, credentials_file):
    """
    Handles the OAuth 2.0 login flow and saves credentials.
    """
    # Check if credentials file exists
    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as credentials_buffer:
            credentials = pickle.load(credentials_buffer)
    else:
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server()
        # Save the credentials for the next run
        with open(credentials_file, 'wb') as credentials_buffer:
            pickle.dump(credentials, credentials_buffer)

    return credentials


def video_uploader(youtube, video_file, title, description, category_id, privacy_status):
    """
    Uploads a video to YouTube.
    """
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category_id,
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": privacy_status
            }
        },
        media_body=MediaFileUpload(video_file)
    )
    response = request.execute()

    return response


def uploding():
    print("uploder activated")
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"
    credentials_file = "youtube_credentials.pickle"

    credentials = login_prompt(client_secrets_file, credentials_file)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    with open('metadata.json','r') as file:
        video_data=json.load(file)
    # Video file and metadata
    print("loading metadata...")
    video_file = video_data['video_file']
    title = video_data['title']
    description = video_data['description']
    category_id = video_data['category_id']
    privacy_status = video_data['privacy_status']
    print("uploading...")
    response = video_uploader(youtube, video_file, title, description, category_id, privacy_status)
    print(response)
    functions.delete_files_in_folder()
    print("uploader exit")
uploding()