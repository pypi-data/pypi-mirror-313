import json
import time

from requests import Response


def dumps(obj, **kwargs):
    return json.dumps(obj, **kwargs, separators=(',', ':'), ensure_ascii=False)


def getDefaultParams(params: dict = None) -> dict:
    rand_params = {
        '_c': lambda: 'jst-epaas',
        '_t': lambda: int(time.time() * 1000),
        '_float': lambda: True,
        'ts___': lambda: int(time.time() * 1000),
        'am___': lambda: 'LoadDataToJSON',
        'owner_co_id' : lambda: 1,
        'authorize_co_id' : lambda: 1
    }
    if params.get('defaultParams'):
        for k in params.get('defaultParams'):
            params.update({k: rand_params.get(k)()})
    del params['defaultParams']
    return params


def JTable1(res: Response):
    text = res.text
    res_data = json.loads(text[text.find('{'):])
    if res_data.get('ReturnValue'):
        try:res_data['ReturnValue'] = json.loads(res_data.get('ReturnValue'))
        except:pass
    res._content = json.dumps(res_data).encode('utf-8')
    return res




def generateChangeBatchItems(items: list, newBatchItems):
    new_items = []
    newBatchItems_to_dict = {i['oi_id']: i for i in newBatchItems}
    for sku in items:
        if sku['oi_id'] not in newBatchItems_to_dict: continue
        new_items.extend([{
            **{k: sku[k] for k in ['is_gift', 'qty']},
            "price": -99999,
            "amount": "-99999",
            "is_del": False,
            "is_new": True,
            **newBatchItems_to_dict[sku['oi_id']],
            "oi_id": 0,
        }, {
            "is_del": True,
            "il_id": None,
            "is_new": False,
            **{k: sku[k] for k in ['sku_id', 'qty', 'price', 'amount', 'is_gift', 'oi_id', 'sku_type']},
        }])
        del newBatchItems_to_dict[sku['oi_id']]
    if newBatchItems_to_dict:
        raise ValueError(f'未找到以下商品: {newBatchItems_to_dict}')
    return new_items