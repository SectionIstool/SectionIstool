<<<<<<< HEAD
from PyQt5.QtWidgets import QListWidget, QMessageBox, QApplication, QMainWindow
import os
import sys

# 导入版本信息
from config import version_info
# 在 createMenus 函数中
current_version = version_info()




# 主代码
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        from custom_message import show_custom_message
        self.show_custom_message = show_custom_message

        from Login_All import load_ClassIsland_links, load_ClassIsland_info, load_Sticky_Attention_links, load_Sticky_Atention_info, load_ZongziTEK_Blackboard_Sticker_links, load_ZongziTEK_Blackboard_Sticker_info
        self.load_ClassIsland_links = load_ClassIsland_links
        self.load_ClassIsland_info = load_ClassIsland_info
        self.load_Sticky_Attention_links = load_Sticky_Attention_links
        self.load_Sticky_Atention_info = load_Sticky_Atention_info
        self.load_ZongziTEK_Blackboard_Sticker_links = load_ZongziTEK_Blackboard_Sticker_links
        self.load_ZongziTEK_Blackboard_Sticker_info = load_ZongziTEK_Blackboard_Sticker_info
        

        # 确保下载目录存在
        try:
            os.makedirs('Downloads', exist_ok=True)
        except Exception as e:
            self.show_custom_message(self, "发生错误", f"创建下载目录时发生错误: {e}", QMessageBox.Critical)
            sys.exit(1)  # 创建下载目录时发生错误，退出程序

        # 封装加载链接的过程
        def load_links(load_method, link_name):
            try:
                links = load_method(self)
                if links is None:
                    self.show_custom_message(self, "加载失败", f"{link_name}链接为空", QMessageBox.Warning)
                    return []
                return links
            except Exception as e:
                self.show_custom_message(self, "发生错误", f"{link_name}链接加载失败: {e}", QMessageBox.Critical)
                sys.exit(1)  # 链接处理发生错误，退出程序

        # 加载各类链接
        self.ClassIsland_links = load_links(self.load_ClassIsland_links, "ClassIsland 资源")
        self.ClassIsland_info = load_links(self.load_ClassIsland_info, "ClassIsland 信息")
        self.Sticky_Attention_links = load_links(self.load_Sticky_Attention_links, "Sticky_attention 资源")
        self.Sticky_Attention_info = load_links(self.load_Sticky_Atention_info, "Sticky_attention 信息")
        self.ZongziTEK_Blackboard_Sticker_links = load_links(self.load_ZongziTEK_Blackboard_Sticker_links, "ZongziTEK Blackboard Sticker 资源")
        self.ZongziTEK_Blackboard_Sticker_info = load_links(self.load_ZongziTEK_Blackboard_Sticker_info, "ZongziTEK Blackboard Sticker 信息")


    # 定义UI初始化函数
    from SectionIstoolUI import initUI


    # 显示主页内容
    def createNavigationList(self):
        list_widget = QListWidget()
        list_widget.addItem('ClassIsland')
        list_widget.addItem('Sticky-attention')
        list_widget.addItem('ZongziTEK Blackboard Sticker')
        list_widget.addItem('设置')
        list_widget.addItem('关于')
        list_widget.itemClicked.connect(self.onNavigationItemClicked)
        return list_widget


    # 菜单栏
    def onNavigationItemClicked(self, item):
        # 根据点击的项显示不同的内容
        if item.text() == 'ClassIsland':
            self.showSoftwareClassIslandDownloadContent()
        elif item.text() == 'Sticky-attention':
            self.showSoftwareStickyAttentionDownloadContent()
        elif item.text() == 'ZongziTEK Blackboard Sticker':
            self.showSoftwareZongziTEKBlackboardStickerDownloadContent()
        elif item.text() == '设置':
            self.showSettingsContent()
        elif item.text() == '关于':
            self.showHomeContent()



    # ClassIsland 下载
    from Software_ClassIsland_Download import showSoftwareClassIslandDownloadContent


    # Sticky_attention 下载
    from Software_Sticky_Attention_Download import showSoftwareStickyAttentionDownloadContent


    # ZongziTEK Blackboard Sticker 下载
    from Software_ZongziTEK_Blackboard_Sticker_Download import showSoftwareZongziTEKBlackboardStickerDownloadContent
    
    
    # 设置
    from Settings import showSettingsContent


    # 简介  
    from Synopsis import showHomeContent
    

    # 创建菜单
    from Menus import createMenus


    # 检测程序是否关闭
    from closeEvent import closeEvent

    
    # 程序报错
    from error_handle import error_handle


