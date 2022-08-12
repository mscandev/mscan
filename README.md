# mscan

##  简介

一款web综合扫描工具，集成最好用的工具，方便一键漏洞扫描。

由于是模块化，方便二次开发，更新第三方工具不影响整个扫描器的使用。

# 主要功能

支持 子域名收集、POC批量验证、目录扫描、检测CDN、域名转IP、主机扫描、过滤重复、检测HTTP状态、压缩程序、XRAY扫描。

# 使用说明

简单用法

```
添加域名
vim domain.txt

启动扫描
python3 mscan.py  (默认使用全部模块)
```

# 架构图

![image-20220811223546040](https://raw.githubusercontent.com/mscandev/mscan/master/images/mscan.png)

## Licenses

本工具禁止进行未授权商业用途，禁止二次开发后进行未授权商业用途。

本工具仅面向合法授权的企业安全建设行为，在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。

如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。

在使用本工具前，请您务必审慎阅读、充分理解各条款内容，限制、免责条款或者其他涉及您重大权益的条款可能会以加粗、加下划线等形式提示您重点注意。

除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要使用本工具。您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。

## 捐赠打赏

mscan的迭代开发离不开每一位用户的支持，如果你觉得mscan好用，麻烦在GitHub中点击 `star`;目前mscan为免费软件，如果你对软件非常认可，也可以给我们进行捐赠，捐赠名单将会公示在mscan主页中，同时对于捐赠的小伙伴，将会获得技术优先支持~