import requests

if __name__ == "__main__":
    url = "https://open.feishu.cn/approval/openapi/v2/file/upload"

    payload={"type": "attachment", "name": "adfadsf.pdf"}
    files=[
        ('content',('adfadsf.pdf',open('/Users/bytedance/Downloads/2305.14283.pdf','rb'),''))
    ]
    headers = {
       'Authorization': 'Bearer t-g1047hadMHRVASE2TQSE5ANXNZ6F5NAPE5EUXOB2',
       # 'User-Agent': 'oapi-sdk-python/v1.2.9',
       # 'Accept': '*/*',
       # 'Host': 'open.feishu.cn',
       # 'Connection': 'keep-alive',
       # 'Content-Type': 'multipart/form-data; boundary=--------------------------246570029802741544561131'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    from requests_toolbelt.utils import dump

    data2 = dump.dump_all(response)

    print(data2)

    print(response.text)
