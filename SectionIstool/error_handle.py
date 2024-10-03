from PyQt5.QtWidgets import QMessageBox, QApplication
import os
import shutil


# 程序报错
def error_handle(self):
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
        # 错误处理机制，错误信息
        self.show_custom_message(self, "错误", f"删除文件或文件夹时出错\n请手动删除以下文件或文件夹:\n{paths_to_delete}", QMessageBox.Warning)

    # 关闭应用程序
    QApplication.instance().quit()  # 使用 PyQt 的 quit 来关闭应用程序
