"""
flask1.0开始, 类似Django, 通过终端执行封装的脚本命令flask run来运行应用, 不再需要调用app.run()
新的形式更加有利于 灵活修改环境配置

export FLASK_APP=xx.py  # 指定flask应用所在的文件路径
export FLASK_ENV=development  # 设置项目的环境, 默认是生产环境
flask run -h 0.0.0.0 -p 8000  # 启动测试服务器并接受请求

环境变量相当于 系统的全局变量, 所有程序可用
# 获取环境变量
export  # 查看所有环境变量
echo $环境变量   # 查看指定的环境变量

# 设置环境变量
export 环境变量名=值  # 给本次会话设置环境变量, 一旦终端关闭, 环境变量会清空
# 将环境变量写入配置文件(.bashrc/.bash_profile), 重新打开终端时再次加载环境变量


定义路由的三个细节
1. 路由对应的URL必须以 / 开头
2. app.url_map 获取所有路由规则
    路由规则中主要包含 URL资源段、支持的请求方式、视图函数标记 三部分内容
3. app.route() 的 methods参数 指定路由支持的请求方式

路由变量的作用是 传递URL路径参数, 实现动态URL
格式: /xx/<路由变量>

路由转换器的作用是 对URL传递的参数进行格式校验, 类似Django设置URL时的正则表达式参数
格式: /xx/<转换器名:路由变量>
所有的转换器类都继承自 BaseConverter 类

除了使用内置的变量转换器, 开发者还可以自定义转换器, 更加灵活的校验路由变量
使用自定义转换器的步骤
    定义转换器类, 继承BaseConverter
    设置regex属性 (正则匹配规则)
    应用添加自定义转换器


flask的请求数据通过 request 对象来获取


"""

# 新建文件helloflask.py
# 导入Flask类
from flask import Flask, request

# 自定义转换器:
# 1.定义转换器类, 继承BaseConverter
# 2.设置regex属性 (正则匹配规则)
# 3.添加自定义转换器
from werkzeug.routing import BaseConverter

from werkzeug.datastructures import FileStorage

# 创建Flask对象, 接收一个参数__name__，它会指向程序所在的包 (后续具体讲解)
# 1.创建Flask应用
app = Flask(__name__)


# 装饰器的作用是将路由映射到视图函数 index
# 3.定义路由
# @app.route("/")
# def index():
#     return 'hello flask'

# 1.路由对应的URL必须以/开头
# 2.通过app的url_map属性获取所有的路由规则 (URL资源段 支持的请求方式 视图函数标记)
# 3.可以通过route方法的methods参数指定路由支持的请求方式
# @app.route("/hello", methods=['post', 'get'])
# def index():
#     return 'index'

# 路由变量: 传递URL路径参数
# 格式: /user/<路由变量名>
# @app.route("/user/<userid>")
# def index(userid):  # 必须定义同名形参接收路由变量的值
#     print(userid)
#     return 'index'

# 路由转换器: 对路由变量进行格式校验  条件不满足返回404
# 格式: /user/<路由转换器名:路由变量>
# @app.route("/user/<int:userid>")   # int: 内置转换器, 要求1-n个整数
# def index(userid):
#     print(userid)
#     return "index"


# 1.定义转换器类
# class MobileConverter(BaseConverter):

    # 2.设置regex属性(匹配规则)
    # regex = '1[3-9]\d{9}$'  # 不要设置开头的^


# 3.添加自定义转换器
# app.url_map.converters['mob'] = MobileConverter


# @app.route('/user/<mob:mobile>')
# def index(mobile):
#     print(mobile)
#     return "index"


@app.route("/", methods=['get', 'post'])
def index():
    # 获取请求的基础数据
    print(request.url)  # 请求的URL
    print(request.method)  # 本次请求的请求方式
    print(request.headers)  # 获取请求头信息  类字典对象
    print(request.headers['Host'])
    print(request.headers.get('Host'))  # 建议使用get方法, 键不存在不报错

    # 请求传递数据
    # 1> URL路径 -> 路由变量
    # 2> 查询字符串 get
    # 3> 请求体  post
    # 4> 请求头 -> request.headers

    # 获取查询字符串 -> request.args  xx?name=zs&age=20  类字典对象
    print(request.args.get('name'))
    print(request.args.get('age'))

    # 请求体:   键值对(表单)   文本(json/xml)  文件(图片/音频)
    # 获取post键值对 -> request.form  类字典对象
    print(request.form.get('weight'))
    print(request.form.get('height'))

    # 获取post文本数据 -> request.data / request.json
    # print(request.data)  # 返回bytes类型

    # print(request.json.get('address'))  # request.json直接将json字符串转为字典

    # 获取post文件 -> request.files  类字典对象
    file = request.files.get("001")  # type: FileStorage
    print(type(file))  # 返回 FileStorage文件对象
    # 将文件保存到本地
    # file.save('123.jpg')


    # 获取post文件 -> request.files  类字典对象
    file = request.files.get("avatar")  # type: FileStorage
    # print(type(file))  # 返回 FileStorage文件对象
    # 将文件保存到本地
    file.save('123.jpg')

    return 'index'








# Flask应用程序实例的 run 方法 启动 WEB 服务器
if __name__ == "__main__":
    # 2.运行应用 (启动一个测试服务器, 接收请求并调用对应的视图函数)
    # app.run()

    """
    app.run的参数
    可以指定运行的主机IP地址，端口，是否开启调试模式
    # host: 绑定的ip(域名)  0.0.0.0
    # port: 监听的端口号
    # debug: 是否开启调试模式  1> 可以在网页上显示python错误 2> 更新代码后测试服务器自动重启
    """

    # app.run(host='0.0.0.0', port=8000, debug=True)

    # print(app.url_map)
    # 获取路由信息
    # for rule in app.url_map.iter_rules():
    #     print(rule.rule, rule.methods, rule.endpoint)
    # app.run()

    # 获取所有的转换器 {转换器名: 转换器类}
    print(app.url_map.converters)
    app.run()




