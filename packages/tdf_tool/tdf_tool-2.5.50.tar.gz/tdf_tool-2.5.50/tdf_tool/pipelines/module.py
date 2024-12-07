from tdf_tool.modules.cli.project_cli import ProjectCLI
from tdf_tool.tools.cmd import Cmd
from tdf_tool.modules.config.config import CLIJsonConfig
from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.tools.vscode.vscode import VsCodeManager
from tdf_tool.tools.tl_version_invalidate import TLOwner
from tdf_tool.tools.print import Print
from tdf_tool.modules.config.packages_config import PackageNode, PackagesJsonConfig


class Module:
    """
    模块相关工具： tl module -h 查看详情
    """

    def _init(self):
        ShellDir.goInShellDir()
        self.__cli = ProjectCLI()
        self.__vscodeManager = VsCodeManager()

    def init(self):
        """
        项目初始化
        """
        self._init()
        ShellDir.goInShellDir()
        self.__cli.initial()

    def deps(self):
        """
        修改initial_config.json文件后，执行该命令，更新依赖(覆写)
        """
        # TLOwner().check_for_package_updates()
        self._init()
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            self.__cli.cliDeps()
        elif projectType == ProjectType.IOS:
            ios_arg = ["bundle", "exec", "pod", "bin", "batch", "clone"]
            Cmd.runAndPrint(ios_arg, shell=False)

    def depsUnSync(self):
        """
        修改initial_config.json文件后，执行该命令，更新依赖(无 git 操作)
        """
        # TLOwner().check_for_package_updates()
        self._init()
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType == ProjectType.FLUTTER:
            self.__cli.depsUnSync()
        elif projectType == ProjectType.IOS:
            ios_arg = ["bundle", "exec", "pod", "bin", "batch", "clone"]
            Cmd.runAndPrint(ios_arg, shell=False)

    def open(self):
        """
        打开vscode，同时将所有模块添加入vscode中
        """
        self._init()
        ShellDir.goInShellDir()
        self.__vscodeManager.openFlutterProject()

    def module_update(self):
        """
        更新存储项目git信息的json文件
        """
        self._init()
        ShellDir.goInShellDir()
        CLIJsonConfig.updateModuleConfig()

    def source(self):
        """
        源码依赖当前壳中的所有 flutter 模块
        """
        self._init()
        ShellDir.goInShellDir()
        # Cmd.system("flutter pub upgrade")

        Print.stage("分析所有的可以源码依赖的模块")
        self.__packagesList: list[PackageNode] = PackagesJsonConfig(
            ShellDir.getShellDir()
        ).packages  # 壳依赖的所有库

        name_list = [bean.packageName for bean in self.__packagesList]

        Print.step(name_list)
