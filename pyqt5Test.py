import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):

        super().__init__(parent)

    def interceptRequest(self, info):

        reqInfo = info.requestUrl() + info.requestMethod() + info.firstPartyUrl()
        if 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list' in reqInfo\
            and 'https://qun.qq.com/member.html#gid=781829297' in reqInfo:
            verify = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QWebEngineView()
    page = QWebEnginePage()
    page.setUrl(QUrl(
        "https://qun.qq.com/member.html#gid=781829297"))
    t = WebEngineUrlRequestInterceptor()
    page.profile().setRequestInterceptor(t)
    view.setPage(page)
    view.resize(600, 400)
    view.show()
    sys.exit(app.exec_())
