import asyncio

from requests_toolbelt import MultipartEncoder

import lark_oapi as lark
from lark_oapi.api.im.v1 import *


def main1():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    file = open("/Users/bytedance/Downloads/test.png", "rb")
    request: CreateImageRequest = CreateImageRequest.builder() \
        .request_body(CreateImageRequestBody.builder()
                      .image_type("message1")
                      .image(file)
                      .build()) \
        .build()

    # 发起请求
    response: CreateImageResponse = client.im.v1.image.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.image.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: {lark.JSON.marshal(response.error)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


async def main2():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    file = open("/Users/bytedance/Downloads/test.png", "rb")
    request: CreateImageRequest = CreateImageRequest.builder() \
        .request_body(CreateImageRequestBody.builder()
                      .image_type("message")
                      .image(file)
                      .build()) \
        .build()

    # 发起请求
    response: CreateImageResponse = await client.im.v1.image.acreate(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.image.acreate failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


def main3():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    file = open("/Users/bytedance/Downloads/test.png", "rb")
    data = {"image_type": "message", "image": file}
    body = MultipartEncoder(lark.Files.parse_form_data(data))
    request: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.POST) \
        .uri("/open-apis/im/v1/images") \
        .headers({"Content-Type": body.content_type}) \
        .token_types({lark.AccessTokenType.TENANT}) \
        .body(body) \
        .build()

    # 发起请求
    response: lark.BaseResponse = client.request(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(str(response.raw.content, lark.UTF_8))


async def main4():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    file = open("/Users/bytedance/Downloads/test.png", "rb")
    request: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.POST) \
        .uri("/open-apis/im/v1/images") \
        .token_types({lark.AccessTokenType.TENANT}) \
        .body({"image_type": "message", "image": file}) \
        .build()

    # 发起请求
    response: lark.BaseResponse = await client.arequest(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(str(response.raw.content, lark.UTF_8))


if __name__ == "__main__":
    main1()
    asyncio.run(main2())
    main3()
    asyncio.run(main4())
