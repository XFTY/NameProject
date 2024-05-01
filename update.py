import json
import traceback
import markdown
import requests
import wget

# 通常情况下，不要手贱调成True，不然程序无法正常运行
debugMode = False

def getUpdateResponse():
    try:
        url = "https://gitee.com/api/v5/repos/XFTYC/NameProject/releases/latest"
        response = requests.get(url)
        return response.json()
    except:
        print(traceback.format_exc())
        return None


def checkUpdate(response, thisNameProjectVersion):
    if thisNameProjectVersion != response["tag_name"]:
        return True
    else:
        return False

def getUpdateInfo(response, needmarkdown=False):
    if needmarkdown:
        body = response["body"].replace("\n", "")
        return markdown.markdown(body, extensions=['markdown.extensions.extra'])
    else:
        return response["body"]

def getUpdateTagName(response):
    return response["tag_name"]


if __name__ == '__main__':
    response = getUpdateResponse()
    print(checkUpdate(response, "v1.0.0"))
    print(getUpdateInfo(response))
