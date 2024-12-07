from typing import Optional, Union, List
from erp_as.erpRequest import Request
from erp_as.utils.util import dumps, getDefaultParams, JTable1, generateChangeBatchItems


def OrderRequest(
        data: dict,
        method: str = 'LoadDataToJSON',
        url='/app/order/order/list.aspx',
        callbackid: str = 'JTable1',
        **kwargs
) -> Request:
    params = getDefaultParams({'defaultParams': ["ts___", "_c"], 'am___': method})
    if kwargs.get('params'):
        params.update(kwargs.get('params'))
    print(params)
    return Request(
        method='POST',
        url=url,
        params=params,
        data={
            '__CALLBACKID': callbackid,
            **data
        },
        callback=JTable1
    )


# 获取订单
def OrderList(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return OrderRequest({
        '_jt_page_size': page_size,
        '__CALLBACKPARAM': dumps(
            {
                "Method": "LoadDataToJSON",
                "Args": [
                    page_num,
                    dumps(queryData),
                    "{}"
                ]
            }
        ),
    }, method='LoadDataToJSON')


# 修改订单异常类型
def Questions(questionName: str, questionMsg: str, oid: Union[str, int]):
    '''
    修改订单异常类型
    :param questionName: 异常分类名称
    :param questionMsg:  异常信息
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return OrderRequest({
        '__CALLBACKPARAM': dumps(
            {"Method": "Questions", "Args": [questionName, questionMsg, str(oid)], "CallControl": "{page}"}
        ),
    },
        method='Questions')


# 转正常
def UnQuestions(oid: Union[str, int]):
    '''
    修改订单异常类型
    :param questionName: 异常分类名称
    :param questionMsg:  异常信息
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return OrderRequest({
        '__CALLBACKPARAM': dumps(
            {"Method": "UnQuestions", "Args": [str(oid)], "CallControl": "{page}"}
        ),
    },
        method='UnQuestions')


# 修改备注
def Remarks(oid: Union[str, int], remarksMsg: str = '', isAppendRemarks: bool = True, flag: str = None):
    '''
    修改备注
    :param oid:  内部订单号
    :param remarksMsg:  备注信息
    :param isAppendRemarks:  是否追加备注
    :param flag:  旗帜类型： 1:红  2:黄  3:绿  4:蓝   5:紫
    :return: 执行结果
    '''
    return OrderRequest({
        '__CALLBACKPARAM': dumps({
            "Method": "SaveAppendRemarks",
            "Args": [
                'null' if flag is None else str(flag),
                remarksMsg,
                str(oid),
                'True' if isAppendRemarks else 'False'
            ],
            "CallControl": "{page}"
        }),
    },
        method='SaveAppendRemarks')


# 换商品
def ChangeBatchItems(oid: Union[str, int], items: list, newBatchItems: List[dict]):
    '''
    换商品
    :param oid:  内部订单号
    :param oldBatchItems:  旧商品
    :param newBatchItems:  新商品
    :return: 执行结果
    '''
    return OrderRequest({
        '__CALLBACKPARAM': dumps({"Method": "ChangeBatchItem",
                                  "Args": [str(oid), dumps({"items": generateChangeBatchItems(items, newBatchItems)})],
                                  "CallControl": "{page}"}),
    }, method='ChangeBatchItem')


# 获取单号物流信息
def LogisticsInfo(params: dict):
    '''
    获取单号物流信息
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return OrderRequest(
        url='/app/order/order/lookExpress.aspx',
        params=params,
        data={
            '__CALLBACKPARAM': dumps({"Method": "LoadTrace", "CallControl": "{page}"}),
        }, method='LoadTrace',
        callbackid='ACall1'
    )
