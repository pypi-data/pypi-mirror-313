
import os
from sqlalchemy import create_engine,text
import sqlalchemy.exc
from sqlalchemy.exc import DBAPIError  # 捕获字段不全异常
from sqlalchemy import inspect         # 获取 MySQL 数据表的列名称
from typing import List, Literal, Union

import pandas as pd
import re
import datetime
import numpy as np
from decimal import Decimal

# 链接MySQL数据库
class SqlConnect:
    """
    链接数据库的上下文管理器
    """
    def __init__(self,database=None, SQLALCHEMY_DATABASE_URI=None):
        """
        SQLALCHEMY_DATABASE_URI 数据库链接字符串（不包含数据库名称），如果参数不传入，则需要设置变量环境 
        database   数据库名称
        """
        if SQLALCHEMY_DATABASE_URI and database:  
            self.db_url = SQLALCHEMY_DATABASE_URI + database
        elif SQLALCHEMY_DATABASE_URI is None  and database is not None:
            data_url = os.environ.get('SQLALCHEMY_DATABASE_URI')
            if data_url is None:
                tishi = "SQLALCHEMY_DATABASE_URI示例:mysql+pymysql://user:password@192.168.1.10:22484/"
                
                data_url = input(tishi +'\n' +"请输入环境变量SQLALCHEMY_DATABASE_URI的值:")
                os.environ['SQLALCHEMY_DATABASE_URI'] = data_url  # 设置一个变量环境

            self.db_url = data_url + database
        else:
            raise ValueError("数据库初始化的参数错误,请传递完成数据链接:mysql+pymysql://{user}:{password}@{host}/{database}，或者设置变量环境 和 传入数据库名称")
        self.engine = None
        self.connection = None

    def __enter__(self):
        self.engine = create_engine(self.db_url)
        self.connection = self.engine.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.connection.rollback()  # 回滚数据库操作
            self.connection.close()
        finally:
            self.engine.dispose()

