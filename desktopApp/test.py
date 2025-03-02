# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel

from qfluentwidgets import *

class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            Demo{background: white}
            QLabel{
                font: 20px 'Segoe UI';
                background: rgb(242,242,242);
                border-radius: 8px;
            }
        """)
        self.resize(900, 1000)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        
        # 创建主界面容器
        self.mainInterface = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainInterface)
        
        # 创建标题标签
        self.mainTitle = QLabel('TEST', self.mainInterface)
        self.mainTitle.setAlignment(Qt.AlignTop)
        
        # 创建 TogglePushButton
        self.toggleButton = TogglePushButton('开始', self.mainInterface)
        self.toggleButton.clicked.connect(self.onToggleButtonClicked)
        
        # 将控件添加到主界面布局
        self.mainLayout.addWidget(self.mainTitle)
        self.mainLayout.addWidget(self.toggleButton)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        
        self.dataInterface = QLabel('Data Interface', self)

        # add items to pivot
        self.addSubInterface(self.mainInterface, 'mainInterface', '首页')
        self.addSubInterface(self.dataInterface, 'dataInterface', '数据')

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 0, 30, 30)

        self.stackedWidget.setCurrentWidget(self.mainInterface)
        self.pivot.setCurrentItem(self.mainInterface.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k:  self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))


    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)

    def onToggleButtonClicked(self):
        if self.toggleButton.isChecked():
            print("按钮被打开")
        else:
            print("按钮被关闭")
            
if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()