# coding: utf-8
# Project：erp_out_of_stock
# File：order.py
# Author：李福成
# Date ：2024-04-28 18:23
# IDE：PyCharm
# 订单API
from datetime import datetime
from typing import Optional, Union
from erp_as.erpRequest import Request
from erp_as.utils.util import dumps, getDefaultParams, JTable1, generateChangeBatchItems


def PrintRequest(data: dict, method: str = 'LoadDataToJSON',
                 url: str = '/app/print/print/Printer.aspx', **kwargs) -> Request:
    params = getDefaultParams({'defaultParams': ["ts___"], 'am___': method})
    if kwargs.get('params'):
        params.update(kwargs.get('params'))
    return Request(
        method='POST',
        url=url,
        params=params,
        data={
            **data
        },
        callback=JTable1
    )


def GetCurrentMoudleSupportJsonPrint(u_id,MAC_ID,randomData,skujson):
    '''
    反确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return PrintRequest({
        "ip": "",
        "uid": u_id,
        "coid": "10174711",
        "data": {
            "isDebugger": False,
            "jstServerVersion": 2,
            "jstJsVersion": 1,
            "jstClientVersion": "3.0.3.301",
            "jstClientId": MAC_ID,
            "clientDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "controlVersion": "0.0.0.0",
            "control": "JST",
            "appName": "ERP",
            "moudle": "AS",
            "preview": 0,
            "previewType": "PDF",
            "printers": "导出为WPS PDF,OneNote (Desktop),Microsoft XPS Document Writer,Microsoft Print to PDF,Fax",
            "service": "",
            "params": {
                "skusJson": skujson,
                "uc_co_id_info": {
                    "UserId": u_id,
                    "Connectionid": 10174711,
                    "WmsCoId": 10174711,
                    "OwnerCoId": 10174711,
                    "SrcOwnerCoId": 10174711,
                    "TemplateCoIds": [
                        10174711
                    ],
                    "ConfigCompanyId": 10174711
                },
                "jstClientVersion": "3.0.3.301",
                "identifiedNo": MAC_ID,
                "json_print_moudle": "goods_after_sale",
                "authorize_co_id": 10174711,
                "co_id": "10174711",
                "u_id": u_id,
                "type": "tags",
                "sub_type": "jm",
                "service_name": "TagAfterSaleJsonPrint"
            },
            "second": 2,
            "randomData": randomData,
            "concurrentId": "0272793a-cdc9-5aa2-c5c7-8207f0acbb37",
            "ip": "",
            "uid": u_id,
            "coid": "10174711",
            "PageMoudle": "售后(退货退款)",
            "queryString": "owner_co_id=10174711&authorize_co_id=10174711",
            "isUseJsonPrint": True
        }
    },
        url='/erp/webapi/PrintApi/Print/GetPrintDatas'
    )


