from .block_position import GetPositionOfBlocks
from .blocks import Block
from .block_separate import SeparateBlocks

def get_receipt_data(file_data):
    blocks = SeparateBlocks(file_data)
    blocks = blocks()
    receipt_data = {}

    for subclass, block in zip(Block.__subclasses__(), blocks):
        data = subclass().get_data(block)
        for key, value in data.items():
            if key in receipt_data:
                receipt_data[key].update(value)
                break
        else:
            receipt_data.update(data)
                

    return receipt_data

def get_position_of_blocks(file_data):
    positions = GetPositionOfBlocks(file_data)
    return positions() 
