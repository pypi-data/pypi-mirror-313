
import pandas as pd
import re
from decimal import Decimal
import datetime
import numpy as np

def cleandf(df:pd.DataFrame):
    """
    df数据清洗
    说明：
        1、去除空数据行
        2、获取不重复数据
        3、去掉数字千分号
        4、去掉数字百分号 如25% 转0.25
        5、去掉字段开头或者结尾的单引号 '
        6、去掉 列标题 的首位空格
        7、将NaN和-替换为None
        8、如果 没有列 "数据写入时间" 则新增列
    返回值：
       df:pd.DataFrame
    """
    if df.empty:
        return '数据为空'
    
    # 设置全局选项，禁用自动向下转型  
    pd.set_option('future.no_silent_downcasting', True)  

    # 删除空数据行
    # axis（0: 行操作（默认）；1: 列操作）；how（any: 只要有空值就删除（默认）；all:全部为空值才删除）
    # inplace（False: 返回新的数据集（默认），True: 在愿数据集上操作）
    df = df.dropna(axis=0, how='all', inplace=False)

    # 获取不重复数据
    df = df.drop_duplicates()
    
    # 通篇去掉 千分号
    def removePermil(number_str):
        """
        删除数字中的千分号  可以识别中文和英文逗号
        可以删除数字之前的逗号 识别的规则是 1-3位数字、逗号、3位数字
        """
        target  =  re.findall(r'\d{1,3}(,)\d{3}.*',number_str)
        for item in target:
            number_str = number_str.replace(item,item.replace(',',''))

        target  =  re.findall(r'\d{1,3}(，)\d{3}.*',number_str)
        for item in target:
            number_str = number_str.replace(item,item.replace('，',''))
        return number_str
    # df = df.applymap(lambda x: removePermil(x) if isinstance(x, str) else x )  # 这个方法被弃用了
    df = df.map(lambda x: removePermil(x) if isinstance(x, str) else x )
    
    # 百分号
    def removeBFH(x):
        """
        将%号数字转化成小数，例如5%，0.05
        """
        try:
            return float(Decimal(x.strip('%')) / Decimal('100'))
        except:
            return x  
    # df = df.applymap(lambda x: x if not '%' in str(x) else removeBFH(x)) # 这个方法被弃用了
    df = df.map(lambda x: x if not '%' in str(x) else removeBFH(x))
    
    # 去掉内容开头或者结尾的 '
    # df =  df.applymap(lambda x: x.strip("'") if isinstance(x, str) else x) # 这个方法被弃用了
    df = df.map(lambda x: x.strip("'") if isinstance(x, str) else x)

    # 去掉列名中的首尾空格字符
    # df.columns = df.columns.str.strip()
    df.columns = df.columns.str.strip().str.replace('\n', '')
    # df.columns = [x.strip() for x in df.columns] 

    # # 将NaN和-替换为None
    df = df.replace({np.nan:None,'-':None,'':None})

    # 去掉每个字段内容中的换行符
    df = df.replace('\t', '', regex=True)

    # # 增加记录时间列
    if "数据写入时间" not in df.columns:
        df['数据写入时间'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # .strftime('%Y-%m-%d %H:%M:%S.%f')
    
    return df