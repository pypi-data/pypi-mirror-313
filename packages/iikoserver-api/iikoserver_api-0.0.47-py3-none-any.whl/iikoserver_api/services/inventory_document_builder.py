from collections import defaultdict

from iikoserver_api.schemas.inventory import Inventory, InventoryItem, InventoryItemEnum


class InventoryDocumentBuilder:
    def __init__(self, items):
        self.items = items

    def process(self):
        documents = defaultdict(list)
        for item in self.items:
            if item.get('documentId'):
                documents[item['documentId']].append(item)

        result = []
        for document, items in documents.items():
            if len(items):
                main_document = items[0]
            else:
                continue
            document_items = []
            incoming_sum = 0
            outgoing_sum = 0
            incoming_account = None
            outgoing_account = None
            for item in items:
                sum = round(float(item['sum']), 2)
                if sum >= 0:
                    incoming_sum += sum
                    if not incoming_account:
                        incoming_account = item.get('secondaryAccount')
                else:
                    outgoing_sum += abs(sum)
                    if not outgoing_account:
                        outgoing_account = item.get('secondaryAccount')

            document_items.append(InventoryItem(
                type=InventoryItemEnum.INCOMING,
                sum=incoming_sum,
                account=incoming_account
            ))
            document_items.append(InventoryItem(
                type=InventoryItemEnum.OUTGOING,
                sum=outgoing_sum,
                account=outgoing_account
            ))

            result.append(Inventory(
                id=main_document['documentId'],
                store=main_document.get('primaryStore'),
                num=main_document.get('documentNum'),
                date=main_document.get('date'),
                incoming_sum=incoming_sum,
                outgoing_sum=outgoing_sum,
                sum=round(incoming_sum-outgoing_sum, 2),
                items=document_items
            ))

        return result



