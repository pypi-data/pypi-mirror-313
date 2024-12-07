import os
from http.client import responses
from urllib.parse import unquote

import requests
import json

from tqdm import tqdm


def fetch_ofl_list_json(api_url="https://api.github.com/repos/google/fonts/contents/ofl"):
    """
    :param api_url:
    :return:
    {
        "name": "abeezee",
        "path": "ofl/abeezee",
        "sha": "83498679c7af31b3e2f28d05e812f6f81c9fe4f6",
        "size": 0,
        "url": "https://api.github.com/repos/google/fonts/contents/ofl/abeezee?ref=main", # WE NEED THIS!
        "html_url": "https://github.com/google/fonts/tree/main/ofl/abeezee",
        "git_url": "https://api.github.com/repos/google/fonts/git/trees/83498679c7af31b3e2f28d05e812f6f81c9fe4f6",
        "download_url": null,
        "type": "dir",
        ...
    }
    """
    headers = {"Authorization": f"token {os.getenv("ACCESS_TOKEN")}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data
    else:
        print(f"Failed to fetch github with token: {os.getenv('ACCESS_TOKEN')}")
        print(f"Please set github token with: `googlefonts config --token your_token`")
        print(f"Or you can temporary use github token with: `googlefonts list --token your_token`")
        exit(1)


def get_ttf_download_url_list_json(url_content):
    """

    :param url_content:
    [
        {
            "path": "ABeeZee-Italic.ttf",
            "mode": "100644",
            "type": "blob",
            "sha": "da4bf4754d583f833e0dd276094697275c0a53d2",
            "size": 47012,
            "url": "https://api.github.com/repos/google/fonts/git/blobs/da4bf4754d583f833e0dd276094697275c0a53d2"
        },
        {
            "path": "ABeeZee-Regular.ttf",
            "mode": "100644",
            "type": "blob",
            "sha": "2ecf01bdec7b6a8568825da840897f9b0aee8a86",
            "size": 46016,
            "url": "https://api.github.com/repos/google/fonts/git/blobs/2ecf01bdec7b6a8568825da840897f9b0aee8a86"
        }
        ...
    ]

    :return:
    """
    download_url_list = []
    if url_content:
        for item in url_content:
            if ".ttf" in str(item["path"]):
                download_url_list.append(item["download_url"])
        return download_url_list
    else:
        print("\033[31mFailed to get download urls. Please retry!\033[0m")
        exit(-1)


def get_font_names(ofl_font_json_list):
    font_names = []
    for font_json in ofl_font_json_list:
        font_names.append(font_json["name"])
    return font_names


def fetch_ttf_url_download_list_by_name(ofl_list, font_name, force=False):
    url = None
    if force:
        url = f"https://api.github.com/repos/google/fonts/contents/ofl/{font_name}?ref=main"
    else:
        for ofl in ofl_list:
            if ofl["name"] == font_name:
                print(f"font_name: {font_name}")
                print(f"name: {ofl['name']}")
                url = ofl["url"]
                print(f"url: {url}")
    if url is None:
        raise Exception(f"Can not find url for font name: {font_name}")

    tqdm.write(f"Fetching fonts {font_name} from formulas")
    headers = {"Authorization": f"token {os.getenv("ACCESS_TOKEN")}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        print(f"\033[31mFailed to get download urls for {font_name}. Please retry!\033[0m")
        exit(-1)
    url_content = json.loads(resp.text)
    tqdm.write(f"Successfully fetched fonts {font_name} from formulas")
    download_list = []
    for download in get_ttf_download_url_list_json(url_content):
        name = unquote(download.split("/")[-1])
        download_url = download
        download_list.append({
            "name": name,
            "download_url": download_url,
        })

    if download_list:
        return download_list
    else:
        exit(-1)


if __name__ == '__main__':
    ttf_download_list = fetch_ttf_url_download_list_by_name("abeezee", True)
    print(ttf_download_list)
