from qfluentwidgets import SubtitleLabel # type: ignore
from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont  # 添加 QFont 导入

class Home_Widget(QFrame):
    def __init__(self, parent: QFrame = None): # type: ignore
        super().__init__(parent=parent)

        # 创建垂直布局
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # 图标设置
        self.icon = QLabel(self)
        pixmap = self.load_pixmap('./icon/SectionIstool_icon.png')
        self.icon.setPixmap(pixmap)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon)

        # 标题
        self.title = SubtitleLabel('SectionIstool 软件', self)
        self.title.setFont(QFont('Arial', 22, QFont.Weight.Bold))  # 使用默认字体 Arial
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        # 介绍文本
        self.introduction = QLabel('SectionIstool 是一款便于用户进行下载的软件，主打一个便利吧?', self)
        self.introduction.setFont(QFont('Arial', 16))  # 使用默认字体 Arial
        self.introduction.setStyleSheet("color: black;")
        self.introduction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.introduction)

        # 特点标题
        self.features_label = SubtitleLabel('特点', self)
        self.features_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))  # 使用默认字体 Arial
        self.features_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.features_label)

        # 特点内容
        self.features = QLabel('1. 基于Python的开源软件。\n'
                               '2. 界面简洁，操作简单，使用起来不费吹灰之力。\n'
                               '3. 开源免费，无需担心版权问题。', self)
        self.features.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 内容居中
        self.features.setFont(QFont('Arial', 16))  # 使用默认字体 Arial
        self.features.setStyleSheet("color: black;")
        layout.addWidget(self.features)

        # 贡献标题
        self.contribution_label = SubtitleLabel('贡献', self)
        self.contribution_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))  # 使用默认字体 Arial
        self.contribution_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.contribution_label)

        # 贡献内容
        self.contribution = QLabel('1. 欢迎各位开发者参与软件的开发。\n'
                                   '2. 欢迎各位用户参与软件的测试和反馈。\n'
                                   '3. 欢迎各位开发者参与软件的优化和修复。', self)
        self.contribution.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 内容居中
        self.contribution.setFont(QFont('Arial', 16))  # 使用默认字体 Arial
        self.contribution.setStyleSheet("color: black;")
        layout.addWidget(self.contribution)

        # 添加额外的间隔
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setObjectName('Home-Interface')

    def load_pixmap(self, path: str) -> QPixmap:
        pixmap = QPixmap(path)
        if pixmap.isNull():
            raise FileNotFoundError(f"图标文件未找到或路径错误: {path}")
        return pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
