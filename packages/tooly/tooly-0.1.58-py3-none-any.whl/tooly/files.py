import csv
from typing import List


def writeCsv(fname: str, datas: List[List[str]], encoding: str = 'utf8'):
    with open(fname, 'w', encoding=encoding) as fd:
        writer = csv.writer(fd)
        writer.writerows(datas)
