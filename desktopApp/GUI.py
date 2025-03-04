import sys
import random
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt5.QtGui import QPainter, QConicalGradient, QColor
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QGraphicsOpacityEffect, QLineEdit)
from data_create import *

class HeartRateWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能手环")
        self.setGeometry(100, 100, 400, 600)
        self.heart_rate = 72
        self.initUI()
        self.initAnimations()
        self.initStyle()

    def initUI(self):
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        # 顶部状态栏
        top_bar = QHBoxLayout()
        self.steps_label = QLabel(f"参数: {random.randint(3000, 10000)}")
        self.id_label = QLabel(f"机器id: {random.randint(150, 450)}kcal")
        top_bar.addWidget(self.steps_label)
        top_bar.addWidget(self.id_label)
        
        self.distance_label = QLabel("跑步距离:")
        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText("公里")
        self.distance_input.setMaximumWidth(80)

        top_bar.addWidget(self.distance_label)
        top_bar.addWidget(self.distance_input)
        top_bar.addWidget(self.steps_label)
        top_bar.addWidget(self.id_label)
        
        # 心率显示区域
        self.heart_display = QWidget()
        self.heart_display.setMinimumSize(300, 300)

        # 心率数值标签
        self.heart_label = QLabel(str(self.heart_rate))
        self.heart_label.setAlignment(Qt.AlignCenter)
        self.heart_label.setObjectName("heartLabel")

        # 底部控制按钮
        self.start_btn = QPushButton("开始监测")
        self.stop_btn = QPushButton("停止监测")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)

        # 组装布局
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.heart_display, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.heart_label)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # 定时更新数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)

    def initAnimations(self):
        # 心率数字跳动动画
        self.anim = QPropertyAnimation(self.heart_label, b"scale")
        self.anim.setDuration(500)
        self.anim.setKeyValueAt(0, 1.0)
        self.anim.setKeyValueAt(0.5, 1.2)
        self.anim.setKeyValueAt(1, 1.0)

        # 渐隐渐显效果
        self.opacity_effect = QGraphicsOpacityEffect(self.heart_display)
        self.heart_display.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(2000)
        self.opacity_anim.setLoopCount(-1)
        self.opacity_anim.setStartValue(0.8)
        self.opacity_anim.setEndValue(1.0)

    def initStyle(self):
        # 应用样式表
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e
                );
                color: #ffffff;
                font-family: 'Segoe UI';
            }
            QLabel#heartLabel {
                font-size: 48px;
                font-weight: bold;
                color: #e94560;
            }
            QPushButton {
                background-color: rgba(255,255,255,0.1);
                border: 2px solid #e94560;
                border-radius: 15px;
                padding: 10px 20px;
                min-width: 120px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e94560;
            }
                    QLineEdit {
            background-color: rgba(255,255,255,0.1);
            border: 1px solid #e94560;
            border-radius: 5px;
            padding: 5px;
            color: #ffffff;
        }
        QLineEdit:focus {
            border: 2px solid #e94560;
        }
        """)

    def paintEvent(self, event):
        """自定义绘制心率圆环"""
        painter = QPainter(self.heart_display)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景圆环
        rect = self.heart_display.rect().adjusted(10, 10, -10, -10)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 30))
        painter.drawEllipse(rect)

        # 绘制动态心率圆环
        gradient = QConicalGradient(rect.center(), -90)
        gradient.setColorAt(0, QColor(233, 69, 96))
        gradient.setColorAt(0.5, QColor(255, 106, 0))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        start_angle = 90 * 16  # 0度在3点钟方向，需要偏移90度
        span_angle = (self.heart_rate % 100) * 3.6 * 16  # 百分比转角度
        painter.drawArc(rect, start_angle, span_angle)

    def update_data(self):
        """模拟实时数据更新"""
        self.heart_rate = random.randint(60, 160)
        self.heart_label.setText(str(self.heart_rate))
        self.anim.start()
        self.update()  # 触发重绘

    def start_monitoring(self):
        """开始监测"""
        self.timer.start(1000)  # 每秒更新
        self.opacity_anim.start()
        self.start_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)

    def stop_monitoring(self):
        """停止监测"""
        self.timer.stop()
        self.opacity_anim.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeartRateWidget()
    
    # 连接按钮信号
    window.start_btn.clicked.connect(window.start_monitoring)
    window.stop_btn.clicked.connect(window.stop_monitoring)
    
    window.show()
    sys.exit(app.exec_())