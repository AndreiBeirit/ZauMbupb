import os
import base64
import sys
import shutil
from io import BytesIO
from urllib.parse import urlparse
import random
import zipfile
import requests
from relog_config import download_username, download_password

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename != "Settings.xml":
            os.unlink(file_path)
        elif os.path.isdir(file_path) and filename != "Settings.xml": 
            shutil.rmtree(file_path)

relog_path = "C:/RELOG/"
chatbot_path = "C:/ChatBot/"

if not os.path.exists(relog_path):
    os.makedirs(relog_path)

if not os.path.exists(chatbot_path):
    os.makedirs(chatbot_path)

shutil.rmtree(chatbot_path, ignore_errors=True)
os.makedirs(chatbot_path, exist_ok=True)

clear_directory(relog_path)

settings_xml_path = os.path.join(relog_path, "Settings.xml")
if os.path.exists(settings_xml_path):
    os.makedirs(relog_path, exist_ok=True)
else:
    shutil.rmtree(relog_path, ignore_errors=True)
    os.makedirs(relog_path, exist_ok=True)

credentials = base64.b64encode(f'{download_username}:{download_password}'.encode()).decode()

headers = {
    'Authorization': f'Basic {credentials}'
}

relog_url = 'https://'
response = requests.get(relog_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        download_urls = [item.get('DownloadURL') for item in data if item.get('DownloadURL')]
        relog_urls = [url for url in download_urls if 'Relog_v' in url]
        if relog_urls:
            random_relog_url = random.choice(relog_urls)

            parsed_url = urlparse(random_relog_url)
            file_name = os.path.basename(parsed_url.path)

            response_file = requests.get(random_relog_url, stream=True)
            if response_file.status_code == 200:
                with zipfile.ZipFile(BytesIO(response_file.content), 'r') as zip_ref:
                    zip_ref.extractall(relog_path)

bot_url = 'https://'
response = requests.get(bot_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        download_urls = [item.get('DownloadURL') for item in data if item.get('DownloadURL')]
        bot_urls = [url for url in download_urls if 'ChatBot_v' in url]
        if bot_urls:
            random_bot_url = random.choice(bot_urls)

            parsed_url = urlparse(random_bot_url)
            file_name = os.path.basename(parsed_url.path)

            response_file = requests.get(random_bot_url, stream=True)
            if response_file.status_code == 200:
                with zipfile.ZipFile(BytesIO(response_file.content), 'r') as zip_ref:
                    zip_ref.extractall(chatbot_path)

sys.exit()