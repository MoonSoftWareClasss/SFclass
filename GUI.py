import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QLabel, QGroupBox, QPushButton

class BloodPressureSimulator(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle('血压计模拟器')
        self.setGeometry(100, 100, 400, 300)

        # 创建布局
        layout = QVBoxLayout()

        # 创建参数设置部分
        self.parameter_group = QGroupBox("参数设置")
        form_layout = QFormLayout()

        # 创建输入框和控件
        self.systolic_mean = QDoubleSpinBox()
        self.systolic_range = QDoubleSpinBox()
        self.diastolic_mean = QDoubleSpinBox()
        self.diastolic_range = QDoubleSpinBox()
        self.line_count = QSpinBox()
        self.sample_period = QSpinBox()

        # 设置默认值
        self.systolic_mean.setValue(120)
        self.systolic_range.setValue(10)
        self.diastolic_mean.setValue(80)
        self.diastolic_range.setValue(10)
        self.line_count.setValue(10)
        self.sample_period.setValue(30)

        # 添加控件到表单布局
        form_layout.addRow("舒张压均值", self.systolic_mean)
        form_layout.addRow("舒张压方差", self.systolic_range)
        form_layout.addRow("收缩压均值", self.diastolic_mean)
        form_layout.addRow("收缩压方差", self.diastolic_range)
        form_layout.addRow("线程序数", self.line_count)
        form_layout.addRow("采样周期", self.sample_period)

        # 设置参数组
        self.parameter_group.setLayout(form_layout)

        # 添加参数设置到主布局
        layout.addWidget(self.parameter_group)

        # 创建开始和停止按钮
        self.start_button = QPushButton("开始")
        self.stop_button = QPushButton("停止")

        # 添加按钮到布局
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        # 设置窗口主布局
        self.setLayout(layout)

# 启动应用程序
app = QApplication(sys.argv)
window = BloodPressureSimulator()
window.show()
sys.exit(app.exec_())
