# 实验室设备管理系统 个人作业文档

###### 17373240 赵婉如



## 目录

[TOC]



## 应用背景

为方便实验室进行设备管理，某大学拟开发实验室设备管理系统 来管理所有实验室里的各种设备。系统可实现管理员登录，查看现有的所有设备， 增加设备等功能。



## 系统结构设计

源码上传[GitHub](https://github.com/Ryan0v0/SoftwareEngineering_Project)



### 开发环境

* Mac OS 
* PyCharm IDE 
* Python3 
* Flask（Web框架） 
* SQLite（数据库）

### 运行方法

##### 准备

1. 安装virtualenv: `pip3 install virtualenv`

2. 创建虚拟环境: `virtualenv venv`

3. 进⼊虚拟环境: `source venv/bin/activate`

4. 安装依赖的包: `pip install -r requirements.txt`

5. 退出虚拟环境: `deactivate`

##### 运⾏ 

1. 更新数据库： `python app.py db upgrade`

2. ⽣成⽤户： `python app.py init`

3. 运⾏： `python app.py runserver`

##### 初始管理员账户

> 邮箱：zhaowrenee@gmail.com 
> 密码：666666



### 功能结构

1. 登录：管理员可以通过输入预置的账号密码进行登录。 
2. 查看设备列表：管理员在登录成功后，应立即展示所有设备信息，设备 信息应包括设备 ID 号，设备名，实验室名，购置时间，购置人。 
3. 增加设备：增加设备时应输入设备名，实验室名，购置人等信息，设备 增加成功后自动返回系统分配的设备 ID 号，购置时间应为系统自动生成(默认为增加设备的时间)。
4. *[附加] 删除设备：管理员本人购置的设备具有顶级重要性，故不能被删除*
5. *[附加] 搜索设备：输入关键词，显示名称中包含关键词的设备列表*

另外保证：

1. 对输入数据进行合法性验证，并进行友好提示。 
2. 对数据库中的密码字段加密处理。

提示 

* 设备 ID 号应保证唯一性。 
* 设备名可重复。



## 功能细节

### 一、UML图

#### 1、活动图

<img src="https://tva1.sinaimg.cn/large/00831rSTly1gdk3d824x9j30u010477y.jpg" alt="image-20200405013518204" style="zoom: 40%;" />

`app.py`中function与` templates`中HTML⽂件对应，展示在⽹⻚页中：

* index() 通过 SearchForm 实现对⽤户信息的检索和展示，并通过 index.html 
* add_device() 通过 UserForm 实现对新设备信息的添加，并调⽤ add_device.html 
* remove_device(id) 通过id删除设备，但不能删除管理员添加的设备
* login() 通过调⽤ LoginForm 实现登录，并调⽤ login.html ⽹⻚页登录，也是服务器提供的第⼀个页⾯
* 其余function对应⼀系列错误处理和必要但和数据库⽆关功能 

#### 2、用例图

![image-20200405103612687](https://tva1.sinaimg.cn/large/00831rSTly1gdk3d8vbdgj31cs0u0jxc.jpg)

#### 3、顺序图

<img src="https://tva1.sinaimg.cn/large/00831rSTly1gdk3ddn269j310r0o3ach.jpg" alt="用户使用系统顺序图 (1)" style="zoom:50%;" />

#### 4、类图



![类图](https://tva1.sinaimg.cn/large/00831rSTly1gdk3dhieb7j31jm0twdic.jpg)

* HTML使⽤Flask-wtf Bootstrap渲染功能，使界⾯更美观

* `app.Role`为⽤户设置的用户或者管理员⻆角⾊类，内部有条件⻆角⾊条件约束 

* `app.User` ⽤户类

  * 记录⽤户名、密码、id等信息，与数据库的属性进行交互 

* `app.Device` 设备类

  * 记录设备名、实验室、购置人、购置时间等信息，与数据库的属性进行交互

* FlaskForm 信息表 

  * 三种Form根据不同的操作需求，设定不同的Field

    

#### 5、状态图

![后台管理界面状态图 (https://tva1.sinaimg.cn/large/00831rSTly1gdk3diuj05j31ai0pdwip.jpg)](/Users/zhaowanru/Downloads/后台管理界面状态图 (1).png)

### ⼆、基本表单的定义

#### 表一：

| roles 身份表 |             |              |                 |            |      |      |
| ------------ | ----------- | ------------ | --------------- | ---------- | ---- | ---- |
| 名称         | 类型        | NOT NULL约束 | PRIMARY KEY约束 | UNIQUE约束 | 默认 | 外键 |
| id           | INTEGER     | √            | √               |            |      |      |
| name         | VARCHAR(64) |              |                 |            |      |      |

```mysql
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR(64), 
	PRIMARY KEY (id), 
	UNIQUE (name)
)
```


表中实体：

| **id** | **name** |
| ------ | -------- |
| **1**  | User     |
| **2**  | Admin    |

#### 表二：

| users 用户表  |              |              |                 |            |      |           |
| ------------- | ------------ | ------------ | --------------- | ---------- | ---- | --------- |
| 名称          | 类型         | NOT NULL约束 | PRIMARY KEY约束 | UNIQUE约束 | 默认 | 外键      |
| id            | INTEGER      | √            | √               |            |      |           |
| number        | VARCHAR(128) |              |                 |            |      |           |
| username      | VARCHAR(64)  |              |                 |            |      |           |
| password_hash | VARCHAR(128) |              |                 |            |      |           |
| role_id       | INTEGER      |              |                 |            |      | roles(id) |


```mysql
CREATE TABLE users (
	id INTEGER NOT NULL, 
	number VARCHAR(128), 
	username VARCHAR(64), 
	password_hash VARCHAR(128), 
	role_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (password_hash), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
)
```

表中实体：

| id   | number                  | username | password_hash                                                | role_id |
| ---- | ----------------------- | -------- | ------------------------------------------------------------ | ------- |
| 1    | zhaowrenee@gmail.com    | Admin    | pbkdf2:sha256:50000$V4ZV7KEr$42b0a9825baa100fa800d0544632a1ad7d6130504ef6c397ecfa6b02ca99298d | 2       |
| 2    | mshi@hotmail.com        | 袁帅     | pbkdf2:sha256:50000$KWFWUdY9$d1c334fe90415612c0d99301d45f3e5f9c3f482726cde598259d19ff1228c217 | 1       |
| 3    | yaoxiuying@mingding.org | 刘东     | pbkdf2:sha256:50000$rNv7gYzZ$381113b96a85934496fe06a2796893fb85689b71c373e97a5e4d9d3adfd5ef26 | 1       |
| 4    | vfan@hotmail.com        | 吴娟     | pbkdf2:sha256:50000$cA7RmNVD$7136167bd1c3163b0ec221638b8644f12f093f3450ecc4f631c72840e26f31f3 | 1       |
| 5    | panjuan@hotmail.com     | 刘玉珍   | pbkdf2:sha256:50000$hSqUMhqa$5dd222a191f376127e3dceb8244310cc7114dcceaa2d3bc5fa585a9429f66a02 | 1       |

#### 表三：

| devices 设备表 |             |              |                 |            |      |           |
| -------------- | ----------- | ------------ | --------------- | ---------- | ---- | --------- |
| 名称           | 类型        | NOT NULL约束 | PRIMARY KEY约束 | UNIQUE约束 | 默认 | 外键      |
| id             | INTEGER     | √            | √               |            |      |           |
| device_id             | VARCHAR(64)     |            |               |            |      |           |
| lab            | VARCHAR(64) |              |                 |            |      |           |
| name           | VARCHAR(64) |              |                 |            |      |           |
| password_hash  | DATETIME    |              |                 |            |      |           |
| user_id        | VARCHAR(64) |              |                 |            |      | users(id) |

```sqlite
CREATE TABLE devices (
	id INTEGER NOT NULL, 
	lab VARCHAR(64), 
	name VARCHAR(64), 
	time DATETIME, 
	user_id VARCHAR(64), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)
```
表中实体：

| id   | device_id   | lab                | name           | time                       | user_id |
| ---- | ----------- | ------------------ | -------------- | -------------------------- | ------- |
| 2    | 2020-QS-002 | 趋势传媒实验室     | 专业VR镜头     | 2020-03-31 22:12:17.000000 | 6       |
| 3    | 2020-LY-003 | 凌云科技实验室     | 专业VR镜头     | 2020-03-15 02:36:25.000000 | 6       |
| 4    | 2020-MX-004 | 盟新传媒实验室     | 联想启天2100   | 2020-03-16 23:44:42.000000 | 1       |
| 5    | 2020-CH-005 | 创汇网络实验室     | DSP实验箱      | 2020-01-17 03:29:31.000000 | 8       |
| 6    | 2020-LT-006 | 联通时科网络实验室 | 功率变换器     | 2020-04-06 07:49:29.000000 | 3       |
| 7    | 2020-HR-007 | 鸿睿思博网络实验室 | 双踪示波器     | 2020-03-05 00:48:16.000000 | 4       |
| 8    | 2020-TY-008 | 天益科技实验室     | 联想启天2100   | 2020-03-03 23:57:45.000000 | 11      |
| 9    | 2020-LY-009 | 凌颖信息信息实验室 | 投影机         | 2020-02-03 20:11:21.000000 | 10      |
| 10   | 2020-DM-010 | 迪摩科技实验室     | 曙光天阔服务器 | 2020-02-12 20:46:27.000000 | 1       |
| 11   | 2020-LR-011 | 联软传媒实验室     | 联想启天2100   | 2020-02-21 11:02:09.000000 | 11      |



## 展示后修改及优化说明

#### 1. 对设备ID进行改进

通常设备编号都有其实际含义，而且通常有使用年限的规定。所以我在展示后对ID进行设计，更加符合实际情况。

id的格式为`购置年份-实验室名称前两字的拼音大写字母缩写-设备编号（三位数补全）`

其中，提取实验室名称的拼音大写字母缩写，我通过利用xpinyin包来完成。

页面中显示的“设备编号”为人为构造的“设备id”，区别于数据库表中自动生成的id。

#### 2. 删除设备时进行安全性提示

因为增加了删除设备这一附加功能，而设备删除是一个具有安全隐患的操作。为了避免发生误操作的情况，在点击“删除”按钮后系统会提示“确定要删除吗？”，此时只有点击”确定“时才会执行删除操作。



## 整体效果及操作流程

##### 1. 登录页面：

![image-20200406201227591](https://tva1.sinaimg.cn/large/00831rSTly1gdlly5cozmj30zo0me4ej.jpg)

###### 如果输入错误密码：

![image-20200406230722637](https://tva1.sinaimg.cn/large/00831rSTly1gdlly48yihj31jz0u04qq.jpg)

###### 如果输入非管理员账号：

![image-20200406230651226](https://tva1.sinaimg.cn/large/00831rSTly1gdlly2iszoj31jj0u04qq.jpg)

##### 2. 查看设备列表：

![image-20200406201729178](https://tva1.sinaimg.cn/large/00831rSTly1gdllxyj3zwj31hi0u0gxl.jpg)

为了批量生成数据，使用python中的faker包来生成不同类型和格式的随机数据来模拟真实情形

其中，设定系统的管理员拥有顶级权限，即可以管理设备购置记录，并且我这里附加了一个功能：其本身购置的设备记录用红色背景标出，表明其重要性。

##### 3. 增加设备：

![image-20200406202054034](https://tva1.sinaimg.cn/large/00831rSTly1gdllxwgtrcj31w20u0wht.jpg)

这里对输入数据进行合法性验证：

* 设备名不能为空/长度超出32个字符

* 购置人必须是数据库中的用户，这里主要是为了确保我们拥有购置人的详细信息（比如说邮箱等），否则我们无法确认购置人的身份、无法联系到他。

![image-20200406202126753](https://tva1.sinaimg.cn/large/00831rSTly1gdllxuakdwj31i80u0ds1.jpg)

##### 4. 删除设备：

![image-20200406201835473](https://tva1.sinaimg.cn/large/00831rSTly1gdllxsykdpj31n70u0n9i.jpg)

这里考虑了可能有设备废弃或者是转让，需要删除设备的情况。

拥有顶级权限的管理员本人购置的设备无法删除。

##### 5. 关键词搜索：

![image-20200406201938874](https://tva1.sinaimg.cn/large/00831rSTly1gdllxr1vhjj32ic0ngtbs.jpg)

##### 6. 注销：

完成操作后点击注销，即可退出登录，此时返回登录页面，因为之前选择了记住密码，下次可直接登录。

