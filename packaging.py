import os
import json
import subprocess

# 读取配置文件
def read_json(json_path):
    if not os.path.exists('./app/Settings'):
        os.makedirs('./app/Settings')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def modify_setting():
    json_path = './app/Settings/Settings.json'
    read_json_dict = read_json(json_path)
    # 读取配置文件的version值
    version = read_json_dict.get('version', 0)
    return version

version_info = modify_setting()

# 设置源文件路径
source_file = 'main.py'

# 设置图标路径
icon_file = 'resources/SectionIstool_icon.ico'

# 设置输出目录
output_dir = 'dist'

qt_plugins_path = 'C:\Users\lzy\AppData\Local\Programs\Python\Python38\Lib\site-packages\PyQt5'

# 构建命令
source_file_abs = os.path.abspath(source_file)
icon_file_abs = os.path.abspath(icon_file)
output_dir_abs = os.path.abspath(output_dir)

build_command = f"nuitka --mingw64 --standalone --windows-console-mode=disable --output-dir={output_dir_abs} --show-progress --show-memory --windows-icon-from-ico={icon_file_abs} --windows-company-name=SectionIstool --windows-product-name=SectionIstool --windows-file-version={version_info} --windows-product-version={version_info} --windows-file-description=该软件会使您在学校班级电脑中方便、快捷的下载适合班级下载各类软件 --remove-output {source_file_abs} --include-plugin-dir={qt_plugins_path}"

# 执行构建命令
try:
    subprocess.run(build_command, check=True, shell=True)
    print("打包成功！")
except subprocess.CalledProcessError as e:
    print(f"打包失败: {e}")
except Exception as e:
    print(f"打包失败: {e}")