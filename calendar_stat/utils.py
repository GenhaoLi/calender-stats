import os
import re
from datetime import datetime

import requests
import logging

import calendar_stat
from calendar_stat.constants import EVENT_GROUP_NAME

p = os.path

def get_data_dir():
    script_dir = p.dirname(p.abspath(__file__))
    return p.normpath(p.join(script_dir, '../data'))

data_dir = get_data_dir()

def download_file(url, save_path):
    http_url = re.sub(r'^webcal', 'http', url)
    response = requests.get(http_url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
        print(f"Downloaded file to {save_path}")


def download_to_local(url):
    """
    Downloads from the given URL and saves it to the local `data` directory
    :return: The path to the downloaded file
    """
    ics_filename = "calendar.ics"
    download_dest = p.join(data_dir, ics_filename)
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    download_file(url, download_dest)
    return download_dest


def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hours, {minutes} minutes"


def truncate_time_zone(dt):
    return dt.replace(tzinfo=None)

def get_today_date():
    # get today's date, e.g. 2024-07-04
    return datetime.now().strftime('%Y-%m-%d')

today_date = get_today_date()

def config_logger() -> logging.Logger:
    logger = logging.getLogger(calendar_stat.__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    debug_file_handler = logging.FileHandler('../data/debug.log', mode='w')
    event_group_file_handler = logging.FileHandler(f'../data/{EVENT_GROUP_NAME}_till_{today_date}.txt', mode='w')

    console_handler.setLevel(logging.DEBUG)
    debug_file_handler.setLevel(logging.DEBUG)
    event_group_file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(debug_file_handler)
    logger.addHandler(event_group_file_handler)
    return logger












