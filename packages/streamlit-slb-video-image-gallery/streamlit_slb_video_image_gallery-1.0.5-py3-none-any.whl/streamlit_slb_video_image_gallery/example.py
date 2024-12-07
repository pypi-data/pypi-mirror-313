import os
import base64
import streamlit as st
import gzip
import json
from typing import List
from PIL import Image
import io

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthInteractive, OAuthClientCredentials
from streamlit_slb_video_image_gallery import streamlit_slb_video_image_gallery

from models.viewer_data import ViewerData
from models.deck import Deck
from models.beacon import Beacon
from models.camera import Camera
from models.coordinate import Coordinate
from pandas import DataFrame
from helpers.cognite_helper import get_deck_list
import ffmpeg
import pandas as pd

import time
import re
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import date, datetime, timezone


def assign_auth(project_name):

    if project_name == "slb-test":
        tenant_id = os.environ.get("CDF_SLBTEST_TENANT_ID")
        client_id = os.environ.get("CDF_SLBTEST_CLIENT_ID")
        client_secret = os.environ.get("CDF_SLBTEST_CLIENT_SECRET")
        cluster = os.environ.get("CDF_SLBTEST_CLUSTER")
    elif project_name == "petronas-pma-dev" or project_name == "petronas-pma-playground":
        tenant_id = os.environ.get("CDF_PETRONASPMA_TENANT_ID")
        cluster = os.environ.get("CDF_PETRONASPMA_CLUSTER")
        client_id = os.environ.get("CDF_PETRONASPMA_CLIENT_ID")
        client_secret = ""
    elif project_name == "hess-malaysia-dev":
        tenant_id = os.environ.get("CDF_HESSDEV_TENANT_ID")
        client_id = os.environ.get("CDF_HESSDEV_CLIENT_ID")
        client_secret = os.environ.get("CDF_HESSDEV_CLIENT_SECRET")
        cluster = os.environ.get("CDF_HESSDEV_CLUSTER")
    elif project_name == "hess-malaysia-prod":
        tenant_id = os.environ.get("CDF_HESSPROD_TENANT_ID")
        client_id = os.environ.get("CDF_HESSPROD_CLIENT_ID")
        client_secret = os.environ.get("CDF_HESSPROD_CLIENT_SECRET")
        cluster = os.environ.get("CDF_HESSPROD_CLUSTER")
    elif project_name == "mubadala-dev":
        # tenant_id = os.environ.get("CDF_MUBADALADEV_TENANT_ID")
        # cluster = os.environ.get("CDF_MUBADALADEV_CLUSTER")
        # client_id = os.environ.get("CDF_MUBADALADEV_CLIENT_ID")
        # client_secret = os.environ.get("CDF_MUBADALADEV_CLIENT_SECRET")
        tenant_id = '6e302fe9-1186-4281-9fb3-944d7bb828cc'
        cluster = 'az-sin-sp-001'
        client_id = '33fbccca-1f13-4339-9d46-641822badbfe'
        client_secret = 'p878Q~xF6VKi2M7QK_wXO4uwIThmWc1~R~fcJb9E'

    base_url = f"https://{cluster}.cognitedata.com"
    scopes = [f"{base_url}/.default"]

    return {
        "tenant_id": tenant_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "cluster": cluster,
        "base_url": base_url,
        "project_name": project_name,
        "scopes": scopes
    }


def interactive_client(project_name):

    auth_data: any = assign_auth(project_name)

    """Function to instantiate the CogniteClient, using the interactive auth flow"""
    return CogniteClient(
        ClientConfig(
            client_name=auth_data['project_name'],
            project=auth_data['project_name'],
            base_url=auth_data['base_url'],
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}",
                client_id=auth_data['client_id'],
                scopes=auth_data['scopes'],
            ),
        )
    )


def client_credentials(project_name):

    auth_data = assign_auth(project_name)

    credentials = OAuthClientCredentials(
        token_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}/oauth2/v2.0/token",
        client_id=auth_data['client_id'],
        client_secret=auth_data['client_secret'],
        scopes=auth_data['scopes']
    )

    config = ClientConfig(
        client_name=auth_data['project_name'],
        project=auth_data['project_name'],
        base_url=auth_data['base_url'],
        credentials=credentials,
    )
    client = CogniteClient(config)

    return client


