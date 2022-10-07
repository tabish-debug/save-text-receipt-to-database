from io import StringIO
from typing import List

from .separators import separators

class SeparateBlocks:
    def __init__(self, data: str) -> None:
        self.file = StringIO(data)

    def __call__(self) -> List[str]:
        blocks: List[str] = []
        block: str = '' 

        lines: List[str] = self.file.readlines()
        
        for line in lines:
            if any(separators(line)):
                block and blocks.append(block)
                block = ''
            else:
                block += line

            if lines.index(line) == lines.index(lines[-1]):
                block and blocks.append(block)

        return blocks
