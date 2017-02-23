# daka

登录网站并打卡（或领金币等）。

当前master是用splinter这个python库实现的。更加符合“人生苦短，我用python”的宗旨O(∩_∩)O~

若要查看原始实现，请切换到分支raw（该分支的后续更新未知）。

目前实现了：
* 沪江部落领金币
* 字幕组打卡
* 蚂蜂窝打卡
* 虾米打卡
* 百度（贴吧/知道）签到

> 很多网站的打卡规则发生了变动，有的甚至取消了打卡功能。因此，有些之前实现打卡的网站不再适用

# 第三方依赖
1. splinter

# 使用
1. 配置`Site/settings.py`中的`browser_params`值
2. 在文件`samples/user_config.ini`中配置对应网站的用户名密码，例如：
```
[hujiang]
username=ictar
password=123456
```
3. 运行samples/run.py

# 扩展
1. 导入Site模块：`from Site import Site`
2. 新建类继承Site
3. 查看网站登录逻辑，编写对应的登录url(`login_url`)、登录表单id/name值以及对应的登录信息、登录按钮等。调用`_login`方法。
4. 查看网站的打卡逻辑
	* 对于直接访问url即可打卡的，编写对应的打卡url。调用`_daka`方法。
	* 对于需要点击进行打卡的，则查看对应点击按钮的获取方式，调用`_click`方法

注：具体可以参考samples目录下对应网站类的实现

# TO-DO
* 优酷
* 淘宝
* 顺丰签到打卡
