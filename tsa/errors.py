# # 错误处理函数
#
#
# from tsa import app
#
# '''
# 使用 app.errorhandler() 装饰器注册一个错误处理函数，它的作用和视图函数类似，当 404 错误发生时，这个函数会被触发，返回值会作为响应主体返回给客户端
# '''
#
#
# @app.errorhandler(404)  # 传入要处理的错误代码
# def page_not_found(e):  # 接受异常对象作为参数
#     return  404  # 返回状态码
#
#
# @app.errorhandler(400)
# def bad_request(e):
#     return  400
#
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     return 500
