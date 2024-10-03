<<<<<<< HEAD
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QFrame
import os 
import webbrowser
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pathlib import Path
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFontDatabase



# 软件下载
def showSoftwareClassIslandDownloadContent(self):
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

    # 创建一个QWidget作为容器
    container = QWidget()

    # 设置容器的样式，添加圆角边框
    container.setStyleSheet(
        "QWidget {"
        "   border: 1px solid #dcdcdc;"  # 设置容器的边框颜色
        "   border-radius: 10px;"        # 设置圆角半径
        "   background-color: #ffffff;"   # 设置容器的背景色
        "   padding: 5px;"                # 设置容器内部的填充
        "}"
    )
    # 创建一个垂直布局
    v_layout = QVBoxLayout(container)

    # 创建下载链接输入框
    self.download_url_input = QLineEdit()
    self.download_url_input.setPlaceholderText("请输入程序ID")
    self.download_url_input.setStyleSheet(f"""
        font-family: '{self.custom_font.family()}'; /* 字体 */
        font-size: {self.fontPointSize}px; /* 字体大小 */
        font-weight: bold; /* 字体加粗 */
    """)

    #使用回车进行搜索
    self.download_url_input.returnPressed.connect(lambda: onGetUrlButtonClicked(self.download_url_input.text()))

    # 创建下载软件按钮
    get_url_button = QPushButton("下载软件")
    get_url_button.clicked.connect(lambda: onGetUrlButtonClicked(self.download_url_input.text()))
    get_url_button.setStyleSheet(
        "QPushButton {"
        "   background-color: #2196F3;"  # 按钮背景色
        "   color: white;"                # 按钮字体颜色
        "   border: none;"                # 去掉按钮边框
        "   padding: 10px;"               # 按钮内边距
        "   border-radius: 5px;"          # 按钮圆角
        f"   font-family: '{self.custom_font.family()}';"            # 设置表头字体
        f"   font-size: {self.fontPointSize + 2}px;"             # 字体大小
        "}"
        "QPushButton:hover {"
        "   background-color: #1976D2;"  # 鼠标悬停时的背景色
        "}"
        "QPushButton:pressed {"
        "   background-color: #2196F3;"   # 按钮按下时的背景色
        "}"
    )



    # 创建一个用于显示当前软件信息的 QWidget
    info_widget = QWidget()
    info_widget.setStyleSheet("background-color: #f0f8ff; padding: 10px; border-radius: 10px;")  # 设置背景颜色和内边距

    # 获取ClassIsland_info
    ClassIsland_info = self.ClassIsland_info

    # 检查ClassIsland_info是否是有效的列表，并获取第一个软件的信息
    if isinstance(ClassIsland_info, list) and len(ClassIsland_info) > 0:
        software_info = ClassIsland_info[0]  # 获取第一个软件的信息

        # 安全获取软件信息
        current_software_name = QLabel(f"软件：{software_info.get('name', '未知软件')}")
        current_software_author = QLabel(f"作者：{software_info.get('author', '未知作者')}")
        current_software_version = QLabel(f"最新版本：{software_info.get('version', '未知版本')}")
        current_software_stars_count = QLabel(f"star人数：{software_info.get('stars_count', '未知')}")
        current_software_description = QLabel(f"简介：{software_info.get('description', '无描述')}")

        # 设置样式表
        for label in [current_software_name, current_software_author, current_software_version, 
                    current_software_stars_count, current_software_description]:
            label.setStyleSheet(f"color: #2196F3; font-size: {self.fontPointSize + 2}px; font-family: '{self.custom_font.family()}';")
    else:
        # 如果ClassIsland_info无效或为空，提供默认信息
        current_software_name = QLabel("ClassIsland")
        current_software_author = QLabel("作者信息加载失败")
        current_software_version = QLabel("版本信息加载失败")
        current_software_stars_count = QLabel("star人数加载失败")
        current_software_description = QLabel("请重启软件即可修复")

        # 设置样式表
        for label in [current_software_name, current_software_author, current_software_version, 
                    current_software_stars_count, current_software_description]:
            label.setStyleSheet(f"color: #2196F3; font-size: {self.fontPointSize + 2}px; font-family: '{self.custom_font.family()}';")





    # 创建水平布局并添加标签
    current_software_layout_one = QHBoxLayout()
    current_software_layout_one.setSpacing(15)  # 设置水平布局内的间距
    current_software_layout_one.addWidget(current_software_name, alignment=Qt.AlignLeft)
    current_software_layout_one.addWidget(current_software_author, alignment=Qt.AlignLeft)
    current_software_layout_one.addWidget(current_software_version, alignment=Qt.AlignLeft)
    current_software_layout_one.addWidget(current_software_stars_count, alignment=Qt.AlignLeft)

    # 创建一个QWidget来容纳水平布局
    h_widget = QWidget()
    h_widget.setLayout(current_software_layout_one)  # 将水平布局设置为h_widget的布局

    # 创建垂直布局并添加标签
    current_software_layout = QVBoxLayout()
    current_software_layout.setSpacing(10)  # 设置垂直布局内的间距
    current_software_layout.addWidget(h_widget, alignment=Qt.AlignCenter)  # 添加h_widget而不是current_software_layout_one
    current_software_layout.addWidget(current_software_description, alignment=Qt.AlignCenter)

    # 将垂直布局添加到info_widget
    current_layout = QVBoxLayout(info_widget)
    current_layout.addLayout(current_software_layout)



        
    # 创建结果显示区域的标签
    result_label = QLabel()
    result_label.setText("ClassIsland 的下载页面")
    result_label.setStyleSheet(f"""
        color: red;
        font-family: '{self.custom_font.family()}'; /* 字体 */
        font-size: {self.fontPointSize + 2}px; /* 字体大小 */
        font-weight: bold; /* 字体加粗 */
    """)

    # 创建搜索框
    search_box = QLineEdit()
    search_box.setPlaceholderText("请输入搜索内容")
    search_box.setStyleSheet(f"""
        font-family: '{self.custom_font.family()}'; /* 字体黑体 */
        font-size: {self.fontPointSize + 2}px; /* 字体大小 */
        font-weight: bold; /* 字体加粗 */
    """)


    # 创建搜索按钮
    search_button = QPushButton("搜索")
    search_button.clicked.connect(lambda: searchSoftwares(search_box.text()))
    search_button.setStyleSheet(
        "QPushButton {"
        "   background-color: #2196F3;"  # 按钮背景色
        "   color: white;"                # 按钮字体颜色
        "   border: none;"                # 去掉按钮边框
        "   padding: 10px;"               # 按钮内边距
        "   border-radius: 5px;"          # 按钮圆角
        f"   font-family: '{self.custom_font.family()}';"            # 设置表头字体为黑体
        f"   font-size: {self.fontPointSize + 2}px;"             # 字体大小
        "}"
        "QPushButton:hover {"
        "   background-color: #1976D2;"  # 鼠标悬停时的背景色
        "}"
        "QPushButton:pressed {"
        "   background-color: #2196F3;"   # 按钮按下时的背景色
        "}"
    )

    #使用回车进行搜索
    search_box.returnPressed.connect(lambda: searchSoftwares(search_box.text()))

    # 创建一个 QFrame 用于包裹表格
    self.frame = QFrame(self)
    self.frame.setStyleSheet(
        "QFrame {"
        "   border: 2px solid #dcdcdc;"     # 外框边框
        "   border-radius: 8px;"            # 外框圆角
        "   padding: 10px;"                  # 内边距
        "}"
    )

    # 将搜索框和按钮放入水平布局
    search_layout = QHBoxLayout()
    search_layout.addWidget(search_box)
    search_layout.addWidget(search_button)

    # 创建结果显示区域的表格
    self.result_table = QTableWidget(self.frame)
    self.result_table.setColumnCount(9)
    self.result_table.setHorizontalHeaderLabels(['ID', '名称', '作者', '版本号', '大小', '文件格式', '下载源', '备注', '发布时间'])
    self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表头宽度
    self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑单元格
    self.result_table.setContextMenuPolicy(Qt.NoContextMenu)  # 禁止右键菜单
    self.result_table.setDragDropOverwriteMode(False)  # 禁止拖动覆盖单元格
    self.result_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 设置左侧表头宽度
    self.result_table.verticalHeader().setVisible(False)  # 禁止显示左侧表头
    self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中一行
    self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 单选
    self.result_table.setAlternatingRowColors(True)  # 交替行背景色
    self.result_table.setSortingEnabled(True)  # 允许排序
    self.result_table.sortByColumn(8, Qt.DescendingOrder)  # 默认按发布时间倒序排列

    # 将表格的样式设置
    self.result_table.setStyleSheet(
        "QTableWidget {"
        "   background-color: #f9f9f9;"    # 设置背景色
        "   gridline-color: #dcdcdc;"      # 设置网格线颜色
        "   border: none;"                 # 去掉QTableWidget的边框
        "   margin: 5px;"                  # 表格外边距，增加整体间距
        "} "
        "QTableWidget::item {"
        "   border: 2px solid #dcdcdc;"    # 设置单元格边框
        "   padding: 5px;"                 # 设置单元格内边距
        "   background-color: #f9f9f9;"    # 设置单元格背景色
        "   border-radius: 5px;"           # 设置圆角半径
        "} "
        "QHeaderView::section {"
        "   background-color: #2196F3;"    # 设置表头背景色
        "   border-radius: 5px;"           # 圆角
        "   color: white;"                 # 设置表头文字颜色
        f"   font-size: {self.fontPointSize}px;"              # 设置表头字体大小
        "   font-weight: bold;"            # 设置表头字体加粗
        f"   font-family: '{self.custom_font.family()}';"            # 设置表头字体为黑体
        "   padding: 5px;"                 # 设置表头内边距
        "   border: 1px solid #dcdcdc;"    # 边框与单元格对齐
        "} "
        "QTableWidget::item:selected {"
        "   background-color: #dcdcdc;"    # 选中时单元格的背景色
        "   border-radius: 5px;"           # 圆角
        "   color: black;"                 # 选中时字体颜色
        "}"
    )


    # 填充表格数据
    for software_info in self.ClassIsland_links:  # 遍历所有软件
        row_num = self.result_table.rowCount()  # 获取当前行数
        self.result_table.insertRow(row_num)  # 插入一行

        # 创建字体对象，设置为黑体
        font = QFont(self.custom_font.family())  # 设置字体为黑体
        font.setPixelSize(self.fontPointSize)  # 设置字体大小

        # 创建ID列的单元格
        id_item = QTableWidgetItem(str(software_info['id']))
        id_item.setFont(font)  # 设置字体
        id_item.setTextAlignment(Qt.AlignCenter)  # 设置ID列文本居中
        self.result_table.setItem(row_num, 0, id_item)

        # 创建名称列的单元格
        name_item = QTableWidgetItem(software_info['name'])
        name_item.setFont(font)  # 设置字体
        name_item.setTextAlignment(Qt.AlignCenter)  # 设置名称列文本居中
        self.result_table.setItem(row_num, 1, name_item)

        # 创建作者列的单元格
        author_item = QTableWidgetItem(software_info['author'])
        author_item.setFont(font)  # 设置字体
        author_item.setTextAlignment(Qt.AlignCenter)  # 设置作者列文本居中
        self.result_table.setItem(row_num, 2, author_item)

        # 创建版本号列的单元格
        version_item = QTableWidgetItem(software_info['version'])
        version_item.setFont(font)  # 设置字体
        version_item.setTextAlignment(Qt.AlignCenter)  # 设置版本号列文本居中
        self.result_table.setItem(row_num, 3, version_item)

        # 创建大小列的单元格
        size_item = QTableWidgetItem(software_info['size'])
        size_item.setFont(font)  # 设置字体
        size_item.setTextAlignment(Qt.AlignCenter)  # 设置大小列文本居中
        self.result_table.setItem(row_num, 4, size_item)

        # 创建文件格式列的单元格
        format_item = QTableWidgetItem(software_info['format'])
        format_item.setFont(font)  # 设置字体
        format_item.setTextAlignment(Qt.AlignCenter)  # 设置文件格式列文本居中
        self.result_table.setItem(row_num, 5, format_item)

        # 创建下载源列的单元格
        source_item = QTableWidgetItem(software_info['source'])
        source_item.setFont(font)  # 设置字体
        source_item.setTextAlignment(Qt.AlignCenter)  # 设置下载源列文本居中
        self.result_table.setItem(row_num, 6, source_item)

        # 创建备注列的单元格
        note_item = QTableWidgetItem(software_info['note'])
        note_item.setFont(font)  # 设置字体
        note_item.setTextAlignment(Qt.AlignCenter)  # 设置备注列文本居中
        self.result_table.setItem(row_num, 7, note_item)

        # 创建发布时间列的单元格
        release_time_item = QTableWidgetItem(software_info['first_release'])
        release_time_item.setFont(font)  # 设置字体
        release_time_item.setTextAlignment(Qt.AlignCenter)  # 设置发布时间列文本居中
        self.result_table.setItem(row_num, 8, release_time_item)



    # 搜索逻辑
    def searchSoftwares(keyword):
        # 根据关键字搜索软件并填充表格
        self.result_table.setRowCount(0)  # 清空表格
        keyword = keyword.lower() # 转换为小写字母
        results = [] # 存储搜索结果
        for software in self.ClassIsland_links: # 遍历所有软件
            if any(keyword in str(value).lower() for value in software.values()): # 找到相关软件
                results.append(software) # 找到相关软件
        
        for software in results: # 填充表格显示
            rowPosition = self.result_table.rowCount() # 获取当前行数
            self.result_table.insertRow(rowPosition) # 插入一行
            for column, key in enumerate(software.keys()): # 填充一行数据
                item = QTableWidgetItem(str(software[key])) # 创建单元格
                item.setTextAlignment(Qt.AlignCenter) # 设置单元格文本居中
                self.result_table.setItem(rowPosition, column, item) # 设置单元格数据
        
        if self.result_table.rowCount() == 0:
            result_label.setText("未找到相关软件，请检查输入")
        else:
            result_label.setText(f"找到 {self.result_table.rowCount()} 个相关软件")


    # 获取下载链接按钮的点击事件处理
    def onGetUrlButtonClicked(program_id):
        # 配置当前功能标识符
        identifier = "Software_Download"
        # 主逻辑
        program_id = self.download_url_input.text()
        for software in self.ClassIsland_links:
            if software['id'] == program_id:
                if askForDownloadConfirmation(software['name'], software['version'], software['source']):
                    download_path = getDownloadPath(software['name'], software['source'])
                    if download_path:
                        custom_filename = create_custom_filename(software)  # 创建自定义文件名
                        # 统一下载逻辑
                        try:
                            # 导入下载功能模块
                            from All_Download import DownloadManager

                            # 创建下载进度实例
                            self.download_manager = DownloadManager()
                            
                            # 开始下载
                            self.download_manager.startDownload(software['url'], download_path, custom_filename, identifier)
                        except ImportError as e:
                            self.show_custom_message(self, "错误", f"下载功能模块未能导入，请向作者反映问题 {str(e)}", QMessageBox.Critical)
                        except AttributeError as e:
                            self.show_custom_message(self, "错误", f"下载功能模块未能正确调用，请向作者反映问题 {str(e)}", QMessageBox.Critical)
                        except Exception as e:
                            self.show_custom_message(self, "错误", f"下载失败，请向作者反映问题 {str(e)}", QMessageBox.Critical)

                    else:
                        result_label.setText('下载路径未设置或选择')
                        return
                else:
                    result_label.setText('取消下载')
                break
        else:
            result_label.setText('未找到相关软件，请检查输入')


    def create_custom_filename(software):
        # 根据软件信息创建自定义文件名
        software_name = software['name']
        version = software['version']
        file_format = software['format']

        # 根据软件名称和下载源进行特殊处理
        if software_name == "ClassIsland":
            # 特定软件名称且来源为GitHub或者是appcenter的特别处理
            custom_filename = f"{software_name}-{version}.{file_format}"

        else:
            # 其他情况的默认处理
            custom_filename = f"{software_name}-{version}.{file_format}"

        return custom_filename # 返回自定义文件名
    

    def askForDownloadConfirmation(software_name, software_version, software_source):
        # 特定软件名称的下载询问用户确认对话框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('确认下载')
        msg_box.setText(f'您确定要下载 {software_name} {software_version}吗?')
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        
        # 自定义按钮样式
        yes_button = msg_box.button(QMessageBox.Yes)
        yes_button.setText("是")  # 自定义按钮文字
        yes_button.setStyleSheet(f"""
            font-family: '{self.custom_font.family()}';        /* 设置字体 */
            background-color: #2196F3;  /* 蓝色背景 */
            color: white;               /* 白色文字 */
            border: none;               /* 去掉边框 */
            border-radius: 5px;         /* 边框圆角 */
            padding: 10px;         /* 内边距 */
            font-size: {self.fontPointSize}px;            /* 字体大小 */
            font-weight: bold;          /* 粗体 */
        """)
        no_button = msg_box.button(QMessageBox.No)
        no_button.setText("否")
        no_button.setStyleSheet(f"""
            font-family: '{self.custom_font.family()}';        /* 设置字体 */
            background-color: #f44336;  /* 红色背景 */
            color: white;               /* 白色文字 */
            border: none;               /* 去掉边框 */
            border-radius: 5px;         /* 边框圆角 */
            padding: 10px;         /* 内边距 */
            font-size: {self.fontPointSize}px;            /* 字体大小 */
            font-weight: bold;          /* 粗体 */
        """)
        
        return msg_box.exec_() == QMessageBox.Yes


    def getDownloadPath(software_name, software_source):
        # 获取应用程序的根目录
        app_dir = Path(os.getcwd())

        default_download_path = geetDownloadPath()
        
        # 系统设置中读取系统默认下载目录
        if not default_download_path:
            # 弹出选择下载目录的对话框
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.DirectoryOnly)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setWindowTitle("选择下载目录")
            
            # 检查是否有默认路径，如果没有则创建
            default_path = os.path.join(app_dir, 'Downloads') 
            if not os.path.exists(os.path.join(app_dir, 'Downloads')):
                os.makedirs(os.path.join(app_dir, 'Downloads'))
            dialog.setDirectory(default_path) # 设置默认路径
            
            # 弹出对话框让用户选择路径
            if dialog.exec_():
                selected_path = dialog.selectedFiles()[0]
                # 提供一个选项让用户选择是否设置为默认路径
                set_default_message_box = QMessageBox(self)
                set_default_message_box.setWindowTitle("设置默认下载目录")
                set_default_message_box.setText("您希望将此目录设置为默认下载目录吗？")
                set_default_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                set_default_message_box.setDefaultButton(QMessageBox.Yes)

                # 自定义按钮样式
                yes_button = set_default_message_box.button(QMessageBox.Yes)
                yes_button.setText("是")  # 自定义按钮文字
                yes_button.setStyleSheet(f"""
                    font-family: '{self.custom_font.family()}';        /* 设置字体 */
                    background-color: #2196F3;  /* 蓝色背景 */
                    color: white;               /* 白色文字 */
                    border: none;               /* 去掉边框 */
                    border-radius: 5px;         /* 边框圆角 */
                    padding: 10px;         /* 内边距 */
                    font-size: {self.fontPointSize}px;            /* 字体大小 */
                    font-weight: bold;          /* 粗体 */
                """)
                no_button = set_default_message_box.button(QMessageBox.No)
                no_button.setText("否")
                no_button.setStyleSheet(f"""
                    font-family: '{self.custom_font.family()}';        /* 设置字体 */
                    background-color: #f44336;  /* 红色背景 */
                    color: white;               /* 白色文字 */
                    border: none;               /* 去掉边框 */
                    border-radius: 5px;         /* 边框圆角 */
                    padding: 10px;         /* 内边距 */
                    font-size: {self.fontPointSize}px;            /* 字体大小 */
                    font-weight: bold;          /* 粗体 */
                """)

                # 自定义消息框文本样式
                set_default_message_box.setStyleSheet(f"""
                    QMessageBox {{
                        font-family: '{self.custom_font.family()}';        /* 设置字体 */
                        background-color: #FFFFFF;
                        font-size: 14px;
                        color: #333333;
                    }}
                """)

                if set_default_message_box.exec_() == QMessageBox.Yes:
                    # 用户选择设置为默认路径
                    setDownloadPath(self, selected_path) # 设置默认下载路径
                    return selected_path # 返回选择的路径
                else:
                    return selected_path # 返回选择的路径
            else:
                return None # 用户取消了对话框
        else:
            return default_download_path # 返回默认下载路径


    def setDownloadPath(self, selected_path):
            # 这里可以根据需要实现设置默认下载路径的逻辑
            # 例如，使用QSettings类保存设置
            # self.default_download_path = selected_path
            if not os.path.exists(os.path.join('config', 'download_file_path')):
                os.makedirs(os.path.join('config', 'download_file_path'))
            with open(os.path.join('config', 'download_file_path', 'default_path.ini'), 'w') as f:
                f.write(selected_path)
                f.close()
                return selected_path


    def geetDownloadPath():
        # 这里可以根据需要实现获取默认下载路径的逻辑
        # 系统设置中读取系统默认下载目录
        if os.path.exists(os.path.join('config', 'download_file_path', 'default_path.ini')):
            with open(os.path.join('config', 'download_file_path', 'default_path.ini'), 'r') as f:
                download_file_path = f.read()
                f.close()
                return download_file_path
        else:
            return None


    def open_web(url):
        # 用户选择打开浏览器
        webbrowser.open(url)


    # 创建结果显示区域的标签
    result_label = QLabel()
    result_label.setStyleSheet("color: red;")

    # 将搜索结果表格、下载链接输入框和按钮添加到布局
    v_layout.addWidget(info_widget)
    v_layout.addLayout(search_layout)
    v_layout.addWidget(self.result_table)
    v_layout.addWidget(result_label)
    v_layout.addWidget(self.download_url_input)
    v_layout.addWidget(get_url_button)

    # 设置容器的布局
    container.setLayout(v_layout)

    # 将容器添加到主窗口的布局中
    self.layout.addWidget(container)
    self.layout.setStretchFactor(container, 1)
    self.setWindowTitle('SectionIstool - ClassIsland 下载')
    

    # 返回container，以便可以在initUI中使用
