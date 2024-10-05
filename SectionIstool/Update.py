from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
import json
import os
from PyQt5.QtCore import Qt
import requests
from datetime import datetime
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QFrame

# 导入版本信息
from config import version_info
# 在 createMenus 函数中
current_version = version_info()

def check_update(self):
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
    self.setFont(self.custom_font)

    # 获取屏幕尺寸
    screen = QDesktopWidget().availableGeometry()
    screenWidth = screen.width()
    screenHeight = screen.height()

    # 定义缩放因子
    font_scale_factor = 0.014

    # 计算字体大小
    self.fontPointSize = int(min(screenWidth, screenHeight) * font_scale_factor)
    self.custom_font.setPointSize(self.fontPointSize)

    # 更新状态标签
    self.update_status_label = QLabel()
    self.update_status_label.setFixedHeight(int(screenHeight * 0.05))
    self.update_status_label.setStyleSheet(f"font-size: {self.fontPointSize + 6}px; font-family: '{self.custom_font.family()}'; color: #000000;")  # 设置颜色
    self.update_status_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 水平居中, 顶部

    # 获取上次检查更新时间标签
    self.last_checked_label = QLabel("上次检查更新时间：")
    self.last_checked_label.setFixedHeight(int(screenHeight * 0.05))
    self.last_checked_label.setStyleSheet(f"font-size: {self.fontPointSize}px; font-family: '{self.custom_font.family()}'; color: #000000;")  # 设置颜色
    self.last_checked_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 水平居中, 顶部

    # 更新日志框
    self.update_log_frame = QFrame()  # 创建一个框
    self.update_log_frame.setStyleSheet("background-color: #F0F0F0; border: 1px solid #CCCCCC; border-radius: 5px;")  # 设置框的样式

    # 更新日志标签
    self.update_log_label = QLabel()
    self.update_log_label.setStyleSheet(f"font-size: {self.fontPointSize + 2}px; font-family: '{self.custom_font.family()}'; color: #000000;")  # 设置颜色
    self.update_log_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 左对齐, 顶部
    self.update_log_label.setWordWrap(True)  # 自动换行

    # 设置更新日志框的布局
    update_log_layout = QVBoxLayout()
    update_log_layout.addWidget(self.update_log_label)  # 将更新日志标签添加到布局中
    self.update_log_frame.setLayout(update_log_layout)  # 将布局设置到框中

    # 设置更新日志框的尺寸
    self.update_log_frame.setFixedWidth(int(screenWidth * 0.5))
    self.update_log_frame.setFixedHeight(int(screenHeight * 0.4))

    # 按钮
    check_update_button = QPushButton("检查更新")
    check_update_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #2196F3;  /* 按钮背景 */
            color: white;                /* 白色文字 */
            border: none;                /* 去掉边框 */
            border-radius: 10px;        /* 圆角 */
            padding: 12px;              /* 内边距 */
            font-family: '{self.custom_font.family()}'; /* 字体 */
            font-size: {self.fontPointSize + 2}px;     /* 字体大小 */
            font-weight: bold;          /* 加粗 */
        }}
        QPushButton:hover {{
            background-color: #1976D2;  /* 鼠标悬停时的背景色 */
        }}
        QPushButton:pressed {{
            background-color: #2196F3;  /* 按钮被按下时的背景色 */
        }}
    """)
    # 宽度自适应
    check_update_button.setFixedWidth(int(screenWidth * 0.2))
    # 高度自适应
    check_update_button.setFixedHeight(int(screenHeight * 0.04))
    # 点击事件
    check_update_button.clicked.connect(lambda: check_for_updates(self))

    # 主布局
    main_layout = QVBoxLayout()
    main_layout.setSpacing(5)
    main_layout.addWidget(self.update_status_label)
    main_layout.addWidget(self.last_checked_label)
    main_layout.addWidget(check_update_button)
    main_layout.addWidget(self.update_log_frame)

    # 设置主布局到您的窗口或容器
    self.setLayout(main_layout)


    # 创建一个容器
    container = QWidget()
    container.setLayout(main_layout)  

    # 主布局设置
    main_layout.setAlignment(Qt.AlignLeft  | Qt.AlignTop)  # 左上角对齐
    main_layout.setContentsMargins(0, 0, 0, 0)  # 设置边距为0，确保居中效果明显

    # 将容器添加到窗口的布局中
    self.layout.addWidget(container)
    self.layout.setStretchFactor(container, 1)
    self.setWindowTitle('SectionIstool - 更新')

    # 显示初始信息
    update_information(self) 

    # 返回容器，以便可以在其他方法中使用
    return container


def update_information(self):
    update_status = get_update_status(self)

    # 检查 Update Status Label
    if self.update_status_label is not None:  # 确保该标签仍然存在
        self.update_status_label.setText(f"{update_status}")
    else:
        print("更新状态标签不可用")

    last_checked_time = get_last_checked_time(self)

    # 检查 Last Checked Label
    if self.last_checked_label is not None:  # 确保该标签仍然存在
        if last_checked_time:
            self.last_checked_label.setText(f"上次检查更新时间：{last_checked_time}")
        else:
            self.last_checked_label.setText("当前未检查更新")
    else:
        print("上次检查更新时间标签不可用")




# 更新时间
def update_last(self):
    last_checked_time = get_shanghai_time(self)  # 获取时间
    save_last_checked_time(self, last_checked_time)  # 保存更新时间

# 保存更新时间到Config\Config.json
def save_last_checked_time(self, last_checked_time):
    config_path = 'Config/Config.json'
    
    # 检查文件是否存在
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            # 读取现有内容
            data = json.load(file)
    else:
        # 如果文件不存在，初始化为空字典
        data = {}
    
    # 更新检查时间
    data['last_checked_time'] = last_checked_time
    
    # 写入更新后的内容
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 保存更新状态到Config\Config.json
def save_update_status(self, update_status):
    config_path = 'Config/Config.json'
    
    # 检查文件是否存在
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            # 读取现有内容
            data = json.load(file)
    else:
        # 如果文件不存在，初始化为空字典
        data = {}

    # 更新状态
    data['update_status'] = update_status

    # 写入更新后的内容
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 获取上海时间（优先从API）
def get_shanghai_time(self):
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/Asia/Shanghai')
        response.raise_for_status()  # 会抛出异常，如果请求失败
        time_info = response.json()
        # 优化时间格式为 年/月/日 时:分:秒
        return datetime.fromisoformat(time_info['datetime']).strftime("%Y年%m月%d日 %H:%M:%S")
    except Exception:
        # 如果请求失败，则获取本地时间并格式化
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# 获取上次更新时间
def get_last_checked_time(self):
    config_path = 'Config/Config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('last_checked_time')
    else:
        return None

# 更新状态标签的文本，并保存到配置文件
def update_status_label_text(self, text):
    save_update_status(self, text)  # 将状态写入配置文件

# 获取更新状态
def get_update_status(self):
    config_path = 'Config/Config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('update_status')
    else:
        return None

def check_for_updates(self):
    update_status_label_text(self, "检查更新中...")  # 更新状态为检查中
    update_information(self)  # 递归调用，以便实时更新
    # 更新时间
    update_last(self)
    # 获取SectionIstool_info
    SectionIstool_info = self.SectionIstool_info[0]
    try:
        latest_version = SectionIstool_info['version']

        # 版本比较
        if latest_version != current_version:
            # 发现新版本
            self.update_log_label.setText(SectionIstool_info['note'])  # 显示更新日志
            update_status_label_text(self, f"发现新版本 {latest_version}")  # 更新状态
            update_information(self)  # 递归调用，以便实时更新
            
            # 创建确认更新的对话框并设置样式
            reply = QMessageBox(self)
            reply.setWindowTitle('更新可用')
            reply.setText(f"发现新版本 {latest_version}，您要更新吗？")
            reply.setStyleSheet(f"""
                QMessageBox {{
                    background-color: #ffffff; /* 背景色 */
                    border: 1px solid #dcdcdc; /* 边框 */
                    border-radius: 8px; /* 圆角 */
                }}
                QLabel {{
                    font-size: {self.fontPointSize + 3}px; /* 字体大小 */
                    font-family: {self.custom_font.family()}; /* 字体 */
                    color: #333333; /* 字体颜色 */
                    padding: 10px; /* 内部填充 */
                }}
            """)
            
            reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            reply.setDefaultButton(QMessageBox.Yes)  # 默认选项为“是”

            # 设置按钮的样式
            yes_button = reply.button(QMessageBox.Yes)
            yes_button.setText('更新')
            yes_button.setStyleSheet(f"""
                font-size: {self.fontPointSize + 2}px; /* 字体大小 */
                font-family: {self.custom_font.family()}; /* 字体 */
                background-color: #2196F3; /* 蓝色背景 */
                color: white; /* 字体颜色 */
                border-radius: 5px; /* 圆角 */
                padding: 10px; /* 内边距 */
            """)

            no_button = reply.button(QMessageBox.No)
            no_button.setText('暂不更新')
            no_button.setStyleSheet(f"""
                font-size: {self.fontPointSize + 2}px; /* 字体大小 */
                font-family: {self.custom_font.family()}; /* 字体 */
                background-color: #f44336; /* 红色背景 */
                color: white; /* 字体颜色 */
                border-radius: 5px; /* 圆角 */
                padding: 10px; /* 内边距 */
            """)

            reply.exec_()  # 显示对话框

            if reply.clickedButton() == yes_button:
                perform_update(self, SectionIstool_info)
            elif reply.clickedButton() == no_button:
                update_status_label_text(self, "已取消更新")  # 更新状态并记录
                update_information(self)  # 递归调用，以便实时更新
        else:
            self.update_log_label.setText("")  # 不显示更新日志
            update_status_label_text(self, "当前已是最新版本")  # 更新状态并记录
            update_information(self)  # 递归调用，以便实时更新
            QMessageBox.information(self, "无更新", "当前已是最新版本")

    except Exception as e:
        update_status_label_text(self, "检查更新失败")  # 更新状态并记录
        update_information(self)  # 递归调用，以便实时更新
        QMessageBox.critical(self, "错误", f"检查更新时出错：{e}")



def perform_update(self, SectionIstool_info):
    # 统一下载逻辑
    try:
        download_path = os.path.join('Downloads')
        name = SectionIstool_info['name'] + '.' + SectionIstool_info['format']
        from All_Download import DownloadManager
        self.download_manager = DownloadManager()
        self.download_manager.startDownload(
            SectionIstool_info['url'], 
            download_path,  # 假设的下载路径
            name, 
            identifier="Software_Download"
        )

    except ImportError as e:
        QMessageBox.critical(self, "错误", f"下载功能模块未能导入，请向作者反映问题 {str(e)}")
    except AttributeError as e:
        QMessageBox.critical(self, "错误", f"下载功能模块未能正确调用，请向作者反映问题 {str(e)}")
    except Exception as e:
        QMessageBox.critical(self, "错误", f"下载失败，请向作者反映问题 {str(e)}")