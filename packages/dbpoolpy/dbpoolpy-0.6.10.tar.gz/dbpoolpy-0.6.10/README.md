# dbpoolpy

#### 介绍

python使用此库可以方便的操作数据库数据，主要是用在关系型数据库，可以支持SQLite3, MySQL, PostgreSQL

#### 安装教程

```
pip install dbpoolpy
```

#### 特点

- 和数据库交互方便，不需要写sql语句
- 支持三种数据库类型：SQLite3, MySQL, PostgreSQL
- 可同时连接多个数据库

#### 使用说明

##### 快速使用教程

为了减少不必要的代码, 在单次数据库交互时可以使用Select, Update, Insert, Delete 操作起来更方便，每次操作都会从连接池里获取连接，操作完后会自动把连接放入连接池里，

参考以下代码

```python
import pymysql
from dbpoolpy import init_pool 
from dbpoolpy import Select, Update, Insert, Delete

DATABASE = {
    'dbcon1':  {              # 连接池名称
        'engine': pymysql,    # 取数据库所使用的插件：mysql使用pymysql, SQLite3使用python自带的sqlite3, PostgreSQL使用psycopg2
        'database': 'imlf',   # 默认连接的数据库
        'host': '',           # 数据库地址
        'port': 51000,        # 数据库端口
        'user': 'atpdev',     # 数据库用户名
        'password': '',       # 数据库的密码
        'charset': 'utf8',    # 字符集类型
        'mincached': 0,       # 初始化连接数
        'maxconnections': 10  # 数据库连接池的最大连接数
    }
}

init_pool(DATABASE)

# 查找一条数据 不带fields，则默认返回所有字段
datas = Select("dbcon1", "table_name").fields("field1, field2").where(field1='152901').first()

# 查找多条数据, 不带fields，则默认返回所有字段,isdict默认为True，返回是dict，如果False, 则返回元组
datas = Select("dbcon1", "table_name").fields("field1").where(field1='152901').all(isdict=False)

# 插入
new_id = Insert("dbcon1", "table_name").values(field1="value1").execute()

# 更新
Update("dbcon1","table_name").values(field1="value1").where(field3=6).execute()

# 删除数据
Delete("dbcon1","table_name").where(id=6).execute()


```

##### 使用with语句执行多次操作

connect_db可以返回连接池的一个连接，在with语句中执行多步数据库操作，期间不会释放连接，
with语句执行完后，会自动把数据库连接放回到连接池里。

操作如下：

```python
init_pool(DATABASE)
from dbpoolpy import init_pool, connect_db

with connect_db('dbcon1') as db:

    # 只取第一条数据
    first_data = db.select("table_name").fields(
         "field1, field2, field3"
    ).where(
        field1='152901',
        field2=("between", ['2022-04-01', '2022-05-01']),
        field3=("in", [1,2,3])
    ).first()
    print(first_data)

    # 取所有数据
    all_datas = db.select("table_name").where(
        field2=(">", '2022-04-01'),
        field3=6,
        field4=("in", ["third_ML", "third_XZ", "third_MF"]),
    ).group_by(           # group_by 可省略
        "field2"
    ).order_by(           # order_by 可省略
        'field1 desc'
    ).limit(              # limit 可省略
        20
    ).all(isdict=False)   # isdict默认为True，返回是dict，如果False, 则返回元组
    print(all_datas)

    # 插入数据
    new_id = db.insert("table_name").values(     # 如果表中有自增主键id，则会返回new_id，如果没有，则不会返回new_id
        field1="value1",     # 字符串值
        field2=3,            # 数字
        field3="2023-05-12", # 日期值
    ).execute()

    # 更新数据
    db.update("table_name").values(
        field1="value1",     # 字符串值
        field2=3,            # 数字
        field3="2023-05-12", # 日期值
    ).where(
        field2=(">", '2022-04-01'),
        field3=6,
        field4=("in", ["third_ML", "third_XZ", "third_MF"]),
    ).execute()

    # 删除数据
    db.delete("table_name").where(
        field1=(">", '2022-04-01'),
        field2=6,
    ).limit(20).execute()    # limit可省略

    # 执行查寻sql语句
    datas = db.query(sql="SELECT * FROM table_name where id=%s", args=(23,))

    # 执行增改删sql
    db.execute(sql="DELETE from table_name where id=%s", args=(23,))

```

