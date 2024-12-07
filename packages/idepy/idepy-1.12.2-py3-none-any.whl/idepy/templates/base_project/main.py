import idepy
from idepy.core import IDEPY
from idepy.core import utils
from idepy.core import API
from idepy.core.main import get_app

""" 
文档地址：https://idepy.com/document
"""


# 主窗口通讯API
class MainWindow(API):

    def __init__(self):
        super().__init__()
        # 设置主窗口
        self.web_data = {
            "version": idepy.__version__
        }

    # 客户端可通过api.btn_click("msg")调用本函数，并异步返回数据
    def btn_click(self, msg):
        # 执行网页JS
        super()._window().evaluate_js(f'alert("消息提示：{msg}")')

        # 其他程序逻辑
        # ....

        # 返回数据给js
        return {
            "msg": f"你好，世界！{msg}"
        }


# 主窗口配置项
main_window_config = {
    "title": "程序主窗口",
    "js_api": MainWindow(),
}


def main():
    # 创建桌面应用实例
    app = IDEPY("IDEPY", main_window_config)

    # 检查当前设备是否支持edgechroium内核，不支持则提示升级
    app.check_support_and_update_edgechromium()

    # utils为工具类，如：utils.get_device_id获取当前设备Id
    print("设备ID", utils.get_device_id())

    # 启动APP，debug为True打开网页开发者工具
    app.start(debug=False)


if __name__ == '__main__':
    main()
