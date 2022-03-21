# -*- coding: utf-8 -*-
import os
from typing import Optional
import pandas as pd

class ExcelReader:

    def __init__(self, file_name, file_path) -> None:
        self.file_name = file_name
        self.file_path = file_path
        pass

    def toDataFrame(self, cols: str | None=...):
        data = pd.read_excel(self.file_path, engine='openpyxl', usecols=None)
        df = pd.DataFrame(data)
        return df

fileName = 'COPR0520220110000002202201100001.xlsx'
filePath = '.\excel\%s' % (fileName)
# columns  = 'A,J,K'
# ExcelReader(fileName, filePath).toDataFrame(columns)
# print(ExcelReader(fileName, filePath).toDataFrame())
# print(ExcelReader(fileName, filePath))

list = os.listdir('./excel/')
for file in list:
    print(str(file), type(file))
