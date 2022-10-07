from io import StringIO
from typing import List, Dict
from operator import eq, ne

from .separators import separators

class Block:
    def __init__(self, 
        begin_row: int = None, begin_col: int = None, 
        end_row: int = None, end_col: int = None
    ) -> None:

        self.begin_row = begin_row
        self.begin_col = begin_col
        self.end_row = end_row
        self.end_col = end_col

class GetPositionOfBlocks:
    def __init__(self, data: str) -> None:
        self.file = StringIO(data)

    def column(self, line, operator, character) -> int:
        column = 0

        while operator(line[column], character):
            column += 1
        
        return column

    def set_begin(self, line_of_block: int, line_no: int, line: str, block: Block):

        if line_of_block == 1:
            block.begin_row = line_no
            block.begin_col = self.column(line, eq, ' ')

    def set_end(self, line_of_block: int, line_no: int, line: str, block: Block):

            if line_of_block:
                block.end_row = line_no
                block.end_col = self.column(line, ne, '\n')

    def __call__(self) -> List[Dict]:

        blocks: List[Dict] = []
        line: str = self.file.readline()
        line_no: int = 1
        line_of_block: int = 1
        block: Block = Block()

        while line:
            next_line = self.file.readline()
            self.set_begin(line_of_block, line_no, line, block)
            
            if any(separators(next_line)) or not next_line:
                self.set_end(line_of_block, line_no, line, block)
                blocks.append(block.__dict__) if line_of_block else None
                block = Block()
                line_of_block = 0
                
            else:
                line_of_block += 1
            
            line = next_line
            line_no += 1

        return blocks
