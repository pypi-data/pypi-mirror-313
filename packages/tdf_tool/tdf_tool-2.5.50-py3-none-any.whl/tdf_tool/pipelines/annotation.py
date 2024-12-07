import os
from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.modules.config.module_json_config import ModuleItemType, ModuleJsonConfig
from tdf_tool.modules.config.packages_config import PackageNode, PackagesJsonConfig
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir, ProjectType

from tdf_tool.pipelines.router import Router
from tdf_tool.pipelines.api_interaction import ApiAnnotation


class Annotation:
    """
    模块间支持相关命令：tl annotation -h 查看详情
    """

    def _init(self):
        Print.title("依赖模块检测中...")
        if ShellDir.getProjectType() == ProjectType.FLUTTER:
            self.__buildRunnerName: str = "build_runner"  # build_runner库名
            self.__routerAnnotation: Router = Router()
            self.__apiAnnotation: ApiAnnotation = ApiAnnotation()
            self.__businessModuleList = self.__api_businessModuleList()

    def start(self):
        """
        tl annotation start：会以交互式进行操作，对指定的模块执行描述文件(包括路由，api交互)生成和自动注册逻辑
        """
        self._init()
        ShellDir.goInShellDir()
        self.__packagesList: list[PackageNode] = PackagesJsonConfig(
            ShellDir.getShellDir()
        ).packages  # 壳依赖的所有库

        Print.str("检测到以下模块可生成描述文件：\n")
        for index, item in enumerate(self.__businessModuleList):
            print(f"{index}: {item}")
        print()
        while True:
            module_name = input(
                "请输入需要生成描述文件的模块名或其下标(input ! 退出，all 自动注册)："
            )
            if module_name == "!" or module_name == "！":
                exit(0)
            elif module_name == "all":
                self.integrate()
                exit(0)
            elif module_name in self.__businessModuleList:
                self.__generateCode(module_name)
                Print.title(module_name + "描述文件生成完成")
                self.integrate()
                exit(0)
            else:
                try:
                    i = int(module_name)
                    if i < len(self.__businessModuleList):
                        _module_anme = self.__businessModuleList[i]
                        self.__generateCode(_module_anme)
                        Print.title(_module_anme + "描述文件生成完成")
                        self.integrate()
                        exit(0)
                    else:
                        Print.warning("输入有误，请重新输入")
                except ValueError:
                    Print.warning("输入有误，请重新输入")

    # 生成指定模块的描述文件
    def __generateCode(self, targetModule: str):
        Print.title(targetModule + " 模块生成注解描述文件...")
        for item in self.__packagesList:
            if item.packageName == targetModule:
                if item.isRemote == False:
                    ShellDir.goInShellDir()
                    if self.__judgeHasBuildRunnerPackage(item.packagePath):
                        ShellDir.goInShellDir()
                        os.chdir(item.packagePath)
                        self.__generatorFunc()
                    else:
                        Print.str(
                            "请确保模块{0}已依赖build_runner，可参考其他模块进行依赖配置❌".format(
                                targetModule
                            )
                        )
                else:
                    Print.str(
                        "检测到模块{0}当前是远程依赖，无法生成路由描述文件❌".format(
                            targetModule
                        )
                    )

    # 生成代码
    def __generatorFunc(self):
        os.system("flutter packages pub run build_runner clean")
        os.system(
            "flutter packages pub run build_runner build --delete-conflicting-outputs"
        )

    # 判断业务组件下是否有依赖必须的build_runner模块
    def __judgeHasBuildRunnerPackage(self, packageLibPath: str) -> bool:
        os.chdir(packageLibPath)
        packageJsonConfig = PackagesJsonConfig(os.getcwd(), filter_by_tdf=False)

        hasBuildRunner = False
        for item in packageJsonConfig.packages:
            if item.packageName == self.__buildRunnerName:
                hasBuildRunner = True

        return hasBuildRunner

    def integrate(self):
        self._init()
        self.__routerAnnotation.integrate_shell()
        self.__apiAnnotation.integrate_shell()
        Print.title("整合完成")

    def __api_businessModuleList(self):
        __module_config = ModuleJsonConfig()
        __list = []
        for item in InitialJsonConfig().moduleNameList:
            cofig_item = __module_config.get_item(item)
            if (
                cofig_item.type == ModuleItemType.Lib
                or cofig_item.type == ModuleItemType.Api
                or cofig_item.type == ModuleItemType.Module
                or cofig_item.type == ModuleItemType.Plugin
            ):
                __list.append(item)
        return __list