=======
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QFrame
import os 
import webbrowser
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from pathlib import Path
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFontDatabase



# 软件下载
def showSoftwareClassIslandDownloadContent(self):
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

    # 创建一个QWidget作为容器
    container = QWidget()

    # 设置容器的样式，添加圆角边框
    container.setStyleSheet(
        "QWidget {"
        "   border: 1px solid #dcdcdc;"  # 设置容器的边框颜色
        "   border-radius: 10px;"        # 设置圆角半径
        "   background-color: #ffffff;"   # 设置容器的背景色
        "   padding: 5px;"                # 设置容器内部的填充
        "}"
    )
    # 创建一个垂直布局
    v_layout = QVBoxLayout(container)

    # 创建下载链接输入框
    self.download_url_input = QLineEdit()
    self.download_url_input.setPlaceholderText("请输入程序ID")
    self.download_url_input.setStyleSheet(f"""
        font-family: '{self.custom_font.family()}'; /* 字体 */
        font-size: {self.fontPointSize}px; /* 字体大小 */
        font-weight: bold; /* 字体加粗 */
    """)

    #使用回车进行搜索
    self.download_url_input.returnPressed.connect(lambda: onGetUrlButtonClicked(self.download_url_input.text()))

    # 创建下载软件按钮
    get_url_button = QPushButton("下载软件")
    get_url_button.clicked.connect(lambda: onGetUrlButtonClicked(self.download_url_input.text()))
    get_url_button.setStyleSheet(
        "QPushButton {"
        "   background-color: #2196F3;"  # 按钮背景色
        "   color: white;"                # 按钮字体颜色
        "   border: none;"                # 去掉按钮边框
        "   padding: 10px;"               # 按钮内边距
        "   border-radius: 5px;"          # 按钮圆角
        f"   font-family: '{self.custom_font.family()}';"            # 设置表头字体
        f"   font-size: {self.fontPointSize + 2}px;"             # 字体大小
        "}"
        "QPushButton:hover {"
        "   background-color: #1976D2;"  # 鼠标悬停时的背景色
        "}"
        "QPushButton:pressed {"
        "   background-color: #2196F3;"   # 按钮按下时的背景色
        "}"
    )



    # 创建一个用于显示当前软件信息的 QWidget
    info_widget = QWidget()
    info_widget.setStyleSheet("background-color: #f0f8ff; padding: 10px; border-radius: 10px;")  # 设置背景颜色和内边距

    # 获取ClassIsland_info
    ClassIsland_info = self.ClassIsland_info

    # 检查ClassIsland_info是否是有效的列表，并获取第一个软件的信息
    if isinstance(ClassIsland_info, list) and len(ClassIsland_info) > 0:
        software_info = ClassIsland_info[0]  # 获取第一个软件的信息

        # 安全获取软件信息
        current_software_name = QLabel(f"软件：{software_info.get('name', '未知软件')}")
        current_software_author = QLabel(f"作者：{software_info.get('author', '未知作者')}")
        current_software_version = QLabel(f"最新版本：{software_info.get('version', '未知版本')}")
        current_software_stars_count = QLabel(f"star人数：{software_info.get('stars_count', '未知')}")
        current_software_description = QLabel(f"简介：{software_info.get('description', '无描述')}")

        # 设置样式表
        for label in [current_software_name, current_software_author, current_software_version, 
                    current_software_stars_count, current_software_description]:
            label.setStyleSheet(f"color: #2196F3; font-size: {self.fontPointSize + 2}px; font-family: '{self.custom_font.family()}';")
    else:
        # 如果ClassIsland_info无效或为空，提供默认信息
        current_software_name = QLabel("ClassIsland")
        current_software_author = QLabel("作者信息加载失败")
        current_software_version = QLabel("版本信息加载失败")
        current_software_stars_count = QLabel("star人数加载失败")
        current_software_description = QLabel("请重启软件即可修复")

        # 设置样式表
        for label in [current_software_name, current_software_author, current_software_version, 
                    current_software_stars_count, current_software_description]:
            label.setStyleSheet(f"color: #2196F3; font-size: {self.fontPointSize + 2}px; font-family: '{self.custom_font.family()}';")





    # 创建水平布局并添加标签
    current_software_layout_one = QHBoxLayout()
    current_software_layout_one.setSpacing(15)  # 设置水平布局内的间距
    current_software_layout_one.addWidget(current_software_name, alignment=Qt.AlignLeft)
    current_software_layout_one.addWidget(current_software_author, alignment=Qt.AlignLeft)
    current_software_layout_one.addWidget(current_software_version, alignment=Qt.AlignLeft)
    current_software_layout_one.addWidget(current_software_stars_count, alignment=Qt.AlignLeft)

    # 创建一个QWidget来容纳水平布局
    h_widget = QWidget()
    h_widget.setLayout(current_software_layout_one)  # 将水平布局设置为h_widget的布局

    # 创建垂直布局并添加标签
    current_software_layout = QVBoxLayout()
    current_software_layout.setSpacing(10)  # 设置垂直布局内的间距
    current_software_layout.addWidget(h_widget, alignment=Qt.AlignCenter)  # 添加h_widget而不是current_software_layout_one
    current_software_layout.addWidget(current_software_description, alignment=Qt.AlignCenter)

    # 将垂直布局添加到info_widget
    current_layout = QVBoxLayout(info_widget)
    current_layout.addLayout(current_software_layout)



        
    # 创建结果显示区域的标签
    result_label = QLabel()
    result_label.setText("ClassIsland 的下载页面")
    result_label.setStyleSheet(f"""
        color: red;
        font-family: '{self.custom_font.family()}'; /* 字体 */
        font-size: {self.fontPointSize + 2}px; /* 字体大小 */
        font-weight: bold; /* 字体加粗 */
    """)

    # 创建搜索框
    search_box = QLineEdit()
    search_box.setPlaceholderText("请输入搜索内容")
    search_box.setStyleSheet(f"""
        font-family: '{self.custom_font.family()}'; /* 字体黑体 */
        font-size: {self.fontPointSize + 2}px; /* 字体大小 */
        font-weight: bold; /* 字体加粗 */
    """)


    # 创建搜索按钮
    search_button = QPushButton("搜索")
    search_button.clicked.connect(lambda: searchSoftwares(search_box.text()))
    search_button.setStyleSheet(
        "QPushButton {"
        "   background-color: #2196F3;"  # 按钮背景色
        "   color: white;"                # 按钮字体颜色
        "   border: none;"                # 去掉按钮边框
        "   padding: 10px;"               # 按钮内边距
        "   border-radius: 5px;"          # 按钮圆角
        f"   font-family: '{self.custom_font.family()}';"            # 设置表头字体为黑体
        f"   font-size: {self.fontPointSize + 2}px;"             # 字体大小
        "}"
        "QPushButton:hover {"
        "   background-color: #1976D2;"  # 鼠标悬停时的背景色
        "}"
        "QPushButton:pressed {"
        "   background-color: #2196F3;"   # 按钮按下时的背景色
        "}"
    )

    #使用回车进行搜索
    search_box.returnPressed.connect(lambda: searchSoftwares(search_box.text()))

    # 创建一个 QFrame 用于包裹表格
    self.frame = QFrame(self)
    self.frame.setStyleSheet(
        "QFrame {"
        "   border: 2px solid #dcdcdc;"     # 外框边框
        "   border-radius: 8px;"            # 外框圆角
        "   padding: 10px;"                  # 内边距
        "}"
    )

    # 将搜索框和按钮放入水平布局
    search_layout = QHBoxLayout()
    search_layout.addWidget(search_box)
    search_layout.addWidget(search_button)

    # 创建结果显示区域的表格
    self.result_table = QTableWidget(self.frame)
    self.result_table.setColumnCount(9)
    self.result_table.setHorizontalHeaderLabels(['ID', '名称', '作者', '版本号', '大小', '文件格式', '下载源', '备注', '发布时间'])
    self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表头宽度
    self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑单元格
    self.result_table.setContextMenuPolicy(Qt.NoContextMenu)  # 禁止右键菜单
    self.result_table.setDragDropOverwriteMode(False)  # 禁止拖动覆盖单元格
    self.result_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 设置左侧表头宽度
    self.result_table.verticalHeader().setVisible(False)  # 禁止显示左侧表头
    self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中一行
    self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)  # 单选
    self.result_table.setAlternatingRowColors(True)  # 交替行背景色
    self.result_table.setSortingEnabled(True)  # 允许排序
    self.result_table.sortByColumn(8, Qt.DescendingOrder)  # 默认按发布时间倒序排列

    # 将表格的样式设置
    self.result_table.setStyleSheet(
        "QTableWidget {"
        "   background-color: #f9f9f9;"    # 设置背景色
        "   gridline-color: #dcdcdc;"      # 设置网格线颜色
        "   border: none;"                 # 去掉QTableWidget的边框
        "   margin: 5px;"                  # 表格外边距，增加整体间距
        "} "
        "QTableWidget::item {"
        "   border: 2px solid #dcdcdc;"    # 设置单元格边框
        "   padding: 5px;"                 # 设置单元格内边距
        "   background-color: #f9f9f9;"    # 设置单元格背景色
        "   border-radius: 5px;"           # 设置圆角半径
        "} "
        "QHeaderView::section {"
        "   background-color: #2196F3;"    # 设置表头背景色
        "   border-radius: 5px;"           # 圆角
        "   color: white;"                 # 设置表头文字颜色
        f"   font-size: {self.fontPointSize}px;"              # 设置表头字体大小
        "   font-weight: bold;"            # 设置表头字体加粗
        f"   font-family: '{self.custom_font.family()}';"            # 设置表头字体为黑体
        "   padding: 5px;"                 # 设置表头内边距
        "   border: 1px solid #dcdcdc;"    # 边框与单元格对齐
        "} "
        "QTableWidget::item:selected {"
        "   background-color: #dcdcdc;"    # 选中时单元格的背景色
        "   border-radius: 5px;"           # 圆角
        "   color: black;"                 # 选中时字体颜色
        "}"
    )


    # 填充表格数据
    for software_info in self.ClassIsland_links:  # 遍历所有软件
        row_num = self.result_table.rowCount()  # 获取当前行数
        self.result_table.insertRow(row_num)  # 插入一行

        # 创建字体对象，设置为黑体
        font = QFont(self.custom_font.family())  # 设置字体为黑体
        font.setPixelSize(self.fontPointSize)  # 设置字体大小

        # 创建ID列的单元格
        id_item = QTableWidgetItem(str(software_info['id']))
        id_item.setFont(font)  # 设置字体
        id_item.setTextAlignment(Qt.AlignCenter)  # 设置ID列文本居中
        self.result_table.setItem(row_num, 0, id_item)

        # 创建名称列的单元格
        name_item = QTableWidgetItem(software_info['name'])
        name_item.setFont(font)  # 设置字体
        name_item.setTextAlignment(Qt.AlignCenter)  # 设置名称列文本居中
        self.result_table.setItem(row_num, 1, name_item)

        # 创建作者列的单元格
        author_item = QTableWidgetItem(software_info['author'])
        author_item.setFont(font)  # 设置字体
        author_item.setTextAlignment(Qt.AlignCenter)  # 设置作者列文本居中
        self.result_table.setItem(row_num, 2, author_item)

        # 创建版本号列的单元格
        version_item = QTableWidgetItem(software_info['version'])
        version_item.setFont(font)  # 设置字体
        version_item.setTextAlignment(Qt.AlignCenter)  # 设置版本号列文本居中
        self.result_table.setItem(row_num, 3, version_item)

        # 创建大小列的单元格
        size_item = QTableWidgetItem(software_info['size'])
        size_item.setFont(font)  # 设置字体
        size_item.setTextAlignment(Qt.AlignCenter)  # 设置大小列文本居中
        self.result_table.setItem(row_num, 4, size_item)

        # 创建文件格式列的单元格
        format_item = QTableWidgetItem(software_info['format'])
        format_item.setFont(font)  # 设置字体
        format_item.setTextAlignment(Qt.AlignCenter)  # 设置文件格式列文本居中
        self.result_table.setItem(row_num, 5, format_item)

        # 创建下载源列的单元格
        source_item = QTableWidgetItem(software_info['source'])
        source_item.setFont(font)  # 设置字体
        source_item.setTextAlignment(Qt.AlignCenter)  # 设置下载源列文本居中
        self.result_table.setItem(row_num, 6, source_item)

        # 创建备注列的单元格
        note_item = QTableWidgetItem(software_info['note'])
        note_item.setFont(font)  # 设置字体
        note_item.setTextAlignment(Qt.AlignCenter)  # 设置备注列文本居中
        self.result_table.setItem(row_num, 7, note_item)

        # 创建发布时间列的单元格
        release_time_item = QTableWidgetItem(software_info['first_release'])
        release_time_item.setFont(font)  # 设置字体
        release_time_item.setTextAlignment(Qt.AlignCenter)  # 设置发布时间列文本居中
        self.result_table.setItem(row_num, 8, release_time_item)



    # 搜索逻辑
    def searchSoftwares(keyword):
        # 根据关键字搜索软件并填充表格
        self.result_table.setRowCount(0)  # 清空表格
        keyword = keyword.lower() # 转换为小写字母
        results = [] # 存储搜索结果
        for software in self.ClassIsland_links: # 遍历所有软件
            if any(keyword in str(value).lower() for value in software.values()): # 找到相关软件
                results.append(software) # 找到相关软件
        
        for software in results: # 填充表格显示
            rowPosition = self.result_table.rowCount() # 获取当前行数
            self.result_table.insertRow(rowPosition) # 插入一行
            for column, key in enumerate(software.keys()): # 填充一行数据
                item = QTableWidgetItem(str(software[key])) # 创建单元格
                item.setTextAlignment(Qt.AlignCenter) # 设置单元格文本居中
                self.result_table.setItem(rowPosition, column, item) # 设置单元格数据
        
        if self.result_table.rowCount() == 0:
            result_label.setText("未找到相关软件，请检查输入")
        else:
            result_label.setText(f"找到 {self.result_table.rowCount()} 个相关软件")


    # 获取下载链接按钮的点击事件处理
    def onGetUrlButtonClicked(program_id):
        # 配置当前功能标识符
        identifier = "Software_Download"
        # 主逻辑
        program_id = self.download_url_input.text()
        for software in self.ClassIsland_links:
            if software['id'] == program_id:
                if askForDownloadConfirmation(software['name'], software['version'], software['source']):
                    download_path = getDownloadPath(software['name'], software['source'])
                    if download_path:
                        custom_filename = create_custom_filename(software)  # 创建自定义文件名
                        # 统一下载逻辑
                        try:
                            # 导入下载功能模块
                            from All_Download import DownloadManager

                            # 创建下载进度实例
                            self.download_manager = DownloadManager()
                            
                            # 开始下载
                            self.download_manager.startDownload(software['url'], download_path, custom_filename, identifier)
                        except ImportError as e:
                            self.show_custom_message(self, "错误", f"下载功能模块未能导入，请向作者反映问题 {str(e)}", QMessageBox.Critical)
                        except AttributeError as e:
                            self.show_custom_message(self, "错误", f"下载功能模块未能正确调用，请向作者反映问题 {str(e)}", QMessageBox.Critical)
                        except Exception as e:
                            self.show_custom_message(self, "错误", f"下载失败，请向作者反映问题 {str(e)}", QMessageBox.Critical)

                    else:
                        result_label.setText('下载路径未设置或选择')
                        return
                else:
                    result_label.setText('取消下载')
                break
        else:
            result_label.setText('未找到相关软件，请检查输入')


    def create_custom_filename(software):
        # 根据软件信息创建自定义文件名
        software_name = software['name']
        version = software['version']
        file_format = software['format']

        # 根据软件名称和下载源进行特殊处理
        if software_name == "ClassIsland":
            # 特定软件名称且来源为GitHub或者是appcenter的特别处理
            custom_filename = f"{software_name}-{version}.{file_format}"

        else:
            # 其他情况的默认处理
            custom_filename = f"{software_name}-{version}.{file_format}"

        return custom_filename # 返回自定义文件名
    

    def askForDownloadConfirmation(software_name, software_version, software_source):
        # 特定软件名称的下载询问用户确认对话框
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('确认下载')
        msg_box.setText(f'您确定要下载 {software_name} {software_version}吗?')
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)
        
        # 自定义按钮样式
        yes_button = msg_box.button(QMessageBox.Yes)
        yes_button.setText("是")  # 自定义按钮文字
        yes_button.setStyleSheet(f"""
            font-family: '{self.custom_font.family()}';        /* 设置字体 */
            background-color: #2196F3;  /* 蓝色背景 */
            color: white;               /* 白色文字 */
            border: none;               /* 去掉边框 */
            border-radius: 5px;         /* 边框圆角 */
            padding: 10px;         /* 内边距 */
            font-size: {self.fontPointSize}px;            /* 字体大小 */
            font-weight: bold;          /* 粗体 */
        """)
        no_button = msg_box.button(QMessageBox.No)
        no_button.setText("否")
        no_button.setStyleSheet(f"""
            font-family: '{self.custom_font.family()}';        /* 设置字体 */
            background-color: #f44336;  /* 红色背景 */
            color: white;               /* 白色文字 */
            border: none;               /* 去掉边框 */
            border-radius: 5px;         /* 边框圆角 */
            padding: 10px;         /* 内边距 */
            font-size: {self.fontPointSize}px;            /* 字体大小 */
            font-weight: bold;          /* 粗体 */
        """)
        
        return msg_box.exec_() == QMessageBox.Yes


    def getDownloadPath(software_name, software_source):
        # 获取应用程序的根目录
        app_dir = Path(os.getcwd())

        default_download_path = geetDownloadPath()
        
        # 系统设置中读取系统默认下载目录
        if not default_download_path:
            # 弹出选择下载目录的对话框
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.DirectoryOnly)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setWindowTitle("选择下载目录")
            
            # 检查是否有默认路径，如果没有则创建
            default_path = os.path.join(app_dir, 'Downloads') 
            if not os.path.exists(os.path.join(app_dir, 'Downloads')):
                os.makedirs(os.path.join(app_dir, 'Downloads'))
            dialog.setDirectory(default_path) # 设置默认路径
            
            # 弹出对话框让用户选择路径
            if dialog.exec_():
                selected_path = dialog.selectedFiles()[0]
                # 提供一个选项让用户选择是否设置为默认路径
                set_default_message_box = QMessageBox(self)
                set_default_message_box.setWindowTitle("设置默认下载目录")
                set_default_message_box.setText("您希望将此目录设置为默认下载目录吗？")
                set_default_message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                set_default_message_box.setDefaultButton(QMessageBox.Yes)

                # 自定义按钮样式
                yes_button = set_default_message_box.button(QMessageBox.Yes)
                yes_button.setText("是")  # 自定义按钮文字
                yes_button.setStyleSheet(f"""
                    font-family: '{self.custom_font.family()}';        /* 设置字体 */
                    background-color: #2196F3;  /* 蓝色背景 */
                    color: white;               /* 白色文字 */
                    border: none;               /* 去掉边框 */
                    border-radius: 5px;         /* 边框圆角 */
                    padding: 10px;         /* 内边距 */
                    font-size: {self.fontPointSize}px;            /* 字体大小 */
                    font-weight: bold;          /* 粗体 */
                """)
                no_button = set_default_message_box.button(QMessageBox.No)
                no_button.setText("否")
                no_button.setStyleSheet(f"""
                    font-family: '{self.custom_font.family()}';        /* 设置字体 */
                    background-color: #f44336;  /* 红色背景 */
                    color: white;               /* 白色文字 */
                    border: none;               /* 去掉边框 */
                    border-radius: 5px;         /* 边框圆角 */
                    padding: 10px;         /* 内边距 */
                    font-size: {self.fontPointSize}px;            /* 字体大小 */
                    font-weight: bold;          /* 粗体 */
                """)

                # 自定义消息框文本样式
                set_default_message_box.setStyleSheet(f"""
                    QMessageBox {{
                        font-family: '{self.custom_font.family()}';        /* 设置字体 */
                        background-color: #FFFFFF;
                        font-size: 14px;
                        color: #333333;
                    }}
                """)

                if set_default_message_box.exec_() == QMessageBox.Yes:
                    # 用户选择设置为默认路径
                    setDownloadPath(self, selected_path) # 设置默认下载路径
                    return selected_path # 返回选择的路径
                else:
                    return selected_path # 返回选择的路径
            else:
                return None # 用户取消了对话框
        else:
            return default_download_path # 返回默认下载路径


    def setDownloadPath(self, selected_path):
            # 这里可以根据需要实现设置默认下载路径的逻辑
            # 例如，使用QSettings类保存设置
            # self.default_download_path = selected_path
            if not os.path.exists(os.path.join('config', 'download_file_path')):
                os.makedirs(os.path.join('config', 'download_file_path'))
            with open(os.path.join('config', 'download_file_path', 'default_path.ini'), 'w') as f:
                f.write(selected_path)
                f.close()
                return selected_path


    def geetDownloadPath():
        # 这里可以根据需要实现获取默认下载路径的逻辑
        # 系统设置中读取系统默认下载目录
        if os.path.exists(os.path.join('config', 'download_file_path', 'default_path.ini')):
            with open(os.path.join('config', 'download_file_path', 'default_path.ini'), 'r') as f:
                download_file_path = f.read()
                f.close()
                return download_file_path
        else:
            return None


    def open_web(url):
        # 用户选择打开浏览器
        webbrowser.open(url)


    # 创建结果显示区域的标签
    result_label = QLabel()
    result_label.setStyleSheet("color: red;")

    # 将搜索结果表格、下载链接输入框和按钮添加到布局
    v_layout.addWidget(info_widget)
    v_layout.addLayout(search_layout)
    v_layout.addWidget(self.result_table)
    v_layout.addWidget(result_label)
    v_layout.addWidget(self.download_url_input)
    v_layout.addWidget(get_url_button)

    # 设置容器的布局
    container.setLayout(v_layout)

    # 将容器添加到主窗口的布局中
    self.layout.addWidget(container)
    self.layout.setStretchFactor(container, 1)
    self.setWindowTitle('SectionIstool - ClassIsland 下载')
    

    # 返回container，以便可以在initUI中使用
>>>>>>> 4fa2a7888d33a4299e04b4d0deacd959883e7656
    return container