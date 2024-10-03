import requests
import os
import time
import math
from PyQt5.QtWidgets import QMessageBox, QProgressBar, QPushButton, QVBoxLayout, QDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QThread
import webbrowser  # 用于打开文件或浏览器
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QFont

class DownloadWorker(QThread):
    progress = pyqtSignal(int, int, str, str, str)  # 更新信号中的参数列表
    finished = pyqtSignal(str)  # 下载完成信号

    def __init__(self, url, download_path, custom_filename, identifier):
        super().__init__()
        self.url = url
        self.download_path = download_path
        self.custom_filename = custom_filename
        self.identifier = identifier
        self.download_active = True

    def run(self):
        download_file = os.path.join(self.download_path, self.custom_filename + '.SectionIstool.download')  # 设置临时文件名
        response = requests.get(self.url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        total_size = int(response.headers.get('content-length', 0))  # 获取文件大小
        downloaded_size = 0
        block_size = 4096  # 块大小

        start_time = time.time()  # 记录开始时间

        with open(download_file, 'wb') as file:
            while self.download_active:
                data = response.raw.read(block_size)
                if not data:
                    break
                file.write(data)
                downloaded_size += len(data)

                # 计算当前下载速度
                elapsed_time = time.time() - start_time

                # 计算速度和剩余时间
                if elapsed_time > 0:
                    speed = downloaded_size / elapsed_time
                    remaining_size = total_size - downloaded_size
                    remaining_time = remaining_size / speed if speed > 0 else float('inf')  # 计算剩余时间
                else:
                    speed = 0
                    remaining_time = float('inf')  # 如果没有下载，则设置为无限大

                # 检查 remaining_time 的值
                if remaining_time == float('inf'):
                    remaining_time_display = "---"  # 设置为合适的默认值
                else:
                    remaining_time_display = self.format_time(remaining_time)  # 格式化剩余时间

                # 发射更新信号
                self.progress.emit(
                    downloaded_size,
                    total_size,
                    self.format_size(downloaded_size),
                    remaining_time_display,  # 使用格式化后的剩余时间
                    self.format_speed(speed)
                )


        if self.download_active:
            self.finalize_download(download_file)
        else:
            pass

    def finalize_download(self, temp_file):
        final_file = os.path.join(self.download_path, self.custom_filename)
        os.rename(temp_file, final_file)  # 重命名文件为最终文件
        self.finished.emit(final_file)  # 发送完成信号

    def stop(self):
        self.download_active = False

    def format_size(self, size):
        """格式化字节大小为可读字符串"""
        if not isinstance(size, (int, float)) or size < 0:  # 检查是否为有效数字并且不小于零
            return "---"  # 当传入的size无效时返回默认值

        if size >= 1024**4:  # 大于等于1 TB
            return f"{size / (1024**4):.2f} TB"
        elif size >= 1024**3:  # 大于等于1 GB
            return f"{size / (1024**3):.2f} GB"
        elif size >= 1024**2:  # 大于等于1 MB
            return f"{size / (1024**2):.2f} MB"
        elif size >= 1024:  # 大于等于1 KB
            return f"{size / 1024:.2f} KB"
        elif size > 0:  # 大于0字节
            return f"{size} B"
        else:
            return "---"


    def format_speed(self, size):
        """格式化字节大小为可读字符串"""
        if not isinstance(size, (int, float)) or size < 0:  # 检查是否为有效数字并且不小于零
            return "---"  # 当传入的size无效时返回默认值

        if size >= 1024**2:
            return f"{size / (1024**2):.2f} MB/s"
        elif size >= 1024:
            return f"{size / 1024:.2f} KB/s"
        elif size > 0:
            return f"{size} B/s"
        else:
            return "---"


    def format_time(self, seconds):
        """将秒数格式化为天、小时、分钟和秒的字符串表示"""
        if not isinstance(seconds, (int, float)) or seconds < 0 or math.isnan(seconds):  # 检查是否为有效数字并且不小于零
            return "---"  # 当传入的seconds无效时返回默认值
        
        if seconds < 0.001:
            return "---"  # 小于一毫秒
        elif seconds < 1:
            return f"{int(seconds * 1000)}毫秒"  # 小于一秒
        elif seconds < 60:
            return f"{int(seconds)}秒"  # 小于一分钟
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes}分钟{int(seconds % 60)}秒"  # 小于一小时
        elif seconds < 86400:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}小时{minutes}分钟{int(seconds % 60)}秒"  # 小于一天
        else:
            days = int(seconds // 86400)
            hours = int((seconds % 86400) // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{days}天{hours}小时{minutes}分钟{int(seconds % 60)}秒"  # 天及其进一步细分




class DownloadManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SectionIstool 下载进度")
        self.download_active = False

        # 加载自定义字体
        font_path = os.path.join(os.path.dirname(__file__), 'font\\HarmonyOS_Sans_Medium.ttf')  # 相对路径
        font_id = QFontDatabase.addApplicationFont(font_path)
        
        # 检查字体是否加载成功
        if font_id != -1:
            self.custom_font = QFont(QFontDatabase.applicationFontFamilies(font_id)[0])
        else:
            self.custom_font = QFont("黑体")  # 默认字体

        # 获取屏幕尺寸
        screen = QDesktopWidget().availableGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # 定义缩放因子
        font_scale_factor = 0.014

        # 计算字体大小
        self.fontPointSize = int(min(screenWidth, screenHeight) * font_scale_factor)
        self.custom_font.setPointSize(self.fontPointSize)

        self.init_screen(0.21, None, None)

        self.initUI()



    def initUI(self):
        self.setStyleSheet("background-color: #ffffff;")

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                font-family: '{self.custom_font.family()}';
                font-size: {self.fontPointSize + 2}px;
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center; 
                background-color: #e0e0e0;  
            }}
            QProgressBar::chunk {{
                background-color: #05B8CC;  /* 默认颜色 */
            }}
        """)
        
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.progress_bar)

        # 显示进度信息标签
        self.info_label = QLabel(self)
        self.info_label.setStyleSheet(f"font-family: '{self.custom_font.family()}'; font-size: {self.fontPointSize + 2}px;")
        self.layout().addWidget(self.info_label)

        # 停止下载按钮
        self.stop_button = QPushButton("停止下载", self)
        self.stop_button.adjustSize()
        self.stop_button.clicked.connect(self.stop_download)
        self.stop_button.setStyleSheet(f"font-family: '{self.custom_font.family()}'; color: black; background-color: #f44336; border-radius: 5px; font-size: {self.fontPointSize + 2}px;")
        self.layout().addWidget(self.stop_button)

        # 创建横向布局以并排放置按钮
        button_layout = QHBoxLayout()

        # 打开文件按钮
        self.open_file_button = QPushButton("打开文件", self)
        self.open_file_button.adjustSize()
        self.open_file_button.clicked.connect(self.open_file)
        self.open_file_button.setStyleSheet(f"font-family: '{self.custom_font.family()}'; color: black; background-color: #2196F3; border-radius: 5px; font-size: {self.fontPointSize + 2}px;")
        button_layout.addWidget(self.open_file_button)

        # 打开文件夹按钮
        self.open_folder_button = QPushButton("打开文件夹", self)
        self.open_folder_button.adjustSize()
        self.open_folder_button.clicked.connect(self.open_folder)
        self.open_folder_button.setStyleSheet(f"font-family: '{self.custom_font.family()}'; color: black; background-color: #2196F3; border-radius: 5px; font-size: {self.fontPointSize + 2}px;")
        button_layout.addWidget(self.open_folder_button)

        # 将横向按钮布局添加到主布局
        self.layout().addLayout(button_layout)

        def update_progress(self, value):
            """更新进度条的值，并进行错误检查"""
            try:
                value = int(value)  # 尝试将值转换为整数
                if 0 <= value <= 100:
                    self.progress_bar.setValue(value)
                    # 计算渐变色
                    r, g, b = self.calculate_gradient_color(value)
                    # 更新进度条样式
                    self.progress_bar.setStyleSheet(f"""
                        QProgressBar {{
                            font-family: '{self.custom_font.family()}';
                            font-size: {self.fontPointSize + 2}px;
                            border: 2px solid grey;
                            border-radius: 5px;
                            text-align: center; 
                            background-color: #e0e0e0;  
                        }}
                        QProgressBar::chunk {{
                            background-color: rgb({r}, {g}, {b});  /* 动态颜色 */
                        }}
                    """)
                else:
                    raise ValueError("进度值必须在0到100之间。")
            except (ValueError, TypeError) as e:
                print(f"错误：{e}")

        def calculate_gradient_color(value):
            """根据进度值计算红色、黄色和绿色的渐变颜色"""
            if value <= 50:
                return 255, int((value / 50) * 255), 0  # 红色到黄色
            else:
                return int(255 - ((value - 50) / 50) * 255), 255, 0  # 黄色到绿色




    def startDownload(self, url, download_path, custom_filename, identifier):
        # 检查是否已存在同名文件
        final_file = os.path.join(download_path, custom_filename)
        if os.path.exists(final_file):
            # 创建自定义的QMessageBox
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("文件已存在")
            msg_box.setText("该文件已存在，是否覆盖下载？")
            msg_box.setIcon(QMessageBox.Warning)  # 设置图标为警告 
            msg_box.adjustSize()

            # 设置样式
            msg_box.setStyleSheet(f"""
                QMessageBox {{
                    font-family: '{self.custom_font.family()}'; 
                    font-size: {self.fontPointSize}px;  /* 根据动态字体大小调整 */
                    background-color: #ffffff; 
                    color: #333333; 
                    border: 2px solid #2196F3;
                    border-radius: 10px;
                    padding: 10px;  /* 增加内边距 */
                }}
                QMessageBox QPushButton {{
                    font-family: '{self.custom_font.family()}'; 
                    font-size: {self.fontPointSize}px;  /* 动态字体大小 */
                    background-color: #2196F3; 
                    color: white; 
                    border: none; 
                    border-radius: 5px; 
                    padding: 8px; 
                }}
                QMessageBox QPushButton:hover {{
                    background-color: #1976D2;  /* 鼠标悬停时的背景颜色 */
                }}
                QMessageBox QLabel {{
                    font-family: '{self.custom_font.family()}'; 
                    font-size: {self.fontPointSize}px;  /* 动态信息标签字体大小 */
                    margin-left: 5px;  /* 标签的左边距 */
                }}
            """)


            # 设置按钮
            yes_button = msg_box.addButton("确定", QMessageBox.AcceptRole)
            no_button = msg_box.addButton("取消", QMessageBox.RejectRole)

            # 需要设置按钮样式
            yes_button.setStyleSheet(f"font-family: '{self.custom_font.family()}'; font-size: {self.fontPointSize}px; background-color: #2196F3; color: white; border-radius: 5px;")
            yes_button.adjustSize()
            no_button.setStyleSheet(f"font-family: '{self.custom_font.family()}'; font-size: {self.fontPointSize}px; background-color: #f44336; color: white; border-radius: 5px;") 
            no_button.adjustSize()   
            
            # 显示对话框并等待用户响应
            msg_box.exec_()
            
            # 根据用户选择继续或返回
            if msg_box.clickedButton() == yes_button:
                # 尝试删除已存在的文件
                try:
                    os.remove(final_file)
                except Exception as e:
                    self.show_custom_message(self, "警告", f"未能成功删除已存在的文件。\n错误信息: {str(e)}", QMessageBox.Warning)
                    self.download_active = False
                    self.close()  # 关闭对话框
                    return

                self.download_active = True
                self.download_identifier = identifier  # 存储标识符

                # 创建并启动下载线程
                self.start_download_thread(url, download_path, custom_filename, identifier)
                self.show()  # 显示下载对话框

            else:
                self.closeEvent_All()

        else:
            self.download_active = True
            self.download_identifier = identifier  # 存储标识符
            self.start_download_thread(url, download_path, custom_filename, identifier)
            self.show()  # 显示下载对话框

    def start_download_thread(self, url, download_path, custom_filename, identifier):
        self.thread = DownloadWorker(url, download_path, custom_filename, identifier)
        self.thread.progress.connect(self.update_progress)  # 连接进度更新信号
        self.thread.finished.connect(self.download_completed)  # 下载完成连接信号
        self.thread.start()  # 启动线程



    def update_progress(self, downloaded_size, total_size, size_display, time_display, speed_display):
        self.progress_bar.setMaximum(total_size)  # 设置进度条最大值
        self.progress_bar.setValue(downloaded_size)  # 更新进度条

        # 更新信息标签的显示内容
        self.info_label.setText(f"下载进度: {downloaded_size / total_size * 100:.2f}%  |  已下载: {size_display}  |  当前速度: {speed_display}  |  剩余时间: {time_display}")

        # 设置信息标签的样式
        self.info_label.setStyleSheet(f"""
            QLabel {{
                font-family: '{self.custom_font.family()}'; 
                font-size: {self.fontPointSize + 2}px; 
                background-color: rgba(255, 255, 255, 0.8);  
                color: black;  
                border: 2px solid #2196F3;  
                border-radius: 10px; 
                padding: 10px;
                margin: 5px;  /* 添加外边距 */
            }}
        """)

        # 显示信息标签
        self.info_label.show()





    def stop_download(self):
        if self.thread.isRunning():
            self.thread.stop()  # 停止下载
            self.download_active = False
            time.sleep(0.5)  # 等待线程停止
            unfinished_file = os.path.join(self.thread.download_path, self.thread.custom_filename + '.SectionIstool.download')
            if os.path.exists(unfinished_file):
                try:
                    os.remove(unfinished_file)  # 尝试删除文件
                    self.show_custom_message(self, "提示", "下载已停止，未完成的下载文件已成功删除。", QMessageBox.Information)
                except Exception as e:
                    self.show_custom_message(self, "警告", f"下载已停止，但未完成的下载文件删除失败。\n错误信息: {str(e)}", QMessageBox.Warning)
            self.close()  # 关闭对话框
        else:
            self.show_custom_message(self, "警告", "下载已结束, 请勿重复操作。", QMessageBox.Warning)
            

    def download_completed(self, final_file):
        self.show_custom_message(self, "完成", "当前下载任务已完成！", QMessageBox.Information)

        if self.download_identifier:
            self.perform_action_based_on_identifier(self.download_identifier)


    def open_file(self):
        final_file = os.path.join(self.thread.download_path, self.thread.custom_filename)
        if os.path.exists(final_file):
            webbrowser.open(final_file)
            self.close()  # 打开文件后关闭对话框
        else:
            self.show_custom_message(self, "警告", "文件不存在，无法打开。", QMessageBox.Warning)

    def open_folder(self):
        folder_path = self.thread.download_path
        webbrowser.open(folder_path)
        self.close()  # 打开文件夹后关闭对话框

    def closeEvent_All(self):
        self.close()  # 忽略关闭事件，等待下载完成后再关闭
        pass

    def perform_action_based_on_identifier(self, identifier):
        if identifier in ["Software_Download", "School_resources", "Wallpaper_Download", "Awesome_Download", "Aotomatic_installation", "None"]:
            pass

        else:
            self.show_custom_message(self, "警告", f"未知的功能标识符: {identifier}", QMessageBox.Warning)