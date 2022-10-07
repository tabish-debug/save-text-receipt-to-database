import re
from datetime import datetime

def quantity_convertor(data: str):
        return int(re.findall(r'\d+', data)[0])

def price_convertor(data: str):
    return float(re.findall(r'\d+\,\d+', data)[0].replace(',', '.'))

def get_digits(data: str):
    return re.findall(r'\d+', data)[0]

def convert_iso_date(data: str):
    data = re.findall(r'\d+\-\d+\-\d+\w\d+\:\d+\:\d+\.\d+', data)[0][:-2]
    return datetime.fromisoformat(data + '+00:00')

def get_hashed(data: str):
    return re.findall(r'[a-fA-F0-9]{30,}', data)[0]

def split_from_space(data: str):
    return [i for i in data.split(' ') if i]

def get_product(product: list):
    p = {}

    product = [i for i in product.split(' ') if i]
    p['quantity'] = quantity_convertor(product[0])
    p['name'] = product[1]
    p['price'] = price_convertor(product[2])
    p['total'] = price_convertor(product[3])
    p['type'] = product[4]

    return p

def get_tax(data: list):
    block = {}

    block['tax_percentage'] = data[0]
    block['gross'] = data[1]
    block['net'] = data[2]
    block['tax_price'] = data[3]

    return block

def get_information(data: list):
    block = {}

    block['table'] = data[0].split(':')[1].strip()
    block['terminal'] = data[1].split(':')[1].strip()
    block['tse_transaktion'] = get_digits(data[2])
    block['tse_signatur_nr'] = get_digits(data[3])
    block['tse_start'] = convert_iso_date(data[4])
    block['tse_stop'] = convert_iso_date(data[5])
    block['tse_seriennummer'] = get_hashed(data[6])
    block['tse_zeitformat'] = split_from_space(data[7])[1]
    block['tse_signatur'] = split_from_space(data[8])[1]
    block['tse_hashalgorithmus'] = split_from_space(data[9])[1]
    block['tse_status'] = ' '.join(split_from_space(data[10])[2:])
    
    return block

def get_bill_no(data: str):
    return re.findall(r'\d+\-\d+', data)[0]

def get_date(data: str):
    return re.findall(r'\d+\:\d+\:\d+\s\d+\.\d+\.\d+', data)[0]

def convert_date(data: str):
    date = get_date(data)
    return datetime.strptime(date, '%H:%M:%S %d.%m.%Y')

def get_payment_method(data: str):
    return re.findall(r'\(\w+\)', data)[0].strip('()')

def multiple_price_convertor(data: str):
    return [float(i.replace(',', '.')) for i in re.findall(r'\d+\,\d+', data)]

def get_tax_percentage(data: str):
    return int(re.findall(r'\d+', data)[0])

def get_ust_id(data: str):
    return re.findall(r'\w+\d+', data)[0]
