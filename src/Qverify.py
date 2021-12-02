import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication

verifyTemp = False
QGid = 716688204
verifyStatus = 0


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)

    def interceptRequest(self, info):
        global verifyTemp
        reqInfo = str(info.requestUrl()) + str(info.requestMethod()) + str(info.firstPartyUrl())
        if 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list' in reqInfo \
                and 'https://qun.qq.com/member.html#gid=' in reqInfo:
            if getQGid() in reqInfo:
                print('验证成功')
                global verifyStatus
                verifyStatus = getSuccess()
            global app
            # noinspection PyUnresolvedReferences
            app.quit()


def verify():
    global app
    app = QApplication(sys.argv)
    view = QWebEngineView()
    page = QWebEnginePage()
    page.setUrl(QUrl(
        "https://qun.qq.com/member.html#gid=" + getQGid()))
    t = WebEngineUrlRequestInterceptor()
    page.profile().setRequestInterceptor(t)
    view.setPage(page)
    view.resize(500, 320)
    view.show()
    # noinspection PyUnresolvedReferences
    app.exec_()


def getQGid():
    return str(QGid ^ 70127613)


def getSuccess():
    return QGid ^ 716687429


app = None
