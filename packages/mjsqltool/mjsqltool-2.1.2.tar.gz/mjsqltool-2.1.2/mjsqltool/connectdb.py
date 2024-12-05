
import os
from sqlalchemy import create_engine
import sqlalchemy.exc
import psycopg2

## 链接数据库
class ConnectDB:
    """
    链接数据库的上下文管理器
    """
    def __init__(self, database=None, db_uri=None):
        """
        初始化数据库链接
            :param database: 数据库名称
            :param DB_URI: 数据库链接参数
        """
        if db_uri and database:

            # 检查并去除最后一个字符，如果它是 '/'
            if db_uri.endswith('/'):
                db_uri = db_uri[:-1]   
            self.db_url = f"{db_uri}/{database}"
            
        elif db_uri is None and database is not None:
            data_url = os.environ.get('DB_URI')
            if data_url is None:
                mysql_example =  "mysql示例:mysql+pymysql://user:password@192.168.1.10:22484"
                postgresql_example= "postgresql示例:postgresql+psycopg2://user:password@192.168.1.10:5432"
                data_url = input(f"请参考以下数据库链接示例填写您的数据库链接:\n{mysql_example}\n{postgresql_example}\n请输入您的数据库链接(环境变量DB_URI的值):\n")
                os.environ['DB_URI'] = data_url  # 设置一个变量环境

            # 检查并去除最后一个字符，如果它是 '/'
            if data_url.endswith('/'):
                data_url = data_url[:-1]   
            self.db_url = f"{data_url}/{database}"
            
        else:
            raise ValueError("数据库链接参数db_uri和database不能为空")
        
        
        
        if self.db_url.startswith('mysql+pymysql:'):
            print(f"初始化MySQL数据库链接")
            self.db_type = 'MySQL'
        elif self.db_url.startswith('postgresql+psycopg2:'):
            print(f"初始化PostgreSQL数据库链接")
            self.db_type = 'PostgreSQL'
        else:
            raise ValueError("数据库链接参数db_uri格式不正确")
        
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