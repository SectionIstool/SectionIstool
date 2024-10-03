from PyQt5.QtWidgets import QMessageBox

def show_custom_message(self, title, message, icon):
    self.adjustSize() 

    """自定义消息框，用于显示提示信息"""
    msg_box = QMessageBox(self)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    msg_box.adjustSize() 

    # 设置消息框样式
    msg_box.setStyleSheet(f"""
        QMessageBox {{
            font-family: '{self.custom_font.family()}'; 
            font-size: {self.fontPointSize + 2}px; 
            background-color: #ffffff; 
            color: #333; 
            border: 2px solid #2196F3;
            border-radius: 10px;
        }}
        QMessageBox QPushButton {{
            font-family: '{self.custom_font.family()}'; 
            font-size: {self.fontPointSize + 2}px; 
            background-color: #2196F3; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            padding: 8px; 
        }}
        QMessageBox QPushButton:hover {{
            background-color: #1976D2;  /* 鼠标悬停时的背景颜色 */
        }}
    """)

    ok_button = msg_box.addButton("确定", QMessageBox.AcceptRole)
    ok_button.setStyleSheet(f"font-family: '{self.custom_font.family()}'; font-size: {self.fontPointSize + 2}px; background-color: #2196F3; color: white; border-radius: 5px;")
    
    msg_box.exec_()  # 显示消息框