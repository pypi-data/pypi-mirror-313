import json
from collections import defaultdict
from datetime import datetime

from iikoserver_api.schemas.incoming_service import IncomingServiceItem, IncomingService
from iikoserver_api.schemas.returning_invoice import ReturningInvoiceItem, ReturningInvoice


class ReturningInvoiceBuilder:
    def __init__(self, items):
        self.items = items

    def process(self):
        documents = defaultdict(dict)
        for item in self.items:
            if not documents[item['Document']].get(item['Product.Id']):
                documents[item['Document']][item['Product.Id']] = [item]
            else:
                documents[item['Document']][item['Product.Id']].append(item)

        result = []
        for document, products in documents.items():
            document_items = []
            main_item = None
            for index, (product, items) in enumerate(products.items()):
                store = None
                account = None
                amount = 0
                sum = 0
                for item in items:
                    if item.get('Account.StoreOrAccount') == 'ACCOUNT':
                        account = item.get('Account.Id')
                        amount += item.get('Amount')
                        sum += item.get('Sum.Incoming')
                        if not main_item:
                            main_item = item
                    else:
                        store = item.get('Account.Id')

                document_items.append(ReturningInvoiceItem(
                    store=store,
                    account=account,
                    num=str(index + 1),
                    product=product,
                    amount=amount,
                    sum=sum
                ))

            result.append(ReturningInvoice(
                items=document_items,
                number=main_item['Document'],
                id=f'{main_item['Document']}_{main_item['DateTime.Typed']}',
                date=datetime.fromisoformat(main_item['DateTime.Typed']),
                account=main_item['Account.Id'],
                counterparty=main_item['Counteragent.Id'],
                conception_code=main_item['Conception.Code']
            ))

        return result

