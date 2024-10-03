from PyQt5.QtWidgets import QLabel, QPushButton, QMessageBox, QVBoxLayout, QWidget
import webbrowser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget
import os


# 简介  
def showHomeContent(self):
    # 清空当前内容
    for i in reversed(range(self.layout.count())):
        self.layout.itemAt(i).widget().deleteLater()

    # 加载自定义字体
    font_path = os.path.join(os.path.dirname(__file__), 'font\\HarmonyOS_Sans_Medium.ttf')  # 相对路径
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    # 检查字体是否加载成功
    if font_id != -1:
        self.custom_font = QFont(QFontDatabase.applicationFontFamilies(font_id)[0])
    else:
        self.custom_font = QFont("黑体")  # 默认字体

    # 设置字体
    font = QFont()
    font.setFamily(self.custom_font.family())  # 使用字体名称
    font.setPointSize(self.fontPointSize)
    self.setFont(font)

    # 获取屏幕尺寸
    screen = QDesktopWidget().availableGeometry()
    screenWidth = screen.width()
    screenHeight = screen.height()

    # 计算字体大小
    font_scale_factor = 0.014
    self.fontPointSize = int(min(screenWidth, screenHeight) * font_scale_factor)
    self.custom_font.setPointSize(self.fontPointSize)

    # 创建一个QWidget作为容器
    container = QWidget()
    container.setStyleSheet("""
        background-color: #f0f0f0;
        padding: 20px;
    """)

    # 创建一个垂直布局
    v_layout = QVBoxLayout(container)

    # 设置布局的对齐标志，使所有控件在布局中垂直居中
    v_layout.setAlignment(Qt.AlignCenter)

    # 设置布局的间距
    v_layout.setSpacing(15)

    # 创建主页简介的标签
    home_synopsis_one = QLabel('基于 Python 编写，使用 PyQt5 框架开发，支持 Windows 10 X64 及以上的版本')
    home_synopsis_one.setStyleSheet(f"""
        font-family: "{self.custom_font.family()}";
        font-size: {self.fontPointSize + 4}px;  
        color: #2c3e50;  
        padding: 15px;  
        border: 1px solid #cccccc;  
        border-radius: 10px;  
        background-color: #ffffff;  
        margin: 10px 0;  
        text-align: center;
    """)

    home_synopsis_four = QLabel('--本软件 SectionIstool 暂不开源、免费，旨在帮助你快速下载各种资源')
    home_synopsis_four.setStyleSheet(f"""
        font-family: "{self.custom_font.family()}";
        font-size: {self.fontPointSize + 4}px;  
        color: #34495e;  
        padding: 12px;  
        border: 1px solid #cccccc;  
        border-radius: 8px;  
        background-color: #ffffff;  
        margin: 8px 0;  
        text-align: center;
    """)

    home_synopsis_three = QLabel('--本项目由 GitHub - lzy98276 开发、维护，欢迎提交 issue')
    home_synopsis_three.setStyleSheet(f"""
        font-family: "{self.custom_font.family()}";
        font-size: {self.fontPointSize + 4}px;  
        color: #34495e;  
        padding: 12px;  
        border: 1px solid #cccccc;  
        border-radius: 8px;  
        background-color: #ffffff;  
        margin: 8px 0;  
        text-align: center;
    """)

    home_synopsis_two = QLabel('本项目 GitHub 开源地址：<a href="https://github.com/lzy98276/SectionIstool" style="color: #0078d7; text-decoration: none;">https://github.com/lzy98276/SectionIstool</a>')
    home_synopsis_two.setOpenExternalLinks(True)  # 使链接可点击
    
    # 设置交互标志
    home_synopsis_two.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 使 QLabel 支持文本浏览器行为

    # 设置样式
    home_synopsis_two.setStyleSheet(f"""
        font-family: "{self.custom_font.family()}";  /* 设置字体 */
        font-size: {self.fontPointSize + 4}px;
        color: #34495e;  
        padding: 12px;  
        border: 1px solid #cccccc;  
        border-radius: 8px;  
        background-color: #ffffff;  
        margin: 8px 0;  
        text-align: center;
    """)



    # 将标签添加到布局中
    v_layout.addWidget(home_synopsis_one)
    v_layout.addWidget(home_synopsis_four)
    v_layout.addWidget(home_synopsis_three)
    v_layout.addWidget(home_synopsis_two)

    # 创建加入群聊按钮
    join_group_button = QPushButton("加入群聊")
    join_group_button.setStyleSheet(f"""
        QPushButton {{
            font-family: "{self.custom_font.family()}";
            font-size: {self.fontPointSize + 2}px;
            color: #ffffff;
            background-color: #0078d7;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            margin-top: 10px;
        }}
        QPushButton:hover {{
            background-color: #005a9e;
        }}
        QPushButton:pressed {{
            background-color: #004c8c;
        }}
    """)

    # 将按钮添加到布局中，并设置对齐方式
    v_layout.addWidget(join_group_button, alignment=Qt.AlignRight | Qt.AlignBottom)

    # 定义按钮点击事件处理函数
    def join_group_clicked():
        message_box = QMessageBox(self)
        message_box.setWindowTitle('选择加群方式')
        message_box.setText("请选择对你方便的加群方式!")
        message_box.setIcon(QMessageBox.Question)

        # 自定义按钮样式
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        message_box.setDefaultButton(QMessageBox.Yes)

        yes_button = message_box.button(QMessageBox.Yes)
        yes_button.setText("电脑加群")
        yes_button.setStyleSheet(f"""
            font-family: "{self.custom_font.family()}";
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: {self.fontPointSize + 2}px;
        """)
        
        no_button = message_box.button(QMessageBox.No)
        no_button.setText("手机加群")
        no_button.setStyleSheet(f"""
            font-family: "{self.custom_font.family()}";
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: {self.fontPointSize + 2}px;
        """)

        cancel_button = message_box.button(QMessageBox.Cancel)
        cancel_button.setText("取消")
        cancel_button.setStyleSheet(f"""
            font-family: "{self.custom_font.family()}";
            background-color: #9E9E9E;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-size: {self.fontPointSize + 2}px;
        """)

        reply = message_box.exec_()
        if reply == QMessageBox.Yes:
            webbrowser.open("https://qm.qq.com/cgi-bin/qm/qr?k=ekF02XA54jmpR0fn_Sc_XN57_dMY4UFh&jump_from=webapi&authKey=KG2qORLnwEQDG6aQWD8bC3C3EOoPcPg1w/CRN3/4cFo2TWMUDwzi3tLYOHHTnHrW")
        elif reply == QMessageBox.No:
            webbrowser.open("https://s3.bmp.ovh/imgs/2024/08/28/2a6668f0837c9f3b.png")

    # 连接按钮点击事件
    join_group_button.clicked.connect(join_group_clicked)

    # 设置容器的布局
    container.setLayout(v_layout)

    # 将容器添加到主窗口的布局中
    self.layout.addWidget(container)
    self.layout.setStretchFactor(container, 1)  # 确保容器在主窗口中垂直居中

    # 设置窗口标题和状态栏消息
    self.setWindowTitle('SectionIstool-关于')

    # 返回container，以便可以在initUI中使用
    return container
