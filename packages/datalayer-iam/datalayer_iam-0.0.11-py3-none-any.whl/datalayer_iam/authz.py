# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

from urllib.parse import urlparse


PROXY_HOST_ALLOW_LIST = set()

PROXY_HOST_ALLOW_LIST.add("api.linkedin.com")
PROXY_HOST_ALLOW_LIST.add("www.linkedin.com")


def check_proxy_url_is_allow_listed(url: str):
    u = urlparse(url)
    if u.scheme != "https":
        raise Exception("Not authorized.")
    print(u)
    print(u.hostname)
    if u.hostname not in PROXY_HOST_ALLOW_LIST:
        raise Exception("Not authorized.")
