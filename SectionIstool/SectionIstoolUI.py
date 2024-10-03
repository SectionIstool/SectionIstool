from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QApplication, QSizePolicy 
import os
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from pathlib import Path
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QFontDatabase


# 定义UI初始化函数
def initUI(self):
    # 获取应用程序的根目录
    app_dir = Path(os.getcwd())

    # 使用os.path.join来构建图标文件的路径
    icon_path = os.path.join(app_dir, 'icon', 'SectionIstool_icon.png')

    # 创建QIcon对象
    app_icon = QIcon(icon_path)

    # 设置应用程序窗口图标
    QApplication.instance().setWindowIcon(app_icon)

    # 设置窗口标题和图标
    self.setWindowTitle('SectionIstool')  # 注意：窗口标题不能为中文
    self.setWindowIcon(QIcon('.\\icon\\SectionIstool_icon.png'))  # 注意：图标文件名不能为中文
    self.setCentralWidget(QWidget())  # 设置窗口中心部件
    self.setUnifiedTitleAndToolBarOnMac(True)  # 统一Mac系统菜单栏和工具栏
    self.setAnimated(True)  # 窗口动画效果
    self.setDockNestingEnabled(True)  # 允许停靠嵌套

    # 根据屏幕尺寸设置窗口大小
    screen = QApplication.desktop().screenGeometry()  # 获取屏幕大小
    screen_geometry = QApplication.desktop().screenGeometry()  # 获取屏幕几何信息
    window_width = int(screen_geometry.width() * 0.625)
    window_height = int(screen_geometry.height() * 0.741)

    self.resize(window_width, window_height)  # 设置新的窗口大小
    self.move(int((screen.width() - self.width()) / 2), int((screen.height() - self.height()) / 2))  # 窗口居中显示

    # self.setFixedSize(self.width(), self.height())  # 设置固定大小

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

    # 设置字体
    font = QFont()
    font.setFamily(self.custom_font.family())  # 使用字体名称
    font.setPointSize(self.fontPointSize)
    self.setFont(font)


    # 设置窗口风格
    self.setStyleSheet(f"""
        QMainWindow, QDockWidget, QListWidget {{
            font-family: '{self.custom_font.family()}';
            background-color: #F0F0F0;   /* 背景色 */
            border-radius: 10px;         /* 圆角 */
            padding: 2px;               /* 内边距 */
            border: 1px solid #CCCCCC;    /* 边框 */
        }}
        QPushButton {{
            font-family: '{self.custom_font.family()}';
            background-color: #2196F3;   /* 新的按钮背景色 */
            color: white;                /* 按钮文字颜色 */
            border: none;                /* 去掉边框 */
            border-radius: 5px;          /* 边框圆角 */
            padding: 10px;          /* 内边距 */
            font-size: {self.fontPointSize}px;             /* 字体大小 */
            font-weight: bold;           /* 粗体 */
            text-align: center;          /* 文字居中 */
        }}
        QPushButton:hover {{
            background-color: #1976D2;   /* 悬停时的背景色 */
        }}
        QPushButton:pressed {{
            background-color: #2196F3;   /* 按下时的背景色 */
        }}
        QLabel, QTextEdit {{
            font-family: '{self.custom_font.family()}';
            color: #333333;               /* 字体颜色 */
            font-size: {self.fontPointSize}px;       /* 字体大小 */
        }}
        QLabel {{
            font-weight: bold;            /* 粗体 */
        }}
        QTextEdit {{
            font-family: '{self.custom_font.family()}';    /* 字体 */
            font-size: {self.fontPointSize}px;          /* 字体大小 */
            border: 1px solid #CCCCCC;    /* 边框 */
            border-radius: 10px;          /* 圆角 */
            padding: 3px;                 /* 内边距 */
            background-color: #FFFFFF;     /* 背景色 */
        }}
        QMessageBox QPushButton#Yes {{
            font-family: '{self.custom_font.family()}';
            background-color: #2196F3;   /* 蓝色背景色 */
            color: white;                /* 按钮文字颜色 */
            border: none;                /* 去掉边框 */
            border-radius: 5px;          /* 边框圆角 */
            padding: 10px;          /* 内边距 */
            font-size: {self.fontPointSize}px;      /* 字体大小 */
            font-weight: bold;           /* 粗体 */
            text-align: center;          /* 文字居中 */
        }}
        QMessageBox QPushButton#Yes:hover {{
            background-color: #1976D2;   /* 悬停时的背景色 */
        }}
        QMessageBox QPushButton#Yes:pressed {{
            background-color: #2196F3;   /* 按下时的背景色 */
        }}
        QMessageBox QPushButton#No {{
            font-family: '{self.custom_font.family()}';
            background-color: #f44336;   /* 红色背景色 */
            color: white;                /* 按钮文字颜色 */
            border: none;                /* 去掉边框 */
            border-radius: 5px;          /* 边框圆角 */
            padding: 10px;          /* 内边距 */
            font-size: {self.fontPointSize}px;    /* 字体大小 */
            font-weight: bold;           /* 粗体 */
            text-align: center;          /* 文字居中 */
        }}
        QMessageBox QPushButton#No:hover {{
            background-color: #FFCDD2;   /* 悬停时的背景色 */
        }}
        QMessageBox QPushButton#No:pressed {{
            background-color: #f44336;   /* 按下时的背景色 */
        }}
    """)


    # 创建左侧导航栏
    self.dock = QDockWidget('SectionIstool', self)
    # 设置导航栏标题背景颜色
    self.dock.setTitleBarWidget(QWidget(self.dock))
    self.dock.titleBarWidget().setStyleSheet("""
        background-color: #2196F3;   /* 标题栏背景色 */
        border-top-left-radius: 12px;  /* 左上角圆角 */
        border-top-right-radius: 12px;  /* 右上角圆角 */
        border-bottom: 1px solid #CCCCCC;  /* 底部边框 */
    """)
    # 设置导航栏标题文本居中
    self.dock.setTitleBarWidget(QWidget(self.dock))
    self.dock.setWidget(self.createNavigationList())  # 设置导航栏内容
    self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)  # 将导航栏添加到左侧边栏
    self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)  # 禁用停靠按钮
    self.dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)  # 允许停靠到左侧和右侧边栏
    self.dock.setFloating(False)  # 禁止拖动停靠栏

    # 设置停靠栏大小策略为自适应
    self.dock.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


    # 设置停靠栏样式
    self.dock.setStyleSheet(f"""
        QDockWidget {{
            font-family: "SimHei";
            background-color: #FAFAFA;      /* 更亮的背景色 */
            border: 1px solid #CCCCCC;      /* 边框 */
            border-radius: 12px;            /* 圆角 */
            padding: 4px;                   /* 内边距 */
        }}
        QListWidget {{
            font-family: '{self.custom_font.family()}';    /* 字体 */
            font-size: {self.fontPointSize + 2}px;    /* 字体大小 */
            border: none;                   /* 去掉边框 */
            background-color: #FFFFFF;      /* 背景色 */
            border-radius: 8px;             /* 圆角 */
            padding: 0px;                   /* 去掉外边距 */
            outline: none;                  /* 去掉选中时的轮廓 */
        }}
        QListWidget::item {{
            padding: 3px;                  /* 增加内边距，提升可点击区域 */
            margin: 2px;                  /* 增加项目间的垂直间隔 */
        }}
        QListWidget::item:selected {{
            background-color: #2196F3;      /* 调整选中项背景色 */
            color: #FFFFFF;                  /* 选中项字体颜色 */
            font-weight: bold;               /* 选中项字体加粗 */
            border-radius: 8px;             /* 圆角 */
        }}
        QListWidget::item:hover {{
            background-color: #1976D2;      /* 悬停背景色 */
            border-radius: 8px;             /* 圆角 */
        }}
    """)


    self.dock.setFont(font)  # 设置字体
    self.dock.setContextMenuPolicy(Qt.NoContextMenu)  # 禁止右键菜单


    # 创建中央窗口并设置布局
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    self.layout = QVBoxLayout(self.central_widget)
    self.layout.setContentsMargins(20, 20, 20, 20)  # 设置布局的边距

    # 正确调用 showHomeContent 并使用其返回值
    self.current_content = self.showHomeContent()

    # 创建菜单
    self.createMenus()

    # 隐藏状态栏
    self.statusBar().hide()