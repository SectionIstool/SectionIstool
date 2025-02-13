import os
import json
from qfluentwidgets import * # type: ignore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTextBrowser
from PyQt5.QtGui import QFont, QTextOption, QIcon, QDesktopServices, QKeyEvent, QCloseEvent
from loguru import logger
import markdown  # type: ignore


# 配置日志记录
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger.add(
    os.path.join(log_dir, f"SectionIstool_{{time:YYYY-MM-DD}}.log"),
    rotation="1 MB",
    encoding="utf-8",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss:SSS} | {level} | {name}:{function}:{line} - {message}"
)


# 读取配置文件
def read_json(json_path):  # type: ignore
    # 确认是否存在设置目录
    if not os.path.exists('./app/Settings'):
        os.makedirs('./app/Settings')
    if os.path.exists(json_path):  # type: ignore
        try:
            with open(json_path, 'r', encoding='utf-8') as file:  # type: ignore
                return json.load(file)
        except json.JSONDecodeError:
            # 如果文件内容不是有效的 JSON 格式，返回空字典
            return {}  # type: ignore
    return {}  # type: ignore


# 读取指定软件配置的某个值
def read_setting(json_path, software_name, key):  # type: ignore
    try:
        with open(json_path, 'r', encoding='utf-8') as file:  # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 'Unknown'
    
    # 检查指定软件的配置是否存在
    if software_name in json_file and key in json_file[software_name]:
        return json_file[software_name][key]
    
    return 'Unknown'


# 自定义 QTextBrowser 以处理点击超链接事件
class CustomTextBrowser(QTextBrowser):
    def __init__(self, parent):  # type: ignore
        super().__init__(parent)
        self.parent_window = parent

    def anchorClicked(self, url) -> None:  # type: ignore
        super().anchorClicked(url)  # type: ignore
        # 关闭窗口
        self.parent_window.setEnabled(True)  # 在关闭前恢复父窗口的启用状态 # type: ignore
        self.parent_window.close()  # type: ignore
        # 打开外部链接
        QDesktopServices.openUrl(url)  # type: ignore

    def keyPressEvent(self, event: QKeyEvent) -> None:  # type: ignore
        if event.key() == Qt.Key.Key_Escape:
            self.parent_window.setEnabled(True)  # 在关闭前恢复父窗口的启用状态 # type: ignore
            self.parent_window.close()  # type: ignore
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:  # type: ignore
        self.parent_window.setEnabled(True)  # 在关闭前恢复父窗口的启用状态 # type: ignore
        super().closeEvent(event)


# 显示更新日志窗口的函数
def show_readme_dialog(parent, software_name_download_second) -> None:  # type: ignore
    download_version_second = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version')  # type: ignore
    try:
        logger.info("显示更新日志")
        readme_window = QFrame()
        readme_window.setWindowTitle(f'{software_name_download_second} {download_version_second} 更新日志')
        readme_window.setWindowIcon(QIcon('./app/resource/icon/SectionIstool_icon.png'))
        readme_window.resize(800, 600)
        readme_window.setFixedSize(800, 600)
        # 设置窗口置顶
        readme_window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        text_edit = CustomTextBrowser(readme_window)
        text_edit.setReadOnly(True)
        text_edit.setAcceptRichText(True)
        text_edit.setOpenExternalLinks(True)  # 允许打开外部链接

        font = QFont()
        font.setPointSize(12)
        text_edit.setFont(font)

        download_version = read_setting('./app/Settings/Settings.json', software_name_download_second, 'download_version')  # type: ignore

        if download_version == 'Unknown':
            logger.error(f"无法读取 {software_name_download_second} 的版本号")
            return

        releases_data = read_json(f'./app/resource/releases/{software_name_download_second}_releases.json')  # type: ignore
        if isinstance(releases_data, list):
            for item in releases_data:  # type: ignore
                if item.get('tag_name') == download_version:  # type: ignore
                    content = item.get('body', 'Unknown')  # type: ignore
                    logger.info(f'当前选择的版本为 {download_version} 的 {software_name_download_second} 更新日志')
                    break
            else:
                content = 'Unknown'
        else:
            content = 'Unknown'

        # 使用 misaka 将内容转换为 HTML
        markdown = markdown.Markdown()  # type: ignore
        html_content = markdown(content)  # type: ignore

        text_edit.setHtml(html_content)  # 使用 setHtml 显示 HTML 内容 # type: ignore

        doc = text_edit.document()
        if doc:
            option = QTextOption()
            option.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置文本居中显示
            option.setWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
            doc.setDefaultTextOption(option)

        layout = QVBoxLayout(readme_window)
        layout.addWidget(text_edit)

        confirm_button = PrimaryPushButton('看完馁 ( ￣▽￣) ', readme_window)
        confirm_button.clicked.connect(lambda: close_readme_dialog(readme_window))  # type: ignore

        layout.addWidget(confirm_button)
        readme_window.setLayout(layout)

        readme_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)  # 修改为 True，以便在窗口关闭后自动删除
        readme_window.show()

    except Exception as e:
        logger.error(f"显示更新日志时发生错误: {e}")


# 关闭更新日志窗口的函数
def close_readme_dialog(readme_window):  # type: ignore
    if readme_window:
        readme_window.close()  # type: ignore


class ParentWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.button = PrimaryPushButton('显示更新日志', self)
        self.button.clicked.connect(lambda: show_readme_dialog(self, 'ExampleSoftware'))  # type: ignore
