#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_chanjet
=================================================
"""
from types import NoneType

import requests
import xmltodict
from addict import Dict
from bs4 import BeautifulSoup


class Pfm(object):
    def __init__(self, base_url: str = None):
        base_url = base_url if isinstance(base_url, str) else ""
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

    def _default_response_handler(self, response: requests.Response = None):
        if isinstance(response, requests.Response) and response.status_code == 200:
            xml_doc = BeautifulSoup(
                response.text,
                features="xml"
            )
            if isinstance(xml_doc, NoneType):
                return [], response

            results = Dict(
                xmltodict.parse(
                    xml_doc.find("NewDataSet").encode(
                        "utf-8"))
            ).NewDataSet.Table
            if isinstance(results, list):
                return results, response
            if isinstance(results, dict) and len(results.keys()):
                return [results], response

    def get_data_set(
            self,
            sql: str = None,
            method: str = "POST",
            url: str = "/estate/webService/ForcelandEstateService.asmx?op=GetDataSet",
            **kwargs
    ):
        """
        get data set
        :param sql:
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        method = method if isinstance(method, str) else "POST"
        url = url if isinstance(url, str) else "/estate/webService/ForcelandEstateService.asmx?op=GetDataSet"
        if not url.startswith("http"):
            if not url.startswith("/"):
                url = f"/{url}"
            url = f"{self.base_url}{url}"
        headers = kwargs.get("headers", {})
        headers.setdefault("Content-Type", "text/xml; charset=utf-8")
        kwargs["headers"] = headers
        data = xmltodict.unparse(
            {
                "soap:Envelope": {
                    "@xmlns:soap": "http://schemas.xmlsoap.org/soap/envelope/",
                    "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                    "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                    "soap:Body": {
                        "GetDataSet": {
                            "@xmlns": "http://zkhb.com.cn/",
                            "sql": f"{sql}",
                        }
                    }
                }
            }
        )
        kwargs["data"] = data
        response = requests.request(method=method, url=url, **kwargs)
        return self._default_response_handler(response)

    def query_actual_collection_with_conditionals(
            self,
            columns: str = None,
            conditionals: str = None
    ):
        """
        conditionals and (cml.EstateID= and cbi.ItemName='' and rd.RmNo='' and cfi.EDate>='')
        :param columns:
        :param conditionals:
        :return:
        """
        columns = columns if isinstance(columns, str) else ""
        conditionals = conditionals if isinstance(conditionals, str) else ""
        sql = f"""select
                    {columns}
                    cml.ChargeMListID,
                    cml.ChargeMListNo,
                    cml.ChargeTime,
                    cml.PayerName,
                    cml.ChargePersonName,
                    cml.ActualPayMoney,
                    cml.EstateID,
                    cml.ItemNames,
                    ed.Caption as EstateName,
                    cfi.ChargeFeeItemID,
                    cfi.ActualAmount,
                    cfi.SDate,
                    cfi.EDate,
                    cfi.RmId,
                    rd.RmNo,
                    cml.CreateTime,
                    cml.LastUpdateTime,
                    cbi.ItemName,
                    cbi.IsPayFull
                from
                    chargeMasterList cml,EstateDetail ed,ChargeFeeItem cfi,RoomDetail rd,ChargeBillItem cbi
                where
                    cml.EstateID=ed.EstateID
                    and
                    cml.ChargeMListID=cfi.ChargeMListID
                    and
                    cfi.RmId=rd.RmId
                    and
                    cfi.CBillItemID=cbi.CBillItemID
                    {conditionals}
                order by cfi.ChargeFeeItemID desc;
                """
        return self.get_data_set(sql=sql)
