import json

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a6867a2d54db900e") \
        .app_secret("nDeZWWv2ORKiFkrKlvXBhetOtDNc0s2x") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: CreateDocumentBlockDescendantRequest = CreateDocumentBlockDescendantRequest.builder() \
        .document_id("AOludXaDLoRtYyxAnOccjnBnn8d") \
        .block_id("AOludXaDLoRtYyxAnOccjnBnn8d") \
        .document_revision_id(-1) \
        .request_body(CreateDocumentBlockDescendantRequestBody.builder()
            .children_id(["headingid_1", "table_id_1"])
            .index(0)
            .descendants([Block.builder()
                .block_id("headingid_1")
                .children([])
                .block_type(3)
                .heading1(Text.builder()
                    .elements([TextElement.builder()
                        .text_run(TextRun.builder()
                            .content("简单表格")
                            .build())
                        .build()
                        ])
                    .build())
                .build(),
                Block.builder()
                .block_id("table_id_1")
                .children(["table_cell1", "table_cell2"])
                .block_type(31)
                .table(Table.builder()
                    .property(TableProperty.builder()
                        .row_size(1)
                        .column_size(2)
                        .build())
                    .build())
                .build(),
                Block.builder()
                .block_id("table_cell1")
                .children(["table_cell1_child1", "table_cell1_child2"])
                .block_type(32)
                .table_cell(TableCell.builder()
                    .build())
                .build(),
                Block.builder()
                .block_id("table_cell2")
                .children(["table_cell2_child"])
                .block_type(32)
                .table_cell(TableCell.builder()
                    .build())
                .build(),
                Block.builder()
                .block_id("table_cell1_child1")
                .children([])
                .block_type(13)
                .ordered(Text.builder()
                    .elements([TextElement.builder()
                        .text_run(TextRun.builder()
                            .content("list 1.1")
                            .build())
                        .build()
                        ])
                    .build())
                .build(),
                Block.builder()
                .block_id("table_cell1_child2")
                .children([])
                .block_type(13)
                .ordered(Text.builder()
                    .elements([TextElement.builder()
                        .text_run(TextRun.builder()
                            .content("list 1.2")
                            .build())
                        .build()
                        ])
                    .build())
                .build(),
                Block.builder()
                .block_id("table_cell2_child")
                .children([])
                .block_type(2)
                .text(Text.builder()
                    .elements([TextElement.builder()
                        .text_run(TextRun.builder()
                            .content("")
                            .build())
                        .build()
                        ])
                    .build())
                .build()
                ])
            .build()) \
        .build()

    # 发起请求
    response: CreateDocumentBlockDescendantResponse = client.docx.v1.document_block_descendant.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document_block_descendant.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()
