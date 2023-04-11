import argparse
import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


def shorten_link(user_input, token):
    url = "https://api-ssl.bitly.com/v4/shorten"
    payload = {
        "long_url": user_input
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, 
    headers=headers)
    response.raise_for_status()
    bitlink = response.json()["link"] 
    return bitlink


def count_clicks(token, bitlink):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(token, link):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{link}"
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    link = urlparse(args.url)
    link_parse = f"{link.netloc}{link.path}"
    try:
        if is_bitlink(token, link_parse):
            clicks_count = count_clicks(token, link_parse)
            print(clicks_count)
        else:
            bitlink = shorten_link(args.url, token)
            print(bitlink)
    except requests.exceptions.HTTPError:
            print("Неверная ссылка")


if __name__ == "__main__":
    main()
