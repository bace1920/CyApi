# CyApi
基于`Django` & `uwsgi`的分布式网络检测API

## 功能
提供简单的接口供用户获取所有分布服务器到一个网络地址的连通性信息，目前支持：
 - Ping检测

## 依赖
 - uwsgi
 - Django
 - requests
 - pexpect

## 使用
 - 根据提示修改`./server.json`
 - 修改`./CyApi_uwsgi.ini`的`chdir`配置
 - 根据提示修改`./CyApi/settings.py`的`CyApi配置信息`
 - http服务的`timeout`不应低于6秒

## ToDo
 - 改为异步处理，不产生处于等待状态的TCP连接
 - TCPing检测
 - Get检测
 - 内网安全认证
