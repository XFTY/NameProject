#! /usr/bin/env python3
# --------------------------------------------------------------------------------------------------
# | 版权所有 XFTY，保留所有权利。
# | 代码遵循Apache 2.0开源协议，浏览在根目录的LICENSE文件以获取更多信息。
# |
# | Copyright (c) 2021-2022 XFTY, All Rights Reserved.
# | Licensed under the Apache License 2.0. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------------

debugMode = True

import json
import requests
import markdown
import traceback

class update:
    def __init__(self):
        pass
    def getUpdateResponse(self):
        if debugMode:
            with open("testData/gitapi.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            try:
                url = "https://gitee.com/api/v5/repos/XFTYC/NameProject/releases/latest"
                response = requests.get(url)
                return response.json()
            except:
                print(traceback.format_exc())
                return None

    def checkUpdate(self, response, thisNameProjectVersion):
        if thisNameProjectVersion != response["tag_name"]:
            return True
        else:
            return False


    def getUpdateInfo(self, response, needmarkdown=False):
        if needmarkdown:
            body = response["body"].replace("\n", "")
            return markdown.markdown(body, extensions=['markdown.extensions.extra'])
        else:
            return response["body"]


    def getUpdateTagName(self, response):
        return response["tag_name"]

    def getUpdateDownloadUrl(self, response):
        return response["assets"][0]["browser_download_url"]

class updater(update):
    def __init__(self):
        super().__init__()
        self.getUpdateInfo()



updater()