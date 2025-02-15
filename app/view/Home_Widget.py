from qfluentwidgets import * # type: ignore
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QSpacerItem, QSizePolicy, QScroller, QScrollArea, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

from ..common.config import load_custom_font

class Home_Widget(QFrame):
    def __init__(self, parent: QFrame = None): # type: ignore
        super().__init__(parent=parent)

        # 创建一个 QWidget 作为 QScrollArea 的内容小部件
        content_widget = QWidget(self)
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)  # 增加组件间距
        layout.setContentsMargins(30, 30, 30, 30)  # 增加边距

        # 创建一个 QScrollArea 并设置内容小部件
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        # 设置滚动条样式
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                border: none;
                background-color: transparent;
            }
            /* 垂直滚动条整体 */
            QScrollBar:vertical {
                background-color: #E5DDF8;   /* 背景透明 */
                width: 8px;                    /* 宽度 */
                margin: 0px;                   /* 外边距 */
            }
            /* 垂直滚动条的滑块 */
            QScrollBar::handle:vertical {
                background-color: rgba(0, 0, 0, 0.3);    /* 半透明滑块 */
                border-radius: 4px;                      /* 圆角 */
                min-height: 20px;                        /* 最小高度 */
            }
            /* 鼠标悬停在滑块上 */
            QScrollBar::handle:vertical:hover {
                background-color: rgba(0, 0, 0, 0.5);
            }
            /* 滚动条的上下按钮和顶部、底部区域 */
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                height: 0px;
            }
        
            /* 水平滚动条整体 */
            QScrollBar:horizontal {
                background-color: #E5DDF8;   /* 背景透明 */
                height: 8px;
                margin: 0px;
            }
            /* 水平滚动条的滑块 */
            QScrollBar::handle:horizontal {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 4px;
                min-width: 20px;
            }
            /* 鼠标悬停在滑块上 */
            QScrollBar::handle:horizontal:hover {
                background-color: rgba(0, 0, 0, 0.5);
            }
            /* 滚动条的左右按钮和左侧、右侧区域 */
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal,
            QScrollBar::left-arrow:horizontal,
            QScrollBar::right-arrow:horizontal {
                width: 0px;
            }
        """)
        # 启用触屏滚动
        QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture) # type: ignore

        # 将 QScrollArea 添加到主布局中
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # 图标设置
        self.icon = QLabel(self)
        pixmap = self.load_pixmap('./app/resource/icon/SectionIstool_icon.png')
        self.icon.setPixmap(pixmap)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon)

        # 添加分隔线
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine) # type: ignore
        separator1.setFrameShadow(QFrame.Sunken) # type: ignore
        layout.addWidget(separator1)

        # 标题
        self.title = SubtitleLabel('SectionIstool 软件', self)
        self.title.setFont(QFont(load_custom_font(), 24, QFont.Weight.Bold))  # 使用自定义字体
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        # 介绍文本
        self.introduction = SubtitleLabel('SectionIstool 是一款便于用户进行下载的软件，主打一个便利吧?', self)
        self.introduction.setFont(QFont(load_custom_font(), 18))  # 使用自定义字体
        self.introduction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.introduction)

        # 添加分隔线
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine) # type: ignore
        separator2.setFrameShadow(QFrame.Sunken) # type: ignore
        layout.addWidget(separator2)

        # 特点标题
        self.features_label = SubtitleLabel('特点', self)
        self.features_label.setFont(QFont(load_custom_font(), 22, QFont.Weight.Bold))  # 使用自定义字体
        self.features_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.features_label)

        # 特点内容
        self.features = SubtitleLabel('1. 基于Python的开源软件。\n'
                               '2. 界面简洁，操作简单，使用起来不费吹灰之力。\n'
                               '3. 开源免费，无需担心版权问题。', self)
        self.features.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 内容居中
        self.features.setFont(QFont(load_custom_font(), 18))  # 使用自定义字体
        layout.addWidget(self.features)

        # 添加分隔线
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine) # type: ignore
        separator3.setFrameShadow(QFrame.Sunken) # type: ignore
        layout.addWidget(separator3)

        # 贡献标题
        self.contribution_label = SubtitleLabel('贡献', self)
        self.contribution_label.setFont(QFont(load_custom_font(), 22, QFont.Weight.Bold))  # 使用自定义字体
        self.contribution_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.contribution_label)

        # 贡献内容
        self.contribution = SubtitleLabel('1. 欢迎各位开发者参与软件的开发。\n'
                                   '2. 欢迎各位用户参与软件的测试和反馈。\n'
                                   '3. 欢迎各位开发者参与软件的优化和修复。', self)
        self.contribution.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 内容居中
        self.contribution.setFont(QFont(load_custom_font(), 18))  # 使用自定义字体
        layout.addWidget(self.contribution)

        # 添加额外的间隔
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setObjectName('Home-Interface')

    def load_pixmap(self, path: str) -> QPixmap:
        pixmap = QPixmap(path)
        if pixmap.isNull():
            raise FileNotFoundError(f"图标文件未找到或路径错误: {path}")
        return pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
