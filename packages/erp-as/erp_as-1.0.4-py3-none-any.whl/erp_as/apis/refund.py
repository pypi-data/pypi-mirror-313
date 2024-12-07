from datetime import datetime, timedelta
from typing import Optional
from erp_as.erpRequest import Request
from erp_as.utils.util import (dumps, getDefaultParams, JTable1)


def RefundRequest(data: dict, method: str = 'LoadDataToJSON',
                  url: str = '/app/order/refund/refund.aspx', **kwargs) -> Request:
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


# 根据售后单号查询退款单
def refundListByafterId(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []

    def generate_date_strings():
        # 获取当天日期
        today_date = datetime.now().strftime("%Y-%m-%d")
        # 计算三个月之前的日期
        three_months_ago_date = (datetime.now() - timedelta(days=3 * 30)).strftime("%Y-%m-%d")
        return [three_months_ago_date, today_date]

    return RefundRequest({
        'id_type': 'as_id',
        'as_id': queryData[0].get('v'),
        'date_type': 'pay_date',
        'pay_date': generate_date_strings(),
        '_jt_page_size': page_size,
        "__CALLBACKID": "JTable1",
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
    },
        method='LoadDataToJSON'
    )


# 取消退款完成
def unfinish(queryData: Optional[list] = None):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return RefundRequest({
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "UnFinishs",
                "Args": queryData,
                "CallControl": "{page}"
            }
        ),
    },
        method='UnFinishs'
    )


# 退款完成
def finish(queryData: Optional[list] = None):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return RefundRequest({
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "Finishs",
                "Args": queryData,
                "CallControl": "{page}"
            }
        ),
    },
        method='Finishs'
    )


# 确认退款订单
def confirm(pay_ids):
    '''
    确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return RefundRequest({
        'isCB': '0',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "Confirms",
                "Args": pay_ids,
                "CallControl": "{page}"
            }
        ),
    },
        method='Confirms',
        url='/app/order/refund/refund.aspx'
    )
