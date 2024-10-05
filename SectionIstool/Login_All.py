from PyQt5.QtWidgets import QMessageBox
import random

from Data_loading import get_all_versions, get_software_info, get_update_info


# SectionIstool
def load_SectionIstool_links(self):
    try:
        repo = 'SectionIstool/SectionIstool'
        software_name = 'SectionIstool'
        software_true_name = 'SectionIstool'
        author = "lzy98276"
        file_extension = 'exe' 
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_SectionIstool_info(self):
    try:
        repo = 'SectionIstool/SectionIstool'
        software_name = 'SectionIstool'
        software_true_name = 'SectionIstool'
        author = "lzy98276"
        file_extension = 'exe' 
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_update_info(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错


# ===================================================================================================================================================


# ClassIsland
def load_ClassIsland_links(self):
    try:
        repo = 'ClassIsland/ClassIsland'
        software_name = 'ClassIsland'
        software_true_name = 'ClassIsland'
        author = "HelloWRC"
        file_extension = 'zip' 
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, min_version, max_version, limit)

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
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错


# ===================================================================================================================================================
        

# Sticky_attention
def load_Sticky_Attention_links(self):
    try:
        repo = 'Sticky-attention/Sticky-attention'
        software_name = 'Sticky-attention'
        software_true_name = 'Sticky-attention'
        author = "HelloWRC/jizilin6732"
        file_extension = 'zip' 
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, min_version, max_version, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错

def load_Sticky_Atention_info(self):
    try:
        repo = 'Sticky-attention/Sticky-attention'
        software_name = 'Sticky-attention'
        software_true_name = 'Sticky-attention'
        author = "HelloWRC/jizilin6732"
        file_extension = 'zip' 
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, limit)

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
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 设置版本范围
        min_version = None  # 您可以根据需求设置最小版本
        max_version = None  # 您可以根据需求设置最大版本

        # 限制结果数量
        limit = 3

        # 调用主函数并获取结果
        return get_all_versions(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, min_version, max_version, limit)

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
        # 1为github，2为github(镜像源)
        source_first = ''
        source_second = '2'

        # GitHub令牌组 仅供 SectionIstool 使用，请勿泄露(仅供读取公开仓库信息)
        # 令牌于2025/10/4失效
        token_lst = ["",""]

        # 随机选择一个 access_token
        access_token = random.choice(token_lst)

        print(f"access_token: {access_token}")

        # 限制结果数量
        limit = 1

        # 调用主函数并获取结果
        return get_software_info(repo, software_name, software_true_name, file_extension, author, source_first, source_second, access_token, limit)

    except Exception as e:
        self.show_custom_message(self, "错误", f"加载文件时发生错误: {e}", QMessageBox.Critical)
        return None  # 明确返回None以指示出错