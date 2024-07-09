import re
import time

import requests
import xmltodict
from pymongo.errors import DuplicateKeyError

from db_util import *


def get_timestamp(pub_date):
    time_array = time.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
    timestamp = time.mktime(time_array)
    return int(timestamp)


def get_time(timestamp):
    time_local = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def get_magnet_link(link):
    magnet_head = "magnet:?xt=urn:btih:"
    pattern = re.compile(r'(?<=show-)(.*?)(?=.html)')
    magnet_hash = pattern.search(link).group(1)
    return magnet_head + magnet_hash


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3622.0 Safari/537.36',
}


def get_ep(raw_title):
    try:
        pattern = re.compile(r'(?<=\[)(\d\d)(?=\]|END\]|[vV]\d\])')
        ep = pattern.search(raw_title).group(1)
    except AttributeError:
        pattern = re.compile(r'(?<=- )(\d\d)(?= \[)')
        ep = pattern.search(raw_title).group(1)
    if 0 <= int(ep) <= 70:
        return ep


def build_episode_dict(anime_data, data):
    episode = {}
    episode['_id'] = int("{}{}".format(anime_data['_id'], get_ep(data['title'])))
    episode['anime_id'] = anime_data['_id']
    episode['name'] = anime_data['name']
    episode['ep'] = int(get_ep(data['title']))
    episode['raw_title'] = data['title']
    episode['magnet'] = get_magnet_link(data['link'])
    episode['torrent'] = data["enclosure"]["@url"]
    episode['pub_date'] = get_time(get_timestamp(data['pubDate']))
    episode['download_flag'] = False
    return episode


def check_episode(ep_dict):
    if get_episode_pub_date(ep_dict['_id']) < ep_dict['pub_date']:  # 数据库中的是旧版本
        delete_episode(ep_dict['_id'])
        add_episode(ep_dict)


def get_episode(anime_data):
    r = requests.get(anime_data['link'], headers=headers)
    r.encoding = 'utf-8'
    data = xmltodict.parse(r.text)['rss']['channel']['item']
    if isinstance(data, dict):
        data = [data]
    last_time = get_timestamp(data[0]['pubDate'])
    if last_time > anime_data['last_time']:
        for d in data:
            if get_timestamp(d['pubDate']) > anime_data['last_time']:
                episode = build_episode_dict(anime_data, d)
                try:
                    add_episode(episode)
                except DuplicateKeyError:
                    check_episode(episode)
            else:
                break
        update_timestamp(anime_data['_id'], last_time)  # 更新last_time