## 数据转化（清洗数据/转成SQL字符串）    
class DataConvert:
    def __init__(self):None
        
    def convert_to_cleandata(self,df):
        '''
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
        '''
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
            target  =  re.findall('\d{1,3}(,)\d{3}.*',number_str)
            for item in target:
                number_str = number_str.replace(item,item.replace(',',''))

            target  =  re.findall('\d{1,3}(，)\d{3}.*',number_str)
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
            df['数据写入时间'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        return df
    
    def convert_to_sqlstring(self, data,table_name, sql_type:Literal['INSERT','REPLACE']='INSERT'):
        """
        函数说明：
            将pandas转化成mysql插入字符串
        参数说明：
            data : pandas数据
            table_name: mysql的数据表名称
            sql_type : 有两个可选参数 'INSERT' 和 'REPLACE'
        返回值：
            正常返回： sql插入语句字符串
        """
        if data.empty:
            raise ValueError("数据表没有数据") 
        
        # 将NaN和-替换为None
        data = data.replace({np.nan:None,'-':None})

        # 插入语句的类型
        savetype = "INSERT IGNORE" if sql_type == 'INSERT' else ("REPLACE" if sql_type == 'REPLACE' else None)
        if savetype is None:
            raise ValueError('Invalid SQL type. Supported types: INSERT, REPLACE')

        
        # 生产列标题
        columnTitle = ", ".join([f"`{col.strip()}`" for col in data.columns])

        # 拼接无头数据内容
        rowData = data.itertuples(index=False, name=None)  # pandas数据转换成元组 
        rowContent = ','.join(str(r)  for r in rowData)

        # 生成并返回sql语句
        sql_statement = f'{savetype} INTO {table_name} ({columnTitle}) VALUES {rowContent}'
        sql_statement = sql_statement.replace("None", 'null')  # 这个替换是生效的
        return sql_statement        


## 数据写入MySQL
class SqlExecute(DataConvert):

    def execute_sql(self,query,conn,data=None,table_name=None):
        """
        函数说明：
            执行SQL语句
                1、当数据表不存在时,提示创建数据表(需要传入table_name)
                2、当数据表字段不全时,提示缺失字段(需要传入table_name)
        参数说明：
            query: sql 语句
            conn : sqlalchemy数据库链接
            data :       数据表 df 默认为None
            table_name : 数据表名 默认为None
        返回值：
            SQL字符串
        
        """
        try:
            query = text(query)  # 将字符串转换为可执行的 SQL 对象
            result = conn.execute(query)
            conn.commit()
            return result
        except (ValueError,sqlalchemy.exc.ProgrammingError)  as error:
            ms = f"MySQL中不存在表：{repr(error)}"
            conn.rollback()  # 回滚事务
            if not data.empty and table_name:
                com =input(ms + '\n' + '请输入creat来创建mysql数据表:')
                if com=='creat':
                    result_nu = data.to_sql(table_name, conn, if_exists='replace', index=False)
                    class Result_01:
                        pass
                    result = Result_01()
                    result.rowcount  =result_nu
                    print(f"{table_name} 数据表创建完成")
                    return result
            else:
                raise ValueError(ms) 
        except DBAPIError as error:
            ms  = f"MySQL中字段不完整：{repr(error)}"
            conn.rollback()  # 回滚事务
            def get_extra_columns(con, data, table_name):
                """
                获取存在于 pandas 数据帧中但不存在于 MySQL 数据表中的列名称明细。
            
                参数：
                - con: SQLAlchemy 数据库连接对象。
                - data: pandas 数据帧。
                - table_name: MySQL 数据表名称。
            
                返回值：
                - extra_columns: 存在于数据帧中但不存在于 MySQL 数据表中的列名称列表。
                """
                # 获取 MySQL 数据表的列名称
                inspector = inspect(con)
                mysql_columns = inspector.get_columns(table_name)
                mysql_column_names = [column['name'] for column in mysql_columns]
            
            
                # 获取数据帧的列名称
                pandas_columns = data.columns.tolist()
            
                # 找出存在于数据帧中但不存在于 MySQL 数据表中的列名称
                extra_columns = [column for column in pandas_columns if column not in mysql_column_names]
                return extra_columns     
            if not data.empty and table_name:
                extra_columns = get_extra_columns(conn,data,table_name) 
                if len(extra_columns) != 0 : 
                    msgtext = f'mysql中不存在字段:{extra_columns},报错信息:{repr(error)}'
                else:
                    msgtext = f'报错信息:{repr(error)}'
                class Test01:
                    pass
                result = Test01()
                result.rowcount  = msgtext
                raise ValueError(msgtext)
            else:
                raise ValueError(ms) 
        except Exception as error:
            conn.rollback()  # 回滚事务
            raise ValueError(repr(error)) 
        # finally:
        #     conn.close()  # 关闭数据库连接

    def data_save_tosql(self,data,table_name,conn, sql_type:Literal['INSERT', 'REPLACE']='INSERT'):
        """
        函数说明：
            将未清洗的数据保存到MySQL
        参数说明：
            data :      pandas数据
            table_name: 数据表名称
            conn :      sqlalchemy数据库链接
            sql_type:   保存类型 有两个可选参数 'INSERT' 和 'REPLACE'
        返回值：
            字符串 f"{保存方法}:{相应数量}"
        """

        # 转换成查询字符串
        query  = self.convert_to_sqlstring(data,table_name, sql_type)
        
        result = self.execute_sql(query,conn)
        res_num = result.rowcount
        return f"{sql_type}:{res_num}"

    def data_cleanerSave_tosql(self,data,table_name,conn, sql_type:Literal['INSERT', 'REPLACE']='INSERT',
                               datalong = None,chunk_size=10000):
        """
        函数说明：
            首先清洗数据,之后将清洗的数据保存到MySQL
        参数说明：
            data :      pandas数据
            table_name: 数据表名称
            conn :      sqlalchemy数据库链接
            sql_type:   保存类型 有两个可选参数 'INSERT' 和 'REPLACE'
            datalong    值为 only 时候,只保存MySQL中存在的字段 默认为None
            chunk_size  每次写入的最大记录数，默认为10000
        返回值：
            字符串 f"{保存方法}:{相应数量}"
        """

        # datalong 为 only 时候,只保存MySQL中存在的字段
        if datalong == "only":
            # 获取 MySQL 数据表的列名称
            inspector = inspect(conn)
            mysql_columns = inspector.get_columns(table_name)
            mysql_column_names = [column['name'] for column in mysql_columns]

            # 获取数据帧的列名称
            pandas_columns = data.columns.tolist()

            new_columns =  [x for x in mysql_column_names if x in pandas_columns]
            data = data[new_columns]

        # 清洗数据
        data = self.convert_to_cleandata(data)

        # 数据变更记录
        changeLog = 0
        errmesg = ''

        chunk_size = chunk_size  # 每次获取的最大记录数
        start_index = 0  # 起始索引
        while start_index < len(data):
            try:
                # 获取当前切片的结束索引
                end_index = min(start_index + chunk_size, len(data))
                
                # 获取当前切片
                df_chunk = data[start_index:end_index]
                
                # 转换成查询字符串
                query = self.convert_to_sqlstring(df_chunk,table_name, sql_type)

                # 运行查询
                result  = self.execute_sql(query,conn,df_chunk,table_name)
                res_num = result.rowcount
                changeLog += res_num
            except Exception as error:
                errmesg = errmesg + f"第{start_index}行—{end_index}行遇到错误:{error}"
                print(errmesg)
                # print("----"*20)
                # print(query)
            # 增加起始索引，以便获取下一个切片
            start_index += chunk_size


        msg = f"{sql_type}:{changeLog}{errmesg}"
        return msg

