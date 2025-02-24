from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel
from qfluentwidgets import *

class MainPage(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isInSelectionMode = False
        self.setObjectName("mainPage")
        self.stackedWidget = PopUpAniStackedWidget(self)
        #create widgets
        self.pushButton = PushButton("开始", self)
    def __initWidgets(self):
        
        self.stackedWidget.addWidget(self.pushButton)
        self.stackedWidget.setCurrentWidget(self.pushButton)
        self.pushButton.clicked.connect(self.switchToNumberPage)
        
        
    def switchToNumberPage(self):
        print("Switch to NumberPage")
        
    
    