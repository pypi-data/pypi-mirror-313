from tdf_tool.tools.print import Print
from tdf_tool.tools.flutter_script import FlutterScript
from tdf_tool.modules.translate.translate_lint import FlutterTranslateLint
from tdf_tool.tools.env import EnvTool


class FlutterI18n:
    """flutter 后台下发国际化规范工具"""

    def start(self):
        """交互式 国际化"""
        businessModuleList = FlutterTranslateLint.businessModuleList()

        Print.str("检测到以下模块可执行国际化脚本：")
        Print.str(businessModuleList)
        while True:
            targetModule = input(
                "请输入需要执行国际化脚本的模块名(input ! 退出，all 所有模块执行)："
            )
            if targetModule == "!" or targetModule == "！":
                exit(0)
            elif targetModule == "all":
                for module in businessModuleList:
                    self.module(module)
                exit(0)
            else:
                self.module(targetModule)
                exit(0)

    def module(self, name: str):
        """指定 模块国际化

        Args:
            name (str): 开发中的模块名
        """
        businessModuleList = FlutterTranslateLint.businessModuleList()
        if name in businessModuleList:
            Print.title(name + " 模块国际化脚本开始执行")
            self.__deal_with_module(name)
            Print.title(name + " 模块国际化执行完成")
        else:
            Print.error(name + " 模块不在开发列表中")

    def path(self, path: str):
        """指定路径国际化

        Args:
            pod_name (str): pod的名称
            strings_path (str): pod的国际化文件存放路径
        """
        self.__deal_with_path(path)

    def __deal_with_path(self, path: str):
        FlutterScript().exec("dart", "synchronize_mapping.dart", [f"--path={path}"])

    def __deal_with_module(self, name: str):
        FlutterScript().exec(
            "dart", "synchronize_mapping.dart", [f"--path={EnvTool.workspace()}", name]
        )
