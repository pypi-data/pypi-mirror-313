import os
from tdf_tool.tools.dependencies_analysis import DependencyAnalysis
from tdf_tool.modules.package.seal_off_package_utils import (
    changeVersionAndDependencies,
    createAndPushTag,
    tagInfoObj,
)
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class Package:
    """
    封包工具相关：tl package -h 查看详情
    """

    def map(self):
        """
        tl package map：以二维数组形式输出模块的依赖顺序，每一item列表代表可同时打tag的模块
        """
        ShellDir.goInShellDir()
        json = DependencyAnalysis().generate()
        print(json)
        exit(0)

    def tagInfo(self):
        """
        tl package tagInfo：输出一个json，每一节点包含一个模块，
        内部包含：remote：远程最新版本号；
        current：模块内配置的版本号；
        upgrade：对比自增后的版本号；
        sort：模块打tag顺序，sort相同即代表可同时打tag
        """
        ShellDir.goInShellDir()
        tagInfoObj()

    def prepareTagTask(self, jsonData: str):
        """
        tl package prepareTagTask：修改yaml中的tag号和所有的依赖，该命令可看成是做打tag前的准备工作，把依赖规范化
        """
        ShellDir.goInShellDir()
        changeVersionAndDependencies(jsonData)

    def tag(self, modules: str):
        """
        tl package tag：批量tag操作，参数通过逗号隔开，不要有空格。如tdf_tool package tag tdf_widgets
        """
        ShellDir.goInShellDir()
        createAndPushTag(modules.split(","))
