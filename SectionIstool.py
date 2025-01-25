from qfluentwidgets import (NavigationItemPosition, FluentWindow, FluentIcon as fIcon, SubtitleLabel, setFont, SplashScreen)
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, QEventLoop, QTimer 


from Home_Widget import Home_Widget



class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class Window(FluentWindow):
    def __init__(self):
        super().__init__()

        # 1. 创建启动页面
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))

        # 2. 在创建其他子页面前先显示主界面
        self.show()

        # 3. 创建子界面
        self.createSubInterface()

        # 4. 隐藏启动页面
        self.splashScreen.finish()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Home_Widget(self)

        self.sectionistool_software = Widget('SectionIstool 旗下软件', self)
        self.ClassIsland_software = Widget('ClassIsland 软件', self)
        self.Class_Widgets_software = Widget('Class Widgets 软件', self)
        self.Sticky_attention_software = Widget('Sticky attention 软件', self)
        self.ElectronClassSchedule_software = Widget('ElectronClassSchedule 软件', self)
        self.Ink_Canvas_software = Widget('Ink Canvas 软件', self)
        self.Ink_Canvas_Artistry_software = Widget('Ink Canvas Artistry 软件', self)
        self.Ink_Canvas_Reborn_software = Widget('Ink Canvas Reborn 软件', self)
        self.Inkeys_software = Widget('Inkeys 软件', self)
        self.Inkways_Classic_software = Widget('Inkways Classic 软件', self)
        self.InkCanvasForClass_software = Widget('InkCanvasForClass 软件', self)
        self.ZongziTEK_software = Widget('ZongziTEK 软件', self)
        self.Ris_ClassTool_software = Widget('Ris_ClassTool 软件', self)
        self.Exam_dashboard_Next_software = Widget('Exam dashboard Next 软件', self)

        self.settingInterface = Widget('Setting Interface', self)
        self.aboutInterface = Widget('About Interface', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, fIcon.HOME, '主页', NavigationItemPosition.TOP)
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.sectionistool_software, QIcon('./icon/SectionIstool_icon.png'), 'SectionIstool 旗下软件', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.ClassIsland_software, QIcon('./icon/ClassIsland_software.svg'), 'ClassIsland', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Class_Widgets_software, QIcon('./icon/Class_Widgets_software.png'), 'Class Widgets', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Sticky_attention_software, QIcon('./icon/Sticky_attention_software.png'), 'Sticky attention', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.ElectronClassSchedule_software, QIcon('./icon/ElectronClassSchedule_software.png'), 'ElectronClassSchedule', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Ink_Canvas_software, QIcon('./icon/Ink_Canvas_software.png'), 'Ink Canvas', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Ink_Canvas_Artistry_software, QIcon('./icon/Ink_Canvas_Artistry_software.png'), 'Ink Canvas Artistry', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Ink_Canvas_Reborn_software, QIcon('./icon/Ink_Canvas_Reborn_software.png'), 'Ink Canvas Reborn', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Inkeys_software, QIcon('./icon/Inkeys_software.png'), 'Inkeys', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Inkways_Classic_software, QIcon('./icon/Inkways_Classic_software.png'), 'Inkways Classic', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.InkCanvasForClass_software, QIcon('./icon/InkCanvasForClass_software.png'), 'InkCanvasForClass', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.ZongziTEK_software, QIcon('./icon/ZongziTEK_software.png'), 'ZongziTEK', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Ris_ClassTool_software, QIcon('./icon/Ris_ClassTool_software.png'), 'Ris ClassTool', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.Exam_dashboard_Next_software, QIcon('./icon/Exam_dashboard_Next_software.svg'), '考试看板 Next', NavigationItemPosition.SCROLL)

        self.addSubInterface(self.settingInterface, fIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, fIcon.INFO, '关于', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1200, 800)
        self.setWindowIcon(QIcon('./icon/SectionIstool_icon.png'))
        self.setWindowTitle('SectionIstool')

        # 获取主屏幕
        screen = QApplication.primaryScreen()
        # 获取屏幕的可用几何信息
        desktop = screen.availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

if __name__ == '__main__':
    app = QApplication([])
    sectionistool = Window()
    sectionistool.show()
    app.exec()