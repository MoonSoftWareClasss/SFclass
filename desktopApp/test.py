import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口
        self.setWindowTitle('信号与槽示例')
        self.setGeometry(100, 100, 300, 200)

        # 创建控件
        self.num1_input = QLineEdit(self)  # 输入框1
        self.num2_input = QLineEdit(self)  # 输入框2
        self.result_label = QLabel('结果: ', self)  # 显示结果
        self.calculate_button = QPushButton('计算和', self)  # 计算按钮

        # 连接按钮点击事件到后端处理函数
        self.calculate_button.clicked.connect(self.calculate_sum)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.num1_input)
        layout.addWidget(self.num2_input)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def calculate_sum(self):
        # 获取输入框中的数字并计算和
        try:
            num1 = float(self.num1_input.text())
            num2 = float(self.num2_input.text())
            result = num1 + num2
            self.result_label.setText(f'结果: {result}')
        except ValueError:
            self.result_label.setText('请输入有效的数字')

# 创建应用程序实例
app = QApplication(sys.argv)

# 创建窗口实例
window = MyApp()
window.show()

# 运行应用程序
sys.exit(app.exec_())
