# CyApi接口规范文档

CyApi工作在`Http`协议下，采用`json`格式作为信息载体

## Network API

### Ping

Ping检测应当返回包含如下字段的`json`结果，当`status`不为`OK`时，时延字段应当为`9999.99`


 - `location` String 服务器所在地的名称简写，例如`UK` `HK`
 - `status` - String `OK`代表正常 `Unknow server`代表DNS解析错误 `Time out`代表超时，目标不可达
 - `max` Number 最大时延
 - `min` Number 最小时延
 - `avg` Number 平均时延
 - `mdev` Number 标准差
