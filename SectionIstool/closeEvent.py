from PyQt5.QtWidgets import QMessageBox, QApplication
import os
import shutil
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget


# 检测程序是否关闭
def closeEvent(self, event):

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


    self.adjustSize()  # 自适应宽度



    # 创建自定义样式的消息框
    msg_box = QMessageBox()

    # 设置消息框样式
    msg_box.setStyleSheet(f"""
    QMessageBox {{
        background-color: #ffffff;  
        border: 2px solid #2196F3;  
        border-radius: 10px;  
    }}
    QMessageBox QLabel {{
        font-family: {self.custom_font.family()};  
        font-size: {self.fontPointSize + 2}px;  
        color: #333;  
    }}
    QMessageBox QPushButton {{
        font-family: {self.custom_font.family()};  
        background-color: #2196F3;  
        color: #FFFFFF;
        border: none;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: {self.fontPointSize + 2}px;
        margin: 5px;  
    }}
    QMessageBox QPushButton:hover {{
        background-color: #1976D2;  
    }}
    """)

    msg_box.setWindowTitle('确认')
    msg_box.setText('确认退出程序？')

    # 设置标准按钮
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msg_box.setDefaultButton(QMessageBox.No)

    # 修改按钮文本
    yes_button = msg_box.button(QMessageBox.Yes)
    no_button = msg_box.button(QMessageBox.No)

    # 修改按钮内容
    yes_button.setText('确定')  # 修改“是”按钮的文本
    no_button.setText('取消')   # 修改“否”按钮的文本

    # 修改按钮样式
    yes_button.setStyleSheet(f"QPushButton{{font-family: {self.custom_font.family()}; background-color: #2196F3; color: #FFFFFF; border: none; padding: 10px; border-radius: 5px; text-align: center; font-size: {self.fontPointSize + 2}px; margin: 5px; }} QPushButton:hover{{background-color: #1976D2;}}")
    no_button.setStyleSheet(f"QPushButton{{font-family: {self.custom_font.family()}; background-color: #f44336; color: #FFFFFF; border: none; padding: 10px; border-radius: 5px; text-align: center; font-size: {self.fontPointSize + 2}px; margin: 5px; }} QPushButton:hover{{background-color: #E53935;}}")

    # 显示消息框并获取用户响应
    reply = msg_box.exec_()



    if reply == QMessageBox.Yes:
        event.accept()  # 关闭程序
    else:
        event.ignore()  # 取消关闭


    if reply == QMessageBox.Yes:
        try:
            # 定义所有需要删除的文件和文件夹路径
            paths_to_delete = [
                os.path.join('Config', 'encs'),
                os.path.join('Config', 'keys'),
                # os.path.join('Downloads')
            ]
            
            # 遍历路径列表，删除存在的文件或文件夹
            for path in paths_to_delete:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
        except Exception:
            self.show_custom_message(self, "错误", f"删除文件或文件夹时出错\n请手动删除以下文件或文件夹:\n{paths_to_delete}", QMessageBox.Warning)

        # 关闭应用程序
        QApplication.instance().quit()  # 使用 PyQt 的 quit 来关闭应用程序
    else:
        event.ignore()




