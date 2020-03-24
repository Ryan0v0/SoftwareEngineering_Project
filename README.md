# SoftwareEngineering_Project

### 北航软工个人项目 实验室设备管理系统

###### 17373240 赵婉如



## 应用背景

为方便实验室进行设备管理，某大学拟开发实验室设备管理系统 来管理所有实验室里的各种设备。系统可实现管理员登录，查看现有的所有设备， 增加设备等功能。



## 系统结构设计

源码上传[GitHub](https://github.com/Ryan0v0/SoftwareEngineering_Project)



### 开发环境

Mac OS 
PyCharm IDE 
Python3 
Flask（Web框架） 
SQLite（数据库）

### 运行方法

##### 准备

1. 安装virtualenv: `pip3 install virtualenv`

2. 创建虚拟环境: `virtualenv venv`

3. 进⼊虚拟环境: `source venv/bin/activate`

4. 安装依赖的包: `pip install -r requirements.txt`

5. 退出虚拟环境: `deactivate`

##### 运⾏ 

1. 更新数据库： `python app.py db upgrade`

2. ⽣成管理员⽤户： `python app.py init`

3. 运⾏： `python app.py runserver`

##### 初始管理员账户

> 邮箱：zhaowrenee@gmail.com 
> 密码：666666



### 功能结构

1. 登录：管理员可以通过输入预置的账号密码进行登录。 
2. 查看设备列表：管理员在登录成功后，应立即展示所有设备信息，设备 信息应包括设备 ID 号，设备名，实验室名，购置时间，购置人。 
3. 增加设备：增加设备时应输入设备名，实验室名，购置人等信息，设备 增加成功后自动返回系统分配的设备 ID 号，购置时间应为系统自动生成(默认为增加设备的时间)。