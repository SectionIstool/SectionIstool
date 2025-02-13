import os
import json
import socket
from concurrent.futures import ThreadPoolExecutor
from qfluentwidgets import * # type: ignore
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import urllib.request
import requests
import aiohttp
import asyncio
from loguru import logger

from app.view.readme_current import show_readme_dialog # type: ignore

socket.setdefaulttimeout(None)

software_name_download_first = 'Ris-Soft'
software_name_download_second = 'Ris_ClassTool'
software_icon = './app/resource/icon/Ris_ClassTool_software.png'
software_info = '简介\n让每堂课都充满活力,让每个学生都能享受到科技带来的教育革新。'
software_author = 'Ris-Soft'
software_github = f'https://github.com/{software_name_download_first}/{software_name_download_second}'
software_bilibili = 'https://space.bilibili.com/1481617182'

# 配置日志记录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger.add(
    os.path.join(log_dir, "SectionIstool_{time:YYYY-MM-DD}.log"),
    rotation="1 MB",
    encoding="utf-8",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | {name}:{function}:{line} - {message}"
)
# 读取配置文件
def read_json(json_path): # type: ignore
    # 确认是否存在设置目录
    if './app/Settings' != None and not os.path.exists('./app/Settings'): # type: ignore
        os.makedirs('./app/Settings')
    if os.path.exists(json_path): # type: ignore
        try:
            with open(json_path, 'r', encoding='utf-8') as file: # type: ignore
                return json.load(file)
        except json.JSONDecodeError:
            # 如果文件内容不是有效的 JSON 格式，返回空字典
            return {} # type: ignore
    return {} # type: ignore

# 读取以及写入配置文件
def write_json(json_path, field_name, default_value):  # type: ignore
    # 确认是否存在设置目录
    if './app/Settings' != None and not os.path.exists('./app/Settings'): # type: ignore
        os.makedirs('./app/Settings')
    try:
        with open(json_path, 'r', encoding='utf-8') as file:  # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        json_file = {}
    json_file[field_name] = default_value
    json_file.update(json_file)  # type: ignore
    with open(json_path, 'w', encoding='utf-8') as file:  # type: ignore
        json.dump(json_file, file, ensure_ascii=False, indent=4)

# 修改或新增指定软件配置中的某个值
def modify_setting(json_path, software_name, key, new_value):  # type: ignore
    # 确认是否存在设置目录
    if not os.path.exists('./app/Settings'):
        os.makedirs('./app/Settings')
    try:
        with open(json_path, 'r', encoding='utf-8') as file:  # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        json_file = {}
    
    # 检查指定软件的配置是否存在
    if software_name not in json_file:
        json_file[software_name] = {}
    elif not isinstance(json_file[software_name], dict):
        # 如果不是字典，将其转换为字典
        json_file[software_name] = {}
    
    # 修改或新增指定键的值
    json_file[software_name][key] = new_value
    
    # 将更新后的数据写回文件
    with open(json_path, 'w', encoding='utf-8') as file: # type: ignore
        json.dump(json_file, file, ensure_ascii=False, indent=4)

# 读取指定软件配置的某个值
def read_setting(json_path, software_name, key): # type: ignore
    try:
        with open(json_path, 'r', encoding='utf-8') as file: # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 'Unknown'
    
    # 检查指定软件的配置是否存在
    if software_name in json_file and key in json_file[software_name]:
        return json_file[software_name][key]
    
    return 'Unknown'

# 写入配置文件
modify_setting('./app/Settings/Settings.json', software_name_download_second, 'source', 'github')
modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download', '[软件根目录/Downloads]')
modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_manner', '异步下载(aiohttp)')

# 读取配置文件中的版本号
read_json_version = read_json(f'./app/resource/releases/{software_name_download_second}_releases.json') # type: ignore
# 提取 tag_name 字段的值
if isinstance(read_json_version, list) and len(read_json_version) > 0:  # type: ignore
    modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version', f'{read_json_version[0]["tag_name"]}')
else:
    modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version', 'Unknown')

