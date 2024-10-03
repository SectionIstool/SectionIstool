from PyQt5.QtWidgets import QMenu, QAction


# 导入版本信息
from config import version_info
# 在 createMenus 函数中
current_version = version_info()


# 创建菜单
def createMenus(self):
    # 创建文件菜单，并显示当前版本
    releases = QMenu(f'当前版本: {current_version}', self)
    # 再文件菜单下添加检查更新的选项
    check_update_action = QAction('检查更新', self)
    # 点击选项时
    check_update_action.triggered.connect(lambda: self.update_version())
    releases.addAction(check_update_action)
    self.menuBar().addMenu(releases)