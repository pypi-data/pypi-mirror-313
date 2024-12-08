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

import py3_requests
import xmltodict
from addict import Dict
from bs4 import BeautifulSoup
from requests import Response


class ReqeustUrl:
    BASE_URL: str = ""
    GET_DATA_SET_URL: str = "/estate/webService/ForcelandEstateService.asmx?op=GetDataSet"


class ResponseHandler:
    @staticmethod
    def normal_handler(response: Response = None):
        if isinstance(response, Response):
            xml_doc = BeautifulSoup(
                response.text,
                features="xml"
            )
            if isinstance(xml_doc, NoneType):
                return []

            results = Dict(
                xmltodict.parse(
                    xml_doc.find("NewDataSet").encode(
                        "utf-8"))
            ).NewDataSet.Table
            if isinstance(results, list):
                return results
            if isinstance(results, dict) and len(results.keys()):
                return [results]
        raise Exception(f"Response Handler Error {response.status_code}|{response.text}")


class Pfm(object):
    def __init__(self, base_url: str = ""):
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url

    def get_data_set(
            self,
            sql: str = None,
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
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("response_handler", ResponseHandler.normal_handler)
        kwargs.setdefault("url", f"{ReqeustUrl.GET_DATA_SET_URL}")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("headers", Dict())
        kwargs.headers.setdefault("Content-Type", "text/xml; charset=utf-8")
        kwargs.setdefault("data", Dict())
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
        kwargs.data = data
        return py3_requests.request(**kwargs.to_dict())

    def query_actual_collection_with_conditionals(
            self,
            columns: str = None,
            conditionals: str = None,
            **kwargs
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
        kwargs = Dict(kwargs)
        kwargs.setdefault("sql", sql)
        return self.get_data_set(**kwargs)
