from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.modules.translate.ios.tools.batch_pod_tools import (
    BatchPodTools,
)
from tdf_tool.modules.translate.ios.tools.ios_module import IosModule


class iOSTranslateLint:

    # 交互式 国际化
    def start():
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))

        Print.str("检测到以下模块可执行国际化 lint 脚本：")
        Print.str(batchPodNames)
        while True:
            targetModule = input(
                "请输入需要执行国际化 lint 脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in batchPodList:
                    iOSTranslateLint.module(module.name)
                exit(0)
            else:
                iOSTranslateLint.module(targetModule)
                exit(0)

    # 指定 模块国际化
    def module(name: str):
        ShellDir.goInShellDir()
        batchPodList = BatchPodTools.batchPodList()
        batchPodNames = list(map(lambda x: x.name, batchPodList))
        if name in batchPodNames:
            Print.title(name + " 模块国际化 lint 脚本开始执行")
            pod = list(filter(lambda x: x.name == name, batchPodList))[0]
            iOSTranslateLint.path(pod.path)
            Print.title(name + " 模块国际化 lint 执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    # 指定路径国际化
    def path(path_str: str):
        Print.title("{} 路径开始国际化".format(path_str))
        module = IosModule(path_str)
        # 检查 .strings 文件的有效性
        module.check_strings_file()
        # 检查是否还有未本地化的字符串
        module.check_location_string()
