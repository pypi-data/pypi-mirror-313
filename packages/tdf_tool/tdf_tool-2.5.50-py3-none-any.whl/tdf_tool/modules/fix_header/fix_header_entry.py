import os
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
)
from tdf_tool.tools.cmd import Cmd
from tdf_tool.modules.fix_header.fix_header_lint_tool import FixHeaderLintTool
from tdf_tool.modules.fix_header.fix_header_replace_tool import FixHeaderReplaceTool
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.tools.print import Print
from enum import Enum


class FixHeaderType(Enum):
    REPLACE = 1
    LINT = 2


class FixHeaderEntry:
    def __init__(self, fix_type: FixHeaderType):
        self.fix_type = fix_type

    def start(self):
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        Print.str("检测到以下模块可执行修复头文件脚本：")
        Print.str(batchPodNames)
        while True:
            targetModuleName = input(
                "请输入需要执行修复头文件脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModuleName == "!" or targetModuleName == "！":
                exit(0)
            elif targetModuleName == "all":
                if self.fix_type == FixHeaderType.REPLACE:
                    path = os.getcwd()
                    BatchPodTools.generate_pod_source_files(batchPodList)
                    fix_header = FixHeaderReplaceTool(path, batchPodList)
                    fix_header.find_remote_pod_header()
                for module in batchPodList:
                    Print.stage("开始处理 {0} 模块的头文件".format(module.name))
                    if self.fix_type == FixHeaderType.LINT:
                        self.lint_path(module.path)
                    else:
                        fix_header.find_local_pod_header(module.name)
                        fix_header.replace_import(module.name)
                exit(0)
            else:
                self.module(targetModuleName)

    def module(self, moduleName: str):
        Print.stage("开始处理 {0} 模块的头文件".format(moduleName))
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if moduleName in batchPodNames:
            targetModule = list(filter(lambda x: x.name == moduleName, batchPodList))[0]
            if self.fix_type == FixHeaderType.LINT:
                self.lint_path(targetModule.path)
            else:
                path = os.getcwd()
                BatchPodTools.generate_pod_source_files(batchPodList)
                fix_header = FixHeaderReplaceTool(path, batchPodList)
                fix_header.start_fix(moduleName)
                Print.stage("{0} 路径下头文件 replace 成功".format(path))
            exit(0)
        else:
            Print.error(moduleName + "不存在开发列表中")

    def lint_path(self, path: str):
        podpsec_path = ShellDir.findPodspec(path)
        if podpsec_path != None:
            self.__lint_header(podpsec_path)
        else:
            Print.error(path + "路径下不存在podspec文件")

    def __lint_header(self, podspec_path: str):
        lint_header = FixHeaderLintTool()
        lint_header.lint(podspec_path)
        Print.stage("{0} 路径下头文件 lint 成功".format(podspec_path))
