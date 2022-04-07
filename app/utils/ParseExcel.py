# -*- coding: utf-8 -*-
from enum import Enum
import math
from .ExcelReader import ExcelReader
import json

class DefValues(Enum):
    _EMPTY = ''
    _DASH = '-'

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

    def __filterField(self, df, columns:list|None=[]):
        try:
            if ( type(columns) is list and len(columns) > 0 ):
                df = df[columns] # filt field
        except KeyError as e:
            # 若輸入不存在key 會報錯還沒處理
            print ('missing key: ', e)              
        except Exception as e:
            print('err:', e)
        
        # df = df # no filt nan
        # df = df.astype(str) # filt nan convert to str
        df = df.fillna(DefValues._EMPTY.value).astype(str) # filt nan
        return df

    def toJson(self, df):
        resultJson = df.to_json(orient = 'records') # to json data
        # encode utf-8
        return resultJson.encode('utf-8').decode('unicode_escape')

def formatApostrophe(str:str):
    return str.replace("\'","''")

fileName = 'COPR0520220110000002202201100001.xlsx'
filePath = '.\excel\%s' % (fileName)
print('filePath:',filePath)
df = ExcelReader(fileName, filePath).toDataFrame()
# defString = "-"
# columns = ["客戶簡稱","客戶代號","通路","品  名"]
d = dict(field='客戶代號',conditionVal='NAUS0001')
c = dict(field='品  名',conditionVal='1/4"螺帽')
paramAry = [c, d]
# res = ParseExcel().filter(df, paramAry, columns)
# res = ParseExcel().filter(df, paramAry)
# res = ParseExcel().filter(df, columns=columns)
res = ParseExcel().filter(df)
# print('res:\n\n',res,'\n\nres type:',type(res))

# res = ParseExcel().toJson(res)

# print('res:\n\n',res,'\n\nres type:',type(res))

# # one col to list
# j = res['通路'].values.tolist()
# print('res:\n\n',j,'\n\nres type:',type(j))

# # list
# j2 = res.values.tolist()
# print('j2:\n\n',j2,'\n\nj2 type:',type(j2))
# for content in j2:
#     print( content ,type(content))
#     print( content ,type(content))

# dict
# r3 = res.fillna(defString).to_dict('records')
# r3 = res.to_dict('records')
r3 = res.drop_duplicates(subset = ['品  號']).to_dict('records') # 排除重複
for content in r3:
    pass

r4 = res.drop_duplicates(subset = ['客戶簡稱','客戶代號','型態']).to_dict('records') # 排除重複
for content in r4:
    pass
    # print('c1', content ,type(content))
    # print('c2', content['通路'] ,type(content['通路']))
    # print('c2', math.isnan(content['通路']) ,type(content['通路']))

# 讀excel 產生 商品測試資料 insert
def readProduct(list):
    insert = f"""insert into p_product_info (
        \'code\',\'name\',\'specification\',
        \'quantity\',\'product_unit\',\'price\',
        \'currency_unit\',\'status\',\'create_by\',\'create_date\',\'update_by\',
        \'update_date\') VALUES
    """
    print(insert)
    for content in list:
        if len(content['客戶簡稱']) == 0:
            continue
        code = formatApostrophe('TH'+content['品  號'])
        name = formatApostrophe( 'TH'+content['品  名'] )
        # customer_prd_code = formatApostrophe(content['品  號'])
        # customer_prd_name = formatApostrophe( content['品  名'] )
        specification = formatApostrophe( content['規  格'] )
        quantity = content['銷貨數量']
        product_unit = formatApostrophe(content['單位'])
        price = content['原幣平均單價']
        currency_unit = content['幣別']
        status = 0
        create_by = 'sa'
        create_date = 'DateTime(\'now\')'
        update_by = 'sa'
        update_date = 'DateTime(\'now\')'

        values = """(\'{}\',\'{}\',\'{}\',{}
        ,\'{}\',{},\'{}\',{}
        ,\'{}\',{},\'{}\',{}),""".format(
            code,name,specification,quantity
        ,product_unit,price,currency_unit,status
        ,create_by,create_date,update_by,update_date)
        # print('values', values ,type(values))
        insert += values
    # print('\n\ninsert:\n',insert[0:-1])
    # print( len(list) )
    return insert[0:-1]
    

# 讀excel 產生 商品測試資料 insert
def readCoustomer(list):
    insert = f"""insert into c_customer_info (
        \'code\', \'name\',\'short_name\',
        \'type\',\'country\',\'region\',\'address\',\'status\',
        \'create_by\',\'create_date\',\'update_by\',
        \'update_date\') VALUES
    """
    print(insert)
    for content in list:
        if len(content['客戶簡稱']) == 0:
            continue
        code = formatApostrophe(content['客戶代號'])
        name = formatApostrophe( content['品  名'] )
        short_name = formatApostrophe(content['客戶簡稱'])
        type = formatApostrophe( content['型態'] )
        country = content['國家']
        region = formatApostrophe(content['地區'])
        address = ''
        status = 0
        create_by = 'sa'
        create_date = 'DateTime(\'now\')'
        update_by = 'sa'
        update_date = 'DateTime(\'now\')'

        values = """(\'{}\',\'{}\',\'{}\',\'{}\'
        ,\'{}\',\'{}\',\'{}\',{}
        ,\'{}\',{},\'{}\',{}),""".format(
            code, name,short_name,type
            ,country,region,address,status
            ,create_by,create_date,update_by,update_date)
        # print('values', values ,type(values))
        insert += values
    
    # print('\n\ninsert:\n',insert[0:-1])
    # print( len(list) )
    return insert[0:-1]

# fr3 = readProduct(r3)
# print(fr3)
# fr4 =readCoustomer(r4)
# print(fr4)
