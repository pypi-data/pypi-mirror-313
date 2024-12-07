from datetime import datetime

from iikoserver_api.schemas.cashshift import OlapCashShift, OlapCashShiftV2


class OlapCashShiftBuilder:
    def __init__(self, items: list[dict]):
        self.items = items

    def process(self):
        result = []
        for item in self.items:
            id = f'{item.get('Document')}_{item.get('DateTime.Typed')}'
            result.append(
                OlapCashShift(
                    id=id,
                    session_number=item.get('Document'),
                    cash_shift_name=item.get('Session.CashRegister'),
                    close_date=datetime.fromisoformat(item.get('DateTime.Typed')),
                    amount=item.get('Sum.Incoming')
                )
            )

        return result


class OlapCashShiftBuilderV2:
    def __init__(self, items: list[dict]):
        self.items = items

    def process(self):
        result = []
        for item in self.items:
            cash_shift_id = f'{item.get('CashRegisterName')}_{item.get('CashRegisterName.Number')}_{item.get('CashRegisterName.CashRegisterSerialNumber')}'
            id = f'olap_{item.get('SessionNum')}_{item.get('OpenDate.Typed')}_{cash_shift_id}'
            result.append(
                OlapCashShiftV2(
                    id=id,
                    session_number=str(item.get('SessionNum')),
                    cash_shift_name=str(item.get('CashRegisterName')),
                    cash_shift_number=str(item.get('CashRegisterName.Number')),
                    cash_shift_serial=str(item.get('CashRegisterName.CashRegisterSerialNumber')),
                    cash_shitf_id=cash_shift_id,
                    close_date=datetime.fromisoformat(item.get('OpenDate.Typed')),
                    amount=item.get('DishDiscountSumInt')
                )
            )

        return result
