import asyncio

import lark_oapi as lark
from lark_oapi.api.contact.v3 import *


def main1():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: BatchGetIdUserRequest = BatchGetIdUserRequest.builder() \
        .user_id_type("open_id") \
        .request_body(BatchGetIdUserRequestBody.builder()
                      .emails([])
                      .mobiles(["15001337958"])
                      .include_resigned(False)
                      .build()) \
        .build()

    # 发起请求
    response: BatchGetIdUserResponse = client.contact.v3.user.batch_get_id(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.contact.v3.user.batch_get_id failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


# 异步方式
async def main2():
    # 创建client
    client = lark.Client.builder() \
        .app_id(lark.APP_ID) \
        .app_secret(lark.APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: BatchGetIdUserRequest = BatchGetIdUserRequest.builder() \
        .user_id_type("open_id") \
        .request_body(BatchGetIdUserRequestBody.builder()
                      .emails([])
                      .mobiles(["15001337958"])
                      .include_resigned(False)
                      .build()) \
        .build()

    # 发起请求
    response: BatchGetIdUserResponse = await client.contact.v3.user.abatch_get_id(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.contact.v3.user.abatch_get_id failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
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
    request: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.POST) \
        .uri("/open-apis/contact/v3/users/batch_get_id") \
        .token_types({lark.AccessTokenType.TENANT}) \
        .queries([("user_id_type", "open_id")]) \
        .body({"emails": ["xxxx@bytedance.com"], "mobiles": ["15001337958"]}) \
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
    request: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.POST) \
        .uri("/open-apis/contact/v3/users/batch_get_id") \
        .token_types({lark.AccessTokenType.TENANT}) \
        .queries([("user_id_type", "open_id")]) \
        .body({"mobiles": ["15001337958"]}) \
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
