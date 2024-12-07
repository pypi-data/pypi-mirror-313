import hashlib
import json
from datetime import datetime, timedelta
import re
from typing import Optional

import requests
import xmltodict

from iikoserver_api.schemas.account import Account
from iikoserver_api.schemas.cashshift import Cashshift
from iikoserver_api.schemas.conception import Conception
from iikoserver_api.schemas.corporation import CorporationStore
from iikoserver_api.schemas.employee import Employee
from iikoserver_api.schemas.incoming_invoice import IncomingInvoice
from iikoserver_api.schemas.nomenclature_group import NomenclatureGroup
from iikoserver_api.schemas.outgoing_invoice import OutgoingInvoice
from iikoserver_api.schemas.product import Product
from iikoserver_api.schemas.write_off import WriteOff
from iikoserver_api.services.implementation_act_builder import ImplementationActBuilder
from iikoserver_api.services.incoming_service_builder import IncomingServiceBuilder
from iikoserver_api.services.inventory_document_builder import InventoryDocumentBuilder
from iikoserver_api.services.olap_cash_shift_builder import OlapCashShiftBuilder, OlapCashShiftBuilderV2
from iikoserver_api.services.outgoing_service_builder import OutgoingServiceBuilder
from iikoserver_api.services.returning_invoice_builder import ReturningInvoiceBuilder


