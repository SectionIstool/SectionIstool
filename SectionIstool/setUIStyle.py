<<<<<<< HEAD
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

    font = QFont()
    font.setFamily(self.custom_font.family())  # 使用字体名称
    font.setPointSize(self.fontPointSize)
    self.setFont(font)

    # 设置窗口
    self.height_window = 0.741
    self.width_window = 0.625
    self.setfixed = None

    # 根据屏幕尺寸设置窗口大小
    screen = QApplication.desktop().screenGeometry()  # 获取屏幕大小
    screen_geometry = QApplication.desktop().screenGeometry()  # 获取屏幕几何信息

    # 用来存储计算后的窗口高度和宽度
    window_height = None
    window_width = None

    # 检测高的值
    if isinstance(self.height_window, (int, float)) and self.height_window >= 0:
        window_height = int(screen_geometry.height() * self.height_window)

    # 检测宽的值
    if isinstance(self.width_window, (int, float)) and self.width_window >= 0:
        window_width = int(screen_geometry.width() * self.width_window)

    # 如果高度和宽度都有值，直接设置高度和宽度
    if window_height is not None and window_width is not None:
        self.resize(window_width, window_height)  # 设置宽度和高度
    # 如果只有高度有值，设置高度
    elif window_height is not None:
        self.setFixedHeight(window_height)
    # 如果只有宽度有值，设置宽度
    elif window_width is not None:
        self.resize(window_width, self.height())  # 仅设置宽度，保持高度不变
    else:
        self.setfixed = None  # 高度和宽度都没有值，则固定窗口大小

    # 居中显示窗口
    self.move(int((screen.width() - self.width()) / 2), int((screen.height() - self.height()) / 2))  # 窗口居中显示

    # 根据设置决定是否固定大小
    if self.setfixed is True:
        self.setFixedSize(self.width(), self.height())  # 设置固定大小
    else:
=======
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

    font = QFont()
    font.setFamily(self.custom_font.family())  # 使用字体名称
    font.setPointSize(self.fontPointSize)
    self.setFont(font)

    # 设置窗口
    self.height_window = 0.741
    self.width_window = 0.625
    self.setfixed = None

    # 根据屏幕尺寸设置窗口大小
    screen = QApplication.desktop().screenGeometry()  # 获取屏幕大小
    screen_geometry = QApplication.desktop().screenGeometry()  # 获取屏幕几何信息

    # 用来存储计算后的窗口高度和宽度
    window_height = None
    window_width = None

    # 检测高的值
    if isinstance(self.height_window, (int, float)) and self.height_window >= 0:
        window_height = int(screen_geometry.height() * self.height_window)

    # 检测宽的值
    if isinstance(self.width_window, (int, float)) and self.width_window >= 0:
        window_width = int(screen_geometry.width() * self.width_window)

    # 如果高度和宽度都有值，直接设置高度和宽度
    if window_height is not None and window_width is not None:
        self.resize(window_width, window_height)  # 设置宽度和高度
    # 如果只有高度有值，设置高度
    elif window_height is not None:
        self.setFixedHeight(window_height)
    # 如果只有宽度有值，设置宽度
    elif window_width is not None:
        self.resize(window_width, self.height())  # 仅设置宽度，保持高度不变
    else:
        self.setfixed = None  # 高度和宽度都没有值，则固定窗口大小

    # 居中显示窗口
    self.move(int((screen.width() - self.width()) / 2), int((screen.height() - self.height()) / 2))  # 窗口居中显示

    # 根据设置决定是否固定大小
    if self.setfixed is True:
        self.setFixedSize(self.width(), self.height())  # 设置固定大小
    else:
>>>>>>> 4fa2a7888d33a4299e04b4d0deacd959883e7656
        self.adjustSize()  # 自适应宽度