# 程序的入口点
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
=======
from PyQt5.QtWidgets import QListWidget, QMessageBox, QApplication, QMainWindow
import os
import sys

# 导入版本信息
from config import version_info
# 在 createMenus 函数中
current_version = version_info()




# 主代码
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        from custom_message import show_custom_message
        self.show_custom_message = show_custom_message

        from Login_All import load_ClassIsland_links, load_ClassIsland_info, load_Sticky_Attention_links, load_Sticky_Atention_info, load_ZongziTEK_Blackboard_Sticker_links, load_ZongziTEK_Blackboard_Sticker_info
        self.load_ClassIsland_links = load_ClassIsland_links
        self.load_ClassIsland_info = load_ClassIsland_info
        self.load_Sticky_Attention_links = load_Sticky_Attention_links
        self.load_Sticky_Atention_info = load_Sticky_Atention_info
        self.load_ZongziTEK_Blackboard_Sticker_links = load_ZongziTEK_Blackboard_Sticker_links
        self.load_ZongziTEK_Blackboard_Sticker_info = load_ZongziTEK_Blackboard_Sticker_info
        

        # 确保下载目录存在
        try:
            os.makedirs('Downloads', exist_ok=True)
        except Exception as e:
            self.show_custom_message(self, "发生错误", f"创建下载目录时发生错误: {e}", QMessageBox.Critical)
            sys.exit(1)  # 创建下载目录时发生错误，退出程序

        # 封装加载链接的过程
        def load_links(load_method, link_name):
            try:
                links = load_method(self)
                if links is None:
                    self.show_custom_message(self, "加载失败", f"{link_name}链接为空", QMessageBox.Warning)
                    return []
                return links
            except Exception as e:
                self.show_custom_message(self, "发生错误", f"{link_name}链接加载失败: {e}", QMessageBox.Critical)
                sys.exit(1)  # 链接处理发生错误，退出程序

        # 加载各类链接
        self.ClassIsland_links = load_links(self.load_ClassIsland_links, "ClassIsland 资源")
        self.ClassIsland_info = load_links(self.load_ClassIsland_info, "ClassIsland 信息")
        self.Sticky_Attention_links = load_links(self.load_Sticky_Attention_links, "Sticky_attention 资源")
        self.Sticky_Attention_info = load_links(self.load_Sticky_Atention_info, "Sticky_attention 信息")
        self.ZongziTEK_Blackboard_Sticker_links = load_links(self.load_ZongziTEK_Blackboard_Sticker_links, "ZongziTEK Blackboard Sticker 资源")
        self.ZongziTEK_Blackboard_Sticker_info = load_links(self.load_ZongziTEK_Blackboard_Sticker_info, "ZongziTEK Blackboard Sticker 信息")


    # 定义UI初始化函数
    from SectionIstoolUI import initUI


    # 显示主页内容
    def createNavigationList(self):
        list_widget = QListWidget()
        list_widget.addItem('ClassIsland')
        list_widget.addItem('Sticky-attention')
        list_widget.addItem('ZongziTEK Blackboard Sticker')
        list_widget.addItem('设置')
        list_widget.addItem('关于')
        list_widget.itemClicked.connect(self.onNavigationItemClicked)
        return list_widget


    # 菜单栏
    def onNavigationItemClicked(self, item):
        # 根据点击的项显示不同的内容
        if item.text() == 'ClassIsland':
            self.showSoftwareClassIslandDownloadContent()
        elif item.text() == 'Sticky-attention':
            self.showSoftwareStickyAttentionDownloadContent()
        elif item.text() == 'ZongziTEK Blackboard Sticker':
            self.showSoftwareZongziTEKBlackboardStickerDownloadContent()
        elif item.text() == '设置':
            self.showSettingsContent()
        elif item.text() == '关于':
            self.showHomeContent()



    # ClassIsland 下载
    from Software_ClassIsland_Download import showSoftwareClassIslandDownloadContent


    # Sticky_attention 下载
    from Software_Sticky_Attention_Download import showSoftwareStickyAttentionDownloadContent


    # ZongziTEK Blackboard Sticker 下载
    from Software_ZongziTEK_Blackboard_Sticker_Download import showSoftwareZongziTEKBlackboardStickerDownloadContent
    
    
    # 设置
    from Settings import showSettingsContent


    # 简介  
    from Synopsis import showHomeContent
    

    # 创建菜单
    from Menus import createMenus


    # 检测程序是否关闭
    from closeEvent import closeEvent

    
    # 程序报错
    from error_handle import error_handle


# 程序的入口点
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
>>>>>>> 4fa2a7888d33a4299e04b4d0deacd959883e7656
    