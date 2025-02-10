from qfluentwidgets import (NavigationItemPosition, FluentWindow, FluentIcon as fIcon, SubtitleLabel, setFont, SplashScreen) # type: ignore
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QEventLoop, QTimer 

import json
import os
from loguru import logger

# 导入子页面
from Home_Widget import Home_Widget

from SectionIstool_Widget import sectionistool_Widget
from ClassIsland_Widget import ClassIsland_Widget
from Class_Widgets_Widget import Class_Widgets_Widget
from ZongziTEK_Widget import ZongziTEK_Widget
from ElectronClassSchedule_Widget import ElectronClassSchedule_Widget

from Sticky_attention_Widget import Sticky_attention_Widget
from ExamAware_Widget import ExamAware_Widget

from Inkeys_Widget import Inkeys_Widget
from Ink_Canvas_Widget import Ink_Canvas_Widget
from Ris_ClassTool_Widget import Ris_ClassTool_Widget

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
    json_path_check(json_path)  # type: ignore
    if os.path.exists(json_path): # type: ignore
        try:
            with open(json_path, 'r', encoding='utf-8') as file: # type: ignore
                return json.load(file)
        except json.JSONDecodeError:
            # 如果文件内容不是有效的 JSON 格式，返回空字典
            return {} # type: ignore
    return {} # type: ignore
#读取以及写入配置文件
def write_json(json_path, field_name, default_value):  # type: ignore
    json_path_check(json_path)  # type: ignore
    # 读取配置文件
    if not os.path.exists(json_path):  # type: ignore
        with open(json_path, 'w', encoding='utf-8') as file:  # type: ignore
            json.dump({field_name: default_value}, file, ensure_ascii=False, indent=4)  # type: ignore
    try:
        with open(json_path, 'r', encoding='utf-8') as file:  # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        json_file = {}
    json_file[field_name] = default_value
    json_file.update(json_file)  # type: ignore
    with open(json_path, 'w', encoding='utf-8') as file:  # type: ignore
        json.dump(json_file, file, ensure_ascii=False, indent=4)

def json_path_check(json_path): # type: ignore
    # 确保配置文件存在
    if json_path is not None and not os.path.exists(json_path): # type: ignore
        os.makedirs(json_path) # type: ignore

# 写入默认数据
write_json('./Settings/Settings.json', 'software_author', 'lzy98276')
write_json('./Settings/Settings.json', 'software_name', 'SectionIstool')
write_json('./Settings/Settings.json', 'version', '1.3.0.0')
write_json('./Settings/Settings.json', 'Start_detection', 'True')


