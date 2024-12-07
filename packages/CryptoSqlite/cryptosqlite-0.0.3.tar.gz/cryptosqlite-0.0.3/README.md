# CryptoSqlite

正儿八经的`sqlite3`结合`sqlcipher`, 且符合`dbapi2`标准的python模块。 兼容各个python版本。

## 安装

本项目python版本要求>= 3.7， 支持Linux、Windows。已有预编译版本`>=3.7 and <=3.12`。

### 源码安装

> 源码安装请确保网络能够流畅访问`github`

默认情况下， 会下载最新的sqlcipher进行编译安装， 如果需要指定版本， 确保在编译前设置环境变量`SQLCIPHER_VERSION`,如`v4.6.1`。

如果系统已经存在sqlcipher, 请设置环境变量`SQLCIPHER_INCLUDE_DIRS`为`sqlite.h`头文件位置，`SQLCIPHER_LIBRARY_DIRS`为`sqlcipher.lib`或`libsqlcipher.a`所在位置。


> 如果设置了`SQLCIPHER_VERSION`将会忽略`SQLCIPHER_INCLUDE_DIRS`及`SQLCIPHER_LIBRARY_DIRS`环境变量

#### Windows

要求: 
- msvc 编译器
- nmake
- 如果python版本低于3.9， 需要确保系统安装了`tclsh`, 且在`PATH`环境变量中


#### Linux

要求: 
- gcc 编译器
- make
- libtool

## 示例

### 加密

```python
key='123456'
exist_db = 'test.db3'
newdb = 'encrypt_db.db3'

conn = sqlite3.connect(exist_db)
cur = conn.cursor()
cur.execute(f"ATTACH DATABASE '{newdb}' AS encrypted KEY '{self.key}'")
cur.execute("SELECT sqlcipher_export('encrypted')")
cur.execute("DETACH DATABASE encrypted")
assert os.path.exists(newdb)

cur.close()
conn.close()
```

### 解密

```python
key='123456'
encrypt_db = 'test.db3'

conn = sqlite3.connect(encrypt_db)
cur = conn.cursor()
cur.execute(f"PRAGMA key='{key}'") 
res = cur.execute("SELECT name FROM sqlite_master")
assert res.fetchone()[0] == 'movie'

cur.close()
conn.close()
```


### 导出为非加密db

```python
olddbname = 'encrypt_xxx.db3'
plaindbname = 'plain_xxx.db3'
key = '123456'
con = sqlite3.connect(olddbname)

cur = con.cursor()
dbname = 'plaindb'
cur.execute(f"PRAGMA key='{key}'")
cur.execute(f"ATTACH DATABASE '{plaindbname}' AS {dbname} KEY ''")
cur.execute(f"SELECT sqlcipher_export('{dbname}')")
cur.execute(f"DETACH DATABASE {dbname}")
cur.close()
con.close()

# 判断是否导出成功
assert os.path.exists(plaindbname)
```

### 修改密码

```python
dbname = 'dbtest.db3'
oldkey = '123456'
newkey = '654321'

conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute(f"PRAGMA key='{oldkey}'") 
cur.execute(f"PRAGMA rekey='{newkey}'") 
cur.close()
conn.close()
```