##### 事务操作

在事务内，一起成功，一起失败

```

with connect_db('dbcon1') as db:
    with db.transaction() as db_trans:
        db_trans.delete("table_name")
        new_id = db_trans.insert('table_name').values(field1="value1").execute()
        new_id2 = db_trans.delete('table_name').where(field1="value1"}).execute()

```

##### 连接多个数据库

dbpoolpy可以同时多个数据库,支持SQLite3, MySQL, PostgreSQL，并自动创建和管理多个数据库连接池, 参考如下代码：

```python
import pymysql
import sqlite3
import psycopg2

DATABASE = {
    'dbcon1':  {
        'engine': pymysql,         # 取数据库所使用的插件
        'database': 'imlf1',       # 默认连接的数据库
        'host': '127.0.0.1',       # 数据库地址
        'port': 51000,             # 数据库端口
        'user': 'atpdev',          # 数据库用户名
        'password': '',            # 数据库的密码
        'charset': 'utf8',         # 字符集类型
        'mincached': 0,            # 初始化连接数
        'maxconnections': 10       # 数据库连接池的最大连接数
    },
    'dbcon2':  {
        'engine': sqlite3,         # 取数据库所使用的插件
        'dbtype': 'sqlite3',       # 数据库类型, 默认是mysql
        'database': 'test_db.db',  # sqlite3数据库路径
        'maxconnections': 10       # 数据库连接池的最大连接数
    },
    'dbcon3':  {
        'engine': psycopg2,        # 取数据库所使用的插件
        'dbtype': 'postgresql',    # 数据库类型, 默认是mysql
        'database': 'dev1',        # 默认连接的数据库
        'host': '127.0.0.1',       # 数据库地址
        'port': 52000,             # 数据库端口
        'user': 'atpdev',          # 数据库用户名
        'password': '',            # 数据库的密码
        'mincached': 0,            # 初始化连接数
        'maxconnections': 10       # 数据库连接池的最大连接数
    },
}
init_pool(DATABASE)
from dbpoolpy import Select

# mysql
datas1 = Select("dbcon1", "table_name1").where(field1='152901').all()
# sqlite3
datas1 = Select("dbcon2", "table_name2").where(field1='152902').all()
# postgresql
datas1 = Select("dbcon3", "table_name3").where(field1='152903').all()

```

##### 使用 Table类 组织项目的数据库操作

dbpoolpy.Table 类可以做到数据库和表映射到python的类上，可以使数据库的操作更加的简便。
可以通过这种形式来实现ORM，并且可以把和数据库相关的操作都集成到一个py文件里, 业务代码放到controller里

db操作代码：

> `db/__init__.py`

```python
from dbpoolpy import init_pool, Table

init_pool(DATABASE)

class Server179:
    __server__ = "dbcon1"          # 数据库连接命名, 在DATABASE里定义的

class ImlfDB(Server179):
    __schema__ = "imlf"            # 库名: 和数据库名保持一致

class TableName1TB(ImlfDB, Table):
    __table__ = "table_name1"      # imlf库里的表名: 和数据库里的表名保持一致

```

业务代码:

> `contrler.py`

```python
from db import TableName1TB

# 查找第一个数据
data = TableName1TB.find_one(field1='152901')

# 查找批量数据
datas = TableName1TB.find(field1='152901')

# 插入
new_id = TableName1TB.add(field1="value1")

# 更新
TableName1TB.set(field1="value1").where(field3=6)

# 删除数据
TableName1TB.rm(id=6)
```

以上数据库的操作直接映射到TB类上的操作, 并且代码非常的简洁, 并且都是连接池操作，不必担心连接数过多的问题。
这种形式，应该是最简的ORM

> Table类还有另一种和connect_db一样更灵活的操作数据的方式：可以链接使用where, values, order_by, group_by, limit, page等方法

```python
# 查找第一个数据
data = TableName1TB.select().where(field1='152901').first()

# 查找批量数据
datas = TableName1TB.select().where(field1='152901').all()

# 插入
new_id = TableName1TB.insert().values(field1="value1").execute()

# 更新
TableName1TB.update().values(field1="value1").where(field3=6).execute()

# 删除数据
TableName1TB.delete().where(id=6).execute()
```

