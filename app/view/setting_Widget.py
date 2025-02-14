from qfluentwidgets import * # type: ignore
from qfluentwidgets import FluentIcon as FIF  # type: ignore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget
from loguru import logger
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import subprocess

from ..common.config import cfg, AUTHOR, VERSION, YEAR, isWin11 # type: ignore
from ..common.signal_bus import signalBus

class setting_Widget(QFrame):
    def __init__(self, parent: QFrame = None): # type: ignore
        super().__init__(parent=parent)

        # 创建一个 QScrollArea
        scroll_area_personal = QScrollArea(self)
        scroll_area_personal.setWidgetResizable(True)
        # 设置 QScrollArea 的样式
        scroll_area_personal.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
        """)

        # 创建一个 QScrollArea
        scroll_area_about = QScrollArea(self)   
        scroll_area_about.setWidgetResizable(True)
        # 设置 QScrollArea 的样式
        scroll_area_about.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea QWidget {
                background-color: transparent;
            }
        """)

        # 创建一个内部的 QFrame 用于放置内容
        inner_frame_personal = QWidget(scroll_area_personal)
        inner_layout_personal = QVBoxLayout(inner_frame_personal)
        inner_layout_personal.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop) # type: ignore

        # 创建一个内部的 QFrame 用于放置内容
        inner_frame_about = QFrame(scroll_area_about)
        inner_layout_about = QVBoxLayout(inner_frame_about)
        inner_layout_about.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop) # type: ignore

        settingLabel = SubtitleLabel("设置")
        settingLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # type: ignore
        settingLabel.setWordWrap(True)

        personalLabel = SubtitleLabel("    个性化")
        personalLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # type: ignore
        personalLabel.setWordWrap(True)

        aboutLabel = SubtitleLabel("    关于")
        aboutLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop) # type: ignore
        aboutLabel.setWordWrap(True)

        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            "应用主题",
            "调整你的应用外观",
            ["浅色", "深色", "跟随系统设置"]
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("界面缩放"),
            self.tr("更改界面和字体的大小"),
            texts=["100%", "125%", "150%", "175%", "200%", self.tr("使用系统设置"),]
        )
        self.micaCard = SwitchSettingCard(
            FluentIcon.TRANSPARENT,
            "启用亚克力效果",
            "亚克力效果的视觉体验更好，但是可能导致窗口卡顿",
            cfg.enableAcrylicBackground
        )

        self.updatemannerCard = OptionsSettingCard(
            cfg.updatemanner,
            FIF.CLOUD_DOWNLOAD,
            self.tr("更新通道"),
            self.tr("控制应用的更新目标版本"),
            texts=["稳定通道", "测试通道"]
        )
        self.updatesourceCard = OptionsSettingCard(
            cfg.updatesource,
            FIF.GLOBE,
            self.tr("更新镜像源"),
            texts=['github', 'github(ghproxy)-已被墙', 'github(ghp)-已被墙', 'github(ghgo)-已被墙', 'github(ghfast)']
        )
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('在应用程序启动时检查更新'),
            self.tr('新版本将更加稳定并拥有更多功能（建议启用此选项）'),
            cfg.checkUpdateAtStartUp
        )
        self.aboutupdateCard = PrimaryPushSettingCard(
            self.tr('检查更新'),
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " + self.tr('当前版本') + " " + VERSION
        )
        # 按钮的点击事件可以用!
        # self.aboutupdateCard.clicked.connect(lambda: self.update_manner_changed()) # type: ignore 
        self.aboutupdateCard.clicked.connect(lambda: self.update_manner_changed_off()) # type: ignore 

        inner_layout_personal.addWidget(self.themeCard)
        inner_layout_personal.addWidget(self.zoomCard)
        inner_layout_personal.addWidget(self.micaCard)

        # inner_layout_personal.addWidget(aboutLabel)
        inner_layout_personal.addWidget(self.updatemannerCard)
        inner_layout_personal.addWidget(self.updatesourceCard)
        # inner_layout_personal.addWidget(self.updateOnStartUpCard)
        inner_layout_personal.addWidget(self.aboutupdateCard)

        # 将内部的 QFrame 设置为 QScrollArea 的内容
        scroll_area_personal.setWidget(inner_frame_personal)
        # scroll_area_about.setWidget(inner_frame_about)

        # 设置主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(settingLabel)
        # main_layout.addWidget(personalLabel)
        main_layout.addWidget(scroll_area_personal)
        # main_layout.addWidget(aboutLabel)
        # main_layout.addWidget(scroll_area_about)

        self.__initWidget()

    def __initWidget(self):
        self.micaCard.setEnabled(isWin11())
        self.__connectSignalToSlot()

    def __showRestartTooltip(self):
        InfoBar.success( # type: ignore
            self.tr('更新成功'),
            self.tr('设置在重启后生效'),
            duration=1500,
            parent=self
        )

    def __connectSignalToSlot(self):
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(setTheme)
        self.micaCard.checkedChanged.connect(signalBus.micaEnableChanged)

    def modify_setting_update_manner(self, json_path, software_name, key): # type: ignore
        try:
            with open(json_path, 'r', encoding='utf-8') as file: # type: ignore
                json_file = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return 'Unknown'
        
        # 检查指定软件的配置是否存在
        if software_name in json_file and key in json_file[software_name]:
            return json_file[software_name][key]
        
        return 'Unknown'
    def update_manner_changed_off(self): # type: ignore
        # 读取配置文件中的版本号
        releases_data = self.modify_setting_update_manner('./app/Settings/Settings.json', 'Update', 'version') # type: ignore
        # 提取 tag_name 字段的值
        if releases_data != 'Unknown':
            release_name = releases_data
        else:
            release_name = 'Unknown'

        if release_name == 'Unknown':
            logger.error(f"无法读取当前版本号, 当前版已暂停自动更新服务(功能), 请前往 SectionIstool 关于页 下载最新版本 ✨")
            InfoBar.error( # type: ignore
                title='无法读取当前版本号',
                content="无法读取当前版本号, 当前版已暂停自动更新服务(功能), 请前往 SectionIstool 关于页 下载最新版本 ✨",
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=20000,
                parent=self
            )
            logger.error(f"无法读取当前版本号, 详情请查看日志文件 ✨")
            return
        logger.info(f"当前版本读取成功, 当前版本号为: {release_name}, 当前版已暂停自动更新服务(功能), 请前往 SectionIstool 关于页 下载最新版本 ✨")
        InfoBar.success( # type: ignore
            title='当前版本读取成功',
            content=f"当前版本读取成功, 当前版本号为: {release_name}, 当前版已暂停自动更新服务(功能), 请前往 SectionIstool 关于页 下载最新版本 ✨",
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=20000,
            parent=self
        )
        return
    
    def update_manner_changed(self): # type: ignore
        # 读取配置文件中的版本号
        releases_data = self.modify_setting_update_manner('./app/Settings/Settings.json', 'Update', 'version') # type: ignore
        # 提取 tag_name 字段的值
        if releases_data != 'Unknown':
            release_name = releases_data
        else:
            release_name = 'Unknown'

        if release_name == 'Unknown':
            logger.error(f"无法读取当前版本号")
            InfoBar.error( # type: ignore
                title='无法读取当前版本号',
                content="无法读取当前版本号, 详情请查看日志文件 ✨",
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=10000,
                parent=self
            )
            logger.error(f"无法读取当前版本号, 详情请查看日志文件 ✨")
            return
        logger.info(f"当前版本读取成功, 当前版本号为: {release_name} ✨")
        InfoBar.success( # type: ignore
            title='当前版本读取成功',
            content=f"当前版本读取成功, 当前版本号为: {release_name} ✨",
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=self
        )

        update_manner = self.modify_setting_update_manner('./app/Settings/config.json', 'Update', 'manner') # type: ignore
        if update_manner == '测试通道': # type: ignore
            github_api_url = f'https://api.github.com/repos/SectionIstool/SectionIstool/releases'
        else:
            github_api_url = f'https://api.github.com/repos/SectionIstool/SectionIstool/releases/latest'

        # 使用 ThreadPoolExecutor 并行执行操作
        with ThreadPoolExecutor() as executor:
            future = executor.submit(urllib.request.urlopen, github_api_url)  # 使用 urllib.request.urlopen 替代 requests.get
            response = future.result()
            if response.getcode() == 200:  # 使用 getcode() 替代 status_code
                releases_data = json.load(response)  # 直接从 response 加载 json 数据
                # 提取 tag_name 字段的值
                if update_manner == '测试通道': # type: ignore
                    tag_name = releases_data[0]['tag_name']
                else:
                    tag_name = releases_data['tag_name']
                logger.info(f"已成功刷新下载源, 即将下载最新版本的 SectionIstool ✨")
                InfoBar.success( # type: ignore
                    title='刷新下载源成功',
                    content="已成功刷新下载源, 可以下载最新版本的 SectionIstool ✨",
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=10000,
                    parent=self
                )
            else:
                logger.error(f"无法获取版本数据: {response.getcode()}")
                InfoBar.error( # type: ignore
                    title='刷新下载源失败',
                    content="刷新下载源失败, 请检查网络连接或稍后重试 ✨",
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=10000,
                    parent=self
                )
                return

        # 提取 tag_name 字段的值
        if tag_name != 'Unknown':  # type: ignore
            release_name_update = tag_name # type: ignore
        else:
            release_name_update = 'Unknown'

        # 将版本号拆分为整数列表
        release_name_parts = list(map(int, release_name.split('.')))
        release_name_update_parts = list(map(int, release_name_update.split('.')))

        # 逐段比较版本号
        if len(release_name_update_parts) == len(release_name_parts):
            for base, update in zip(release_name_parts, release_name_update_parts):
                if update > base:
                    break
                elif update < base:
                    logger.info(f"当前已是最新版本的 SectionIstool ✨")
                    InfoBar.success( # type: ignore
                        title='当前已是最新版本',
                        content="当前已是最新版本的 SectionIstool ✨",
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=10000,
                        parent=self
                    )
                    return
            else:
                logger.info(f"当前已是最新版本的 SectionIstool ✨")
                InfoBar.success( # type: ignore
                    title='当前已是最新版本',
                    content="当前已是最新版本的 SectionIstool ✨",
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=10000,
                    parent=self
                )
                return
        else:
            logger.info(f"版本号格式不一致, 无法比较")
            InfoBar.error( # type: ignore
                title='版本号格式不一致',
                content="版本号格式不一致, 无法比较 ✨",
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )
            return

        logger.info(f"发现新版本的 SectionIstool ✨")
        InfoBar.success( # type: ignore
            title='发现新版本',
            content=f"发现新版本的 SectionIstool ✨",
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=self
        )
        
        update_manner = self.modify_setting_update_manner('./app/Settings/config.json', 'Update', 'manner') # type: ignore
        if update_manner == '测试通道': # type: ignore
            url_update = f'https://github.com/SectionIstool/SectionIstool/releases/download/{release_name_update}/SectionIstool.zip'
        else:
            url_update = f'https://github.com/SectionIstool/SectionIstool/releases/download/{release_name_update}/SectionIstool.zip'  # 设置默认的 url_update

        source_combo_box_data = self.modify_setting_update_manner('./app/Settings/config.json', 'Update', 'source') # type: ignore
        # 提取 {software_name_download_second}_source 字段的值
        if source_combo_box_data != 'Unknown':
            source_combo_box_value = source_combo_box_data
            if source_combo_box_value == 'github':
                download_url = url_update # type: ignore
            elif source_combo_box_value in ['github(ghproxy)-已被墙', 'github(ghp)-已被墙', 'github(ghgo)-已被墙']:
                logger.warning(f"下载源 {source_combo_box_value} 被阻止, 回退到默认的 github 源")
                download_url = url_update # type: ignore
            elif source_combo_box_value == 'github(ghfast)':
                download_url = f"https://ghfast.top/{url_update}" # type: ignore
            else:
                download_url = url_update # type: ignore
        else:
            download_url = url_update # type: ignore

        # 执行下载操作
        logger.info(f"开始下载最新版本的 SectionIstool ✨")
        InfoBar.success( # type: ignore
            title='开始下载',
            content="开始下载最新版本的 SectionIstool ✨",
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=10000,
            parent=self
        )

        # 确认是否存在下载目录
        if './app/update' != 'Unknown' and not os.path.exists('./app/update'): # type: ignore
            os.makedirs('./app/update')
            # 使用 aiohttp 进行异步下载 
            asyncio.run(self.async_download(download_url, download_path, version_name_names)) # type: ignore

        # 确认是否存在解压目录
        if './app/update/SectionIstool_update_temp' != 'Unknown' and not os.path.exists('./app/update/SectionIstool_update_temp'): # type: ignore
            os.makedirs('./app/update/SectionIstool_update_temp')

        # 解压最新版本的 SectionIstool
        try:
            import zipfile
            with zipfile.ZipFile(f'./app/update/SectionIstool.zip', 'r') as zip_ref:
                zip_ref.extractall(f'./app/update/SectionIstool_update_temp')
            logger.info(f"解压最新版本的 SectionIstool 成功 ✨")
            InfoBar.success( # type: ignore
                title='解压成功',
                content="解压最新版本的 SectionIstool 成功 ✨",
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )
        except Exception as e:
            logger.error(f"解压最新版本的 SectionIstool 失败: {e}")
            InfoBar.error( # type: ignore
                title='解压失败',
                content=f"解压最新版本的 SectionIstool 失败: {e} ✨",
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )
            return

        # 启动更新程序
        try:
            logger.info(f"尝试启动更新程序 ✨")
            # 获取当前脚本所在的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建批处理文件的绝对路径
            bat_file_path = os.path.join(current_dir, '..', 'update', 'update_SectionIstool.bat')
            # 使用 subprocess 模块来执行批处理文件，更推荐这种方式
            try:
                subprocess.run([bat_file_path], check=True, shell=True)
                logger.info("批处理文件执行成功")
            except subprocess.CalledProcessError as e:
                logger.error(f"批处理文件执行失败: {e}")
            logger.info(f"启动更新程序成功 ✨")
            InfoBar.success( # type: ignore
                title='启动成功',
                content="启动更新程序成功, 即将结束当前进程 ✨",
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )
        except Exception as e:
            logger.error(f"启动更新程序失败: {e}")
            InfoBar.error( # type: ignore
                title='启动失败',
                content=f"启动更新程序失败: {e} ✨",
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )
        # 结束当前进程
        try:
            os._exit(0) # type: ignore
            logger.info(f"结束当前进程成功 ✨")
        except Exception as e:
            logger.error(f"结束当前进程失败: {e}")
            InfoBar.error( # type: ignore
                title='结束失败',
                content=f"结束当前进程失败: {e} ✨",
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=10000,
                parent=self
            )