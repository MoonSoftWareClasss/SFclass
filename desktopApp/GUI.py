# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel,QHBoxLayout   
from qfluentwidgets import FluentWindow
from qfluentwidgets import OpacityAniStackedWidget, PopUpAniStackedWidget, setTheme, PushButton
from qfluentwidgets import SegmentedWidget
from qfluentwidgets import FluentIcon as FIF

class MainWindow(FluentWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isInSelectionMode = False
        self.setObjectName("mainWindow")
        self.createWidgets()
        self.initWidget()
        
    
    def createWidgets(self):
        self.totalStackWidget = OpacityAniStackedWidget(self)
        self.splashScreen = SplashScreen(self)
        # subMainWindow is used to put navigation interface and subStackWidget
        self.subMainWindow = QWidget(self)
        # that need to be displayed on the right side of navigationInterface
        self.subStackWidget = PopUpAniStackedWidget(self.subMainWindow)
        self.pushButton = PushButton(FIF.FOLDER,"开始", self)
        # create navigation interface
        self.navigationInterface = SegmentedWidget(self.subMainWindow)

    def initWidget(self):
        self.initWindow()
        # self.subStackWidget.addWidget(self.mainPage)
        self.stackedWidget.addWidget(self.pushButton)
        self.stackedWidget.setAlignment(self.pushButton, Qt.AlignCenter)
        
    def initWindow(self):
        r = self.devicePixelRatioF()
        # w, h = desktop.width(), desktop.height()
        self.resize(500,800)
        self.setWindowTitle(self.tr("智能手环"))
        # self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
        
        

    
class SplashScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground)
        # color = '2b2b2b'
        # self.setStyleSheet(f'background:#{color}')
        
        
if __name__ == '__main__':
    # setTheme("dark")
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()