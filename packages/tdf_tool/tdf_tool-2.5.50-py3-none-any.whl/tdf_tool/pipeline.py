import sys
from tdf_tool.pipelines.module import Module
from tdf_tool.pipelines.translate import Translate
from tdf_tool.pipelines.annotation import Annotation
from tdf_tool.pipelines.fix_header import FixHeader
from tdf_tool.pipelines.package import Package
from tdf_tool.pipelines.i18n import I18n
from tdf_tool.pipelines.flutter_upgrade import FlutterUpgrade

from tdf_tool.pipelines.git import Git
from tdf_tool.pipelines.upgrade import Upgrade
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.tools.tl_version_invalidate import TLOwner


class Pipeline:
    """
    二维火 Flutter 脚手架工具，包含项目构建，依赖分析，git等功能。。
    """

    def __init__(self):
        TLOwner().check_for_package_updates()

        ShellDir.dirInvalidate()

        self.module = Module()
        self.translate = Translate()
        self.package = Package()
        self.fixHeader = FixHeader()
        self.i18n = I18n()

        # 注解整合命令
        self.annotation = Annotation()

        # flutter 组件版本号升级的命令
        self.flutterUpgrade = FlutterUpgrade()

    def git(self, *kwargs, **kwargs1):
        """
        tdf_tool git【git 命令】：批量操作 git 命令, 例如 tdf_tool git push
        """
        Git(sys.argv[2:]).run()