class Ris_ClassTool_Widget(QFrame):
    def __init__(self, parent: QFrame = None): # type: ignore
        super().__init__(parent=parent)

        # 创建一个 QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # 设置 QScrollArea 的样式
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
        """)
        # 创建一个内部的 QFrame 用于放置内容
        inner_frame = QFrame(scroll_area)
        inner_layout = QVBoxLayout(inner_frame)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建软件图标标签
        icon_label = QLabel(inner_frame)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_pixmap = QPixmap(f"{software_icon}")  # 确保路径正确
        icon_label.setPixmap(icon_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        # 创建软件作者文本
        author_label = SubtitleLabel(f"作者\n{software_author}", inner_frame)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author_label.setWordWrap(True)

        # 创建软件介绍文本
        description_label = SubtitleLabel(f"{software_info}", inner_frame)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)

        # 创建打开Github项目主页按钮
        GitHub_project_button = PushButton("Github 项目主页", inner_frame)
        GitHub_project_button.setObjectName("downloadButton")
        # 设置按钮的提示信息
        GitHub_project_button.setToolTip(f'点击即可打开 Github 上的 {software_name_download_second} 项目主页 ✨')
        GitHub_project_button.setToolTipDuration(2000)
        GitHub_project_button.installEventFilter(ToolTipFilter(GitHub_project_button, showDelay=300, position=ToolTipPosition.TOP))
        # 定义项目主页的 URL
        project_url = QUrl(f"{software_github}")
        # 连接按钮的 clicked 信号到打开 URL 的槽函数
        GitHub_project_button.clicked.connect(lambda: QDesktopServices.openUrl(project_url)) # type: ignore
        GitHub_project_button.setMinimumWidth(350) 

        # 创建作者B站主页按钮
        author_Bilibili_button = PushButton("Bilibili 主页", inner_frame)
        author_Bilibili_button.setObjectName("authorBilibilibutton")
        # 设置按钮的提示信息
        author_Bilibili_button.setToolTip('点击即可打开作者的 Bilibili 主页 ✨')
        author_Bilibili_button.setToolTipDuration(1500)
        author_Bilibili_button.installEventFilter(ToolTipFilter(author_Bilibili_button, showDelay=300, position=ToolTipPosition.TOP))
        # 定义作者 Bilibili 主页的 URL
        author_Bilibili_url = QUrl(f"{software_bilibili}") 
        # 连接按钮的 clicked 信号到打开 URL 的槽函数
        author_Bilibili_button.clicked.connect(lambda: QDesktopServices.openUrl(author_Bilibili_url)) # type: ignore
        author_Bilibili_button.setMinimumWidth(350)

        # 添加垂直间距
        vertical_spacer_20 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        # 创建下载源选择下拉框
        source_combo_box = ComboBox(inner_frame)
        source_combo_box.setPlaceholderText("选择一个下载源")
        items_source_combo_box = ['github', 'github(ghproxy)-已被墙', 'github(ghp)-已被墙', 'github(ghgo)-已被墙', 'github(ghfast)']
        source_combo_box.addItems(items_source_combo_box)
        source_combo_box.currentIndexChanged.connect(lambda index: modify_setting('./app/Settings/Settings.json', software_name_download_second, 'source', f'{source_combo_box.currentText()}')) # type: ignore
        source_combo_box.setMaximumWidth(350) 
        # 设置下拉框的提示信息
        source_combo_box.setToolTip('选择一个下载源 ✨')
        source_combo_box.setToolTipDuration(1500)
        source_combo_box.installEventFilter(ToolTipFilter(source_combo_box, showDelay=300, position=ToolTipPosition.TOP))

        def version_combo_box_update(version_data): # type: ignore
            # 清空现有的选项
            version_combo_box.clear()
            if isinstance(version_data, list) and len(version_data) > 0: # type: ignore
                version_names = [item.get('tag_name', 'Unknown') for item in version_data] # type: ignore
                version_combo_box.addItems(version_names) # type: ignore
            else:
                version_combo_box.addItem('Unknown') # type: ignore

        # 创建版本选择下拉框
        version_combo_box = ComboBox(inner_frame)
        version_combo_box.setPlaceholderText("选择一个版本")
        version_data = read_json(f'./app/resource/releases/{software_name_download_second}_releases.json') # type: ignore
        version_combo_box_update(version_data) # type: ignore
        version_combo_box.currentIndexChanged.connect(lambda index: modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version', f'{version_combo_box.currentText()}')) # type: ignore
        version_combo_box.currentIndexChanged.connect(lambda index: version_name_combo_box_update((read_json(f'./app/resource/releases/{software_name_download_second}_releases.json')))) # type: ignore
        version_combo_box.setMaximumWidth(350) 
        # 设置下拉框的提示信息
        version_combo_box.setToolTip('选择一个你需要下载的版本 ✨')
        version_combo_box.setToolTipDuration(1500)
        version_combo_box.installEventFilter(ToolTipFilter(version_combo_box, showDelay=300, position=ToolTipPosition.TOP))

        def version_name_combo_box_update(version_name_data): # type: ignore
            # 清空现有的选项
            version_name_combo_box.clear()
            if isinstance(version_name_data, list) and len(version_name_data) > 0: # type: ignore
                tag_name_current = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version')
                for item in version_name_data: # type: ignore
                    if item.get('tag_name') == (tag_name_current): # type: ignore
                        assets = item.get('assets', []) # type: ignore
                        if assets:  # 检查 assets 列表是否为空
                            version_names = [asset.get('name', 'Unknown') for asset in assets] # type: ignore
                            version_name_combo_box.addItems(version_names) # type: ignore
                            modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version_name', f'{version_names}') # type: ignore
                            logger.info(f'当前选择的版本为 {tag_name_current}, 自动选择 {version_names} 版本')
                            break
                        else:
                            version_name_combo_box.addItem('Unknown') # type: ignore
                else:
                    version_name_combo_box.addItem('Unknown') # type: ignore
            else:
                version_name_combo_box.addItem('Unknown') # type: ignore


        # 创建软件文件名选择下拉框
        version_name_combo_box = ComboBox(inner_frame)
        version_name_combo_box.setPlaceholderText("选择一个软件版本")
        version_name_combo_box_update((read_json(f'./app/resource/releases/{software_name_download_second}_releases.json'))) # type: ignore
        version_name_combo_box.currentIndexChanged.connect(lambda index: modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version_name', f'{version_name_combo_box.currentText()}')) # type: ignore
        version_name_combo_box.setMaximumWidth(350) 
        # 设置下拉框的提示信息
        version_name_combo_box.setToolTip('选择一个你需要下载的版本 ✨')
        version_name_combo_box.setToolTipDuration(1500)
        version_name_combo_box.installEventFilter(ToolTipFilter(version_name_combo_box, showDelay=300, position=ToolTipPosition.TOP))

        # 创建下载目录选择下拉框
        download_combo_box = ComboBox(inner_frame)
        download_combo_box.setPlaceholderText("选择一个下载目录")
        items_download_combo_box = ['[软件根目录/Downloads]', '[桌面/Downloads]', 'C:/Users/[自动获取]/Downloads', 'D:/Downloads', 'E:/Downloads', 'F:/Downloads', 'G:/Downloads', 'H:/Downloads', 'I:/Downloads', 'J:/Downloads', 'K:/Downloads', 'L:/Downloads', 'M:/Downloads', 'N:/Downloads', 'O:/Downloads', 'P:/Downloads', 'Q:/Downloads', 'R:/Downloads', 'S:/Downloads', 'T:/Downloads', 'U:/Downloads', 'V:/Downloads', 'W:/Downloads', 'X:/Downloads', 'Y:/Downloads', 'Z:/Downloads']
        download_combo_box.addItems(items_download_combo_box)
        download_combo_box.currentIndexChanged.connect(lambda index: modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download', f'{download_combo_box.currentText()}')) # type: ignore
        download_combo_box.setMaximumWidth(350) 
        # 设置下拉框的提示信息
        download_combo_box.setToolTip('选择一个当前软件的下载目录 ✨')
        download_combo_box.setToolTipDuration(2000)
        download_combo_box.installEventFilter(ToolTipFilter(download_combo_box, showDelay=300, position=ToolTipPosition.TOP))

        # 创建下载方式选择下拉框
        download_manner_combo_box = ComboBox(inner_frame)
        download_manner_combo_box.setPlaceholderText("选择一个下载方式")
        items_download_manner_combo_box = ['异步下载(aiohttp)', '多线程(ThreadPoolExecutor)', '单线程(urllib.request)', '单线程(requests)']
        download_manner_combo_box.addItems(items_download_manner_combo_box)
        download_manner_combo_box.currentIndexChanged.connect(lambda index: modify_setting('./app/Settings/Settings.json', software_name_download_second, 'download_manner', f'{download_manner_combo_box.currentText()}')) # type: ignore
        download_manner_combo_box.setMaximumWidth(350) 
        # 设置下拉框的提示信息
        download_manner_combo_box.setToolTip('选择一个下载方式 ✨')
        download_manner_combo_box.setToolTipDuration(1500)
        download_manner_combo_box.installEventFilter(ToolTipFilter(download_manner_combo_box, showDelay=300, position=ToolTipPosition.TOP))

        # 创建下载按钮
        self.readme_button = PushButton("查看当前选择版本的更新日志", inner_frame)
        self.readme_button.setObjectName("downloadButton")
        self.readme_button.setMinimumWidth(150)
        # 设置按钮的提示信息
        self.readme_button.setToolTip(f'点击即可查看当前选择版本的 更新日志 ✨')
        self.readme_button.setToolTipDuration(1500)
        self.readme_button.installEventFilter(ToolTipFilter(self.readme_button, showDelay=300, position=ToolTipPosition.TOP))
        # 连接按钮的 clicked 信号到下载函数
        self.readme_button.clicked.connect(lambda index: show_readme_dialog(self, self.readme_button, software_name_download_second)) # type: ignore

        # 创建下载按钮
        self.download_button = PushButton("下载当前选择版本", inner_frame)
        self.download_button.setObjectName("downloadButton")
        self.download_button.setMinimumWidth(150)
        # 设置按钮的提示信息
        self.download_button.setToolTip(f'点击即可下载最新版的 {software_name_download_second} ✨')
        self.download_button.setToolTipDuration(1500)
        self.download_button.installEventFilter(ToolTipFilter(self.download_button, showDelay=300, position=ToolTipPosition.TOP))
        # 连接按钮的 clicked 信号到下载函数
        self.download_button.clicked.connect(self.showTeachingTip_download_latest_version) # type: ignore
        self.download_button.clicked.connect(lambda index: self.download_latest_version(read_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version_name'))) # type: ignore

        def refresh_latest_version():
            # 读取配置文件中的下载源
            github_api_url = f'https://api.github.com/repos/{software_name_download_first}/{software_name_download_second}/releases'

            # 使用 ThreadPoolExecutor 并行执行操作
            with ThreadPoolExecutor() as executor:
                future = executor.submit(urllib.request.urlopen, github_api_url)  # 使用 urllib.request.urlopen 替代 requests.get
                response = future.result()
                if response.getcode() == 200:  # 使用 getcode() 替代 status_code
                    releases_data = json.load(response)  # 直接从 response 加载 json 数据
                    # 确保 releases 文件夹存在
                    os.makedirs('releases', exist_ok=True)
                    with open(f'./app/resource/releases/{software_name_download_second}_releases.json', 'w', encoding='utf-8') as file:
                        json.dump(releases_data, file, ensure_ascii=False, indent=4)
                    version_combo_box_update((read_json(f'./app/resource/releases/{software_name_download_second}_releases.json'))) # type: ignore
                    logger.info(f"已成功刷新下载源, 可以下载最新版本的 {software_name_download_second} ✨")
                else:
                    logger.error(f"无法获取版本数据: {response.getcode()}")
                    pass

        # 创建刷新按钮
        self.refresh_button = PushButton("刷新软件版本", inner_frame)
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.setMinimumWidth(150)
        # 设置按钮的提示信息
        self.refresh_button.setToolTip('点击即可刷新下载源(一天内不要多用,容易刷新不了-用的API) ✨')
        self.refresh_button.setToolTipDuration(2000)
        self.refresh_button.installEventFilter(ToolTipFilter(self.refresh_button, showDelay=300, position=ToolTipPosition.TOP))
        # 连接按钮的 clicked 信号到刷新函数
        self.refresh_button.clicked.connect(self.showTeachingTip_refresh_latest_version) # type: ignore
        self.refresh_button.clicked.connect(refresh_latest_version) # type: ignore

        # 创建打开下载文件夹按钮
        self.open_download_folder_button = PushButton("打开下载文件夹", inner_frame)
        self.open_download_folder_button.setObjectName("openDownloadFolderButton")
        self.open_download_folder_button.setMinimumWidth(150)
        # 设置按钮的提示信息
        self.open_download_folder_button.setToolTip('点击即可打开下载文件夹 ✨')
        self.open_download_folder_button.setToolTipDuration(1500)
        self.open_download_folder_button.installEventFilter(ToolTipFilter(self.open_download_folder_button, showDelay=300, position=ToolTipPosition.TOP))
        # 连接按钮的 clicked 信号到打开下载文件夹函数
        self.open_download_folder_button.clicked.connect(self.open_download_folder) # type: ignore

        # 创建标签以显示图片
        image_label = QLabel(inner_frame)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.load_image_content(image_label) # type: ignore

        # 添加图标到布局
        inner_layout.addWidget(icon_label)
        # 添加垂直间距
        inner_layout.addItem(vertical_spacer_20)
        # 添加作者到布局
        inner_layout.addWidget(author_label)
        # 添加介绍到布局
        inner_layout.addWidget(description_label)
        # 添加垂直间距
        inner_layout.addItem(vertical_spacer_20)
        # 添加 Github 项目主页和作者 Bilibili 主页按钮到布局并使其居中
        GitHub_project_and_author_Bilibili_button_layout = QHBoxLayout()
        GitHub_project_and_author_Bilibili_button_layout.addStretch()
        GitHub_project_and_author_Bilibili_button_layout.addWidget(GitHub_project_button)
        GitHub_project_and_author_Bilibili_button_layout.addWidget(author_Bilibili_button)
        GitHub_project_and_author_Bilibili_button_layout.addStretch()
        inner_layout.addLayout(GitHub_project_and_author_Bilibili_button_layout)
        # 添加垂直间距
        inner_layout.addItem(vertical_spacer_20)

        # 添加下拉框到布局并使其居中
        source_combo_box_layout = QHBoxLayout()
        source_combo_box_layout.addStretch()
        source_combo_box_layout.addWidget(source_combo_box)
        source_combo_box_layout.addWidget(version_combo_box)
        source_combo_box_layout.addWidget(version_name_combo_box)
        source_combo_box_layout.addWidget(download_combo_box)
        source_combo_box_layout.addWidget(download_manner_combo_box)
        source_combo_box_layout.addStretch()
        inner_layout.addLayout(source_combo_box_layout)

        # 添加按钮到布局并使其居中
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.readme_button)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.open_download_folder_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()
        inner_layout.addLayout(button_layout)

        # 添加图片到布局
        # 添加垂直间距
        inner_layout.addItem(vertical_spacer_20)
        inner_layout.addWidget(image_label)

        # 将内部的 QFrame 设置为 QScrollArea 的内容
        scroll_area.setWidget(inner_frame)

        # 设置主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

    def load_image_content(self, image_label): # type: ignore
        try:
            image_path = f'./app/resource/README/{software_name_download_second}/README.png'
            image_pixmap = QPixmap(image_path)
            if image_pixmap.isNull():
                raise FileNotFoundError
            image_label.setPixmap(image_pixmap) # type: ignore
            logger.info(f"已成功加载 README.png 文件") # type: ignore
        except FileNotFoundError:
            image_label.setText("README.png 文件未找到") # type: ignore
            logger.error(f"README.png 文件未找到") # type: ignore

    def showTeachingTip_refresh_latest_version(self):
        TeachingTip.create( # type: ignore
            target=self.refresh_button,
            icon=InfoBarIcon.SUCCESS,
            title='刷新成功',
            content=f"已成功刷新下载源, 可以下载最新版本的 {software_name_download_second} ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=5000,
            parent=self
        )
        logger.info(f"已成功刷新下载源, 可以下载最新版本的 {software_name_download_second} ✨")

    def showTeachingTip_download_latest_version(self):
        TeachingTip.create( # type: ignore
            target=self.download_button,
            icon=InfoBarIcon.SUCCESS,
            title='下载启动成功',
            content=f"已成功启动下载最新版本的 {software_name_download_second} ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.info(f"已成功启动下载最新版本的 {software_name_download_second} ✨")

    def showTeachingTip_download_latest_version_stop_version(self):
        TeachingTip.create( # type: ignore
            target=self.download_button,
            icon=InfoBarIcon.ERROR,
            title='下载失败',
            content="下载失败, 无法读取版本号, 详情请查看日志文件 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.error(f"下载失败, 无法读取版本号, 详情请查看日志文件 ✨")

    def showTeachingTip_download_latest_version_stop_download(self):
        TeachingTip.create( # type: ignore
            target=self.download_button,
            icon=InfoBarIcon.ERROR,
            title='下载失败',
            content="下载失败, 详情请查看日志文件 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.error(f"下载失败, 详情请查看日志文件 ✨")

    def showTeachingTip_download_latest_version_info_download_timeout(self):
        TeachingTip.create( # type: ignore
            target=self.download_button,
            icon=InfoBarIcon.ERROR,
            title='下载超时',
            content="下载超时, 详情请查看日志文件 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.error(f"下载超时, 详情请查看日志文件 ✨")
    
    def showTeachingTip_download_latest_version_info_download_manner_not_found(self):
        TeachingTip.create( # type: ignore
            target=self.download_button,
            icon=InfoBarIcon.ERROR,
            title='下载方式未知',
            content="下载方式未知, 回退到 异步下载(aiohttp), 详情请查看日志文件 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.error(f"下载方式未知, 回退到 异步下载(aiohttp), 详情请查看日志文件 ✨")
    
    def showTeachingTip_download_latest_version_open_download_folder_no(self):
        TeachingTip.create( # type: ignore
            target=self.open_download_folder_button,
            icon=InfoBarIcon.ERROR,
            title='打开下载目录失败',
            content="打开下载目录失败, 详情请查看日志文件 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )

    def showTeachingTip_download_latest_version_info_download(self):
        TeachingTip.create( # type: ignore
            target=self.download_button,
            icon=InfoBarIcon.SUCCESS,
            title='下载完成',
            content="下载完成, 请到下载目录查看 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.info(f"下载完成, 请到下载目录查看 ✨")

    def showTeachingTip_download_latest_version_open_download_folder_yes(self):
        TeachingTip.create( # type: ignore
            target=self.open_download_folder_button,
            icon=InfoBarIcon.SUCCESS,
            title='打开下载目录成功',
            content="打开下载目录成功, 请到下载目录查看 ✨",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        logger.info(f"打开下载目录成功, 请到下载目录查看 ✨")   

    async def async_download(self, download_url, download_path, version_name_names): # type: ignore
        try:
            timeout = aiohttp.ClientTimeout(total=60)  # 设置超时时间为 60 秒
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url, timeout=timeout) as response: # type: ignore
                    response.raise_for_status()  # type: ignore
                    with open(os.path.join(download_path, f'{version_name_names}'), 'wb') as file: # type: ignore
                        while True:
                            chunk = await response.content.read(8192)
                            if not chunk:
                                break
                            file.write(chunk)
                    logger.info(f"下载已完成: {download_url}")
                    self.showTeachingTip_download_latest_version_info_download()
        except Exception as e:
            logger.error(f"下载失败: {e}")
            self.showTeachingTip_download_latest_version_stop_download()

    def download_latest_version(self, version_name_names): # type: ignore
        # 读取配置文件中的版本号
        releases_data = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version')
        # 提取 tag_name 字段的值
        if releases_data != 'Unknown':
            release_name = releases_data
        else:
            release_name = 'Unknown'

        if release_name == 'Unknown':
            logger.error(f"无法读取版本号")
            self.showTeachingTip_download_latest_version_stop_version()
            return

        source_combo_box_data = read_setting('./app/Settings/Settings.json', software_name_download_second, 'source')
        # 提取 {software_name_download_second}_source 字段的值
        if source_combo_box_data != 'Unknown':
            source_combo_box_value = source_combo_box_data
            if source_combo_box_value == 'github':
                download_url = f"https://github.com/{software_name_download_first}/{software_name_download_second}/releases/download/{release_name}/{version_name_names}"
            elif source_combo_box_value in ['github(ghproxy)-已被墙', 'github(ghp)-已被墙', 'github(ghgo)-已被墙']:
                logger.warning(f"下载源 {source_combo_box_value} 被阻止, 回退到默认的 github 源")
                download_url = f"https://github.com/{software_name_download_first}/{software_name_download_second}/releases/download/{release_name}/{version_name_names}"
            elif source_combo_box_value == 'github(ghfast)':
                download_url = f"https://ghfast.top/https://github.com/{software_name_download_first}/{software_name_download_second}/releases/download/{release_name}/{version_name_names}"
            else:
                download_url = f"https://github.com/{software_name_download_first}/{software_name_download_second}/releases/download/{release_name}/{version_name_names}"
        else:
            download_url = f"https://github.com/{software_name_download_first}/{software_name_download_second}/releases/download/{release_name}/{version_name_names}"
        


        # 确认是否存在下载目录
        download_combo_box_data = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download')
        # 提取 {software_name_download_second}_download 字段的值
        if download_combo_box_data != 'Unknown':
            download_combo_box_value = download_combo_box_data
            if download_combo_box_value == '[软件根目录/Downloads]':
                download_path = os.path.join('Downloads')
            elif download_combo_box_value == '[桌面/Downloads]':
                download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Downloads')
            elif download_combo_box_value == 'C:/Users/[自动获取]/Downloads':
                download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            else:
                drive_letters = ['D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
                for drive in drive_letters:
                    if download_combo_box_value == f'{drive}/Downloads':
                        download_path = f'{drive}/Downloads'
                        break
                else:
                    download_path = os.path.join('Downloads')
        else:
            download_path = os.path.join('Downloads') 

        try:
            # 确认是否存在下载目录
            if download_path != 'Unknown' and not os.path.exists(download_path): # type: ignore
                os.makedirs(download_path)
        except FileNotFoundError as e:
            logger.error(f"下载路径不存在: {e}")
            self.showTeachingTip_download_latest_version_open_download_folder_no()
        except Exception as e:
            logger.error(f"打开下载路径失败: {e}")
            self.showTeachingTip_download_latest_version_open_download_folder_no()

        # 确认是否存在下载方式
        download_manner_combo_box_data = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download_manner')
        # 提取 {software_name_download_second}_download_manner 字段的值
        if download_manner_combo_box_data != 'Unknown':
            download_manner_combo_box_value = download_manner_combo_box_data
            if download_manner_combo_box_value == '多线程(ThreadPoolExecutor)':
                # 使用 ThreadPoolExecutor 并行执行操作
                # 设置超时时间为60秒
                timeout = 60
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(urllib.request.urlretrieve, download_url, os.path.join(download_path, f'{version_name_names}'))
                    try:
                        future.result(timeout=timeout)
                        logger.info(f"下载已完成: {download_url}")
                        self.showTeachingTip_download_latest_version_info_download()
                    except TimeoutError:
                        logger.error(f"下载超时: {download_url}")
                        self.showTeachingTip_download_latest_version_info_download_timeout()
                    except Exception as e:
                        logger.error(f"下载失败: {e}")
                        self.showTeachingTip_download_latest_version_stop_download()
            elif download_manner_combo_box_value == '单线程(urllib.request)':
                # 使用 urllib.request.urlretrieve 下载文件
                try:
                    # 设置超时时间为60秒
                    timeout = 60
                    socket.setdefaulttimeout(timeout)
                    urllib.request.urlretrieve(download_url, os.path.join(download_path, f'{version_name_names}')) # type: ignore
                    logger.info(f"下载已完成: {download_url}")
                    self.showTeachingTip_download_latest_version_info_download()
                except TimeoutError:
                    logger.error(f"下载超时: {download_url}")
                    self.showTeachingTip_download_latest_version_info_download_timeout()
                except Exception as e:
                    logger.error(f"下载失败: {e}")
                    self.showTeachingTip_download_latest_version_stop_download()
                finally:
                    # 重置超时时间为默认值
                    socket.setdefaulttimeout(None)
            elif download_manner_combo_box_value == '单线程(requests)':
                # 使用 requests.get 下载文件
                try:
                    # 设置超时时间为60秒
                    timeout = 60
                    response = requests.get(download_url, stream=True, timeout=timeout)
                    response.raise_for_status()
                    with open(os.path.join(download_path, f'{version_name_names}'), 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    logger.info(f"下载已完成: {download_url}")
                    self.showTeachingTip_download_latest_version_info_download()
                except TimeoutError:
                    logger.error(f"下载超时: {download_url}")
                    self.showTeachingTip_download_latest_version_info_download_timeout()
                except Exception as e:
                    logger.error(f"下载失败: {e}")
                    self.showTeachingTip_download_latest_version_stop_download()
            elif download_manner_combo_box_value == '异步下载(aiohttp)':
                # 使用 aiohttp 进行异步下载
                asyncio.run(self.async_download(download_url, download_path, version_name_names)) # type: ignore
            else:
                logger.warning(f"未知下载方式：{download_manner_combo_box_value} 回退到 异步下载(aiohttp)")
                self.showTeachingTip_download_latest_version_info_download_manner_not_found()
                # 使用 aiohttp 进行异步下载
                asyncio.run(self.async_download(download_url, download_path, version_name_names)) # type: ignore
        else:
            logger.error("下载方式设置不正确")
            self.showTeachingTip_download_latest_version_stop_download()
            return
        
    def open_download_folder(self):
        # 确认是否存在下载目录
        download_combo_box_data = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download')
        # 提取 {software_name_download_second}_download 字段的值
        if download_combo_box_data != 'Unknown':
            download_combo_box_value = download_combo_box_data
            if download_combo_box_value == '[软件根目录/Downloads]':
                download_path = os.path.join('Downloads')
            elif download_combo_box_value == '[桌面/Downloads]':
                download_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'Downloads')
            elif download_combo_box_value == 'C:/Users/[自动获取]/Downloads':
                download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            else:
                drive_letters = ['D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']
                for drive in drive_letters:
                    if download_combo_box_value == f'{drive}/Downloads':
                        download_path = f'{drive}/Downloads'
                        break
                else:
                    download_path = os.path.join('Downloads')
        else:
            download_path = os.path.join('Downloads') 

        try:
            # 确认是否存在下载目录
            if download_path != 'Unknown' and not os.path.exists(download_path): # type: ignore
                os.makedirs(download_path)
        except FileNotFoundError as e:
            logger.error(f"下载路径不存在: {e}")
            self.showTeachingTip_download_latest_version_open_download_folder_no()
        except Exception as e:
            logger.error(f"打开下载路径失败: {e}")
            self.showTeachingTip_download_latest_version_open_download_folder_no()
        
        try:
            if download_path != 'Unknown': # type: ignore
                os.startfile(download_path) # type: ignore
                logger.info("打开下载路径成功")
                self.showTeachingTip_download_latest_version_open_download_folder_yes()
        except FileNotFoundError as e:
            logger.error(f"下载路径不存在: {e}")
            self.showTeachingTip_download_latest_version_open_download_folder_no()
        except Exception as e:
            logger.error(f"打开下载路径失败: {e}")
            self.showTeachingTip_download_latest_version_open_download_folder_no()