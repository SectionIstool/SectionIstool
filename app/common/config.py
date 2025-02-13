# coding:utf-8
import sys
import os
from qfluentwidgets import *  # type: ignore

# 读取配置文件
def read_json(json_path): # type: ignore
    # 确认是否存在设置目录
    if './app/Settings' != None and not os.path.exists('./app/Settings'): # type: ignore
        os.makedirs('./app/Settings')
    if os.path.exists(json_path): # type: ignore
        try:
            with open(json_path, 'r', encoding='utf-8') as file: # type: ignore
                return json.load(file)
        except json.JSONDecodeError:
            # 如果文件内容不是有效的 JSON 格式，返回空字典
            return {} # type: ignore
    return {} # type: ignore

def modify_setting(): # type: ignore
    json_path = './app/Settings/Settings.json'
    read_json_dict = read_json(json_path) # type: ignore
    # 读取配置文件的version值
    version = read_json_dict.get('version', 0)  # type: ignore
    return version  # type: ignore

# 修改或新增指定软件配置中的某个值
def modify_setting_config(json_path, software_name, key, new_value):  # type: ignore
    # 确认是否存在设置目录
    if not os.path.exists('./app/Settings'):
        os.makedirs('./app/Settings')
    try:
        with open(json_path, 'r', encoding='utf-8') as file:  # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        json_file = {}
    
    # 检查指定软件的配置是否存在
    if software_name not in json_file:
        json_file[software_name] = {}
    elif not isinstance(json_file[software_name], dict):
        # 如果不是字典，将其转换为字典
        json_file[software_name] = {}
    
    # 修改或新增指定键的值
    json_file[software_name][key] = new_value
    
    # 将更新后的数据写回文件
    with open(json_path, 'w', encoding='utf-8') as file: # type: ignore
        json.dump(json_file, file, ensure_ascii=False, indent=4)

def modify_setting_update_manner(json_path, software_name, key): # type: ignore
    try:
        with open(json_path, 'r', encoding='utf-8') as file: # type: ignore
            json_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "稳定通道"
    
    # 检查指定软件的配置是否存在
    if software_name in json_file and key in json_file[software_name]:
        return json_file[software_name][key]
    
    return "稳定通道"

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    # 主题模式
    dpiScale = OptionsConfigItem(
        "Window", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    # 亚克力效果
    enableAcrylicBackground = ConfigItem("Window", "EnableAcrylicBackground", False, BoolValidator())
    # 窗口透明度
    micaEnabled = ConfigItem("Window", "MicaEnabled", isWin11(), BoolValidator())
    # 软件启动时检查更新
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())
    # 更新通道
    updatemanner = OptionsConfigItem("Update", "manner", "稳定通道", OptionsValidator(["稳定通道", '测试通道']))
    # 更新镜像源
    updatesource = OptionsConfigItem("Update", "source", "github(ghfast)", OptionsValidator(["github", "github(ghproxy)-已被墙", "github(ghp)-已被墙", "github(ghgo)-已被墙", "github(ghfast)"]))

update_manner = modify_setting_update_manner('./app/Settings/config.json', 'Update', 'manner')
modify_setting_text = modify_setting() # type: ignore

modify_setting_config('./app/Settings/Settings.json', 'Update', 'version', modify_setting_text)

YEAR = 2025
AUTHOR = "lzy98276"
VERSION = modify_setting_text # type: ignore
HELP_URL = "https://qfluentwidgets.com"
REPO_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"
EXAMPLE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples"
FEEDBACK_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues"
RELEASE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases/latest"
ZH_SUPPORT_URL = "https://qfluentwidgets.com/zh/price/"
EN_SUPPORT_URL = "https://qfluentwidgets.com/price/"


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('./app/Settings/config.json', cfg)  # type: ignore