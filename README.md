# resolve2CIDR

解析[IPIP.net](www.ipip.net)   官方提供的mydata*.txtx文件 将起始IP段合并为 CIDR 格式

## 主要依赖

* [pandas](https://github.com/pandas-dev/pandas)  科学计算模块 大幅提高解析效率
* [netaddr](https://github.com/drkjam/netaddr) Python的网络地址操作库 主要用来合并网段

## 相关优化

```txt
1. 读取优化
    设置 names 和 usecols 只读取需要的列

2. 内存占用优化
    需要的数据不需要做什么计算 读取data的时候统一设置 dtype 为 category 类型 降低90%+ 内存占用
    参考文章：https://zhuanlan.zhihu.com/p/47957596

2. 迭代优化
    数据量偏大 使用python for循环 效率比较慢
    在不断改代码测试时间效率中发现 循环pandas dataframe中的数据时 使用 .itertuples() 方法 效率大幅度提高 如果处理数据时 能用pandas矢量化计算 优先使用矢量化计算
    参考文章：http://www.xiejingyang.com/2018/04/24/high-performance-pandas-code/
```

## .txtx 源文件格式注意事项

```txt
    1. 国家分类的时候 主要根据 country_code[国家代码] 和
    continent_code[大洲代码]分类
    country_code    - 分类决定部分国家
    continent_code  - 分类欧洲地区 将欧洲地区统一为一个List
    注意事项：欧洲地区包含 大洲代码为 RU 的 俄罗斯 而俄罗斯
    我们需要单独分类出来[ru.list] 所以 欧洲地区需要从中剔除掉
    俄罗斯 避免重复合段

    2. 分类中国各省的时候 conntry_code 为CN的 只包含中国大陆
    不包含 香港 台湾 澳门
```
