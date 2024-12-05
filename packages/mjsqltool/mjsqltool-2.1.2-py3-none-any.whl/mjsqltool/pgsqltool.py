from sqlalchemy import MetaData, Table
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from typing import Literal

from mjsqltool.connectdb import ConnectDB
from mjsqltool.clean import cleandf


def upsert_factory(on_conflict:Literal['do_nothing', 'do_update']='do_nothing'):
    """
    工厂函数，用于生成带有自定义冲突处理行为的 upsert 方法。pandas  method 的自定义方法
    
    参数说明:
    - on_conflict: str, 冲突处理策略，可选值为 'do_nothing' 或 'do_update'
    
    用法示例：
        result =df.to_sql(schema= 'douyin_shop',name='your_table_test_2', con=conn, if_exists='append', method=upsert_factory(on_conflict='do_nothing'), index=False)
        result2=df.to_sql(schema= 'douyin_shop',name='your_table_test_2', con=conn, if_exists='append', method=upsert_factory(on_conflict='do_update'), index=False)
    返回值:
    - custom_upsert: function, 自定义的 upsert 方法
    """
    def custom_upsert(table, conn, keys, data_iter):
        # 获取表名和模式
        table_name = table.name
        table_schema = table.schema or 'public'  # PostgreSQL 默认模式为 'public'

        # 使用 SQLAlchemy 反射来获取表结构
        metadata = MetaData()
        reflected_table = Table(table_name, metadata, schema=table_schema, autoload_with=conn)
        
        # 检查 DataFrame 与数据库表结构是否匹配
        db_columns = set(column.name for column in reflected_table.columns) # 获取数据库表的列名
        df_columns = set(keys) # 获取 DataFrame 的列名
        missing_columns = df_columns - db_columns # 找出 DataFrame 中存在但数据库表中不存在的列
        if missing_columns:
            print("以下列在 DataFrame 中存在但在数据库表中不存在:")
            for col in missing_columns:
                print(f"- {col}")
            raise ValueError(f"DataFrame 与数据库表结构不匹配。{missing_columns}")

        # 获取主键列名
        primary_key_columns = [pk_column.name for pk_column in reflected_table.primary_key.columns]

        if not primary_key_columns:
            raise ValueError("The table must have a primary key to use ON CONFLICT.")

        # Prepare the data as a list of dictionaries for the executemany call
        data = [dict(zip(keys, row)) for row in data_iter]

        # 创建 INSERT 语句
        stmt = insert(reflected_table).values(data)

        if on_conflict == 'do_nothing':
            # 在 stmt 上添加 ON CONFLICT DO NOTHING 子句
            stmt = stmt.on_conflict_do_nothing(
                index_elements=primary_key_columns  # 指定冲突目标为主键列
            )
        elif on_conflict == 'do_update':
            # Define the ON CONFLICT clause. Use all primary key columns as the conflict target.
            update_set = {key: getattr(stmt.excluded, key) for key in keys if key not in primary_key_columns}
            # 在 stmt 上添加 ON CONFLICT DO UPDATE 子句
            stmt = stmt.on_conflict_do_update(
                index_elements=primary_key_columns,
                set_=update_set
            )
        else:
            raise ValueError("Invalid on_conflict value. Use 'do_nothing' or 'do_update'.")

        result = conn.execute(stmt)
        return result.rowcount

    return custom_upsert


def dftopostgresql(df, conn, schema, table_name, on_conflict:Literal['do_nothing', 'do_update']='do_nothing',chunksize=1000):
    """
    将 DataFrame 写入 PostgreSQL 数据库。
    
    参数说明:
    - df: DataFrame, 待写入的 DataFrame 数据
    - conn: Connection, 数据库连接
    - schema: str, 数据库模式
    - table_name: str, 数据库表名
    - on_conflict: str, 冲突处理策略，可选值为 'do_nothing' 或 'do_update'
    - index: bool, 是否在写入时保留索引，默认为 False
    
    返回值:
    - result: int, 写入数据的行数
    """
    # 获取表结构    
    try:
        df = cleandf(df)
        result =df.to_sql(schema= schema,name=table_name, con=conn, if_exists='append', method=upsert_factory(on_conflict=on_conflict), chunksize=chunksize,index=False)
        print(f"写入数据到 {schema}.{table_name} 成功{result}条数据,主键冲突处理方式{on_conflict}。")
        return result
    except Exception as e:
        print(f"写入数据到 {schema}.{table_name} 失败,主键冲突处理方式{on_conflict}。{repr(e)}")
        return repr(e)
    