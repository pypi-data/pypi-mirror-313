from enum import Enum
import os
from tdf_tool.tools.env import EnvTool
from tdf_tool.tools.print import Print
from ruamel import yaml


class ProjectType(Enum):
    NONE = 0
    FLUTTER = 1
    IOS = 2


class ShellDir:
    __project_path: str = ""

    def __getcwd():
        _workspace = EnvTool.workspaceOrNone()
        if _workspace:
            return _workspace
        else:
            return ShellDir.__project_path

    # 查找路径下的podspec文件
    def findPodspec(path: str) -> str:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                if file.endswith(".podspec"):
                    return path + "/" + file
        return None

    # 查找路径下的podfile文件
    def findPodfile(path: str) -> str:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                if file.endswith(".podfile"):
                    return path + "/" + file
        return None

    # 获取当前路径下项目的类型
    def getProjectType() -> ProjectType:
        path = ShellDir.__getcwd()
        if os.path.exists(path + "/Podfile"):
            Print.title("当前是iOS壳")
            return ProjectType.IOS
        elif os.path.exists(path + "/pubspec.yaml"):
            Print.title("当前是flutter壳")
            return ProjectType.FLUTTER
        else:
            for name in os.listdir(path):
                if name.endswith(".podspec"):
                    return ProjectType.IOS
            return ProjectType.NONE

    # 目录校验，确保只能在壳下执行tdf_tool
    def dirInvalidate():
        ShellDir.__project_path = os.getcwd()
        if EnvTool.is_debug():
            pass
        else:
            try:
                projectType = ShellDir.getProjectType()

                if projectType == ProjectType.FLUTTER:
                    try:
                        with open(
                            "./tdf_cache/initial_config.json", encoding="utf-8"
                        ) as f:
                            f.close()
                            pass
                    except Exception as e:
                        # 其他异常通用处理
                        Print.error("当前不是壳工程目录，禁止执行tdf_tool命令")

                    # 临时先用上面的判定是否是壳工程

                    # with open("pubspec.yaml", encoding="utf-8") as f:
                    #     doc = yaml.round_trip_load(f)
                    #     if isinstance(doc, dict) and doc.__contains__("flutter"):
                    #         if (
                    #             isinstance(doc["flutter"], dict)
                    #             and doc["flutter"].__contains__("module") is not True
                    #         ):
                    #             Print.error("当前不是壳工程目录，禁止执行tdf_tool命令")
                    #     f.close()
                elif projectType == ProjectType.NONE:
                    Print.error("当前不是壳工程目录，禁止执行tdf_tool命令")
            except IOError:
                Print.error("当前不是壳工程目录，禁止执行tdf_tool命令")

    def getShellDir() -> str:
        return ShellDir.__getcwd()

    # 进入到壳内
    def goInShellDir():
        __path = ShellDir.__getcwd()
        if os.path.exists(__path):
            os.chdir(__path)
            Print.title(f"进入路径:{__path}")
        else:
            Print.error(__path + "路径不存在")

    # 进入到壳的 libs
    def goInShellLibDir():
        path = ShellDir.__getcwd() + "/lib"
        if os.path.exists(path):
            os.chdir(path)
        else:
            Print.error(path + "路径不存在")

    # 获取指定模块的目录
    def getModuleDir(module: str) -> str:
        return ShellDir.__getcwd() + "/../.tdf_flutter/" + module

    # 进入到指定模块内
    def goInModuleDir(module: str):
        module_path = ShellDir.getModuleDir(module)
        if os.path.exists(module_path):
            os.chdir(module_path)
        else:
            Print.error(module_path + "路径不存在")

    # 获取指定模块的 lib 目录
    def getModuleLibDir(module: str) -> str:
        return ShellDir.__getcwd() + "/../.tdf_flutter/" + module + "/lib"

    # 进入到指定模块 Lib 内
    def goInModuleLibDir(module: str):
        module_path = ShellDir.getModuleLibDir(module)
        if os.path.exists(module_path):
            os.chdir(module_path)
        else:
            Print.error(module_path + "路径不存在")

    # 获取到指定模块 tdf_intl 路径
    def getInModuleIntlDir(module: str):
        return ShellDir.__getcwd() + "/../.tdf_flutter/" + module + "/lib/tdf_intl"

    # 进入到指定模块 tdf_intl 内
    def goInModuleIntlDir(module: str):
        module_path = ShellDir.getInModuleIntlDir(module)
        if os.path.exists(module_path):
            os.chdir(module_path)
        else:
            Print.error(module_path + "路径不存在")

    # 进入.tdf_flutter文件夹
    def getInTdfFlutterDir():
        return ShellDir.getShellDir() + "/../.tdf_flutter"

    # 进入.tdf_flutter文件夹
    def goInTdfFlutterDir():
        __path = ShellDir.getInTdfFlutterDir()
        if not os.path.exists(__path):
            os.mkdir(__path)
        os.chdir(__path)

    # 进入缓存文件目录
    def goTdfCacheDir():
        ShellDir.goInShellDir()
        if os.path.exists("tdf_cache"):
            os.chdir("tdf_cache")
        elif not os.path.exists("tdf_cache"):
            create = input("当前目录没有找到tdf_cache缓存文件夹，是否创建？(y/n):")
            if create == "y":
                os.mkdir("tdf_cache")
            else:
                Print.error("Oh,it's disappointing.")
                exit(1)

    # 获取模块名
    def getModuleNameFromYaml(yaml_path: str) -> str:
        with open(yaml_path, "r", encoding="utf-8") as rF:
            dic = yaml.round_trip_load(rF.read())
            if dic is not None and dic.__contains__("name"):
                shellModule = dic["name"]
                return shellModule
            else:
                Print.error(
                    "读取壳模块模块名失败，请确保壳模块的pubspec.yaml配置了name属性"
                )
