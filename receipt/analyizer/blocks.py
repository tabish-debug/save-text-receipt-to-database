from abc import ABC, abstractmethod
from typing import List, Dict

from .util import (
    get_bill_no, 
    convert_date,
    get_tax, 
    price_convertor,
    get_payment_method,
    multiple_price_convertor,
    get_tax_percentage,
    get_ust_id,
    get_product,
    get_tax,
    get_information
)

class Block(ABC):
    @abstractmethod
    def get_data(self, data: str):
        pass

class Block1(Block):
    def get_data(self, data: str) -> List[str]:
        block: Dict = {}

        data = data.split('\n')
        info = [i.strip() for i in data if i]
        block['company_name'] = ' '.join(info[:2])
        block['address'] = ' '.join(info[2:])

        return block
        
class Block2(Block):
    def get_data(self, data: str) -> List[str]:
        block = {}

        block['bill_no'] = get_bill_no(data)
        block['created_at'] = convert_date(data)
        
        return block

class Block3(Block):
    def get_data(self, data: str):
        block = { 'products': [] }

        for product in data.split('\n'):
            if product:
                block['products'].append(get_product(product))

        return block

class Block4(Block):
    def get_data(self, data: str):
        block = {}

        block['grand_total'] = price_convertor(data)
        
        return dict(payment=block)

class Block5(Block):
    def get_data(self, data: str):
        block = {}
        
        block['payment_method'] = get_payment_method(data)
        block['paid_price'] = price_convertor(data)
        
        return dict(payment=block)

class Block6(Block):
    def get_data(self, data: str):
        d: list = [get_tax_percentage(data)]
        d += multiple_price_convertor(data)

        block = get_tax(d)
        
        return dict(payment=block)

class Block7(Block):
    def get_data(self, data: str):
        informations = [i.strip() for i in data.split('\n')]
        block = get_information(informations)

        return dict(information=block)

        
class Block8(Block):
    def get_data(self, data: str):
        block = {}
        
        block['ust_id'] = get_ust_id(data)
        
        return dict(information=block)
