import json
import time
import uuid
from typing import Optional
from urllib.parse import urljoin

from lxml import etree
from pydantic import BaseModel
from requests import Session as S, Request as Req, Response as Res
from lxml import html

from erp_as.config import DEFAULT_HEADERS, Erp321BaseUrl, ErpApiBaseUrl


class UserInfoType(BaseModel):
    u_cid: Optional[str]
    u_co_id: Optional[str]
    u_co_name: Optional[str]
    u_id: Optional[str]
    u_name: Optional[str]
    u_lid: Optional[str]


class Session(S):
    def __init__(self):
        super().__init__()
        self.headers.update(DEFAULT_HEADERS)
        self.proxies = {'http': "", 'https': ""}
        self.viewstateItems = dict()
        self.userInfo: Optional[UserInfoType]

    def erpSend(self, request: Req, **kwargs) -> Res:
        if not request.headers:
            request.headers = self.headers
        hostType = getattr(request, 'hostType', None)
        if hostType:
            send_func = getattr(self, hostType + "Send", None)
            if send_func is None:
                raise Exception(f"{hostType}没有这个域的send方法")
            return send_func(request, **kwargs)
        raise Exception('hostType is None')

    def erp321Send(self, request, **kwargs):
        request.url = urljoin(Erp321BaseUrl, request.url)
        if request.method == 'POST':
            request.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            viewstate_ = self.get_viewstate(request.url).items()
            request.data.update(viewstate_)

        prepare_request = self.prepare_request(request)
        res = super().send(prepare_request, **kwargs)
        if request.callback:
            if request.callback == 'as_item':
                html_content = res.text
                tree = html.fromstring(html_content)
                div = tree.xpath('//div[@id="_jt_data"]')
                if div:
                    content = div[0].text_content()
                    return json.loads(content)['datas']
                return None
            return request.callback(res)
        return res

    def erpApiSend(self, request, **kwargs):
        request.url = urljoin(ErpApiBaseUrl, request.url)
        res = super().send(self.prepare_request(request), **kwargs)
        if request.callback:
            if request.callback == 'login':
                res_json = res.json()
                if res_json.get('code') == 0:
                    self.cookies.set('SessionCode', str(uuid.uuid4()))
                    self.userInfo = UserInfoType(**res_json.get('cookie'))
            else:
                return request.callback(res)
        return res

    def get_viewstate(self, url):
        if self.viewstateItems.get(url) and self.viewstateItems.get(url).get("updateTime") > time.time() - 60 * 60 * 24:
            return self.viewstateItems.get(url)
        if not self.viewstateItems.get(url):
            self.viewstateItems.update({url: {"updateTime": time.time()}})
        res = self.get(url)
        etree_xpath = etree.HTML(res.text)

        def extract_first(xpath):
            r = etree_xpath.xpath(xpath)
            return r[0] if r else None

        self.viewstateItems.get(url).update(
            {
                "__VIEWSTATE": extract_first("//*[@id='__VIEWSTATE']/@value"),
                "__VIEWSTATEGENERATOR": extract_first("//*[@id='__VIEWSTATEGENERATOR']/@value"),
                "__EVENTVALIDATION": extract_first("//*[@id='__EVENTVALIDATION']/@value"),
                "owner_co_id": 10174711,
                "authorize_co_id": self.userInfo.u_co_id
            }
        )
        return self.viewstateItems.get(url)


class Request(Req):

    def __init__(self,
                 hostType: str = 'erp321',
                 callback: callable = None,
                 **kwargs
                 ):
        self.hostType = hostType
        self.callback = callback
        super().__init__(**kwargs)
