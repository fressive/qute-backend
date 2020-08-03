import config
import requests
from pixivpy3 import ByPassSniApi

RECOMMENDED = 0
KONACHAN = 1
YANDERE = 2
DANBOORU = 3
PIXIV = 4

pixivApi = ByPassSniApi()
pixivApi.require_appapi_hosts()

def login():
    if config.pixiv_login_mode == 0:
        pixivApi.auth(refresh_token=config.pixiv_refresh_token)
    else:
        pixivApi.login(username=config.pixiv_username, password=config.pixiv_password)

    if config.pixiv_print_refresh_token:
        print("Your pixiv account refresh_token is '{}'.".format(pixivApi.refresh_token))

