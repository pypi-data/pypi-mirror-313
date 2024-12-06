import pydash
import requests
import webview
from webview import Window


class API:

    def __init__(self):
        super().__init__()
        self.window_index = 0
        self.web_data = {}

    def get_data(self):
        return self.web_data

    def set_data(self, data):
        self.web_data = data
        return self.web_data

    def _refresh_web_data(self):
        self._window().evaluate_js("refreshData();")

    def _update_data(self, key, value):
        pydash.objects.update(key, value)
        self._refresh_web_data()

    # 设置当前窗口
    def _set_window(self, window_index):
        self.window_index = window_index

    def _window(self) -> Window:
        from idepy.core import settings
        return settings.WINDOW_MAPPER.get(settings.WINDOW_INDEX, None)

    # 代理请求内容
    def iglobal_proxy_request_get(self, url, params=None, headers=None, cookies=None, timeout=60):
        if cookies is None:
            cookies = {}

        if headers is None:
            headers = {
                'User-Agent': self._window().evaluate_js('navigator.userAgent')
            }

        if params is None:
            params = {}

        res = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=timeout)
        data = None
        if res.status_code == 200:
            try:
                # 自动将 JSON 文本转换为字典
                data = res.json()
            except ValueError as e:
                data = res.text

        return {
            "status": res.status_code,
            "data": data,
        }

    # 代理请求内容
    def iglobal_proxy_request_post(self, url, request_data=None, headers=None, cookies=None, timeout=60):
        if cookies is None:
            cookies = {}

        if headers is None:
            headers = {
                'User-Agent': self._window().evaluate_js('navigator.userAgent')
            }

        if request_data is None:
            request_data = {}

        res = requests.get(url, data=request_data, headers=headers, cookies=cookies, timeout=timeout)
        data = None
        if res.status_code == 200:
            try:
                # 自动将 JSON 文本转换为字典
                data = res.json()
            except ValueError as e:
                data = res.text

        return {
            "status": res.status_code,
            "data": data,
        }

    # 代理请求内容
    def iglobal_proxy_request_json(self, url, request_data=None, headers=None, cookies=None, timeout=60):
        if cookies is None:
            cookies = {}

        if headers is None:
            headers = {
                'User-Agent': self._window().evaluate_js('navigator.userAgent')
            }

        if request_data is None:
            request_data = {}

        res = requests.get(url, json=request_data, headers=headers, cookies=cookies, timeout=timeout)
        data = None
        if res.status_code == 200:
            try:
                # 自动将 JSON 文本转换为字典
                data = res.json()
            except ValueError as e:
                data = res.text

        return {
            "status": res.status_code,
            "data": data,
        }


    def iglobal_window_close(self):
        """
        关闭当前窗口
        :return:
        """
        self._window().destroy()

    def iglobal_window_minimize(self):
        """
        最小化窗口
        :return:
        """
        self._window().minimize()

    def iglobal_window_maximize(self):
        """
        最大化窗口
        :return:
        """
        self._window().maximize()

    def iglobal_window_hide(self):
        """
        隐藏当前窗口
        :return:
        """
        return self._window().hide()

    def iglobal_window_show(self):
        """
        显示当前窗口
        :return:
        """
        return self._window().show()

    def iglobal_clear_cookies(self):
        """
        清理cookies
        :return:
        """
        return self._window().clear_cookies()
