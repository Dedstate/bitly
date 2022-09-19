import argparse
from urllib.parse import urlparse
import requests
from settings import BITLY_TOKEN


def shorten_link(token, long_link):
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"long_url": long_link}

    responce = requests.post(url, headers=headers, json=data)
    responce.raise_for_status()  # check status
    return responce.json()["link"]


def total_clicks(token, short_link):
    headers = {"Authorization": f"Bearer {token}"}
    url_parsed = urlparse(short_link)
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_parsed.netloc + url_parsed.path}/clicks"

    responce = requests.get(url, headers=headers)
    responce.raise_for_status()
    return responce.json()["link_clicks"][0]["clicks"]


def is_bitlink(token, link):
    headers = {"Authorization": f"Bearer {token}"}
    url_parsed = urlparse(link)
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{url_parsed.netloc + url_parsed.path}"

    responce = requests.get(url, headers=headers)
    return responce.ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("link")
    args = parser.parse_args()
    user_input = args.link

    if is_bitlink(BITLY_TOKEN, user_input):
        print(total_clicks(BITLY_TOKEN, user_input))
    else:
        print(shorten_link(BITLY_TOKEN, user_input))