class IikoServerApi:
    # _default_headers = {'Content-Type': 'application/xml'}

    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = hashlib.sha1(password.encode()).hexdigest()
        self.token = None
        self.connected = False

    def send(self,
             action: str,
             method: str = 'GET',
             params: dict = None,
             headers: dict = None,
             data: any = None,
             json=None):
        # if headers is None:
        #     headers = self._default_headers
        url = f'{self.url}{action}/'
        response = requests.request(method=method, url=url, params=params, headers=headers, data=data, json=json)

        if response.ok:
            if action.startswith('v2'):
                return response.json()
            return response.content
        else:
            error_info = {
                "response_status": response.status_code,
                "response_info": response.content.decode()
            }
            raise ConnectionError(error_info)

    def auth(self):
        params = {
            'login': self.login,
            'pass': self.password,
        }
        response = self.send(action='auth', params=params)
        data = response.decode()
        self.token = data
        self.connected = True

    def logout(self):
        params = {
            'key': self.token
        }
        data = self.send(action='logout', params=params)
        self.token = None
        self.connected = False
        return data

    def export_outgoing_invoice(self, from_datetime: datetime,
                                to_datetime: datetime) -> Optional[list[OutgoingInvoice]]:
        params = {
            'key': self.token,
            'from': from_datetime.strftime('%Y-%m-%d'),
            'to': to_datetime.strftime('%Y-%m-%d'),
        }
        data = self.send(action='documents/export/outgoingInvoice', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        documents = xml_dict_data['outgoingInvoiceDtoes']
        if documents:
            documents = [documents['document']] if type(documents['document']) is dict else documents['document']
        else:
            return
        result = []
        for document in documents:
            document_items = document['items']
            if not document_items:
                continue
            document_items = document_items.get('item')
            if document_items:
                document_items = [document['items']['item']] \
                    if type(document['items']['item']) is dict else document['items']['item']
            else:
                continue
            dict_data = {'items': []}
            for key, value in document.items():
                if key == 'items':
                    continue
                key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                dict_data[key] = value

            for item in document_items:
                new_item = {}
                for key, value in item.items():
                    key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                    new_item[key] = value

                dict_data['items'].append(new_item)

            result.append(OutgoingInvoice(**dict_data))

        return result

    def export_incoming_invoice(self, from_datetime: datetime,
                                to_datetime: datetime) -> Optional[list[IncomingInvoice]]:
        params = {
            'key': self.token,
            'from': from_datetime.strftime('%Y-%m-%d'),
            'to': to_datetime.strftime('%Y-%m-%d'),
        }
        data = self.send(action='documents/export/incomingInvoice', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        documents = xml_dict_data['incomingInvoiceDtoes']
        if documents:
            documents = [documents['document']] if type(documents['document']) is dict else documents['document']
        else:
            return
        result = []
        for document in documents:
            document_items = document['items']
            if not document_items:
                continue
            document_items = document_items.get('item')
            if document_items:
                document_items = [document['items']['item']] \
                    if type(document['items']['item']) is dict else document['items']['item']
            else:
                continue
            dict_data = {'items': []}
            for key, value in document.items():
                if key == 'items':
                    continue
                key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                dict_data[key] = value

            for item in document_items:
                new_item = {}
                for key, value in item.items():
                    key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                    new_item[key] = value

                dict_data['items'].append(new_item)

            result.append(IncomingInvoice(**dict_data))

        return result or []

    def get_employee(self, pk: str) -> Optional[Employee]:
        params = {
            'key': self.token,
            # 'from': from_datetime.strftime('%Y-%m-%d'),
            # 'to': to_datetime.strftime('%Y-%m-%d'),
        }
        data = self.send(action=f'employees/byId/{pk}', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        employee = xml_dict_data['employee']
        dict_data = {}
        for key, value in employee.items():
            key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            if value in ['true', 'false']:
                value = True if value == 'true' else False
            dict_data[key] = value

        return Employee(**dict_data)
        # documents = xml_dict_data['incomingInvoiceDtoes']

    def export_nomenclature_group(self):
        params = {
            'key': self.token,
        }
        data = self.send(action='v2/entities/products/group/list', params=params)
        result = []
        for el in data:
            result.append(NomenclatureGroup(**el))
        return result

    def export_products(self):
        params = {
            'key': self.token,
        }
        data = self.send(action='v2/entities/products/list', params=params)
        result = []
        for el in data:
            result.append(Product(**el))
        return result

    def export_cashshifts(self, from_datetime: datetime, to_datetime: datetime, status: str = 'ANY'):
        params = {
            'key': self.token,
            'openDateFrom': from_datetime.strftime('%Y-%m-%d'),
            'openDateTo': to_datetime.strftime('%Y-%m-%d'),
            'status': status,
        }
        data = self.send(action='v2/cashshifts/list', params=params)
        result = []
        for el in data:
            result.append(Cashshift(**el))
        return result

    def export_cashshift_payments(self, pk: str):
        params = {
            'key': self.token,
            'hideAccepted': False
        }
        data = self.send(action=f'v2/cashshifts/payments/list/{pk}', params=params)
        return data

    def export_stores(self) -> list[CorporationStore]:
        params = {
            'key': self.token,
        }
        data = self.send(action='corporation/stores', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        stores = xml_dict_data['corporateItemDtoes']['corporateItemDto']
        results = []
        for store in stores:
            dict_data = {}
            for key, value in store.items():
                key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                if value in ['true', 'false']:
                    value = True if value == 'true' else False
                dict_data[key] = value
            results.append(CorporationStore(**dict_data))

        return results

    def get_terminals(self):
        params = {
            'key': self.token,
        }
        data = self.send('corporation/departments', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        return xml_dict_data

    def export_pal(self):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        end_date = datetime.now()
        start_date = end_date - timedelta(days=3)
        data = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Account.Name",
                "Account.Id",
                "Account.StoreOrAccount",
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": start_date.strftime('%Y-%m-%d'),
                    "to": end_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                }
            }
        }
        data = self.send('v2/reports/olap', method='POST', json=data, params=params)
        return data

    def export_write_offs(self, from_datetime: datetime, to_datetime: datetime,):
        params = {
            'key': self.token,
            'dateFrom': from_datetime.strftime('%Y-%m-%d'),
            'dateTo': to_datetime.strftime('%Y-%m-%d'),
        }
        data = self.send(action=f'v2/documents/writeoff', params=params)
        result = []
        for el in data.get('response', []):
            result.append(WriteOff(**el))
        return result

    def export_accounts(self):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        end_date = datetime.now() + timedelta(days=1)
        start_date = end_date - timedelta(days=90)
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Account.Name",
                "Account.Id",
                "Account.StoreOrAccount",
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": start_date.strftime('%Y-%m-%d'),
                    "to": end_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "Account.StoreOrAccount": {
                    "filterType": "IncludeValues",
                    "values": ["ACCOUNT"]
                }
            }
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        result = []
        for item in data.get('data', []):
            result.append(Account(**item))
        return result

    def export_suppliers(self) -> list[Employee]:
        params = {
            'key': self.token,
        }
        data = self.send(action='suppliers', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        employees = xml_dict_data['employees']['employee']
        result = []
        for employee in employees:
            dict_data = {}
            for key, value in employee.items():
                key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                if value in ['true', 'false']:
                    value = True if value == 'true' else False
                dict_data[key] = value
            result.append(Employee(**dict_data))

        return result

    def export_employees(self) -> list[Employee]:
        params = {
            'key': self.token,
        }
        data = self.send(action='employees', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        employees = xml_dict_data['employees']['employee']
        result = []
        for employee in employees:
            dict_data = {}
            for key, value in employee.items():
                key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
                if value in ['true', 'false']:
                    value = True if value == 'true' else False
                dict_data[key] = value
            result.append(Employee(**dict_data))

        return result

    def export_inventory(self, from_date: datetime = datetime.now() - timedelta(days=30), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'documentTypes': ['INCOMING_INVENTORY'],
            'dateFrom': from_date.strftime('%d.%m.%Y'),
            'dateTo': to_date.strftime('%d.%m.%Y'),
        }
        data = self.send(action='reports/storeOperations', params=params)
        xml_dict_data = xmltodict.parse(data.decode())
        items = xml_dict_data.get('storeReportItemDtoes') or {}
        items = items.get('storeReportItemDto', {})
        return InventoryDocumentBuilder(items).process()

    def export_incoming_service(self, from_date: datetime = datetime.now() - timedelta(days=3), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Document",
                "Account.Id",
                "Product.Id",
                "DateTime.Typed",
                "Counteragent.Id",
                "Conception.Code"
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "TransactionType": {
                    "filterType": "IncludeValues",
                    "values": ["INCOMING_SERVICE"]
                }
            },
            "aggregateFields": [
                "Sum.Incoming",
                "Sum.Outgoing",
                "Sum.ResignedSum",
                "Amount.Out",
                "Amount.In",
                "Amount"
            ]
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        return IncomingServiceBuilder(items).process()

    def export_outgoing_service(self, from_date: datetime = datetime.now() - timedelta(days=3), to_date: datetime = datetime.now() + timedelta(days=1)):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Document",
                "Account.Id",
                "Product.Id",
                "DateTime.Typed",
                "Counteragent.Id",
                "Account.CounteragentType",
                "Conception.Code"
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "TransactionType": {
                    "filterType": "IncludeValues",
                    "values": ["OUTGOING_SERVICE"]
                }
            },
            "aggregateFields": [
                "Sum.Incoming",
                "Sum.Outgoing",
                "Sum.ResignedSum",
                "Amount.Out",
                "Amount.In",
                "Amount"
            ]
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        return OutgoingServiceBuilder(items).process()

    def export_columns(self):
        params = {
            'key': self.token,
            'reportType': 'SALES'
        }
        data = self.send('v2/reports/olap/columns', method='GET', params=params)
        return data

    def export_implementation_act(self, from_date: datetime = datetime.now() - timedelta(days=2), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": ["TransactionType", "Account.Id", "Account.StoreOrAccount", "Account.Name"],
            "groupByColFields": [
                "Document",
                "Product.Id",
                "DateTime.Typed",
                "Conception.Code"
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "TransactionType": {
                    "filterType": "IncludeValues",
                    "values": ["SALES_REVENUE", "SESSION_WRITEOFF"]
                }
            },
            "aggregateFields": [
                "Sum.Incoming",
                "Sum.Outgoing",
                "Sum.ResignedSum",
                "Amount.Out",
                "Amount.In",
                "Amount"
            ]
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        result = ImplementationActBuilder(items).process()
        return result

    def export_olap_cash(self, from_date: datetime = datetime.now() - timedelta(days=2), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Document",
                "Session.CashRegister",
                "DateTime.Typed",
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "TransactionType": {
                    "filterType": "IncludeValues",
                    "values": ["CASH"]
                }
            },
            "aggregateFields": [
                "Sum.Incoming",
                "Sum.Outgoing",
                "Sum.ResignedSum",
            ]
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        return OlapCashShiftBuilder(items).process()

    def export_olap_cash_2(self, from_date: datetime = datetime.now() - timedelta(days=2), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'reportType': 'SALES'
        }
        json = {
            "reportType": "SALES",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "CashRegisterName",
                "CashRegisterName.Number",
                "CashRegisterName.CashRegisterSerialNumber",
                "OpenDate.Typed",
                "PayTypes",
                "SessionNum",
            ],
            "filters": {
                "OpenDate.Typed": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "PayTypes": {
                    "filterType": "IncludeValues",
                    "values": ["Наличные"]
                }
            },
            "aggregateFields": [
                "DishDiscountSumInt",
            ]
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        return OlapCashShiftBuilderV2(items).process()

    def export_conceptions_deprecated(self, from_date: datetime = datetime.now() - timedelta(days=365), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Conception.Code",
                "Conception",
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "TransactionType": {
                    "filterType": "IncludeValues",
                    "values": ["CASH"]
                }
            },
            "aggregateFields": []
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        result = []
        for item in items:
            result.append(Conception(
                id=item.get('Conception.Code'),
                name=item.get('Conception')
            ))
        return result

    def export_returning_invoice(self, from_date: datetime = datetime.now() - timedelta(days=2), to_date: datetime = datetime.now()):
        params = {
            'key': self.token,
            'reportType': 'TRANSACTIONS'
        }
        json = {
            "reportType": "TRANSACTIONS",
            "buildSummary": "false",
            "groupByRowFields": [],
            "groupByColFields": [
                "Document",
                "DateTime.Typed",
                "Conception.Code",
                "Counteragent.Id",
                "TransactionType",
                "Account.Id",
                "Account.StoreOrAccount",
                "Account.Name",
                "Product.Id",
                "Product.Name",
            ],
            "filters": {
                "DateTime.DateTyped": {
                    "filterType": "DateRange",
                    "periodType": "CUSTOM",
                    "from": from_date.strftime('%Y-%m-%d'),
                    "to": to_date.strftime('%Y-%m-%d'),
                    "includeLow": True,
                    "includeHigh": True
                },
                "TransactionType": {
                    "filterType": "IncludeValues",
                    "values": ["RETURNED_INVOICE_COST_AFFECTED"]
                }
            },
            "aggregateFields": [
                "Sum.Incoming",
                "Sum.Outgoing",
                "Sum.ResignedSum",
                "Amount.Out",
                "Amount.In",
                "Amount"
            ]
        }
        data = self.send('v2/reports/olap', method='POST', json=json, params=params)
        items = data.get('data', [])
        return ReturningInvoiceBuilder(items).process()

    def export_conceptions(self):
        params = {
            'key': self.token,
            'rootType': 'Conception'
        }
        data = self.send('v2/entities/list', method='GET', params=params)
        result = []
        for item in data:
            result.append(Conception(**item))
        return result

    def __enter__(self):
        self.auth()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()



