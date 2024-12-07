from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.modules.config.module_json_config import ModuleItemType, ModuleJsonConfig
from tdf_tool.modules.module.module_tools import ModuleTools
from tdf_tool.tools.shell_dir import ProjectType, ShellDir
from tdf_tool.tools.print import Print
from ruamel import yaml


class FlutterUpgrade:
    """
    flutter自动修改组件版本号的命令：tl flutterUpgrade -h 查看详情
    """

    def __init(self):
        self.__moduleConfig = ModuleJsonConfig()
        self.__moduleNameList = ModuleTools.getModuleNameList()
        self.__all_version_dict = dict()

    def start(self, all_module=False):
        """ "
        tl flutterUpgrade start 开始批量修改版本号
        """
        ShellDir.dirInvalidate()
        self.__init()
        ShellDir.goInShellDir()
        projectType = ShellDir.getProjectType()
        if projectType != ProjectType.FLUTTER:
            Print.error("tl fixHeader 只支持Flutter")
            return
        Print.str("检测到以下模块可修改版本号：")
        Print.str(self.__moduleNameList)
        inputStr = "!"
        if all_module:
            inputStr = "all"
        else:
            inputStr = input("请输入需要修改的模块名(input ! 退出, all 全选)：")

        if inputStr == "!" or inputStr == "！":
            exit(0)
        elif inputStr == "all":
            self.__get_all_module_version()
            for module in self.__moduleNameList:
                self.__upgrade_module(module)
            exit(0)
        elif inputStr in self.__moduleNameList:
            self.__get_all_module_version()
            self.__upgrade_module(inputStr)
            exit(0)

    def __get_all_module_version(self):
        """
        获取全部库的版本号
        """
        for module in self.__moduleNameList:
            # 读取yaml内容
            with open(f"../.tdf_flutter/{module}/pubspec.yaml", encoding="utf-8") as f:
                pubspec = yaml.round_trip_load(f)
                self.__all_version_dict[module] = pubspec["version"]

    def __upgrade_module(self, module_name: str):
        """
        升级单个模块
        """
        Print.str("开始升级模块：" + module_name)
        with open(f"../.tdf_flutter/{module_name}/pubspec.yaml", encoding="utf-8") as f:
            pubspec = yaml.round_trip_load(f)
            dependencies = pubspec.get("dependencies")
            if dependencies != None:
                self.__deal_with_dependencies(dependencies)
                pubspec["dependencies"] = dependencies
            dev_dependencies = pubspec.get("dev_dependencies")
            if dev_dependencies != None:
                self.__deal_with_dependencies(dev_dependencies)
                pubspec["dev_dependencies"] = dev_dependencies
            f.close()
            with open(
                f"../.tdf_flutter/{module_name}/pubspec.yaml", "w+", encoding="utf-8"
            ) as rwf:
                pubspec["environment"]["sdk"] = ">=2.19.6 <3.0.0"
                pubspec["environment"]["flutter"] = ">=3.7.10"
                yaml.round_trip_dump(
                    pubspec,
                    rwf,
                    default_flow_style=False,
                    encoding="utf-8",
                    allow_unicode=True,
                )
                Print.str(pubspec)
                rwf.close()

        Print.str("升级模块：" + module_name + " 完成")

    def __deal_with_dependencies(self, dependencies: dict):
        for itemName in dependencies.keys():
            if itemName in self.__all_version_dict:
                item = dependencies[itemName]
                if type(item) is str:
                    dependencies[itemName] = self.__deal_with_version_item(
                        item, itemName
                    )
                    continue
                if item.get("hosted") != None:
                    dependencies[itemName] = self.__deal_with_hosted_item(
                        item, itemName
                    )
                    continue
                if item.get("path") != None:
                    dependencies[itemName] = self.__deal_with_path_item(itemName)
                    continue

    def __deal_with_path_item(self, itemName: str) -> dict:
        item_config = self.__moduleConfig.get_item(itemName)
        new_version = self.__all_version_dict[itemName]
        if item_config.type == ModuleItemType.Module:
            return {
                "hosted": {"name": itemName, "url": "http://flutter.2dfire.com"},
                "version": new_version,
            }
        else:
            return {
                "hosted": {"name": itemName, "url": "http://flutter.2dfire.com"},
                "version": "^" + new_version,
            }

    def __deal_with_hosted_item(self, item: dict, itemName: str) -> dict:
        old_version = item["version"]
        new_version = self.__all_version_dict[itemName]
        if old_version.startswith("^"):
            Print.str(f"{itemName} 升级版本号：{old_version} -> ^{new_version}")
            new_version = "^" + new_version
        else:
            Print.str(f"{itemName} 升级版本号：{old_version} -> {new_version}")
        return {
            "hosted": {"name": itemName, "url": "http://flutter.2dfire.com"},
            "version": new_version,
        }

    def __deal_with_version_item(self, old_version: str, itemName: str) -> dict:
        new_version = self.__all_version_dict[itemName]
        if old_version.startswith("^"):
            Print.str(f"{itemName} 升级版本号：{old_version} -> ^{new_version}")
            new_version = "^" + new_version
        else:
            Print.str(f"{itemName} 升级版本号：{old_version} -> {new_version}")
        return {
            "hosted": {"name": itemName, "url": "http://flutter.2dfire.com"},
            "version": new_version,
        }
