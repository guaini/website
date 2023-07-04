# 系统安全报告
## 概述
本报告对一款具备登录功能和图片查看功能的Web应用进行了系统安全评估。评估的目标是确定系统的安全性、评估可能存在的风险，并提供相关的防护措施。通过对系统的安全性进行全面分析，我们能够确保用户数据和系统的保密性、完整性和可用性。


## 静态代码检测
使用**pycodestyle**工具进行代码检查。
![检查结果](https://upload-images.jianshu.io/upload_images/27526813-bf9bebb693ea1a99.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
没有发现代码中存在安全性问题

## 动态渗透测试（弱口令漏洞）
**漏洞描述**：
目标网站管理入口（或数据库等组件的外部连接）使用了容易被猜测的**简单字符口令**、或者是**默认系统账号口令**。

由于登录过程中没有设置验证码，因此可以直接使用burpsuite进行爆破。

使用Burp Suite抓包时，发现请求信息被抓取，且登录账号和密码都是明文，可以遍历请求测试。
![](https://upload-images.jianshu.io/upload_images/27526813-21a4efbea1dd671d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

使用大小为12801的密码字典进行爆破测试，用户密码被破译。
![](https://upload-images.jianshu.io/upload_images/27526813-be951242d3fbbd95.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

风险评级：**高风险**

安全建议：
- 在登录时增加验证码功能
- 默认口令以及修改口令都应保证复杂度，比如：大小写字母与数字或特殊字符的组合，口令长度不小于8位等


## 参考资料
[软件的安全性测试](https://zhuanlan.zhihu.com/p/412994661)

[Python 常用静态代码检查工具简介](https://www.jianshu.com/p/a61afb09026a)

[Web渗透测试（全流程）](https://blog.csdn.net/qqchaozai/article/details/102515046)

[密码爆破字典](https://github.com/zxcvbn001/password_brute_dictionary)