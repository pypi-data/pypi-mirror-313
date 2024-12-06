import idepy
from idepy.core import utils
from idepy.core import API
from idepy.core.main import get_app

window_key = ""


# 窗口通讯API
class WindowAPI(API):

    def __init__(self):
        super().__init__()
        # 设置窗口初始数据
        self.web_data = {

        }


# 主口配置项
window_config = {
    "title": "子窗口",
    "js_api": WindowAPI(),

    # 设置窗口对应的html文件
    "url": f"/windows/{window_key}/index.html",
}


# 加载并显示窗口，同时返回窗口对象
def load_window():
    return get_app().create_window(**window_config)
