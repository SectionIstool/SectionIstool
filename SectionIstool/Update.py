from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import json
import os
from PyQt5.QtCore import Qt
import requests
from datetime import datetime
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QFrame

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


    # 软件信息
    self.SectionIstool_info = {
        "name": "SectionIstool",
        "version": "1.1.1.1",
        "url": "https://mirror.ghproxy.com/https://github.com/SectionIstool/SectionIstool/releases/download/1.1.1.1/Toolbox_Setup_v1.1.1.1.exe",
        "format": "exe",
        "body": "1. 修复了一些已知问题。\n2. 优化了界面。\n3. 新增了一些功能。"
    }
    
    # 当前版本信息
    self.current_version = "1.1.1.0"  # 示例版本号

    # 更新状态标签的框
    self.update_status_frame = QFrame()
    self.update_status_frame.setStyleSheet("""
        QFrame {
            background-color: #E3F2FD; /* 淡蓝色背景 */
            border: 1px solid #9FC8E9; /* 边框颜色 */
            border-radius: 5px; /* 圆角 */
        }
    """)

    # 更新状态标签
    self.update_status_label = QLabel("当前更新状态：")
    self.update_status_label.setFont(QFont(f'{self.custom_font.family()}', self.fontPointSize + 6))
    self.update_status_label.setStyleSheet("color: #2196F3;")  # 设置颜色
    self.update_status_label.setAlignment(Qt.AlignLeft)  # 左对齐
    self.update_status_label.setContentsMargins(10, 10, 10, 10)  # 设置内边距

    # 将更新状态标签添加到框中
    update_status_layout = QVBoxLayout()
    update_status_layout.addWidget(self.update_status_label)
    self.update_status_frame.setLayout(update_status_layout)

    # 上次检查更新时间的框
    self.last_checked_frame = QFrame()
    self.last_checked_frame.setStyleSheet("""
        QFrame {
            background-color: #E3F2FD; /* 淡蓝色背景 */
            border: 1px solid #9FC8E9; /* 边框颜色 */
            border-radius: 5px; /* 圆角 */
        }
    """)

    # 获取上次检查更新时间标签
    self.last_checked_label = QLabel("上次检查更新时间：")
    self.last_checked_label.setFont(QFont(f'{self.custom_font.family()}', self.fontPointSize + 4))
    self.last_checked_label.setStyleSheet("color: #2196F3;")  # 设置颜色
    self.last_checked_label.setAlignment(Qt.AlignLeft)  # 左对齐
    self.last_checked_label.setContentsMargins(10, 10, 10, 10)  # 设置内边距

    # 将上次检查更新时间标签添加到框中
    last_checked_layout = QVBoxLayout()
    last_checked_layout.addWidget(self.last_checked_label)
    self.last_checked_frame.setLayout(last_checked_layout)

    # 更新日志标签
    self.update_log_label = QLabel()
    self.update_log_label.setFont(QFont(f'{self.custom_font.family()}', self.fontPointSize + 2))
    self.update_log_label.setStyleSheet("color: #333333;")  # 设置颜色
    self.update_log_label.setAlignment(Qt.AlignLeft)  # 左对齐
    self.update_log_label.setContentsMargins(10, 10, 10, 10)  # 设置内边距



    # 按钮
    check_update_button = QPushButton("检查更新")
    check_update_button.setFont(QFont(f'{self.custom_font.family()}', self.fontPointSize + 2))
    check_update_button.setStyleSheet("background-color: #2196F3; color: white;")
    check_update_button.clicked.connect(lambda: check_for_updates(self))

    # 选项卡
    self.tabs = QTabWidget()
    # 设置大小
    self.tabs.adjustSize()
    self.tabs.setStyleSheet(f"""
        QTabWidget {{
            background-color: #ffffff; /* 设置选项卡容器背景色为白色 */
            border: 1px solid #dcdcdc; /* 选项卡边框 */
            border-radius: 8px; /* 圆角 */
        }}
        QTabBar::tab {{
            font-family: {self.custom_font.family()};
            font-size: {self.fontPointSize + 2}px; /* 字体大小 */
            background: #f0f8ff; /* 选项卡背景颜色 */
            color: #333333; /* 文字颜色 */
            padding: 12px; /* 内部填充 */
            border: 1px solid #dcdcdc; /* 边框 */
            border-bottom: none; /* 底部边框去掉 */
            border-radius: 8px 8px 0 0; /* 上圆角效果 */
        }}
        QTabBar::tab:selected {{
            background: #f0f8ff; /* 选中时的背景颜色 */
            font-weight: bold; /* 加粗文字 */
        }}
        QTabBar::tab:hover {{
            background: #f0f8ff; /* 鼠标悬停背景颜色 */
        }}
    """)


    update_log_widget = QWidget()  # 创建新的 QWidget 作为选项卡内容
    update_log_layout = QVBoxLayout()  # 创建新的布局

    # 为更新日志标签设置美化样式
    self.update_log_label.setAlignment(Qt.AlignLeft)  # 设置对齐方式为左对齐
    self.update_log_label.setStyleSheet(f"""
        font-size: {self.fontPointSize + 2}px;
        font-family: {self.custom_font.family()};
        color: #333333; 
        padding: 10px; /* 内部填充 */
    """)  # 设置文本颜色和内部填充


    # 创建标题标签并设置样式
    title_label = QLabel(f"SectionIstool - {self.SectionIstool_info['version']} 更新内容")
    title_label.setFont(self.custom_font)  # 使用自定义字体
    title_label.setStyleSheet("""
        font-size: 16px; /* 字体大小 */
        font-weight: bold; /* 加粗 */
        color: #000000; /* 字体颜色 */
        padding: 10px; /* 内部填充 */
    """)

    # 将标题标签和更新日志标签添加到布局中
    update_log_layout.addWidget(title_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # 添加标题标签到更新日志布局的顶部

    update_log_layout.addWidget(self.update_log_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # 将更新日志标签添加到布局中并设置对齐方式
    update_log_widget.setLayout(update_log_layout)  # 将布局设置给新的 QWidget
    self.tabs.addTab(update_log_widget, "更新日志")  # 将这个 QWidget 添加到选项卡中

    # 主布局
    main_layout = QVBoxLayout()
    main_layout.addWidget(self.update_status_frame)
    main_layout.addWidget(self.last_checked_frame)
    main_layout.addWidget(check_update_button)
    main_layout.addWidget(self.tabs)

    # 创建一个容器
    container = QWidget()
    container.setLayout(main_layout)  # 设置容器的主布局

    # 将容器添加到主窗口的布局中
    self.layout.addWidget(container)
    self.layout.setStretchFactor(container, 1)
    self.setWindowTitle('SectionIstool - 更新')

    # 显示初始信息
    update_information(self) 

    # 初始化定时器
    self.timer = QTimer(self)
    self.timer.timeout.connect(lambda: update_information(self))
    self.timer.start(800) 

    # 返回容器，以便可以在其他方法中使用
    return container

def update_information(self):
    # 更新状态标签
    update_status = get_update_status(self)
    if update_status:
        self.update_status_label.setText(f"当前更新状态：{update_status}")
    else:
        self.update_status_label.setText("当前未检查更新")

    # 更新时间标签
    last_checked_time = get_last_checked_time(self)
    if last_checked_time:
        self.last_checked_label.setText(f"上次检查更新时间：{last_checked_time}")
    else:
        self.last_checked_label.setText("当前未检查更新")


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
        return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

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
    # 更新时间
    update_last(self)
    # 获取SectionIstool_info
    SectionIstool_info = self.SectionIstool_info
    try:
        latest_version = SectionIstool_info['version']

        # 版本比较
        if latest_version != self.current_version:
            # 发现新版本
            self.update_log_label.setText(SectionIstool_info['body'])  # 显示更新日志
            update_status_label_text(self, f"发现新版本 {latest_version}")  # 更新状态
            
            # 创建确认更新的对话框并设置样式
            reply = QMessageBox(self)
            reply.setWindowTitle('更新可用')
            reply.setText(f"发现新版本 {latest_version}，您要更新吗？")
            reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            reply.setDefaultButton(QMessageBox.Yes)  # 默认选项为“是”

            # 设置按钮的样式
            yes_button = reply.button(QMessageBox.Yes)
            yes_button.setText('更新')
            yes_button.setStyleSheet(f"""
                font-size: {self.fontPointSize + 2}px; /* 字体大小 */
                font-family: {self.custom_font.family()}; /* 字体 */
                background-color: #4CAF50; /* 绿色背景 */
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
        
        else:
            self.update_log_label.setText("")  # 不显示更新日志
            update_status_label_text(self, "当前已是最新版本")  # 更新状态并记录
            QMessageBox.information(self, "无更新", "当前已是最新版本")

    except Exception as e:
        update_status_label_text(self, "检查更新失败")  # 更新状态并记录
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