# -*- coding: UTF-8 -*-
import lark_oapi as lark
from lark_oapi.api.drive.v1 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("YOUR_APP_ID") \
        .app_secret("Bearer t-g1045tc0CNPSQTOKBGBNHTQDQVRSAYVOAXGMHF7P ") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: DeleteFileRequest = DeleteFileRequest.builder() \
        .build()

    # 发起请求
    response: DeleteFileResponse = client.drive.v1.file.delete(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.drive.v1.file.delete failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()