class Widget(QFrame):

    def __init__(self, text: str, parent=None): # type: ignore
        super().__init__(parent=parent) # type: ignore
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class Window(FluentWindow):
    def __init__(self):
        super().__init__() # type: ignore
        self.resize(1200, 800)
        self.setWindowTitle('SectionIstool')
        self.setWindowIcon(QIcon('./icon/SectionIstool_icon.png'))
        # 获取主屏幕
        screen = QApplication.primaryScreen()
        # 获取屏幕的可用几何信息
        desktop = screen.availableGeometry() # type: ignore
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(256, 256))
        self.show()
        self.createSubInterface()
        self.splashScreen.finish()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(500, loop.quit) # type: ignore
        loop.exec()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Home_Widget(self) # type: ignore

        self.ClassIsland_software = ClassIsland_Widget(self) # type: ignore
        self.ClassIsland_software.setObjectName("ClassIsland_software")  # 设置对象名称

        self.Class_Widgets_software = Class_Widgets_Widget(self) # type: ignore
        self.Class_Widgets_software.setObjectName("Class_Widgets_software")  # 设置对象名称

        self.ZongziTEK_software = ZongziTEK_Widget(self) # type: ignore
        self.ZongziTEK_software.setObjectName("ZongziTEK_software")  # 设置对象名称

        self.ElectronClassSchedule_software = ElectronClassSchedule_Widget(self) # type: ignore
        self.ElectronClassSchedule_software.setObjectName("ElectronClassSchedule_software")  # 设置对象名称

        self.Sticky_attention_software = Sticky_attention_Widget(self) # type: ignore
        self.Sticky_attention_software.setObjectName("Sticky_attention_software")  # 设置对象名称

        self.dsz_exam_showboard = ExamAware_Widget(self) # type: ignore
        self.dsz_exam_showboard.setObjectName("dsz_exam_showboard")  # 设置对象名称

        # self.Exam_dashboard_Next_software = Exam_dashboard_Next_Widget(self) # type: ignore
        # self.Exam_dashboard_Next_software.setObjectName("Exam_dashboard_Next_software")  # 设置对象名称

        # self.InkCanvasForClass_software = InkCanvasForClass_Widget(self) # type: ignore
        # self.InkCanvasForClass_software.setObjectName("InkCanvasForClass_software")  # 设置对象名称

        self.Inkeys_software = Inkeys_Widget(self) # type: ignore
        self.Inkeys_software.setObjectName("Inkeys_software")  # 设置对象名称

        # self.Ink_Canvas_Artistry_software = Ink_Canvas_Artistry_Widget(self) # type: ignore
        # self.Ink_Canvas_Artistry_software.setObjectName("Ink_Canvas_Artistry_software")  # 设置对象名称

        self.Ink_Canvas_software = Ink_Canvas_Widget(self) # type: ignore
        self.Ink_Canvas_software.setObjectName("Ink_Canvas_software")  # 设置对象名称
        
        # self.Ink_Canvas_Reborn_software = Ink_Canvas_Reborn_Widget(self) # type: ignore
        # self.Ink_Canvas_Reborn_software.setObjectName("Ink_Canvas_Reborn_software")  # 设置对象名称


        # self.Inkways_Classic_software = Inkways_Classic_Widget(self) # type: ignore
        # self.Inkways_Classic_software.setObjectName("Inkways_Classic_software")

        self.Ris_ClassTool_software = Ris_ClassTool_Widget(self) # type: ignore
        self.Ris_ClassTool_software.setObjectName("Ris_ClassTool_software")  # 设置对象名称

        self.settingInterface = Widget('还没做...', self) # type: ignore
        self.aboutInterface = sectionistool_Widget(self) # type: ignore
        self.aboutInterface.setObjectName("aboutInterface")  # 设置对象名称

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, fIcon.HOME, '主页', NavigationItemPosition.TOP) # type: ignore
        
        self.navigationInterface.addSeparator()

        self.addSubInterface(self.ClassIsland_software, QIcon('./icon/ClassIsland_software.svg'), 'ClassIsland', NavigationItemPosition.SCROLL) # type: ignore
        self.addSubInterface(self.Class_Widgets_software, QIcon('./icon/Class_Widgets_software.png'), 'Class Widgets', NavigationItemPosition.SCROLL) # type: ignore
        self.addSubInterface(self.ZongziTEK_software, QIcon('./icon/ZongziTEK_software.png'), 'ZongziTEK', NavigationItemPosition.SCROLL) # type: ignore
        self.addSubInterface(self.ElectronClassSchedule_software, QIcon('./icon/ElectronClassSchedule_software.png'), 'ElectronClassSchedule', NavigationItemPosition.SCROLL) # type: ignore
        
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)

        self.addSubInterface(self.Sticky_attention_software, QIcon('./icon/Sticky_attention_software.png'), '作业看板 Sticky attention', NavigationItemPosition.SCROLL) # type: ignore
        self.addSubInterface(self.dsz_exam_showboard, QIcon('./icon/dsz_exam_showboard.png'), '考试看板 ExamAware', NavigationItemPosition.SCROLL) # type: ignore
        # self.addSubInterface(self.Exam_dashboard_Next_software, QIcon('./icon/Exam_dashboard_Next_software.svg'), '考试看板 Next', NavigationItemPosition.SCROLL) # type: ignore
        
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)
        
        # self.addSubInterface(self.InkCanvasForClass_software, QIcon('./icon/InkCanvasForClass_software.png'), 'InkCanvasForClass', NavigationItemPosition.SCROLL) # type: ignore
        self.addSubInterface(self.Inkeys_software, QIcon('./icon/Inkeys_software.png'), '智绘教 Inkeys', NavigationItemPosition.SCROLL) # type: ignore
        # self.addSubInterface(self.Ink_Canvas_Artistry_software, QIcon('./icon/Ink_Canvas_Artistry_software.png'), 'Ink Canvas Artistry', NavigationItemPosition.SCROLL) # type: ignore
        self.addSubInterface(self.Ink_Canvas_software, QIcon('./icon/Ink_Canvas_software.png'), 'Ink Canvas', NavigationItemPosition.SCROLL) # type: ignore
        # self.addSubInterface(self.Ink_Canvas_Reborn_software, QIcon('./icon/Ink_Canvas_Reborn_software.png'), 'Ink Canvas Reborn', NavigationItemPosition.SCROLL) # type: ignore
        # self.addSubInterface(self.Inkways_Classic_software, QIcon('./icon/Inkways_Classic_software.png'), 'Inkways Classic', NavigationItemPosition.SCROLL) # type: ignore
        
        self.navigationInterface.addSeparator(NavigationItemPosition.SCROLL)
        
        self.addSubInterface(self.Ris_ClassTool_software, QIcon('./icon/Ris_ClassTool_software.png'), 'Ris ClassTool', NavigationItemPosition.SCROLL) # type: ignore

        self.navigationInterface.addSeparator(NavigationItemPosition.BOTTOM)

        self.addSubInterface(self.settingInterface, fIcon.SETTING, '设置', NavigationItemPosition.BOTTOM) # type: ignore
        self.addSubInterface(self.aboutInterface, fIcon.INFO, '关于', NavigationItemPosition.BOTTOM) # type: ignore

    def initWindow(self):
        self.resize(1200, 800)
        self.setWindowIcon(QIcon('./icon/SectionIstool_icon.png'))
        self.setWindowTitle('SectionIstool')

        # 获取主屏幕
        screen = QApplication.primaryScreen()
        # 获取屏幕的可用几何信息
        desktop = screen.availableGeometry() # type: ignore
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

if __name__ == '__main__':
    app = QApplication([])
    sectionistool = Window()
    sectionistool.show()
    app.exec()