def connect(project_name):
    auth = assign_auth(project_name=project_name)
    if auth["client_secret"] == "":
        return interactive_client(project_name)
    else:
        return client_credentials(project_name)


st.set_page_config(layout='wide')
st.subheader("Streamlit Slb Image and Video Gallery")

client: CogniteClient = connect("mubadala-dev")

selected_deck_external_id: int = None
selected_deck_image_id: int = None
imagelist_df: DataFrame = None
viewer_data: ViewerData = None
data_3d = None


def render_selectbox() -> int:
    deckData = get_deck_list(client=client)
    options = {item["name"]: item["externalId"]
               for item in deckData["listDeck"]["items"]}
    deck_name = st.selectbox(label="Select Deck", options=options.keys())
    selected_deck_external_id = options[deck_name]
    return selected_deck_external_id


def get_image_from_id(image_id) -> str:
    image_bytes = client.files.download_bytes(id=image_id)
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str


def get_files_metadata(source):
    file_list = client.files.list(source=source, limit=-1)
    return file_list


def parse_date(time_string):
    for fmt in ["%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]:
        try:
            return datetime.strptime(time_string, fmt).date()
        except ValueError:
            continue
    raise ValueError(
        f"Time data '{time_string}' does not match any supported format")


def check_files_within_date_range():
    # start = datetime.strptime("09/30/2024", "%m/%d/%Y").date()
    start = date(2024, 10, 1)
    end = date(2024, 10, 30)
    # st.write(st.session_state)
    # end = datetime.strptime("09/01/2024", "%m/%d/%Y").date()
    files_within_date_range = []
    temp = []
    file_metadata = get_files_metadata("agora")
    print(len(file_metadata), 'file metadata len')
    # st.write(len(file_metadata), 'file metadata len')
    temp_item = []
    for item in file_metadata:
        temp_item.append(item)
        if item.metadata != None:
            # image_date = datetime.strptime(item.metadata["alert_time"], "%m/%d/%Y %H:%M").date()
            image_date = parse_date(item.metadata["alert_time"])
            temp.append(image_date)
            if start <= image_date <= end:
                # st.text
                files_within_date_range.append(item)
    print(files_within_date_range[0])
    print(len(files_within_date_range))

    relations = client.relationships.list(
        target_external_ids=["169c02838b37a296f90c9f84451cd028a7dda09d2ff84eac1c1ec8bb5c14a5a3"])
    print(relations)
    # print(files_within_date_range[0])
    return files_within_date_range


def get_solx_ppe_violation():
    event_list = client.events.list(
        limit=-1, type='SOLX_PPE_VIOLATION', source='agora_solx')

    print(event_list[0].external_id)

    # res = client.events.retrieve(external_id=event_list[0].asset_ids[0])
    # print(res)

    seq_res = client.sequences.list(limit=-1,
                                    asset_subtree_ids=[event_list[0].asset_ids[0]])

    # print(seq_res)
    # agora:ppe:solx:48:46:00:02:64:00:2024-09-07 06:25:09
    SOLX_PEGAGA_TEMPERATURE_DATA_DATA = []
    SOLX_PEGAGA_HUMIDITY_DATA_DATA = []
    SOLX_PEGAGA_BEACON_DATA_DATA = []
    SOLX_PEGAGA_STEPS_DATA_DATA = []
    SOLX_PEGAGA_NOISE_DATA_DATA = []
    for seq in seq_res:

        pattern = r'(\d{2}:\d{2}:\d{2}:\d{2}:\d{2}:\d{2})'

        # Search for the pattern
        match = re.search(
            pattern, 'agora:ppe:solx:48:46:00:02:64:00:2024-09-07 06:25:09')

        # Extract and print the result
        if match:
            extracted = match.group(1)
           #  print(extracted, 'extracted????')
            if extracted in seq.name:
                print('seq found')
                if seq.description == "SOLX_PEGAGA_TEMPERATURE_DATA_DATA":
                    SOLX_PEGAGA_TEMPERATURE_DATA_DATA.append(seq)
                if seq.description == "SOLX_PEGAGA_HUMIDITY_DATA_DATA":
                    SOLX_PEGAGA_HUMIDITY_DATA_DATA.append(seq)
                if seq.description == "SOLX_PEGAGA_BEACON_DATA_DATA":
                    SOLX_PEGAGA_BEACON_DATA_DATA.append(seq)
                if seq.description == "SOLX_PEGAGA_STEPS_DATA_DATA":
                    SOLX_PEGAGA_STEPS_DATA_DATA.append(seq)
                if seq.description == "SOLX_PEGAGA_NOISE_DATA_DATA":
                    SOLX_PEGAGA_NOISE_DATA_DATA.append(seq)
                # print(extracted)
        else:
            print("No match found")

    print(len(SOLX_PEGAGA_TEMPERATURE_DATA_DATA),
          "SOLX_PEGAGA_TEMPERATURE_DATA_DATA")
    print(len(SOLX_PEGAGA_HUMIDITY_DATA_DATA),
          "SOLX_PEGAGA_HUMIDITY_DATA_DATA")
    print(len(SOLX_PEGAGA_BEACON_DATA_DATA), "SOLX_PEGAGA_BEACON_DATA_DATA")
    print(len(SOLX_PEGAGA_STEPS_DATA_DATA), "SOLX_PEGAGA_STEPS_DATA_DATA")
    print(len(SOLX_PEGAGA_NOISE_DATA_DATA), "SOLX_PEGAGA_NOISE_DATA_DATA")
    print(SOLX_PEGAGA_NOISE_DATA_DATA[0])

    df = client.sequences.data.retrieve_dataframe(
        external_id=SOLX_PEGAGA_NOISE_DATA_DATA[0].external_id, start=0, end=None)
    print(df.head())

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    filter_df = df[df["Timestamp"] == event_list[0].start_time]
    print(filter_df)

    timestamp_s = event_list[0].start_time / 1000
    # agora:ppe:solx:48:46:00:02:64:00:2024-08-07 01:29:31
    # Convert to datetime
    dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
    print(event_list[0].id)
    print(dt)  # Outputs the datetime in UTC
    # for noise in SOLX_PEGAGA_NOISE_DATA_DATA:
    #     # Convert milliseconds to seconds
    #     timestamp_s = noise.created_time / 1000

    #     # Convert to datetime
    #     dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)

    #     print(dt)  # Outputs the datetime in UTC
    #     # print(noise.created_time)


def get_event_list():
    start = date(2024, 9, 20)
    end = date(2024, 9, 30)

    event_list = client.events.list(
        limit=-1, type='PPE_VIOLATION', source='agora')

    event_within_date_range = []

    for item in event_list:
        if item.metadata != None:

            event_date = parse_date(item.metadata["datetime"])
            if start <= event_date <= end:
                # st.text
                event_within_date_range.append(item)

    print(len(event_within_date_range), 'event_list')

    # relations = client.relationships.list(
    #     target_external_ids=["169c02838b37a296f90c9f84451cd028a7dda09d2ff84eac1c1ec8bb5c14a5a3"])
    # print(relations)

    return event_within_date_range


def get_sequence_from_event():
    event_list = get_event_list()

    event_list2 = client.events.list(
        limit=-1, type='SOLX_PPE_VIOLATION', source='agora_solx')

    for event1 in event_list:
        for event2 in event_list2:
            if event2.metadata["agora_eid"] == event1.external_id:
                pass


def get_image_vid_from_event(event_list):
    event_gallery = []
    start = time.time()
    thumbnail_img = client.files.download_bytes(
        external_id='va_aio_248_63e46239-ec40-401c-90be-feff714bd67c.jpg')
    compressed_thumbnail_img = process_image(thumbnail_img)

    for event in event_list:
        # get relations
        # relations = client.relationships.list(
        #     target_external_ids=[event.external_id])
        alert = translate_to_violation(
            event.metadata['alert_type'].strip().replace(" ", "").strip("{'}"))
        temp = {
            'id': event.external_id, 'alert_type2': alert, **event.metadata, 'alert_time': event.metadata['datetime'],
            'image': compressed_thumbnail_img,

        }
        # for relation in relations:
        # 'environmentCondition'
        #     relation_type = relation.source_external_id.split('.')[1]
        #     try:
        #         # file_bytes = client.files.download_bytes(
        #         #     external_id=relation.source_external_id)
        #         if relation_type == 'jpg':

        #             # image_bytes = process_image(file_bytes)
        #             # temp['image'] = image_bytes
        #             temp['image_id'] = relation.source_external_id
        #         elif relation_type == 'mp4':

        #             # video_bytes = process_video(file_bytes)
        #             # temp['video'] = video_bytes
        #             temp['video_id'] = relation.source_external_id

        #     except:
        #         print(relation.source_external_id, 'cannot process')
        event_gallery.append(temp)

        # get image and video

    end = time.time()
    event_gallery[0]['environmentCondition'] = {
        "noise": 30,
        "temperature": 30,
        "humidity": 30
    }

    print(f"{end-start} elapse time get_image_vid_from_event")

    return event_gallery


def translate_to_violation(violation_type):
    if violation_type == 'GLOVE_DETECTION':
        return 'GLOVE VIOLATION'
    elif violation_type == 'HELMET_DETECTION':
        return 'HELMET VIOLATION'
    elif violation_type == 'GLOVE_DETECTION,HELMET_DETECTION':
        return 'GLOVE AND HELMET VIOLATION'


def process_image(file_bytes):

    pil_image = Image.open(io.BytesIO(file_bytes))
    optimized_image = io.BytesIO()
    pil_image.save(optimized_image, format="JPEG",
                   quality=50)  # Adjust quality (1-100)
    optimized_image.seek(0)
    compressed_bytes = optimized_image.getvalue()

    base64_image = base64.b64encode(compressed_bytes).decode('utf-8')

    return base64_image


def process_video(file_bytes):
    # return compress_video(file_bytes)

    base64_image = base64.b64encode(file_bytes).decode('utf-8')

    return base64_image


def compress_video(input_video_bytes):
    # Create a byte buffer from the input video bytes
    input_video_stream = io.BytesIO(input_video_bytes)

    # Prepare an output buffer to store the compressed video
    output_video_stream = io.BytesIO()

    process = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', vcodec='libx264', crf=28, format='mp4')
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    # Write the input video bytes to the process's stdin
    stdout, stderr = process.communicate(input=input_video_bytes)

    # Check for errors
    if process.returncode != 0:
        raise RuntimeError(
            f"FFmpeg process failed with error: {stderr.decode('utf-8')}")

    # Write the output to the output buffer
    output_video_stream.write(stdout)

    # Get the compressed video bytes from the output buffer
    compressed_video_bytes = output_video_stream.getvalue()

    return compressed_video_bytes


def get_image_vid(file_data):
    # 2024-09-07 06:25
    # Total number of API requests
    # total_requests = len(external_id_list)
    images = []
    start = time.time()

    for i, data in enumerate(file_data):
        temp = client.files.download_bytes(external_id=data.external_id)
        # (len(temp), 'before_compress')
        if data.mime_type == 'video/mp4':
            video = compress_video(temp)

        elif data.mime_type == 'image/jpeg':

            pil_image = Image.open(io.BytesIO(temp))
            optimized_image = io.BytesIO()
            pil_image.save(optimized_image, format="JPEG",
                           quality=50)  # Adjust quality (1-100)
            optimized_image.seek(0)
            compressed_bytes = optimized_image.getvalue()

            # print(f"Compressed size: {len(compressed_bytes)} bytes")

            # base64_image = base64.b64encode(temp).decode('utf-8')
            base64_image = base64.b64encode(compressed_bytes).decode('utf-8')
            images.append(
                {'image': base64_image, 'id': data.external_id, **data.metadata, 'alert_type2': data.metadata['alert_type'].strip().replace(" ", "").strip("{'}")})
    # print(images[0])
    end = time.time()

    print(f"{end-start} elapse time")
    # return images
    return images


def get_new_token():
    import http.client

    conn = http.client.HTTPSConnection("login.microsoftonline.com")
    payload = 'client_id=33fbccca-1f13-4339-9d46-641822badbfe&client_secret=p878Q~xF6VKi2M7QK_wXO4uwIThmWc1~R~fcJb9E&grant_type=client_credentials&scope=https%3A%2F%2Faz-sin-sp-001.cognitedata.com%2F.default'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic MzNmYmNjY2EtMWYxMy00MzM5LTlkNDYtNjQxODIyYmFkYmZlOnA4NzhRfnhGNlZLaTJNN1FLX3dYTzR1d0lUaG1XYzF+Un5mY0piOUU=',
        'Cookie': 'fpc=Au4DMIvEJLdHsvDyA0hDs9Du4d2mAQAAALEe2t4OAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
    }
    conn.request(
        "POST", "/6e302fe9-1186-4281-9fb3-944d7bb828cc/oauth2/v2.0/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print('hello world?/')
    # print(data.decode("utf-8").access_token)

    # Decode bytes to string (utf-8 assumed)
    response_text = data.decode("utf-8")
    response_json = json.loads(response_text)  # Parse the string into JSON

    print(response_json.keys())
    # token = response_json['access_token']
    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Inp4ZWcyV09OcFRrd041R21lWWN1VGR0QzZKMCIsImtpZCI6Inp4ZWcyV09OcFRrd041R21lWWN1VGR0QzZKMCJ9.eyJhdWQiOiJodHRwczovL2F6LXNpbi1zcC0wMDEuY29nbml0ZWRhdGEuY29tIiwiaXNzIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNmUzMDJmZTktMTE4Ni00MjgxLTlmYjMtOTQ0ZDdiYjgyOGNjLyIsImlhdCI6MTczMjg0Njk5NiwibmJmIjoxNzMyODQ2OTk2LCJleHAiOjE3MzI4NTA4OTYsImFpbyI6ImsyQmdZQkROYy9oaDFaRnp6Ym5IYUdyYUY4Yk5BQT09IiwiYXBwaWQiOiIzM2ZiY2NjYS0xZjEzLTQzMzktOWQ0Ni02NDE4MjJiYWRiZmUiLCJhcHBpZGFjciI6IjEiLCJncm91cHMiOlsiNDc5YTM2M2QtZGQ5Ny00ZTNjLTk5MjktMWQyOTljODk0ZmIxIiwiNGZhYzhhNWMtNjQzNC00MzQwLTgzMTQtNWRiOWQ0ZjdjNzBiIl0sImlkcCI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzZlMzAyZmU5LTExODYtNDI4MS05ZmIzLTk0NGQ3YmI4MjhjYy8iLCJvaWQiOiI1OGYzZjk5ZS1kZWUxLTQ4YmEtODYyMS00ZThkNzMzZmU4NzUiLCJyaCI6IjEuQWNZQTZTOHdib1lSZ1VLZnM1Uk5lN2dvekVMc1hQNlk0cWhPcWZkVmZLbTFVYTdHQUFER0FBLiIsInN1YiI6IjU4ZjNmOTllLWRlZTEtNDhiYS04NjIxLTRlOGQ3MzNmZTg3NSIsInRpZCI6IjZlMzAyZmU5LTExODYtNDI4MS05ZmIzLTk0NGQ3YmI4MjhjYyIsInV0aSI6InpSRmhLUWRiemt1aG9OaXFDYnJKQUEiLCJ2ZXIiOiIxLjAifQ.IwPvoxfaEoW1lQXsbe8XyWAdGRmS1PJUKcPAAtNB8CFG1fvVAGXd7ORWlSsYcfuVx14_jjgwXX3j4FUbF6uDKBjksPrQPV4BGTHjxOSeJdfgO4BOGe1Mll_Zgiu1NgAa5TT6CgnNE6sJxv8a7BfroSLC7Jj6fUdEO1IN00VIHifDQ3Kxq3P5ybXc9AdGx4-rMOvy5z7S3oB2Bh6c8z2vaEkH6QBvEyb7_oSS15RTlidfUswWG-8AaCY1nuNakm-69GyIyUGrpgYIOXonHTs2nZZD34rRl4KdX7SX-AdoDpCVsXVKqYHqgtGInRhWAg_CgqiB7E-QkyqPTwSpfiNPOg'
    return response_json['access_token'], time.time() + response_json['expires_in']
    # return token
    # decoded_token = jwt.decode(token, options={
    #                            "verify_signature": False})

    # # Extract the expiration timestamp from the 'exp' claim
    # exp_timestamp = decoded_token.get("exp")
    # if not exp_timestamp:
    #     raise ValueError("Token does not have an 'exp' claim.")

    # return data.decode("utf-8")


def is_token_expired(token: str) -> bool:
    try:
        # Decode the JWT token without verifying the signature
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        # Extract the expiration timestamp from the 'exp' claim
        exp_timestamp = decoded_token.get("exp")
        if not exp_timestamp:
            raise ValueError("Token does not have an 'exp' claim.")

        # Convert expiration timestamp to a datetime object
        expiration_time = datetime.fromtimestamp(
            exp_timestamp, tz=timezone.utc)

        # Check if the current time is greater than the expiration time
        return expiration_time < datetime.now(timezone.utc)
    except ExpiredSignatureError:
        return True  # Token is expired
    except (InvalidTokenError, ValueError) as e:
        print(f"Token error: {e}")
        return True  # If invalid token or no 'exp' claim, assume expired


def get_token():
    if 'access_token' not in st.session_state or 'token_expiry' not in st.session_state:
        st.session_state['access_token'], st.session_state['token_expiry'] = get_new_token(
        )

    if is_token_expired(st.session_state['access_token']):
        st.session_state['access_token'], st.session_state['token_expiry'] = get_new_token(
        )

    return st.session_state['access_token']


@st.dialog("Helmet Violation")
def vote(item):

    # Display the icon with dynamic text
    st.markdown(f"""
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <div style="display: flex; align-items: center; gap: 20px;">
            <!-- Time Icon and Text -->
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="material-icons" style="color: blue;">schedule</span>
                <span style="font-size: 18px;">{st.session_state["card_data"]['alert_time']}</span>
            </div>
            <!-- Camera Icon and Text -->
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="material-icons" style="color: blue;">camera_alt</span>
                <span style="font-size: 18px;">{st.session_state["card_data"]['alert_time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Image", "Video"])
    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg",
                 use_column_width=True)
    with tab2:
        st.header("A dog")
        st.video(
            "https://pixabay.com/en/videos/star-long-exposure-starry-sky-sky-6962")

    # if "vote" not in st.session_state:
    #     st.write("Vote for your favorite")
    #     if st.button("A"):


@st.fragment()
def render_viewer():
    global viewer_data
    global data_3d
    # temp = check_files_within_date_range()
    event_list = get_event_list()
    data = get_image_vid_from_event(event_list)
    algorithms = ["HS256"]
    token = get_token()
    # if is_token_expired(getToken(), algorithms):
    #     print("The token has expired.")
    # else:
    #     print("The token is still valid.")

    # file_bytes = client.files.download_bytes(
    #     external_id="va_aio_576_eb4a8375-c625-47bf-ab12-2cc059b6724b.jpg")
    # external id got white space
    # va_aio_576_eb4a8375-c625-47bf-ab12-2cc059b6724b.jpg
    # va_aio_576_eb4a8375-c625-47bf-ab12-2cc059b6724b.jpg
    # print(len(data), 'data')
    # deck_image_str = get_image_from_id(selected_deck_image_id)
    # with threed_container:
    # print(data[0])
    # print(len(temp))
    data_3d = 1
    num_of_images_per_page = 10

    start_idx = (data_3d - 1) * num_of_images_per_page
    end_idx = start_idx + num_of_images_per_page

    # data = get_image_vid(temp[start_idx:end_idx])
    # data = get_image_vid(temp)

    if "card_data" not in st.session_state:
        st.session_state["card_data"] = {}

    get_solx_ppe_violation()

    col1, col2 = st.columns(2)

    with col1:
        st.empty()

    with col2:
        st.empty()
        # st.session_state["card_data"] = streamlit_slb_video_image_gallery(
        #     height=1000, deck_image='', enable_animation=False, data=data, dataLength=0, token=token)
    with st.container():
        st.session_state["card_data"] = streamlit_slb_video_image_gallery(
            height=1000, deck_image='', enable_animation=False, data=data, dataLength=0, token=token)

    if st.session_state["card_data"] is not None:
        vote("A")
        st.write(st.session_state["card_data"])

    # st.write("This many: %s" % data_3d)
    # show_3d_data()


@st.fragment()
def show_3d_data():
    # data_container.empty()
    # with data_container:
    #     if data_3d is not None:
    #         st.write(data_3d)
    # data_container.empty()
    # with st.container(height=900):
    #     if data_3d is not None:
    #         st.write(data_3d)
    pass


# viewer_data = get_data()
render_viewer()
