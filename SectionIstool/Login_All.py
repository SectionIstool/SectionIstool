<<<<<<< HEAD
import os
from PyQt5.QtWidgets import QMessageBox

from Data_loading import get_all_versions, get_software_info


# ClassIsland
def load_ClassIsland_links(self):
    try:
        repo = 'ClassIsland/ClassIsland'
        software_name = 'ClassIsland'
        software_true_name = 'ClassIsland'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_ClassIsland_info(self):
    try:
        repo = 'ClassIsland/ClassIsland'
        software_name = 'ClassIsland'
        software_true_name = 'ClassIsland'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, source, author, token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错


# ===================================================================================================================================================
        

# Sticky_attention
def load_Sticky_Attention_links(self):
    try:
        repo = 'Sticky-attention/Sticky-attention'
        software_name = 'Release'
        software_true_name = 'Sticky-attention'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_Sticky_Atention_info(self):
    try:
        repo = 'Sticky-attention/Sticky-attention'
        software_name = 'Release'
        software_true_name = 'Sticky-attention'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, source, author, token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错


# ===================================================================================================================================================


# ZongziTEK_Blackboard_Sticker
def load_ZongziTEK_Blackboard_Sticker_links(self):
    try:
        repo = 'STBBRD/ZongziTEK-Blackboard-Sticker'
        software_name = 'ZongziTEK_Blackboard_Sticker'
        software_true_name = 'ZongziTEK_Blackboard_Sticker'
        author = "STBBRD"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_ZongziTEK_Blackboard_Sticker_info(self):
    try:
        repo = 'STBBRD/ZongziTEK-Blackboard-Sticker'
        software_name = 'ZongziTEK_Blackboard_Sticker'
        software_true_name = 'ZongziTEK_Blackboard_Sticker'
        author = "STBBRD"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, source, author, token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
=======
import os
from PyQt5.QtWidgets import QMessageBox

from Data_loading import get_all_versions, get_software_info


# ClassIsland
def load_ClassIsland_links(self):
    try:
        repo = 'ClassIsland/ClassIsland'
        software_name = 'ClassIsland'
        software_true_name = 'ClassIsland'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_ClassIsland_info(self):
    try:
        repo = 'ClassIsland/ClassIsland'
        software_name = 'ClassIsland'
        software_true_name = 'ClassIsland'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, source, author, token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错


# ===================================================================================================================================================
        

# Sticky_attention
def load_Sticky_Attention_links(self):
    try:
        repo = 'Sticky-attention/Sticky-attention'
        software_name = 'Release'
        software_true_name = 'Sticky-attention'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_Sticky_Atention_info(self):
    try:
        repo = 'Sticky-attention/Sticky-attention'
        software_name = 'Release'
        software_true_name = 'Sticky-attention'
        author = "HelloWRC"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, source, author, token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错


# ===================================================================================================================================================


# ZongziTEK_Blackboard_Sticker
def load_ZongziTEK_Blackboard_Sticker_links(self):
    try:
        repo = 'STBBRD/ZongziTEK-Blackboard-Sticker'
        software_name = 'ZongziTEK_Blackboard_Sticker'
        software_true_name = 'ZongziTEK_Blackboard_Sticker'
        author = "STBBRD"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, source, author, token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_ZongziTEK_Blackboard_Sticker_info(self):
    try:
        repo = 'STBBRD/ZongziTEK-Blackboard-Sticker'
        software_name = 'ZongziTEK_Blackboard_Sticker'
        software_true_name = 'ZongziTEK_Blackboard_Sticker'
        author = "STBBRD"
        file_extension = 'zip' 
        source = 'github'

        # 从环境变量中获取GitHub令牌（如果已设置）
        token = os.getenv("")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, source, author, token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
>>>>>>> 4fa2a7888d33a4299e04b4d0deacd959883e7656
        return None  # 明确返回None以指示出错