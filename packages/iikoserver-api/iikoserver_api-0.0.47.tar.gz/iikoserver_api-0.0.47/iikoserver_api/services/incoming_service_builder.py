import json
from collections import defaultdict
from datetime import datetime

from iikoserver_api.schemas.incoming_service import IncomingServiceItem, IncomingService


class IncomingServiceBuilder:
    def __init__(self, items):
        self.items = items

    def process(self):
        documents = defaultdict(dict)
        for item in self.items:
            if not documents[f'{item.get('Document')}_{item.get('DateTime.Typed')}'].get(item.get('Product.Id')):
                documents[f'{item.get('Document')}_{item.get('DateTime.Typed')}'][item.get('Product.Id')] = []
            documents[f'{item.get('Document')}_{item.get('DateTime.Typed')}'][item.get('Product.Id')].append(item)

        result = []
        for document, product in documents.items():
            document_items = []
            main_document = None
            for num, (product_id, items) in enumerate(product.items()):
                needed_items = [item for item in items if item.get('Amount.In')]
                if needed_items:
                    if not main_document:
                        main_document = needed_items[0]
                else:
                    continue

                data = {
                    'num': str(num + 1),
                    'product': product_id,
                    'account': needed_items[0]['Account.Id'],
                    'amount': 0,
                    'sum': 0
                }
                for item in items:
                    data['amount'] += item.get('Amount.In')
                    data['sum'] += item.get('Sum.Outgoing')

                document_items.append(IncomingServiceItem(
                    **data
                ))

            if document_items and main_document:
                result.append(IncomingService(
                    id=document,
                    date=datetime.fromisoformat(main_document.get('DateTime.Typed')),
                    num=main_document.get('Document'),
                    account=main_document.get('Account.Id'),
                    counterparty=main_document.get('Counteragent.Id'),
                    items=document_items,
                    conception_code=main_document.get('Conception.Code'),
                ))

        return result

