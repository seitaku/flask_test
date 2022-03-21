# -*- coding: utf-8 -*-
from .ExcelReader import ExcelReader

class ParseExcel:

    def __init__(self):
        pass

    def filter(self, df, paramAry: list|None=[], columns: list|None=[]):
        # print('df:\n\n',df)
        result = df # init
        if( type(paramAry) == list and len(paramAry) > 0 ):
            for conditionDict in paramAry:
                result = self.__filterByParam(result, conditionDict)
            
        return self.__filterField(result, columns)

    def __filterByParam(self, df, param):
        field = param.get('field')
        conditionVal = param.get('conditionVal')
        return df.loc[df[field].str.contains(conditionVal, regex=True, na=False)]

    def __filterField(self, df, columns):
        if ( type(columns) is list and len(columns) > 0 ):
            try:
                defString = '-'
                df = df[columns] # filt field
                df = df.fillna(defString).astype(str) # filt nan
            except KeyError as e:
                # 若輸入不存在key 會報錯還沒處理
                print ('missing key: ', e)              
            except Exception as e:
                print('err:', e)
        return df

    def toJson(self, df):
        resultJson = df.to_json(orient = 'records') # to json data
        # encode utf-8
        return resultJson #resultJson.encode('utf-8').decode('unicode_escape')

fileName = 'COPR0520220110000002202201100001.xlsx'
filePath = '.\excel\%s' % (fileName)
df = ExcelReader(fileName, filePath).toDataFrame()

columns = ["客戶簡稱","客戶代號","通路","品  名"]
d = dict(field='客戶代號',conditionVal='NAUS0001')
c = dict(field='品  名',conditionVal='1/4"螺帽')
paramAry = [c, d]
# res = ParseExcel().filter(df, paramAry, columns)
# res = ParseExcel().filter(df, paramAry)
# res = ParseExcel().filter(df, columns=columns)
# res = ParseExcel().filter(df)
# print('res:\n\n',res)

# print('json:\n\n',ParseExcel().toJson(res))
# for content in res:
#     content = content[columns] # filt field
#     content = content.fillna(defString).astype(str) # filt nan
#     resultJson = content.to_json(orient = 'records') # to json data
#     # encode utf-8
#     print (resultJson.encode('utf-8').decode('unicode_escape'),type(resultJson))

