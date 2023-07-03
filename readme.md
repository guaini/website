### 代码说明

* homework文件夹中内容为项目的基本配置文件
* backend文件夹中内容如下：
  * static文件夹：存放所有用到的css文件和图片
  * templates文件夹：存放用到的html文件
  * index.py：负责图片排序等操作的分派函数，将请求分派到views.py的具体函数中
  * models.py：包含数据库中所有表的定义，以类的形式呈现
  * pictures.py：负责图片收藏，点赞，获取图片信息等操作的分派函数，将请求分派到views.py的具体函数中
  * search.py：搜索功能的实现函数
  * urls.py：各分派函数以及图片上传函数的url转发配置
  * user.py：负责用户注册，登录，更新信息等操作的分派函数，将请求分派到views.py的具体函数中
  * views.py：处理各种请求的函数的实现。