
## 使用说明

变量环境设置（数据库的链接信息存储在变量环境中）
```
# 设置环境变量 user 是用户名，password 是密码，192.168.1.10:22484 数据库地址
os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@192.168.1.10:22484/'

# 获取环境变量，如果不存在则使用默认值
value = os.environ.get('SQLALCHEMY_DATABASE_URI', 'default_value')
print(value+"DY_DSLP")
```
windwow cmd 设置永久环境变量
```
setx SQLALCHEMY_DATABASE_URI "mysql+pymysql://user:password@192.168.1.10:22484/"
```

1、安装包模块
```
pip install mjsqltool
pip install --upgrade mjsqltool
```
2、引入包模块
```
from mjsqltool import SqlConnect,DataConvert,SqlExecute
```

#### SqlConnect
链接数据库,使用完毕后自动关闭
```
# 数据库名称
db  = 'database'
with SqlConnect(db) as cn:
    .....
```

#### DataConvert
数据转换
1、清洗数据
2、数据转SQL
```
convert = DataConvert()
df = pd.read_exce("jjjj.xlsx")

# 清洗数据
df = convert.convert_to_cleandata(df)

# 转成SQL语句  sql_type:   保存类型 有两个可选参数 'INSERT' 和 'REPLACE'
data = df
table_name = '测试表格'
sql_type='REPLACE'
query = convert.convert_to_sqlstring(data,table_name, sql_type)

```

#### SqlExecute 
SqlExecute 将数据保存到MySQL
SqlExecute 继承了 DataConvert,

```
from mjsqltool import SqlConnect,DataConvert,SqlExecute
import pandas as pd

with SqlConnect("MJ_DATA") as cn:
    df = pd.read_excel(r"C:\Users\manji\Downloads\联盟订单.xlsx")
    SqlExecute().data_cleanerSave_tosql(df,"测试表格",cn)
```

#### SqlExecute().data_cleanerSave_tosql

参数说明
```
sql_type='INSERT', 
# sql_type='INSERT' 自动忽略重复主键记录 有两个可选参数 'INSERT' 和 'REPLACE'

datalong = None, 
# datalong="only" 为 only时,只写入mysql中存在的数据字段

chunk_size=10000   
# 每次最大写入数据的数据记录,例如90条数据，每次写入10条,则自动拆分成10次写入
```

#### 使用pandas读取MySQL数据
```
reportSql = 'select * from TB_table'
with SqlConnect(database="TB_GGTF") as cn:
    reportSql = text(reportSql)  # 将字符串转换为可执行的 SQL 对象
    df = pd.read_sql_query(reportSql,cn)  
    print(df)
```

## 打包
```
python setup.py sdist bdist_wheel