##### 批量操作

dbpoolpy的批量操作，可以方便的实现批量数据的插入和更新

```python
# 数据准备: 要插入的数据
insert_datas = [
    {
        "field1":"value11",
        "field2":"value12",
        "field3":"value13",
        "field4":"value14",

    },{
        "field1":"value21",
        "field2":"value22",
        "field3":"value23",
        "field4":"value24",
    }
]

# 数据准备: 要更新的字段的值
many_values = [
    {
        "field1":"value1",
    },{
        "field1":"value2",
    }
]

# 数据准备: 要更新的where条件
many_where = [
    {
        "field2":"value3",
    },{
        "field2":"value4",
    }
]


# 第一种：使用connect_db操作
with connect_db('dbcon1') as db:
    # 插入数据
    db.insert_batch(
        "table_name",     # 表名
        insert_datas,     # 要插入的数据列表
        batch=2000        # batch是批量插入时一批插入的数量，默认是2000
    )

    # 更新数据
    db.update_batch(
        "table_name",              # 表名
        many_values=many_values,   # 更新数据的values列表，和many_where列表长度一致
        many_where=many_where,     # 更新数据的where条件列表，和many_values列表长度一致
        batch=2000                 # 更新批次数量，默认2000
    )

# 第二种：使用Table的ORM表类实现批量操作
# 批量插入
TableName1TB.add_batch(
    insert_datas,     # 要插入的数据列表
    batch=2000        # batch是批量插入时一批插入的数量，默认是2000
)

# 批量更新数据
TableName1TB.set_batch(
    many_values=many_values,   # 更新数据的values列表，和many_where列表长度一致
    many_where=many_where,     # 更新数据的where条件列表，和many_values列表长度一致
    batch=2000                 # 更新批次数量，默认2000
)

```

##### 分页取数据

分页取数据是后端接口经常使用的数据库操作

``` python
# 第一种：使用connect_db操作
with connect_db('dbcon1') as db:
    # 插入数据
    page_data = db.select("table_name").where(
        field1='152901'
    ).page(page=1,size=20)   # page: 第n页，size: 每页数量


# 第二种：使用Table的ORM表类操作
page_datas = TableName1TB.select().where(
    field1='152901'
).order_by("field2 desc").page(page=1,size=20)   # page: 第n页，size: 每页数量

# 第三种：使用Select类操作
page_datas = Select("dbcon1", "table_name").where(
    field1='152901'
).page(page=1,size=20)   # page: 第n页，size: 每页数量

```

分页取数据会返回一个nametuple:

```
Page = namedtuple("Page", ["total", "pages", "page", "size", "data"])

# total: 总数据量
# pages: 总页数
# page: 第n页
# size: 每页显示数量
# data: 第n页的数据

```

##### 调试日志打印

日志打印默认不开启，开启日志后会打印数据库连接信息、连接池信息、sql语句信息、返回信息、报错信息等。

开启调试日志：

```
from dbpoolpy import init_pool, settings
settings.DEBUG = True
init_pool(DATABASE)
```

开始调试后每条和数据库交互的日志都会打印出来，这样可能会减慢数据库的交互时间，在线上使用时，不建议开启调试。

调试日志如下：

```
server=mysql|id=4072|name=179|user=atpdev|addr=10.12.3.179:51000|db=imlf|idle=0|busy=1|max=10|trans=0|time=402411|ret=0|num=191|sql='select * from imlf.modules'|args=None|err=
```

一条日志使用`"|"`符号分隔，日志中各值的信息如下：

- server: 数据库类型：mysql、sqlite3、postgresql
- id: 数据库的连接id
- name: 数据库连接池名称
- user: 用户名
- addr：数据库地址和端口号
- db: 数据库表名
- idle: 空闲连接的个数
- busy: 正在使用的连接数
- max: 连接池的最大连接数
- trans: 是否正在使用事务
- time: sql语句执行时间微秒(0.000001秒)
- ret: 返回结果, 返回列表时显示0
- num: 返回值数量, 返回列表时显示数量
- sql: 执行的sql语句
- args：sql语句里的传参
- err: 报错信息

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
