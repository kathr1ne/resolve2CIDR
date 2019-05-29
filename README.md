# resolve2CIDR

解析[IPIP.net](www.ipip.net)   官方提供的mydata*.txtx文件 将起始IP段合并为 CIDR 格式

## 依赖

* [pandas](https://github.com/pandas-dev/pandas)  科学计算模块 大幅提高解析效率
* [netaddr](https://github.com/drkjam/netaddr) Python的网络地址操作库 主要用来合并网段
