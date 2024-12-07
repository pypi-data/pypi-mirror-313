from collections import defaultdict
from datetime import datetime

from iikoserver_api.schemas.implementation_act import ImplementationActItem, ImplementationActItemTypeEnum, \
    ImplementationAct


class ImplementationActBuilder:
    def __init__(self, items):
        self.items = items

    def process(self):
        document = defaultdict(dict)
        for item in self.items:
            document_id = f'{item['Document']}_{item['DateTime.Typed']}'
            account = item.get('Account.Id')
            product = item.get('Product.Id')
            transaction_type = item.get('TransactionType')
            if not document[document_id].get(account):
                document[document_id][account] = defaultdict(dict)
            if not document[document_id][account].get(product):
                document[document_id][account][product] = defaultdict(list)
            document[document_id][account][product][transaction_type].append(item)

        result = []
        for document_id, accounts in document.items():
            main_document = None
            store = None
            account = None
            conception = None
            document = {
                'id': document_id,
            }
            document_items = []
            for account_id, products in accounts.items():
                for product_id, transactions in products.items():
                    for transaction_type, items in transactions.items():
                        for item in items:
                            if not conception:
                                conception = item.get('Conception.Code')
                            if transaction_type == 'SALES_REVENUE':
                                if not item.get('Sum.Outgoing'):
                                    continue
                                if not account:
                                    account = account_id
                                data = {
                                    'type': ImplementationActItemTypeEnum.INCOMING,
                                    'sum': item.get('Sum.Outgoing'),
                                    'amount': abs(item.get('Amount')),
                                    'account': account_id,
                                }
                            else:
                                if not item.get('Account.StoreOrAccount') == 'STORE' or not item.get('Sum.Outgoing'):
                                    continue
                                if not store:
                                    store = account_id
                                data = {
                                    'type': ImplementationActItemTypeEnum.OUTGOING,
                                    'sum': item.get('Sum.Outgoing'),
                                    'amount': item.get('Amount.Out'),
                                    'store': account_id
                                }
                            if not main_document:
                                main_document = item

                            document_items.append(ImplementationActItem(
                                product=product_id,
                                **data
                            ))

            if not main_document:
                continue

            document['num'] = main_document.get('Document')
            document['date'] = datetime.fromisoformat(main_document.get('DateTime.Typed'))
            document['store'] = store
            document['account'] = account
            document['items'] = document_items
            document['conception_code'] = conception

            result.append(ImplementationAct(
                **document
            ))

        return result

